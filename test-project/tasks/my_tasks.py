from core.celery import app


@app.task()
def get_celery(msg) -> str:
    print('test11')
    return 'complete'
