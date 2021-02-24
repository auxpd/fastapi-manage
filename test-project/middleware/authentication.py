import base64
import binascii
from abc import ABC

import jose
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from pydantic import ValidationError, typing
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, BaseUser, UnauthenticatedUser, AuthCredentials
)
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.types import ASGIApp
from starlette.exceptions import HTTPException

import schemas
from core import security
from core.config import settings


class BearerAuthenticationMiddleware(AuthenticationMiddleware):
    def __init__(
            self,
            app: ASGIApp,
            on_error=None,
    ) -> None:
        backend = BearerAuthBackend()
        super().__init__(app, backend, on_error)

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        if len(exc.args) > 1 and isinstance(exc.args[1], int):
            return JSONResponse(exc.args[0], status_code=exc.args[1])
        return PlainTextResponse(str(exc), status_code=400)


class BearerAuthBackend(AuthenticationBackend):
    headers = "Authorization"
    auth_type = 'bearer'
    token_payload = schemas.TokenPayload

    async def authenticate(self, request):
        if self.headers not in request.headers:
            return AuthCredentials(), UnauthenticatedUser()

        auth = request.headers[self.headers]
        scheme, token = get_authorization_scheme_param(auth)
        if scheme.lower() != self.auth_type:
            return AuthCredentials(), UnauthenticatedUser()

        return self.verify_token(token)

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
            token_data = self.token_payload(**payload)
        except jose.ExpiredSignatureError:
            raise AuthenticationError({'detail': 'Signature has expired.'},  401)
        except(jose.JWTError, ValidationError) as e:
            raise AuthenticationError({'detail': 'Invalid bearer auth credentials.'}, 400)
        return AuthCredentials(['auth']), AuthUser(str(token_data.sub))


class AuthUser(BaseUser, ABC):
    def __init__(self, userid: str, username: str = None) -> None:
        self.userid = userid
        self.username = username

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

