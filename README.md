# fastapi_manage

#### 介绍
fastapi的模板生成，数据库版本管理项目  
fastapi+sqlalchemy  
此项目包含了模板目录(./templates)和模板应用工具(./serializer.py) 提供给开发者自行定制修改的一个工具

#### 软件架构
软件架构说明


#### 使用说明

1.  templates 存放着模板文件
    - 支持开发者修改自定义模型
2.  serializer 负责将模板文件写入到main.py中，成为一个变量 
    - 支持开发者进行修改或开发新的模板
3.  main 负责提供所有功能，创建项目，执行迁移等等 

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


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
