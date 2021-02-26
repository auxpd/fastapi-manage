from fastapi import FastAPI
from sentry_asgi import SentryMiddleware
import sentry_sdk

app = FastAPI()

sentry_sdk.init(dsn='xxx')
app.add_middleware(SentryMiddleware)


@app.get('/t1')
async def get_t1():
    print('test')
    return 'OK!'


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
