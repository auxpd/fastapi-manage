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
##### 0.7.1
- 增加了alembic依赖,在安装fastapi-manage时自动安装
##### 0.7.0
- 修改了生成密码hash的方式，可自定义调整加盐的次数
- 修复了在windows系统下使用serializer的兼容问题

#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
