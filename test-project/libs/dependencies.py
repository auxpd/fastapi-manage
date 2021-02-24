from typing import List, Union

from fastapi import HTTPException, Request
from starlette.authentication import has_required_scope


class BaseDepends:
    def __init__(self):
        pass

    def __call__(self, request: Request):
        self.request = request


class Utils(BaseDepends):
    """
    工具类
    返回Request对象
    """
    def __init__(self, auth: bool = True, scopes: Union[List[str], str] = None):
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
        return request
