import os
import sys
import time
import argparse
import subprocess

import dataclasses
import secrets

from configobj import ConfigObj
from jinja2 import Environment, FileSystemLoader, Template

from conf import config


def startproject_menu(conf_: config):
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


def startproject(project_name: str = None):
    # 输入项目信息
    config.project_name = project_name
    conf = startproject_menu(config)

    # 设置秘钥
    conf.secret_key = secrets.token_urlsafe(32)

    # 配置项目文件和模板文件位置
    base_dir = conf.project_name

    # 创建项目根目录
    os.mkdir(base_dir)

    # 创建文件模版
    create_project_serializer(base_dir)
    # create_project(base_dir, conf)


def make_migrations():
    parser = argparse.ArgumentParser()
    parser.add_argument('makemigrations', nargs=1)
    parser.add_argument('-m', default='auto commit', help='commit message.')
    args = parser.parse_args()
    commit_msg = args.m

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
        print('error: database configuration exception. Check the database configuration in the config.py')
        sys.exit()

    # 修改ini文件
    alembic_path = 'alembic.ini'
    ini_config = ConfigObj(alembic_path, encoding='UTF8', write_empty_values=True)
    ini_config['alembic']['sqlalchemy.url'] = project.SQLALCHEMY_DATABASE_URI
    ini_config.write()

    subprocess.call(f'alembic revision --autogenerate -m "{commit_msg}"', shell=True)


def migrate():
    subprocess.call('alembic upgrade head', shell=True)


def runserver():
    parser = argparse.ArgumentParser()
    parser.add_argument('runserver', nargs=1)
    parser.add_argument('--host', help='Bind socket to this host.  [default:127.0.0.1].')
    parser.add_argument('-p', '--port', help='Bind socket to this port.  [default: 8000].')
    parser.add_argument('-w', '--workers', help=' Number of worker processes.')
    parser.add_argument('--reload', nargs='?', default=True, help='Enable auto-reload.')  # 有填写则为None

    # 获取参数
    args = parser.parse_args()
    host = args.host
    port = args.port
    workers = args.workers
    reload = args.reload

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


def help_info():
    print('\033[32m帮助信息：')
    print('\033[0m\tstartproject        创建一个fastapi项目 项目根文件夹名称为[项目名]')
    print('\033[0m\tmakemigrations      执行迁移')
    print('\033[0m\tmigrate             应用到数据库')
    print('\033[0m\trunserver           运行服务 --host [ip]服务器地址 '
          ' -p --post [int]端口号 -w -workers [int]进程数 --reload 是否自动加载')


def create_project(base_dir, conf):
    templates_dir = conf.templates_dir
    abs_tmp_dir = os.path.abspath(templates_dir)

    # 获取模板文件
    tmp_files = os.walk(os.path.join(os.getcwd(), templates_dir))

    # 创建模板目录
    env = Environment(loader=FileSystemLoader(templates_dir))
    for root, dirs, files in tmp_files:
        root = root.split(abs_tmp_dir)[-1]
        root = root if root and root[0] != os.sep else root[1:]

        for directory in dirs:
            os.mkdir(os.path.join(base_dir, root, directory))

        # 创建文件
        for file in files:
            # 模板文件
            if file.endswith('.py-tpl'):
                template = env.get_template(os.path.join(root, file))
                data = template.render(conf=conf)
                ext = file.split('.')
                source_ext = ext[-1].split('-')[0]
                file = ext[0] + '.' + source_ext
            # 普通文件
            else:
                with open(os.path.join(templates_dir, root, file), 'r') as f:
                    data = f.readlines()

            with open(os.path.join(base_dir, root, file), 'w') as f:
                f.writelines(data)


def create_project_serializer(base_dir):
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


def main():
    if len(sys.argv) < 2:
        command = 'help'
    else:
        command = sys.argv[1]

    if command == 'startproject':
        if len(sys.argv) < 3:
            print('error: You must provide a project name.')
            sys.exit()
        project_name = sys.argv[2]
        startproject(project_name)

    elif command == 'makemigrations':
        make_migrations()

    elif command == 'migrate':
        migrate()

    elif command == 'runserver':
        runserver()

    elif command == 'help':
        help_info()

    else:
        print('\033[31mError:错误的命令')
        help_info()


if __name__ == '__main__':
    main()
