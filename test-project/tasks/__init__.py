from celery import Celery

from core.config import settings
from . import config

app = Celery(settings.PROJECT_NAME)
app.config_from_object(config)
