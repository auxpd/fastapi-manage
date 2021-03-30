from loguru import logger
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from db.session import SessionFactory


class DBSessionMiddleware(BaseHTTPMiddleware):
    """
    DB session automatic management
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        request.state.db = DBSession()
        response = await call_next(request)
        request.state.db.__del__()
        return response


class DBSessionBase:
    @property
    def session(self):
        logger.error('DBSessionMiddleware must be installed to access session')
        raise NotImplementedError('DBSessionMiddleware must be installed to access session')


class DBSession(DBSessionBase):
    def __init__(self):
        self._db = None

    def __del__(self):
        if self._db:
            self._db.close()
            logger.debug('close db session')

    @property
    def session(self) -> Session:
        if not self._db:
            self._db = SessionFactory()
            logger.debug('create db session')
        return self._db
