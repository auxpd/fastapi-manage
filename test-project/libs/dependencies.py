from typing import List, Sequence, Union

from loguru import logger
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import HTTPConnection

from core.config import settings
from middleware.authentication import BearerAuthenticationMiddleware
from middleware.auto_db_session import DBSessionBase

oauth2 = OAuth2PasswordBearer(tokenUrl=settings.UTILS_LOGIN_PATH)


"""
在使用前需要在config.py中配置登陆接口 UTILS_LOGIN_PATH
之后直接导入即可 
"""


class BaseDepends:
    def __init__(self):
        pass

    def __call__(self, request: Request):
        self.request = request


class UtilsBase(BaseDepends):
    def __init__(self, auth: bool = False, scopes: Union[List[str], str] = None):
        super().__init__()
        self.auth = auth
        self.scopes = scopes

    def __call__(self, request: Request):
        super().__call__(request)
        if self.auth:
            if not request.user.is_authenticated:
                raise HTTPException(detail='permission denied', status_code=403)
            if self.scopes:
                scopes_list = [self.scopes] if isinstance(self.scopes, str) else list(self.scopes)
                if not self.has_required_scope(request, scopes_list):
                    raise HTTPException(detail='permission denied', status_code=403)
        if not hasattr(request.state, 'db'):
            request.state.db = DBSessionBase()
        request.db = request.state.db
        return request

    @staticmethod
    def has_required_scope(conn: HTTPConnection, scopes: Sequence[str]) -> bool:
        """ Group authentication is passed as long as the user belongs to one of the groups """
        if not len(conn.auth.scopes):
            return False
        for scope in scopes:
            if scope in conn.auth.scopes:
                return True
        return False


class Utils(UtilsBase):
    """
    工具类
    返回Request对象, 额外包含db属性
    utils.app  # app对象
    utils.client  # 客户端的来源地址和端口
    utils.method  # 请求方法
    utils.headers  # 请求头
    utils.cookies  # cookies
    utils.query_params  # 查询参数(page=1&page_size=10)
    utils.scope  # scope对象
    utils.session
    utils.user  # 包含is_authenticated, display_name 属性  需要添加authentication中间件！
    utils.auth  # 包含scopes(用户所在的组 list)  需要添加authentication中间件！
    utils.db.session  # 数据库会话对象  需要添加DBSessionMiddleware中间件！
    ...
    """
    middleware_check_flag = False

    def __call__(self, request: Request, token: str = Depends(oauth2)):
        if not self.middleware_check_flag:
            logger.debug('Dependency checking')
            user_middleware = [mw.cls for mw in request.app.user_middleware]
            if BearerAuthenticationMiddleware not in user_middleware:
                raise NameError('auth dependent AuthenticationMiddleware, But not added')
            else:
                Utils.middleware_check_flag = True
        return super().__call__(request)

    def __new__(cls, auth: bool = False, *args, **kwargs):
        return object.__new__(cls) if auth else UtilsBase(auth, *args, **kwargs)
