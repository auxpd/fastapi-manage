import functools
import asyncio
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from sqlalchemy.orm import Session, Query as QueryType
from starlette.authentication import requires

import models
import schemas
from libs.Pagination import Pagination
from libs.dependencies import Utils
from core.config import settings
from core.security import create_access_token

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl='/api/v1/user/login')


@router.post('/login', summary='登陆试图')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    return {'access_token': create_access_token('1234'), 'token_type': 'bearer'}


@router.get('/t1')
async def get_t1(*, utils: Utils(True) = Depends(), flag: bool):
    if flag:
        session = utils.db.session
        await asyncio.sleep(1)
        print(session)
    return settings.TEST_1


@router.get('/users')
async def get_user(*, utils: Utils(True, ['user']) = Depends(), ) -> Any:
    session: Session = utils.db.session
    sql = "select * FROM user where id = 1;"
    result = session.execute(sql).fetchall()
    print(settings.TEST_1)
    return result


@router.get('/t2')
async def get_paginate(*, utils: Utils(False) = Depends(), pagination: Pagination(400) = Depends()) -> Any:
    session: Session = utils.db.session
    queryset = session.query(models.User)
    pagination.set_queryset(queryset)
    print(pagination.count())
    return pagination.get_page()
