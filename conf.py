from pydantic import BaseSettings


class Configure(BaseSettings):
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


config = Configure()
