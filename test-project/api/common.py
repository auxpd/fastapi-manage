from typing import Generator, Tuple, Optional

import jose
from jose import jwt
from fastapi import HTTPException
from pydantic import ValidationError

import crud
import models
import schemas
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
