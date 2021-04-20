import asyncio
from loguru import logger
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from db.session import SessionFactory, engine


class DBSessionMiddleware(BaseHTTPMiddleware):
    """
    DB session automatic management
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        request.state.db = DBSession()
        response = await call_next(request)
        await request.state.db.close()
        return response


class DBSessionBase:
    @property
    def session(self):
        logger.error('DBSessionMiddleware must be installed to access session')
        raise NotImplementedError('DBSessionMiddleware must be installed to access session')


class DBSession(DBSessionBase):
    def __init__(self):
        self._db = None

    async def close(self):
        if self._db:
            if asyncio.iscoroutinefunction(self._db.close):
                await self._db.close()
                logger.debug('关闭异步会话')
            else:
                loop = asyncio.get_event_loop()
                loop.run_in_executor(None, self._db.close)
                logger.debug('关闭同步会话')
            logger.debug('close db session')

    @property
    def session(self) -> Session:
        if not self._db:
            self._db = SessionFactory()
            logger.debug('create db session')
        return self._db

    @property
    def is_async(self) -> bool:
        return engine.dialect.is_async