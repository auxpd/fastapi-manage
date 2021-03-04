import time
from ipaddress import ip_address
from typing import Dict, Sequence, Tuple, Callable, Awaitable

from aredis import StrictRedis
from loguru import logger
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from ratelimit import RateLimitMiddleware as RateLimitMixin, Rule
from ratelimit.backends import BaseBackend
from ratelimit.backends.redis import RedisBackend as redisBackendMixin
from ratelimit.core import default_429
from ratelimit.types import Scope
from starlette.types import ASGIApp

from core import security
from core.config import settings
import schemas


"""
1. 在config中配置rate后端RATE_LIMIT_BACKEND_HOST, RATE_LIMIT_BACKEND_PORT, RATE_LIMIT_BACKEND_DB, RATE_LIMIT_BACKEND_PASS
2. 确定如何取唯一标识的函数(auth_func)
3. 配置config参数, 也就是每个接口的访问频率限制 格式:  { r'^/hello': [Rule(minute=2, group='default'), Rule(group='admin')] }
4. 注册中间件 app.add_middleware(RateLimitMiddleware, config=config)
"""


async def auth_func(scope: Scope) -> Tuple[str, str]:
    """
    Resolve the user's unique identifier and the user's group from ASGI SCOPE.

    If there is no user information, it should raise `EmptyInformation`.
    If there is no group information, it should return "default".
    """
    # FIXME
    # You must write the logic of this function yourself,
    # or use the function in the following document directly.
    # return USER_UNIQUE_ID, GROUP_NAME

    # 1. authenticated, take jwt as the unique identity, group: jwt.group or 'default'
    auth_headers = "authorization"
    auth_type = 'bearer'
    headers = {hd[0]: hd[1] for hd in scope.get('headers')}
    if auth_headers.encode() in headers:
        scheme, token = get_authorization_scheme_param(headers[auth_headers.encode()].decode())
        if scheme.lower() == auth_type:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
                token_data = schemas.TokenPayload(**payload)
                return str(token_data.sub), token_data.group or 'default'  # return USER_UNIQUE_ID, GROUP_NAME
            except Exception as e:
                logger.warning(e)

    # 2. unauthorized, Take IP as the unique identity, group: default
    real_ip = ""
    if scope["client"]:
        real_ip, port = tuple(scope["client"])
        for name, value in scope["headers"]:  # type: bytes, bytes
            if name == b"x-real-ip":
                ip = value.decode("utf8")
                if not real_ip and ip_address(ip).is_global:
                    real_ip = ip
    return real_ip, "default"  # return USER_UNIQUE_ID, GROUP_NAME


class RedisBackend(redisBackendMixin):
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            password: str = None,
    ) -> None:
        host = settings.RATE_LIMIT_REDIS_BACKEND_HOST if hasattr(settings, 'RATE_LIMIT_REDIS_BACKEND_HOST') else host
        port = settings.RATE_LIMIT_REDIS_BACKEND_PORT if hasattr(settings, 'RATE_LIMIT_REDIS_BACKEND_PORT') else port
        db = settings.RATE_LIMIT_REDIS_BACKEND_DB if hasattr(settings, 'RATE_LIMIT_REDIS_BACKEND_DB') else db
        password = settings.RATE_LIMIT_REDIS_BACKEND_PASS if hasattr(settings, 'RATE_LIMIT_REDIS_BACKEND_PASS') else password
        super().__init__(host, port, db, password)


class RateLimitMiddleware(RateLimitMixin):
    def __init__(
            self,
            *,
            app: ASGIApp,
            config: Dict[str, Sequence[Rule]],
            authenticate: Callable[[Scope], Awaitable[Tuple[str, str]]] = auth_func,
            backend: BaseBackend = RedisBackend(),
            on_blocked: ASGIApp = default_429,
    ) -> None:
        super().__init__(app, authenticate, backend, config, on_blocked=on_blocked)
