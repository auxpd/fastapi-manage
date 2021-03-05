from typing import Generator, Tuple, Optional

import jose
from jose import jwt
from fastapi import HTTPException
from pydantic import ValidationError

import models
import schemas
from libs.security import TokenPayload
from libs import security
from core.config import settings
from db.session import SessionFactory


def get_session() -> Generator:
    """
    get database session
    """
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

#
# def verify_token(token: str) -> Tuple[bool, Optional[models.User]]:
#     """
#     token验证
#     :param token:
#     :return: (status: bool 认证成功返回True, User: 用户对象)
#     """
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
#         token_data = TokenPayload(**payload)
#     except(jose.JWTError, ValidationError):
#         return False, None
#     db = SessionFactory()
#     try:
#         user = crud.user.get_by_userid(db, token_data.sub)
#         if not user:
#             raise HTTPException(status_code=401, detail='user does not exist')
#         if not user.is_active:
#             raise HTTPException(status_code=401, detail='account is disabled')
#         return True, user
#     finally:
#         db.close()
