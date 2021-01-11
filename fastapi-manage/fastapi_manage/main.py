import os
import secrets
import subprocess
import sys
from typing import Optional

import typer
from configobj import ConfigObj
from jinja2 import Template

file_data = {'': {'__init__.py-tpl': ['\n'], 'README.md': [], 'alembic.ini': ['# A generic, single database configuration.\n', '\n', '[alembic]\n', '# path to migration scripts\n', 'script_location = alembic\n', '\n', '# template used to generate migration files\n', '# file_template = %%(rev)s_%%(slug)s\n', '\n', '# timezone to use when rendering the date\n', '# within the migration file as well as the filename.\n', '# string value is passed to dateutil.tz.gettz()\n', '# leave blank for localtime\n', '# timezone =\n', '\n', '# max length of characters to apply to the\n', '# "slug" field\n', '# truncate_slug_length = 40\n', '\n', "# set to 'true' to run the environment during\n", "# the 'revision' command, regardless of autogenerate\n", '# revision_environment = false\n', '\n', "# set to 'true' to allow .pyc and .pyo files without\n", '# a source .py file to be detected as revisions in the\n', '# versions/ directory\n', '# sourceless = false\n', '\n', '# version location specification; this defaults\n', '# to alembic/versions.  When using multiple version\n', '# directories, initial revisions must be specified with --version-path\n', '# version_locations = %(here)s/bar %(here)s/bat alembic/versions\n', '\n', '# the output encoding used when revision files\n', '# are written from script.py.mako\n', '# output_encoding = utf-8\n', '\n', 'sqlalchemy.url =\n', '\n', '\n', '[post_write_hooks]\n', '# post_write_hooks defines scripts or Python functions that are run\n', '# on newly generated revision scripts.  See the documentation for further\n', '# detail and examples\n', '\n', '# format using "black" - use the console_scripts runner, against the "black" entrypoint\n', '# hooks=black\n', '# black.type=console_scripts\n', '# black.entrypoint=black\n', '# black.options=-l 79\n', '\n', '# Logging configuration\n', '[loggers]\n', 'keys = root, sqlalchemy, alembic\n', '\n', '[handlers]\n', 'keys = console\n', '\n', '[formatters]\n', 'keys = generic\n', '\n', '[logger_root]\n', 'level = WARN\n', 'handlers = console\n', 'qualname = \n', '\n', '[logger_sqlalchemy]\n', 'level = WARN\n', 'handlers = \n', 'qualname = sqlalchemy.engine\n', '\n', '[logger_alembic]\n', 'level = INFO\n', 'handlers = \n', 'qualname = alembic\n', '\n', '[handler_console]\n', 'class = StreamHandler\n', 'args = (sys.stderr, )\n', 'level = NOTSET\n', 'formatter = generic\n', '\n', '[formatter_generic]\n', 'format = %(levelname)-5.5s [%(name)s] %(message)s\n', 'datefmt = %H:%M:%S\n'], 'requirements.txt': ['aiocontextvars==0.2.2\n', 'aiofiles==0.5.0\n', 'aiomysql==0.0.21\n', 'aioredis\n', 'alembic==1.4.3\n', 'aniso8601==7.0.0\n', 'async-exit-stack==1.0.1\n', 'async-generator==1.10\n', 'bcrypt==3.2.0\n', 'certifi==2020.12.5\n', 'cffi==1.14.4\n', 'chardet==3.0.4\n', 'click==7.1.2\n', 'contextvars==2.4\n', 'databases==0.4.1\n', 'dataclasses==0.8\n', 'dnspython==2.0.0\n', 'ecdsa==0.14.1\n', 'email-validator==1.1.2\n', 'fastapi==0.62.0\n', 'future==0.18.2\n', 'graphene==2.1.8\n', 'graphql-core==2.3.2\n', 'graphql-relay==2.0.1\n', 'h11==0.9.0\n', 'httptools==0.1.1\n', 'idna==2.10\n', 'immutables==0.14\n', 'itsdangerous==1.1.0\n', 'Jinja2==2.11.2\n', 'ldap3==2.8.1\n', 'Mako==1.1.3\n', 'MarkupSafe==1.1.1\n', 'orjson==3.4.6\n', 'passlib==1.7.4\n', 'promise==2.3\n', 'pyasn1==0.4.8\n', 'pycparser==2.20\n', 'pydantic==1.7.3\n', 'pyguacamole==0.9\n', 'PyMySQL==0.9.3\n', 'python-dateutil==2.8.1\n', 'python-editor==1.0.4\n', 'python-jose==3.2.0\n', 'python-multipart==0.0.5\n', 'PyYAML==5.3.1\n', 'requests==2.25.0\n', 'rsa==4.6\n', 'Rx==1.6.1\n', 'six==1.15.0\n', 'SQLAlchemy==1.3.20\n', 'starlette==0.13.6\n', 'ujson==3.2.0\n', 'urllib3==1.26.2\n', 'uvicorn==0.11.8\n', 'uvloop==0.14.0\n', 'websockets==8.1\n', 'cryptography'], 'manage.py-tpl': ['import os\n', 'import sys\n', '\n', '\n', 'def main():\n', "    command = 'fastapi-manage '\n", "    command += ' '.join(sys.argv[1:])\n", '    os.chdir(sys.path[0])\n', '    os.system(command)\n', '\n', '\n', "if __name__ == '__main__':\n", '    main()\n', '\n'], 'main.py-tpl': ['from fastapi import FastAPI\n', 'from starlette.middleware.cors import CORSMiddleware\n', '\n', 'from core.config import settings\n', 'from api.api_v1.api import api_router\n', '\n', 'app = FastAPI(\n', '    title=settings.PROJECT_NAME,\n', "    openapi_url=f'{settings.API_V1_STR}/openapi.json',\n", "    docs_url='/docs',\n", "    redoc_url='/redoc',\n", ')\n', '\n', 'if settings.BACKEND_CORS_ORIGINS:\n', '    app.add_middleware(\n', '        CORSMiddleware,\n', '        allow_origins=settings.BACKEND_CORS_ORIGINS,\n', '        allow_credentials=True,\n', '        allow_methods=["*"],\n', '        allow_headers=["*"],\n', '    )\n', '\n', '\n', '# app.include_router(api_router)\n', '\n', '# V1\n', 'app.include_router(api_router, prefix=settings.API_V1_STR)\n', '\n']}, 'test': {'__init__.py-tpl': ['\n']}, 'schemas': {'__init__.py-tpl': ['from .token import Token, TokenPayload\n', 'from .user import User, UserUpdate, UserCreate, UserInDB\n', '\n'], 'token.py-tpl': ['from typing import Optional\n', '\n', 'from pydantic import BaseModel\n', '\n', '\n', 'class Token(BaseModel):\n', '    access_token: str\n', '    token_type: str\n', '\n', '\n', 'class TokenPayload(BaseModel):\n', '    sub: Optional[int] = None\n', '\n'], 'user.py-tpl': ['import time\n', 'from typing import Optional\n', '\n', 'from pydantic import BaseModel, validator\n', '\n', '\n', 'class UserBase(BaseModel):\n', '    userid: str\n', "    username: Optional[str] = ''\n", "    department: Optional[str] = ''\n", '    role: Optional[int] = None\n', "    email: Optional[str] = ''\n", '    last_login: Optional[int] = None\n', '    date_joined: Optional[int] = int(time.time())\n', '    is_active: Optional[bool] = True\n', '    is_staff: Optional[bool] = False\n', '    is_superuser: Optional[bool] = False\n', '\n', '\n', 'class UserCreate(UserBase):\n', '    role: int\n', '    password: str = None  # 内部人员不需要设置密码\n', '    is_staff: Optional[bool] = False\n', '\n', '\n', 'class UserUpdate(UserCreate):\n', '    userid: str = None\n', '    role: str = None\n', '    password: Optional[str] = None\n', '\n', '\n', 'class UserInDBBase(UserBase):\n', '    id: Optional[int] = None\n', '\n', '    class Config:\n', '        orm_mode = True\n', '\n', '\n', 'class User(UserInDBBase):\n', '\n', "    @validator('last_login')\n", '    def last_login(cls, value):\n', "        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value)) if value else ''\n", '\n', "    @validator('date_joined')\n", '    def date_joined(cls, value):\n', "        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value)) if value else ''\n", '\n', '\n', 'class UserInDB(UserInDBBase):\n', '    hashed_password: str\n', '\n']}, 'core': {'__init__.py-tpl': ['\n'], 'security.py-tpl': ['from datetime import datetime, timedelta\n', 'from typing import Any, Union\n', '\n', 'from jose import jwt\n', 'from passlib.context import CryptContext\n', '\n', 'from .config import settings\n', '\n', "pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')\n", '\n', "ALGORITHM = 'HS256'\n", '\n', '\n', '# create token\n', 'def create_access_token(\n', '    subject: Union[str, Any], expires_delta: timedelta = None\n', ') -> str:\n', '    if expires_delta:\n', '        expire = datetime.utcnow() + expires_delta\n', '    else:\n', '        expire = datetime.utcnow() + timedelta(\n', '            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES\n', '        )\n', '    to_encode = {"exp": expire, "sub": str(subject)}\n', '    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)\n', '    return encoded_jwt\n', '\n', '\n', '# verify password\n', 'def verify_password(plain_password: str, hashed_password: str) -> bool:\n', '    return pwd_context.verify(plain_password, hashed_password)\n', '\n', '\n', '# password hash\n', 'def get_password_hash(password: str) -> str:\n', '    return pwd_context.hash(password)\n', '\n'], 'config.py-tpl': ['from typing import List\n', '\n', 'from pydantic import BaseSettings\n', '\n', '\n', 'class Settings(BaseSettings):\n', '\tPROJECT_NAME: str = "{{ conf.project_name }}"\n', '\n', '\tAPI_V1_STR: str = "/api/v1"\n', '\n', '\tSECRET_KEY: str = "{{ conf.secret_key }}"\n', '\t# JWT过期时间\n', '\tACCESS_TOKEN_EXPIRES_MINUTES: int = 60 * 24\n', '\n', '\t# 跨域请求配置\n', '\tBACKEND_CORS_ORIGINS: List = ["*"]\n', '\n', '\t# 数据库配置\n', '\tMYSQL_USER: str = "{{ conf.mysql_user }}"\n', '\tMYSQL_PASS: str = "{{ conf.mysql_pass }}"\n', '\tMYSQL_HOST: str = "{{ conf.mysql_host }}"\n', '\tMYSQL_DB: str = "{{ conf.mysql_db }}"\n', '\tMYSQL_PORT: str = "{{ conf.mysql_port }}"\n', '\tSQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"\n', '\n', '\t# redis储存地址\n', '\tREDIS_STORAGE = "redis://{{ conf.redis_host }}:{{ conf.redis_port }}/?password={{ conf.redis_password }}"\n', '\n', '\tclass Config:\n', '\t\tcase_sensitive = True\n', '\n', '\n', 'settings = Settings()\n', '\n']}, 'db': {'__init__.py-tpl': ['\n'], 'init_db.py-tpl': ['from db.base_class import Base\n', 'from db import engine\n', '\n', '\n', "if __name__ == '__main__':\n", '    Base.metadata.create_all(bind=engine)\n', '\n'], 'base.py-tpl': ['from db.base_class import Base\n', 'from models.user import User\n', '\n'], 'session.py-tpl': ['from sqlalchemy import create_engine\n', 'from sqlalchemy.orm import sessionmaker\n', '\n', 'from core.config import settings\n', '\n', '\n', 'engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=8)\n', 'SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)\n', '\n'], 'base_class.py-tpl': ['from sqlalchemy import Column\n', 'from sqlalchemy.dialects.mysql import INTEGER\n', 'from sqlalchemy.ext.declarative import as_declarative, declared_attr\n', '\n', '\n', '@as_declarative()\n', 'class Base:\n', '    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)\n', '    __name__: str\n', '\n', '    # Automatically assigns a table name that is lowercase for the current class name\n', '    @declared_attr\n', '    def __tablename__(cls) -> str:\n', '        return cls.__name__.lower()\n', '\n', '    # set engine\n', '    @declared_attr\n', '    def __table_args__(self) -> dict:\n', "        return {'mysql_engine': 'InnoDB'}\n", '\n']}, 'api': {'__init__.py-tpl': ['\n'], 'common.py-tpl': ['from typing import Generator, Tuple, Optional\n', '\n', 'import jose\n', 'from jose import jwt\n', 'from fastapi import HTTPException\n', 'from pydantic import ValidationError\n', '\n', 'import crud\n', 'import models\n', 'import schemas\n', 'from core import security\n', 'from core.config import settings\n', 'from db.session import SessionFactory\n', '\n', '\n', 'def get_session() -> Generator:\n', '    """\n', '    get database session\n', '    """\n', '    db = SessionFactory()\n', '    try:\n', '        yield db\n', '    finally:\n', '        db.close()\n', '\n', '\n', 'def verify_token(token: str) -> Tuple[bool, Optional[models.User]]:\n', '    """\n', '    token验证\n', '    :param token:\n', '    :return: (status: bool 认证成功返回True, User: 用户对象)\n', '    """\n', '    try:\n', '        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])\n', '        token_data = schemas.TokenPayload(**payload)\n', '    except(jose.JWTError, ValidationError):\n', '        return False, None\n', '    db = SessionFactory()\n', '    try:\n', '        user = crud.user.get_by_userid(db, token_data.sub)\n', '        if not user:\n', "            raise HTTPException(status_code=401, detail='用户不存在')\n", '        if not user.is_active:\n', "            raise HTTPException(status_code=401, detail='用户账户被禁用')\n", '        return True, user\n', '    finally:\n', '        db.close()\n', '\n']}, 'api/api_v1': {'__init__.py-tpl': ['\n'], 'api.py-tpl': ['from fastapi import APIRouter\n', '\n', 'from api.api_v1.endpoints import user\n', '\n', 'api_router = APIRouter()\n', '# user\n', "api_router.include_router(user.router, prefix='/user', tags=['user'])\n", '\n']}, 'api/api_v1/endpoints': {'__init__.py-tpl': ['\n'], 'user.py-tpl': ['from fastapi import APIRouter\n', '\n', 'router = APIRouter()\n', '\n']}, 'models': {'__init__.py-tpl': ['from .user import User\n', '\n'], 'user.py-tpl': ['import time\n', '\n', 'from sqlalchemy import Boolean, Column, String, SmallInteger\n', 'from sqlalchemy.dialects.mysql import INTEGER\n', '\n', 'from db.base_class import Base\n', '\n', '\n', 'class User(Base):\n', '    userid = Column(String(10), unique=True, index=True)\n', "    username = Column(String(20), default='')\n", '    hashed_password = Column(String(255), nullable=True)\n', "    department = Column(String(50), default='')\n", '    role = Column(SmallInteger, nullable=True)\n', "    email = Column(String(50), default='')\n", '\n', '    last_login = Column(INTEGER(unsigned=True), nullable=True)\n', '    date_joined = Column(INTEGER(unsigned=True), default=int(time.time()))\n', '    is_active = Column(Boolean, default=True)\n', '    is_staff = Column(Boolean, default=False)\n', '    is_superuser = Column(Boolean, default=False)\n', '\n']}, 'crud': {'__init__.py-tpl': ['from .crud_user import user\n', '\n'], 'crud_user.py-tpl': ['from typing import Optional, Union, Dict, Any\n', '\n', 'from sqlalchemy.orm import Session\n', '\n', 'import schemas\n', 'import models\n', 'from .base import CRUDBase\n', 'from core.security import get_password_hash, verify_password\n', '\n', '\n', 'class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):\n', '    """\n', '    user crud methods\n', '    """\n', '    def get_by_userid(self, db: Session, userid: str) -> Optional[models.User]:\n', '        return db.query(models.User).filter_by(userid=userid).first()\n', '\n', '    def create(self, db: Session, obj_in: schemas.UserCreate) -> models.User:\n', '        obj_data = obj_in.dict(exclude_unset=True)\n', "        if 'password' in obj_data.keys():\n", "            obj_data['hashed_password'] = get_password_hash(obj_data['password'])\n", "            del obj_data['password']\n", '        db_obj = self.model(**obj_data)\n', '        db.add(db_obj)\n', '        db.commit()\n', '        db.refresh(db_obj)\n', '        return db_obj\n', '\n', '    def update(\n', '            self, db: Session, db_obj: models.User, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]\n', '    ) -> models.User:\n', '        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)\n', "        if 'password' in update_data.keys():\n", "            update_data['hashed_password'] = get_password_hash(update_data['password'])\n", "            del update_data['password']\n", '        return super().update(db, db_obj, update_data)\n', '\n', '    def authenticate(self, db: Session, userid: str, password: str) -> Optional[models.User]:\n', '        man = db.query(models.User).filter_by(userid=userid).first()\n', '        if not man:\n', '            return None\n', '        if not verify_password(password, man.hashed_password):\n', '            return None\n', '        return man\n', '\n', '\n', 'user = CRUDUser(models.User)\n', '\n'], 'base.py-tpl': ['from typing import Any, Dict, Generic, TypeVar, Type, Optional, List, Union\n', '\n', 'from fastapi.encoders import jsonable_encoder\n', 'from pydantic.main import BaseModel\n', 'from sqlalchemy.orm import Session\n', '\n', 'from db.base_class import Base\n', '\n', "ModelType = TypeVar('ModelType', bound=Base)\n", "CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)\n", "UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)\n", '\n', '\n', 'class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):\n', '    def __init__(self, model: Type[ModelType]):\n', '        self.model = model\n', '\n', '    def get(self, db: Session, pk: Any) -> Optional[ModelType]:\n', '        return db.query(self.model).filter_by(id=pk).first()\n', '\n', '    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:\n', '        return db.query(self.model).offset(skip).limit(limit).all()\n', '\n', '    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:\n', '        obj_in_data = jsonable_encoder(obj_in)\n', '        db_obj = self.model(**obj_in_data)\n', '        db.add(db_obj)\n', '        db.commit()\n', '        db.refresh(db_obj)\n', '        return db_obj\n', '\n', '    def update(self, db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:\n', '        obj_data = jsonable_encoder(db_obj)\n', '        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)\n', '        for field in obj_data:\n', '            if field in update_data:\n', '                setattr(db_obj, field, update_data[field])\n', '        db.add(db_obj)\n', '        db.commit()\n', '        db.refresh(db_obj)\n', '        return db_obj\n', '\n', '    def remove(self, db: Session, pk: int) -> ModelType:\n', '        obj = db.query(self.model).get(pk)\n', '        db.delete(obj)\n', '        db.commit()\n', '        return obj\n', '\n']}, 'alembic': {'env.py-tpl': ['import sys\n', 'import os\n', 'from logging.config import fileConfig\n', '\n', 'from sqlalchemy import engine_from_config\n', 'from sqlalchemy import pool\n', '\n', 'from alembic import context\n', '\n', 'sys.path.insert(0, os.getcwd())\n', '\n', 'from db import base\n', '\n', '# this is the Alembic Config object, which provides\n', '# access to the values within the .ini file in use.\n', 'config = context.config\n', '\n', '# Interpret the config file for Python logging.\n', '# This line sets up loggers basically.\n', 'fileConfig(config.config_file_name)\n', '\n', "# add your model's MetaData object here\n", "# for 'autogenerate' support\n", '# from myapp import mymodel\n', '# target_metadata = mymodel.Base.metadata\n', 'target_metadata = base.Base.metadata\n', '\n', '# other values from the config, defined by the needs of env.py,\n', '# can be acquired:\n', '# my_important_option = config.get_main_option("my_important_option")\n', '# ... etc.\n', '\n', '\n', 'def run_migrations_offline():\n', '    """Run migrations in \'offline\' mode.\n', '\n', '    This configures the context with just a URL\n', '    and not an Engine, though an Engine is acceptable\n', '    here as well.  By skipping the Engine creation\n', "    we don't even need a DBAPI to be available.\n", '\n', '    Calls to context.execute() here emit the given string to the\n', '    script output.\n', '\n', '    """\n', '    url = config.get_main_option("sqlalchemy.url")\n', '    context.configure(\n', '        url=url,\n', '        target_metadata=target_metadata,\n', '        literal_binds=True,\n', '        dialect_opts={"paramstyle": "named"},\n', '    )\n', '\n', '    with context.begin_transaction():\n', '        context.run_migrations()\n', '\n', '\n', 'def run_migrations_online():\n', '    """Run migrations in \'online\' mode.\n', '\n', '    In this scenario we need to create an Engine\n', '    and associate a connection with the context.\n', '\n', '    """\n', '    connectable = engine_from_config(\n', '        config.get_section(config.config_ini_section),\n', '        prefix="sqlalchemy.",\n', '        poolclass=pool.NullPool,\n', '    )\n', '\n', '    with connectable.connect() as connection:\n', '        context.configure(\n', '            connection=connection, target_metadata=target_metadata\n', '        )\n', '\n', '        with context.begin_transaction():\n', '            context.run_migrations()\n', '\n', '\n', 'if context.is_offline_mode():\n', '    run_migrations_offline()\n', 'else:\n', '    run_migrations_online()\n', '\n'], 'script.py.mako': ['"""${message}\n', '\n', 'Revision ID: ${up_revision}\n', 'Revises: ${down_revision | comma,n}\n', 'Create Date: ${create_date}\n', '\n', '"""\n', 'from alembic import op\n', 'import sqlalchemy as sa\n', '${imports if imports else ""}\n', '\n', '# revision identifiers, used by Alembic.\n', 'revision = ${repr(up_revision)}\n', 'down_revision = ${repr(down_revision)}\n', 'branch_labels = ${repr(branch_labels)}\n', 'depends_on = ${repr(depends_on)}\n', '\n', '\n', 'def upgrade():\n', '    ${upgrades if upgrades else "pass"}\n', '\n', '\n', 'def downgrade():\n', '    ${downgrades if downgrades else "pass"}\n']}, 'alembic/versions': {}}
project_dir = ['test', 'schemas', 'core', 'db', 'api/api_v1/endpoints', 'models', 'crud', 'alembic/versions']


