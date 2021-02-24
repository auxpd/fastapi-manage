import functools
from fastapi import APIRouter, Depends, Request
from starlette.authentication import requires

from libs.dependencies import Utils
from core.config import settings

router = APIRouter()
settings.TEST_1 = '456'


@router.get('/t1')
async def get_t1(*, utils: Utils(False) = Depends(), flag: bool):
    if flag:
        session = utils.state.db.session
        print(session)
    return settings.TEST_1
