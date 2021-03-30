import os
from pydantic import BaseSettings


class Configure(BaseSettings):
    templates_dir: str = 'templates'
    bin_dir: str = os.path.join('fastapi-manage', 'fastapi_manage')
    bin_file: str = 'main.py'

    file_dir_num = 11
    file_data_num = 10

    project_name: str = ""
    secret_key: str = ""

    db_user: str = ""
    db_pass: str = ""
    db_host: str = ""
    db_db: str = ""
    db_port: str = ""

    redis_host: str = "127.0.0.1"
    redis_port: str = "6379"
    redis_password: str = ""


config = Configure()