app = typer.Typer()


class Configure:
    templates_dir: str = 'templates'
    bin_file: str = 'bin_files'

    project_file_dir: str = 'project_file_dir.py'
    project_file_data: str = 'project_file_data.py'

    project_name: str = ""
    secret_key: str = ""

    mysql_user: str = ""
    mysql_pass: str = ""
    mysql_host: str = ""
    mysql_db: str = ""
    mysql_port: str = ""

    redis_host: str = "127.0.0.1"
    redis_port: str = "6379"
    redis_password: str = ""


def startproject_menu(conf_: Configure):
    try:
        # print('\033[32m请输入数据库信息')
        # conf_.mysql_user = input('\033[0m user:')
        # conf_.mysql_pass = input(' password:')
        # conf_.mysql_host = input(' host:')
        # conf_.mysql_port = input(' port:')
        # conf_.mysql_db = input(' db:')
        return conf_
    except KeyboardInterrupt:
        print('exit')
        sys.exit(0)


@app.command()
def startproject(project_name: str):
    """
    创建一个fastapi项目 项目根文件夹名称为[项目名]
    """
    # 输入项目信息
    config = Configure()
    config.project_name = project_name
    conf = startproject_menu(config)
    #
    # 设置秘钥
    conf.secret_key = secrets.token_urlsafe(32)

    # 配置项目文件和模板文件位置
    base_dir = conf.project_name

    # 创建项目根目录
    os.mkdir(base_dir)

    # 创建文件模版
    create_project_serializer(base_dir, config)


