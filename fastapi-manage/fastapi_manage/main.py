import os
import secrets
import subprocess
import sys
from typing import Optional

import typer
from configobj import ConfigObj
from jinja2 import Template

file_data = {'': {'alembic.ini': ['# A generic, single database configuration.\n', '\n', '[alembic]\n', '# path to migration scripts\n', 'script_location = alembic\n', '\n', '# template used to generate migration files\n', '# file_template = %%(rev)s_%%(slug)s\n', '\n', '# timezone to use when rendering the date\n', '# within the migration file as well as the filename.\n', '# string value is passed to dateutil.tz.gettz()\n', '# leave blank for localtime\n', '# timezone =\n', '\n', '# max length of characters to apply to the\n', '# "slug" field\n', '# truncate_slug_length = 40\n', '\n', "# set to 'true' to run the environment during\n", "# the 'revision' command, regardless of autogenerate\n", '# revision_environment = false\n', '\n', "# set to 'true' to allow .pyc and .pyo files without\n", '# a source .py file to be detected as revisions in the\n', '# versions/ directory\n', '# sourceless = false\n', '\n', '# version location specification; this defaults\n', '# to alembic/versions.  When using multiple version\n', '# directories, initial revisions must be specified with --version-path\n', '# version_locations = %(here)s/bar %(here)s/bat alembic/versions\n', '\n', '# the output encoding used when revision files\n', '# are written from script.py.mako\n', '# output_encoding = utf-8\n', '\n', 'sqlalchemy.url =\n', '\n', '\n', '[post_write_hooks]\n', '# post_write_hooks defines scripts or Python functions that are run\n', '# on newly generated revision scripts.  See the documentation for further\n', '# detail and examples\n', '\n', '# format using "black" - use the console_scripts runner, against the "black" entrypoint\n', '# hooks=black\n', '# black.type=console_scripts\n', '# black.entrypoint=black\n', '# black.options=-l 79\n', '\n', '# Logging configuration\n', '[loggers]\n', 'keys = root, sqlalchemy, alembic\n', '\n', '[handlers]\n', 'keys = console\n', '\n', '[formatters]\n', 'keys = generic\n', '\n', '[logger_root]\n', 'level = WARN\n', 'handlers = console\n', 'qualname = \n', '\n', '[logger_sqlalchemy]\n', 'level = WARN\n', 'handlers = \n', 'qualname = sqlalchemy.engine\n', '\n', '[logger_alembic]\n', 'level = INFO\n', 'handlers = \n', 'qualname = alembic\n', '\n', '[handler_console]\n', 'class = StreamHandler\n', 'args = (sys.stderr, )\n', 'level = NOTSET\n', 'formatter = generic\n', '\n', '[formatter_generic]\n', 'format = %(levelname)-5.5s [%(name)s] %(message)s\n', 'datefmt = %H:%M:%S\n'], 'main.py-tpl': ['from fastapi import FastAPI\n', 'from starlette.middleware.cors import CORSMiddleware\n', '\n', 'from core.config import settings\n', 'from api.api_v1.api import api_router\n', '\n', 'app = FastAPI(\n', '    title=settings.PROJECT_NAME,\n', "    openapi_url=f'{settings.API_V1_STR}/openapi.json',\n", "    docs_url='/docs',\n", "    redoc_url='/redoc',\n", ')\n', '\n', 'if settings.BACKEND_CORS_ORIGINS:\n', '    app.add_middleware(\n', '        CORSMiddleware,\n', '        allow_origins=settings.BACKEND_CORS_ORIGINS,\n', '        allow_credentials=True,\n', '        allow_methods=["*"],\n', '        allow_headers=["*"],\n', '    )\n', '\n', '\n', '# app.include_router(api_router)\n', '\n', '# V1\n', 'app.include_router(api_router, prefix=settings.API_V1_STR)\n', '\n'], 'manage.py-tpl': ['import os\n', 'import sys\n', '\n', '\n', 'def main():\n', "    command = 'fastapi-manage '\n", "    command += ' '.join(sys.argv[1:])\n", '    os.chdir(sys.path[0])\n', '    os.system(command)\n', '\n', '\n', "if __name__ == '__main__':\n", '    main()\n', '\n'], 'README.md': [], '__init__.py-tpl': ['\n']}, 'alembic': {'env.py-tpl': ['import sys\n', 'import os\n', 'from logging.config import fileConfig\n', '\n', 'from sqlalchemy import engine_from_config\n', 'from sqlalchemy import pool\n', '\n', 'from alembic import context\n', '\n', 'sys.path.insert(0, os.getcwd())\n', '\n', 'from db import base\n', '\n', '# this is the Alembic Config object, which provides\n', '# access to the values within the .ini file in use.\n', 'config = context.config\n', '\n', '# Interpret the config file for Python logging.\n', '# This line sets up loggers basically.\n', 'fileConfig(config.config_file_name)\n', '\n', "# add your model's MetaData object here\n", "# for 'autogenerate' support\n", '# from myapp import mymodel\n', '# target_metadata = mymodel.Base.metadata\n', 'target_metadata = base.Base.metadata\n', '\n', '# other values from the config, defined by the needs of env.py,\n', '# can be acquired:\n', '# my_important_option = config.get_main_option("my_important_option")\n', '# ... etc.\n', '\n', '\n', 'def run_migrations_offline():\n', '    """Run migrations in \'offline\' mode.\n', '\n', '    This configures the context with just a URL\n', '    and not an Engine, though an Engine is acceptable\n', '    here as well.  By skipping the Engine creation\n', "    we don't even need a DBAPI to be available.\n", '\n', '    Calls to context.execute() here emit the given string to the\n', '    script output.\n', '\n', '    """\n', '    url = config.get_main_option("sqlalchemy.url")\n', '    context.configure(\n', '        url=url,\n', '        target_metadata=target_metadata,\n', '        literal_binds=True,\n', '        dialect_opts={"paramstyle": "named"},\n', '    )\n', '\n', '    with context.begin_transaction():\n', '        context.run_migrations()\n', '\n', '\n', 'def run_migrations_online():\n', '    """Run migrations in \'online\' mode.\n', '\n', '    In this scenario we need to create an Engine\n', '    and associate a connection with the context.\n', '\n', '    """\n', '    connectable = engine_from_config(\n', '        config.get_section(config.config_ini_section),\n', '        prefix="sqlalchemy.",\n', '        poolclass=pool.NullPool,\n', '    )\n', '\n', '    with connectable.connect() as connection:\n', '        context.configure(\n', '            connection=connection, target_metadata=target_metadata\n', '        )\n', '\n', '        with context.begin_transaction():\n', '            context.run_migrations()\n', '\n', '\n', 'if context.is_offline_mode():\n', '    run_migrations_offline()\n', 'else:\n', '    run_migrations_online()\n', '\n'], 'script.py.mako': ['"""${message}\n', '\n', 'Revision ID: ${up_revision}\n', 'Revises: ${down_revision | comma,n}\n', 'Create Date: ${create_date}\n', '\n', '"""\n', 'from alembic import op\n', 'import sqlalchemy as sa\n', '${imports if imports else ""}\n', '\n', '# revision identifiers, used by Alembic.\n', 'revision = ${repr(up_revision)}\n', 'down_revision = ${repr(down_revision)}\n', 'branch_labels = ${repr(branch_labels)}\n', 'depends_on = ${repr(depends_on)}\n', '\n', '\n', 'def upgrade():\n', '    ${upgrades if upgrades else "pass"}\n', '\n', '\n', 'def downgrade():\n', '    ${downgrades if downgrades else "pass"}\n']}, 'alembic/versions': {}, 'api': {'common.py-tpl': ['from typing import Generator, Tuple, Optional\n', '\n', 'import jose\n', 'from jose import jwt\n', 'from fastapi import HTTPException\n', 'from pydantic import ValidationError\n', '\n', 'import crud\n', 'import models\n', 'import schemas\n', 'from core import security\n', 'from core.config import settings\n', 'from db.session import SessionFactory\n', '\n', '\n', 'def get_session() -> Generator:\n', '    """\n', '    get database session\n', '    """\n', '    db = SessionFactory()\n', '    try:\n', '        yield db\n', '    finally:\n', '        db.close()\n', '\n', '\n', 'def verify_token(token: str) -> Tuple[bool, Optional[models.User]]:\n', '    """\n', '    token验证\n', '    :param token:\n', '    :return: (status: bool 认证成功返回True, User: 用户对象)\n', '    """\n', '    try:\n', '        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])\n', '        token_data = schemas.TokenPayload(**payload)\n', '    except(jose.JWTError, ValidationError):\n', '        return False, None\n', '    db = SessionFactory()\n', '    try:\n', '        user = crud.user.get_by_userid(db, token_data.sub)\n', '        if not user:\n', "            raise HTTPException(status_code=401, detail='user does not exist')\n", '        if not user.is_active:\n', "            raise HTTPException(status_code=401, detail='account is disabled')\n", '        return True, user\n', '    finally:\n', '        db.close()\n', '\n'], '__init__.py-tpl': ['\n']}, 'api/api_v1': {'api.py-tpl': ['from fastapi import APIRouter\n', '\n', 'from api.api_v1.endpoints import user\n', '\n', 'api_router = APIRouter()\n', '# user\n', "api_router.include_router(user.router, prefix='/user', tags=['user'])\n", '\n'], '__init__.py-tpl': ['\n']}, 'api/api_v1/endpoints': {'user.py-tpl': ['from fastapi import APIRouter\n', '\n', 'router = APIRouter()\n', '\n'], '__init__.py-tpl': ['\n']}, 'core': {'config.py-tpl': ['from typing import List\n', '\n', 'from pydantic import BaseSettings\n', '\n', '\n', 'class Settings(BaseSettings):\n', '\tPROJECT_NAME: str = "{{ conf.project_name }}"\n', '\n', '\tAPI_V1_STR: str = "/api/v1"\n', '\n', '\tSECRET_KEY: str = "{{ conf.secret_key }}"\n', '\tSALT_ROUNDS: int = 4\n', '\n', '\t# JWT expiration time\n', '\tACCESS_TOKEN_EXPIRES_MINUTES: int = 60 * 24\n', '\n', '\t# Cross-domain request configuration\n', '\tBACKEND_CORS_ORIGINS: List = ["*"]\n', '\n', '\t# Database configuration\n', '\tMYSQL_USER: str = "{{ conf.mysql_user }}"\n', '\tMYSQL_PASS: str = "{{ conf.mysql_pass }}"\n', '\tMYSQL_HOST: str = "{{ conf.mysql_host }}"\n', '\tMYSQL_DB: str = "{{ conf.mysql_db }}"\n', '\tMYSQL_PORT: str = "{{ conf.mysql_port }}"\n', '\tSQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"\n', '\n', '\t# Redis store address\n', '\tREDIS_STORAGE = "redis://{{ conf.redis_host }}:{{ conf.redis_port }}/?password={{ conf.redis_password }}"\n', '\n', '\tclass Config:\n', '\t\tcase_sensitive = True\n', '\n', '\n', 'settings = Settings()\n', '\n'], 'security.py-tpl': ['from datetime import datetime, timedelta\n', 'from typing import Any, Union\n', '\n', 'import bcrypt\n', 'from jose import jwt\n', '\n', 'from .config import settings\n', '\n', '\n', "ALGORITHM = 'HS256'\n", '\n', '\n', '# create token\n', 'def create_access_token(\n', '    subject: Union[str, Any], expires_delta: timedelta = None\n', ') -> str:\n', '    if expires_delta:\n', '        expire = datetime.utcnow() + expires_delta\n', '    else:\n', '        expire = datetime.utcnow() + timedelta(\n', '            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES\n', '        )\n', '    to_encode = {"exp": expire, "sub": str(subject)}\n', '    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)\n', '    return encoded_jwt\n', '\n', '\n', '# verify password\n', 'def verify_password(plain_password: str, hashed_password: str) -> bool:\n', '    hashed_password = hashed_password.encode()\n', '    result = bcrypt.hashpw(plain_password.encode(), hashed_password)\n', '    return result == hashed_password\n', '\n', '\n', '# password hash\n', 'def get_password_hash(password: str) -> str:\n', '    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(settings.SALT_ROUNDS)).decode()\n', '\n'], '__init__.py-tpl': ['\n']}, 'crud': {'base.py-tpl': ['from typing import Any, Dict, Generic, TypeVar, Type, Optional, List, Union\n', '\n', 'from fastapi.encoders import jsonable_encoder\n', 'from pydantic.main import BaseModel\n', 'from sqlalchemy.orm import Session\n', '\n', 'from db.base_class import Base\n', '\n', "ModelType = TypeVar('ModelType', bound=Base)\n", "CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)\n", "UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)\n", '\n', '\n', 'class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):\n', '    def __init__(self, model: Type[ModelType]):\n', '        self.model = model\n', '\n', '    def get(self, db: Session, pk: Any) -> Optional[ModelType]:\n', '        return db.query(self.model).filter_by(id=pk).first()\n', '\n', '    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:\n', '        return db.query(self.model).offset(skip).limit(limit).all()\n', '\n', '    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:\n', '        obj_in_data = jsonable_encoder(obj_in)\n', '        db_obj = self.model(**obj_in_data)\n', '        db.add(db_obj)\n', '        db.commit()\n', '        db.refresh(db_obj)\n', '        return db_obj\n', '\n', '    def update(self, db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:\n', '        obj_data = jsonable_encoder(db_obj)\n', '        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)\n', '        for field in obj_data:\n', '            if field in update_data:\n', '                setattr(db_obj, field, update_data[field])\n', '        db.add(db_obj)\n', '        db.commit()\n', '        db.refresh(db_obj)\n', '        return db_obj\n', '\n', '    def remove(self, db: Session, pk: int) -> ModelType:\n', '        obj = db.query(self.model).get(pk)\n', '        db.delete(obj)\n', '        db.commit()\n', '        return obj\n', '\n'], 'crud_user.py-tpl': ['from typing import Optional, Union, Dict, Any\n', '\n', 'from sqlalchemy.orm import Session\n', '\n', 'import schemas\n', 'import models\n', 'from .base import CRUDBase\n', 'from core.security import get_password_hash, verify_password\n', '\n', '\n', 'class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):\n', '    """\n', '    user crud methods\n', '    """\n', '    def get_by_userid(self, db: Session, userid: str) -> Optional[models.User]:\n', '        return db.query(models.User).filter_by(userid=userid).first()\n', '\n', '    def create(self, db: Session, obj_in: schemas.UserCreate) -> models.User:\n', '        obj_data = obj_in.dict(exclude_unset=True)\n', "        if 'password' in obj_data.keys():\n", "            obj_data['hashed_password'] = get_password_hash(obj_data['password'])\n", "            del obj_data['password']\n", '        db_obj = self.model(**obj_data)\n', '        db.add(db_obj)\n', '        db.commit()\n', '        db.refresh(db_obj)\n', '        return db_obj\n', '\n', '    def update(\n', '            self, db: Session, db_obj: models.User, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]\n', '    ) -> models.User:\n', '        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)\n', "        if 'password' in update_data.keys():\n", "            update_data['hashed_password'] = get_password_hash(update_data['password'])\n", "            del update_data['password']\n", '        return super().update(db, db_obj, update_data)\n', '\n', '    def authenticate(self, db: Session, userid: str, password: str) -> Optional[models.User]:\n', '        man = db.query(models.User).filter_by(userid=userid).first()\n', '        if not man:\n', '            return None\n', '        if not verify_password(password, man.hashed_password):\n', '            return None\n', '        return man\n', '\n', '\n', 'user = CRUDUser(models.User)\n', '\n'], '__init__.py-tpl': ['from .crud_user import user\n', '\n']}, 'db': {'base.py-tpl': ['from db.base_class import Base\n', 'from models.user import User\n', '\n'], 'base_class.py-tpl': ['from sqlalchemy import Column\n', 'from sqlalchemy.dialects.mysql import INTEGER\n', 'from sqlalchemy.ext.declarative import as_declarative, declared_attr\n', '\n', '\n', '@as_declarative()\n', 'class Base:\n', '    id = Column(INTEGER(unsigned=True), primary_key=True, index=True, autoincrement=True)\n', '    __name__: str\n', '\n', '    # Automatically assigns a table name that is lowercase for the current class name\n', '    @declared_attr\n', '    def __tablename__(cls) -> str:\n', '        return cls.__name__.lower()\n', '\n', '    # set engine\n', '    @declared_attr\n', '    def __table_args__(self) -> dict:\n', "        return {'mysql_engine': 'InnoDB'}\n", '\n'], 'init_db.py-tpl': ['from db.base_class import Base\n', 'from db import engine\n', '\n', '\n', "if __name__ == '__main__':\n", '    Base.metadata.create_all(bind=engine)\n', '\n'], 'session.py-tpl': ['from sqlalchemy import create_engine\n', 'from sqlalchemy.orm import sessionmaker\n', '\n', 'from core.config import settings\n', '\n', '\n', 'engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_size=8)\n', 'SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)\n', '\n'], '__init__.py-tpl': ['\n']}, 'models': {'user.py-tpl': ['import time\n', '\n', 'from sqlalchemy import Boolean, Column, String, SmallInteger\n', 'from sqlalchemy.dialects.mysql import INTEGER\n', '\n', 'from db.base_class import Base\n', '\n', '\n', 'class User(Base):\n', '    userid = Column(String(10), unique=True, index=True)\n', "    username = Column(String(20), default='')\n", '    hashed_password = Column(String(255), nullable=True)\n', "    department = Column(String(50), default='')\n", '    role = Column(SmallInteger, nullable=True)\n', "    email = Column(String(50), default='')\n", '\n', '    last_login = Column(INTEGER(unsigned=True), nullable=True)\n', '    date_joined = Column(INTEGER(unsigned=True), default=int(time.time()))\n', '    is_active = Column(Boolean, default=True)\n', '    is_staff = Column(Boolean, default=False)\n', '    is_superuser = Column(Boolean, default=False)\n', '\n'], '__init__.py-tpl': ['from .user import User\n', '\n']}, 'schemas': {'token.py-tpl': ['from typing import Optional\n', '\n', 'from pydantic import BaseModel\n', '\n', '\n', 'class Token(BaseModel):\n', '    access_token: str\n', '    token_type: str\n', '\n', '\n', 'class TokenPayload(BaseModel):\n', '    sub: Optional[int] = None\n', '\n'], 'user.py-tpl': ['import time\n', 'from typing import Optional\n', '\n', 'from pydantic import BaseModel, validator\n', '\n', '\n', 'class UserBase(BaseModel):\n', '    userid: str\n', "    username: Optional[str] = ''\n", "    department: Optional[str] = ''\n", '    role: Optional[int] = None\n', "    email: Optional[str] = ''\n", '    last_login: Optional[int] = None\n', '    date_joined: Optional[int] = int(time.time())\n', '    is_active: Optional[bool] = True\n', '    is_staff: Optional[bool] = False\n', '    is_superuser: Optional[bool] = False\n', '\n', '\n', 'class UserCreate(UserBase):\n', '    role: int\n', '    password: str = None\n', '    is_staff: Optional[bool] = False\n', '\n', '\n', 'class UserUpdate(UserCreate):\n', '    userid: str = None\n', '    role: str = None\n', '    password: Optional[str] = None\n', '\n', '\n', 'class UserInDBBase(UserBase):\n', '    id: Optional[int] = None\n', '\n', '    class Config:\n', '        orm_mode = True\n', '\n', '\n', 'class User(UserInDBBase):\n', '\n', "    @validator('last_login')\n", '    def last_login(cls, value):\n', "        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value)) if value else ''\n", '\n', "    @validator('date_joined')\n", '    def date_joined(cls, value):\n', "        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(value)) if value else ''\n", '\n', '\n', 'class UserInDB(UserInDBBase):\n', '    hashed_password: str\n', '\n'], '__init__.py-tpl': ['from .token import Token, TokenPayload\n', 'from .user import User, UserUpdate, UserCreate, UserInDB\n', '\n']}, 'test': {'__init__.py-tpl': ['\n']}}
project_dir = ['alembic/versions', 'api/api_v1/endpoints', 'core', 'crud', 'db', 'models', 'schemas', 'test']


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
        # print('\033[32m input your database information')
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
    Create a FastAPI project with the project root folder name [project name]
    """
    # enter project information
    config = Configure()
    config.project_name = project_name
    conf = startproject_menu(config)

    # set the secret key
    conf.secret_key = secrets.token_urlsafe(32)

    # configure project file and template file locations
    base_dir = conf.project_name

    # create the project root directory
    os.mkdir(base_dir)

    # create a file template
    create_project_serializer(base_dir, config)


@app.command()
def makemigrations(
        commit_msg: Optional[str] = typer.Option('auto commit', '-m', help='commit message.')
):
    """
    Perform the migration
    """
    # import the config package
    try:
        sys.path.insert(-1, os.path.join(os.path.abspath('.')))
        conf = __import__('core.config').config
        project = conf.settings
    except ModuleNotFoundError:
        print('error: not in the project directory.')
        sys.exit()

    # determine database configuration
    if not project.MYSQL_USER or not project.MYSQL_PASS \
            or not project.MYSQL_HOST or not project.MYSQL_DB or not project.MYSQL_PORT:
        print('error: database configuration exception. Check the database configuration in the config.py')
        sys.exit()

    # modify ini file
    alembic_path = 'alembic.ini'
    ini_config = ConfigObj(alembic_path, encoding='UTF8', write_empty_values=True)
    ini_config['alembic']['sqlalchemy.url'] = project.SQLALCHEMY_DATABASE_URI
    ini_config.write()

    subprocess.call(f'alembic revision --autogenerate -m "{commit_msg}"', shell=True)


@app.command()
def migrate():
    """
    Apply to the database
    """
    subprocess.call('alembic upgrade head', shell=True)


@app.command()
def runserver(
        host: Optional[str] = typer.Option('127.0.0.1', '--host', '-h'),
        port: Optional[int] = typer.Option(8000, '--port', '-p'),
        workers: int = typer.Option(1, '--workers', '-w', help='the number of threads'),
        reload: bool = typer.Option(False, help='Code changes detected automatically reload'),
):
    """
    Run the service
    """
    # joint
    command = 'uvicorn main:app'
    if host:
        command += f' --host={host}'
    if port:
        command += f' --port={port}'
    if workers:
        command += f' --workers={workers}'
    if reload is None:
        command += f' --reload'

    # execute the command
    os.system(command)


@app.command()
def help():
    """
    Help information
    """
    print('\033[32mHelp information：')
    print('\033[0m\tstartproject        Create a FastAPI project with the project root folder name [project name]')
    print('\033[0m\tmakemigrations      Perform the migration')
    print('\033[0m\tmigrate             Apply to the database')
    print('\033[0m\trunserver           Run the service --host [IP] server address '
          ' -p --port [int] port number -w -workers [int] process number -- whether reload is automatically loaded')


def create_project_serializer(base_dir, config: Configure):
    """
    Create the project from the template
    """
    # parse the directory in the file
    for directory in project_dir:
        os.makedirs(os.path.join(base_dir, directory))

    for directory, value in file_data.items():
        for file_name, data in value.items():
            # Template file
            if file_name.endswith('.py-tpl'):
                template = Template(''.join(data))
                data = template.render(conf=config)
                ext = file_name.split('.')
                source_ext = ext[-1].split('-')[0]
                file_name = ext[0] + '.' + source_ext
            # common file
            with open(os.path.join(base_dir, directory, file_name), 'w', encoding="utf-8") as f:
                f.writelines(data)
