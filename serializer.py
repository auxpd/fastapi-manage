import os
import subprocess
import alembic

from conf import config


def main():
    tmp_dir = config.templates_dir
    abs_tmp_dir = os.path.abspath(config.templates_dir)

    # 序列化目录
    tmp_files = os.walk(os.path.join(os.getcwd(), tmp_dir))
    result = []
    for root, dirs, files in tmp_files:
        root = root.split(abs_tmp_dir)[-1].split('/')[1:]
        if root[:-1] not in result and root:  # 不重复且不为空
            result.append(root)
        elif root:
            result.remove(root[:-1])
            result.append(root)

    # 解析文件里的目录
    project_dir = []
    for directory in result:
        path = os.path.join(*directory)
        project_dir.append(path)
        # os.makedirs()  # 项目文件夹加上path，递归创建文件夹
    with open(os.path.join(config.bin_dir, config.bin_file), 'r') as f:
        file_list = f.readlines()
        file_list[config.file_dir_num] = f'project_dir = {project_dir}\n'

    # 序列化文件
    tmp_files = os.walk(os.path.join(os.getcwd(), tmp_dir))
    file_data = {}
    for root, dirs, files in tmp_files:
        root = root.split(abs_tmp_dir)[-1].split(os.sep)[1:]
        if not root:
            root = ['']
        path = os.path.join(*root)
        if path not in file_data:
            file_data[path] = {}
        for file in files:
            print(file)
            with open(os.path.join(tmp_dir, path, file), 'r') as f:
                file_data[path][file] = f.readlines()
    file_list[config.file_data_num] = f'file_data = {file_data}\n'
    with open(os.path.join(config.bin_dir, config.bin_file), 'w') as f:
        f.writelines(file_list)


if __name__ == '__main__':
    main()
    # subprocess.call('pyinstaller -F fastapi_manage.py', shell=True,  cwd=os.getcwd())
