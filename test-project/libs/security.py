from datetime import datetime, timedelta
from typing import Any, List, Optional, Union

import bcrypt
from jose import jwt
from pydantic import BaseModel

from core.config import settings


ALGORITHM = 'HS256'


class TokenPayload(BaseModel):
    exp: int
    sub: int = None
    group: Optional[List[str]] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# create token
def create_access_token(
    subject: Union[str, Any], group: Optional[List[str]] = None, expires_delta: timedelta = None
) -> Token:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), 'group': group}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type='bearer')


# verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    hashed_password = hashed_password.encode()
    result = bcrypt.hashpw(plain_password.encode(), hashed_password)
    return result == hashed_password


# password hash
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(settings.SALT_ROUNDS)).decode()
