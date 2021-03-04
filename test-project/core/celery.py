from celery import Celery

from core.config import settings


app = Celery(settings.PROJECT_NAME,
             broker=settings.CELERY_BROKER,
             backend=settings.CELERY_BACKEND)
app.autodiscover_tasks(['tasks'])

# app.conf.task_routes = {'tasks.my_tasks.get_celery': {'queue': 'my-queue'}}
app.conf.broker_transport_options = {'visibility_timeout': 2}

