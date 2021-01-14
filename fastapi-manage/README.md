# fastapi_manage

#### Project description
fastapi的模板生成，数据库版本管理项目。  
FastAPI template generation, database version management tools.  
Just like Django.  

fastapi+sqlalchemy  

#### Installation
```shell
pip install fastapi-manage
```

#### Usage
##### startproject
Creates a fastapi project directory structure for the given project name in the
current directory or optionally in the given directory.
```shell
fastapi-manage startproject yourproject
```

##### makemigrations
Creates new migration(s) for project.
```shell
cd ./yourproject
python manage.py makemigrations
```

##### migrate
Updates database schema. Manages both apps with migrations and those without.
```shell
cd ./yourproject
python manage.py migrate
```

##### runserver
Start a Web server
```shell
cd ./yourproject
python mange.py runserver
```
Options:  
-h, --host　　　　　[default:127.0.0.1]  
-p, --port　　　　　[default:8000]  
-w, --workers　　　[default:1]  
--reload　　　　　　auto-reloader  
