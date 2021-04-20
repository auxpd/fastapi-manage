from functools import lru_cache

from fastapi_manage.redis import StrictRedis

from core.config import settings
#TEST:
from core.auto_session import auto_sessionmaker, auto_engine

engine = auto_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=8)
SessionFactory = auto_sessionmaker(engine, autocommit=False, autoflush=False)  # 异步建议增加 expire_on_commit=False


@lru_cache()
def redis_session(db: int = 0) -> StrictRedis:
    return StrictRedis(host=settings.REDIS_STORAGE_HOST, port=settings.REDIS_STORAGE_PORT,
                       password=settings.REDIS_STORAGE_PASS or None, db=db, decode_responses=True)