@app.command()
def makemigrations(
        commit_msg: Optional[str] = typer.Option('auto commit', '-m', help='commit message.')
):
    """
    执行迁移
    """
    # 导入config包
    try:
        sys.path.insert(-1, os.path.join(os.path.abspath('fastapi-manage')))
        conf = __import__('core.config').config
        project = conf.settings
    except ModuleNotFoundError:
        print('error: not in the project directory.')
        sys.exit()

    # 判断数据库配置
    if not project.MYSQL_USER or not project.MYSQL_PASS \
            or not project.MYSQL_HOST or not project.MYSQL_DB or not project.MYSQL_PORT:
        print('error: database configuration exception. Check the database configuration in the config.py')
        sys.exit()

    # 修改ini文件
    alembic_path = 'alembic.ini'
    ini_config = ConfigObj(alembic_path, encoding='UTF8', write_empty_values=True)
    ini_config['alembic']['sqlalchemy.url'] = project.SQLALCHEMY_DATABASE_URI
    ini_config.write()

    subprocess.call(f'alembic revision --autogenerate -m "{commit_msg}"', shell=True)


@app.command()
def migrate():
    """
    应用到数据库
    """
    subprocess.call('alembic upgrade head', shell=True)


@app.command()
def runserver(
        host: Optional[str] = typer.Option('127.0.0.1', '--host', '-h'),
        port: Optional[int] = typer.Option(8000, '--port', '-p'),
        workers: int = typer.Option(1, '--workers', '-w', help='线程数'),
        reload: bool = typer.Option(False, help='检测到代码变更自动重新加载'),
):
    """
    运行服务
    """
    # 拼接
    command = 'uvicorn main:app'
    if host:
        command += f' --host={host}'
    if port:
        command += f' --port={port}'
    if workers:
        command += f' --workers={workers}'
    if reload is None:
        command += f' --reload'

    # 执行命令
    os.system(command)


@app.command()
def help():
    """
    帮助
    """
    print('\033[32m帮助信息：')
    print('\033[0m\tstartproject        创建一个fastapi项目 项目根文件夹名称为[项目名]')
    print('\033[0m\tmakemigrations      执行迁移')
    print('\033[0m\tmigrate             应用到数据库')
    print('\033[0m\trunserver           运行服务 --host [ip]服务器地址 '
          ' -p --port [int]端口号 -w -workers [int]进程数 --reload 是否自动加载')


def create_project_serializer(base_dir, config: Configure):
    """ 根据模板创建项目 """
    # 解析文件里的目录
    for directory in project_dir:
        os.makedirs(os.path.join(base_dir, directory))

    for directory, value in file_data.items():
        for file_name, data in value.items():
            # 模板文件
            if file_name.endswith('.py-tpl'):
                template = Template(''.join(data))
                data = template.render(conf=config)
                ext = file_name.split('.')
                source_ext = ext[-1].split('-')[0]
                file_name = ext[0] + '.' + source_ext
            # 普通文件
            with open(os.path.join(base_dir, directory, file_name), 'w') as f:
                f.writelines(data)
