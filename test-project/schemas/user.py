import time
from typing import Optional

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    userid: str
    username: Optional[str] = ''
    department: Optional[str] = ''
    role: Optional[int] = None
    email: Optional[str] = ''
    last_login: Optional[int] = None
    date_joined: Optional[int] = int(time.time())
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    role: int
    password: str = None
    is_staff: Optional[bool] = False


class UserUpdate(UserCreate):
    userid: str = None
    role: str = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):

    @validator('last_login')
    def last_login(cls, value):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value)) if value else ''

    @validator('date_joined')
    def date_joined(cls, value):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value)) if value else ''


class UserInDB(UserInDBBase):
    hashed_password: str
