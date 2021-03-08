from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=8)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
