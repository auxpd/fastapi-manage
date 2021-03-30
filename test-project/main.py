from loguru import logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from api.api_v1.api import api_router
from middleware.auto_db_session import DBSessionMiddleware
from middleware.authentication import BearerAuthenticationMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    docs_url='/docs',
    redoc_url='/redoc',
)

# middleware
app.add_middleware(BearerAuthenticationMiddleware)  # auth middleware
app.add_middleware(DBSessionMiddleware)  # auto db session manage middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# log config
# logger.remove(handler_id=None)
# logger.add(sink=f'logs/{settings.PROJECT_NAME}-{{time:YYYY-MM-DD}}.log',
#            format="{time:YYYY-MM-DD HH:mm:ss}-{level}-{name}:{function}:{line}-{level}-{message}",
#            level=settings.LOG_LEVEL,
#            enqueue=True,
#            diagnose=True,
#            retention="10 days",
#            rotation="24h",
#            encoding='utf-8',
#            # compression='zip'
#            )


# app.include_router(api_router)

# V1
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
