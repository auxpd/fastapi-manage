import time

from sqlalchemy import Boolean, Column, String, SmallInteger
from sqlalchemy.dialects.mysql import INTEGER

from db.base_class import Base


class User(Base):
    userid = Column(String(10), unique=True, index=True)
    username = Column(String(20), default='')
    hashed_password = Column(String(255), nullable=True)
    department = Column(String(50), default='')
    role = Column(SmallInteger, nullable=True)
    email = Column(String(50), default='')

    last_login = Column(INTEGER(unsigned=True), nullable=True)
    date_joined = Column(INTEGER(unsigned=True), default=int(time.time()))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
