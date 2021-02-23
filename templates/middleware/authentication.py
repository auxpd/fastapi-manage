import base64
import binascii
from abc import ABC

from pydantic import typing
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser, AuthCredentials
)
from starlette.requests import HTTPConnection
from starlette.responses import Response
from starlette.types import ASGIApp


class BearerAuthenticationMiddleware(AuthenticationMiddleware):
    def __init__(self, app: ASGIApp, on_error: typing.Callable[
        [HTTPConnection, AuthenticationError], Response
    ] = None) -> None:
        backend: AuthenticationBackend = BearerAuthBackend()
        super().__init__(app, backend, on_error)


class BearerAuthBackend(AuthenticationBackend):
    headers = "Authorization"
    auth_type = 'bearer'

    async def authenticate(self, request):
        if self.headers not in request.headers:
            return None

        auth = request.headers[self.headers]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != self.auth_type:
                return None
            decoded = base64.b64decode(credentials).decode('ascii')
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid bearer auth credentials')

        # TODO: 认证操作
        print(decoded)
        # return AuthCredentials(), UnauthenticatedUser()
        return AuthCredentials(["authenticated"]), AuthUser('123')


class AuthUser(SimpleUser, ABC):
    def __init__(self, username: str) -> None:
        super().__init__(username)
