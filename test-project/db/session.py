from functools import lru_cache

from fastapi_manage.redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=8)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@lru_cache()
def redis_session(db: int = 0) -> StrictRedis:
    return StrictRedis(host=settings.REDIS_STORAGE_HOST, port=settings.REDIS_STORAGE_PORT,
                       password=settings.REDIS_STORAGE_PASS or None, db=db, decode_responses=True)
