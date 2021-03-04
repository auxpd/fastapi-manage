import time

from loguru import logger

from core.celery import app
from core.config import settings
import models
from db.session import SessionFactory


@app.task()
def get_celery(seconds: int) -> str:
    time.sleep(seconds)
    print('test11')
    return 'complete'


@app.task()
def show_conf() -> None:
    print(settings.TEST_1)
    return None


@app.task()
def get_users() -> None:
    session = SessionFactory()
    result = session.query(models.User.username).all()
    print(result)
    return None
