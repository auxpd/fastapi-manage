from sqlalchemy import Boolean, Column, String, SmallInteger, DATETIME, text
from sqlalchemy.dialects.mysql import INTEGER

from db.base_class import Base, UserBase


class User(UserBase):
    __tablename__ = 'user'

    userid = Column(String(10), unique=True, index=True)
    username = Column(String(20), default='')
    hashed_password = Column(String(255), nullable=True)
    department = Column(String(50), default='')
    role = Column(SmallInteger, nullable=True)
    email = Column(String(50), default='')

    last_login = Column(DATETIME, nullable=True)
    date_joined = Column(DATETIME, nullable=False, server_default=text('NOW()'))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
