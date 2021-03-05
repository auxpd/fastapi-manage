import os
import secrets
import subprocess
import sys
from typing import Optional

import typer
from configobj import ConfigObj
from jinja2 import Template


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
        sys.path.insert(-1, os.path.join(os.path.abspath('.')))
        conf = __import__('core.config').config
        project = conf.settings
    except ModuleNotFoundError:
        print('error: not in the project directory.')
        sys.exit()

    # 判断数据库配置
    if not project.MYSQL_USER or not project.MYSQL_PASS \
            or not project.MYSQL_HOST or not project.MYSQL_DB or not project.MYSQL_PORT:
        print('error: database configuration exception. Check the database configuration in the config.py-tpl')
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
        workers: int = typer.Option(1, '--workers', '-w'),
        reload: bool = typer.Option(False),
):
    """
    运行服务 --host [ip]服务器地址 -p --post [int]端口号 -w -workers [int]进程数 --reload 是否自动加载
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
          ' -p --post [int]端口号 -w -workers [int]进程数 --reload 是否自动加载')


def create_project_serializer(base_dir, config: Configure):
    """ 根据模板创建项目 """
    # 解析文件里的目录
    from bin_files.project_file_dir import project_dir
    from bin_files.project_file_data import file_data

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


if __name__ == '__main__':
    app()
