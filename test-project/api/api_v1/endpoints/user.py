import functools
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, Query as QueryType
from starlette.authentication import requires

import models
import schemas
from libs.Pagination import Pagination
from libs.dependencies import Utils
from core.config import settings

router = APIRouter()


@router.get('/t1')
async def get_t1(*, utils: Utils(False) = Depends(), flag: bool):
    if flag:
        session = utils.state.db.session
        print(session)
    return settings.TEST_1


@router.get('/users')
async def get_user(*, utils: Utils(False, ['user']) = Depends(), ) -> Any:
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
