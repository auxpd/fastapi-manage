from celery import Celery

app = Celery('fastapi-worker', broker='redis://127.0.0.1:6379/7?password=')
# app.conf.task_router = {'tasks.my_tasks.get_celery': {'queue': 'my-queue'}}
app.autodiscover_tasks(['tasks'])
