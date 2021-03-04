from typing import List, Union

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.authentication import has_required_scope

oauth2 = OAuth2PasswordBearer(tokenUrl='/api/v1/user/login')


class BaseDepends:
    def __init__(self):
        pass

    def __call__(self, request: Request):
        self.request = request


class UtilsBase(BaseDepends):
    """
    工具类
    返回Request对象
    utils.db.session = Session
    """
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
                if not has_required_scope(request, scopes_list):
                    raise HTTPException(detail='permission denied', status_code=403)
        request.db = request.state.db
        assert isinstance(request.db.session, Session)
        return request


class Utils(UtilsBase):

    def __call__(self, request: Request, token: str = Depends(oauth2)):
        return super().__call__(request)

    def __new__(cls, auth: bool = False, *args, **kwargs):
        obj = cls if auth else UtilsBase
        return object.__new__(obj)
