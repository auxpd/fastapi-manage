from typing import Any, List, MutableMapping, Sequence, Union

from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.datastructures import Address, Headers, QueryParams, State, URL
from starlette.requests import HTTPConnection
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, Request

from core.config import settings
from middleware.auto_db_session import DBSession, DBSessionBase
from middleware.authentication import AuthUser, BearerAuthenticationMiddleware

oauth2 = OAuth2PasswordBearer(tokenUrl=settings.API_LOGIN_URL)


class UtilsObject(object):
    def __init__(self, request: Request, db: Union[DBSessionBase, DBSession]):
        if SessionMiddleware in [mw.cls for mw in request.app.user_middleware]:
            self.session = request.session
        self.db: Union[DBSession, DBSessionBase] = db
        self.app: FastAPI = request.app
        self.auth: AuthCredentials = request.auth
        self.base_url: URL = request.base_url
        self.client: Address = request.client
        self.cookies: dict = request.cookies
        self.headers: Headers = request.headers
        self.method: str = request.method
        self.path_params: dict = request.path_params
        self.query_params: QueryParams = request.query_params
        self.scope: MutableMapping[str, Any] = request.scope
        self.state: State = request.state
        self.url: URL = request.url
        self.user: Union[UnauthenticatedUser, AuthUser] = request.user


class BaseDepends:
    def __init__(self):
        pass

    def __call__(self, request: Request):
        self.request = request


class UtilsBase(BaseDepends):
    def __init__(self, auth: bool = False, scopes: Union[List[str], str] = None):
        super().__init__()
        self._auth = auth
        self._scopes = scopes

    def __call__(self, request: Request) -> UtilsObject:
        super().__call__(request)
        if self._auth:
            if not request.user.is_authenticated:
                raise HTTPException(detail='permission denied', status_code=403)
            if self._scopes:
                scopes_list = [self._scopes] if isinstance(self._scopes, str) else list(self._scopes)
                if not self.has_required_scope(request, scopes_list):
                    raise HTTPException(detail='permission denied', status_code=403)
        if not hasattr(request.state, 'db'):
            request.state.db = DBSessionBase()
        return UtilsObject(request, request.state.db)

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
    expansion of the request obj
    """
    middleware_check_flag = False

    def __call__(self, request: Request, token: str = Depends(oauth2)) -> UtilsObject:
        if not self.middleware_check_flag:
            logger.debug('Dependency checking')
            if BearerAuthenticationMiddleware not in [mw.cls for mw in request.app.user_middleware]:
                raise NameError('auth dependent AuthenticationMiddleware, But not added')
            else:
                Utils.middleware_check_flag = True
        return super().__call__(request)

    def __new__(cls, auth: bool = False, *args, **kwargs):
        return object.__new__(cls) if auth else UtilsBase(auth, *args, **kwargs)
