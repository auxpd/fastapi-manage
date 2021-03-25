# fastapi-manage

#### 介绍
fastapi的模板生成，数据库版本管理工具   
fastapi+sqlalchemy  
此项目包含了模板目录(./templates)和模板应用工具(./serializer.py) 提供给开发者自行定制修改的一个工具


#### 使用说明

1.  templates 存放着模板文件
    - 支持开发者修改自定义模型
2.  serializer.py 负责将模板文件写入到main.py中，成为一个变量 
    - 支持开发者进行修改或开发新的模板
3.  conf.py 里包含可配置的模板参数
4.  main 负责提供所有功能，创建项目，执行迁移等等
#### 项目组件的使用
1. 中间件：
    1. 认证中间件
    2. 限流中间件
    
2. 库：
    1. 分页库
    2. 工具库

#### fastapi-manage的使用
##### 安装
```shell
pip install fastapi-manage
```
##### 使用
###### startproject
在当前目录下创建一个fastapi项目， 目录名为当前输入的项目名
```shell
fastapi-manage startproject yourproject
```

###### makemigrations
为项目创建一个新的迁移
```shell
cd ./yourproject
python manage.py makemigrations
```

###### migrate
将迁移应用到数据库
```shell
cd ./yourproject
python manage.py migrate
```

###### runserver
启动一个web服务
```shell
cd ./yourproject
python mange.py runserver
```
Options:  
-h, --host　　　　　[default:127.0.0.1]  
-p, --port　　　　　[default:8000]  
-w, --workers　　　[default:1]  
--reload　　　　　　auto-reloader  


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 版本说明
##### 0.7.0
- 修改了生成密码hash的方式，可自定义调整加盐的次数
- 修复了在windows系统下使用serializer的兼容问题

##### 0.8.0
- 调整了目录结构，增加了常用中间件，以及一个工具类  
- 整合了aredis，redisbloom，使用db/session/redis_session(x)即可调用  
- 修改了core/config 中的数据库字段，与旧版本不兼容，可手动修改字段名称实现兼容  