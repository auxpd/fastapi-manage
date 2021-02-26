import functools
from typing import Any

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.authentication import requires

import models
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
async def get_user(*, utils: Utils(False) = Depends(),) -> Any:
    session: Session = utils.db.session
    sql = "select * FROM user where id = 1;"
    result = session.execute(sql).fetchall()
    print(settings.TEST_1)
    return result
