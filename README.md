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
python manage.py runserver
```
Options:  
-h, --host　　　　　[default:127.0.0.1]  
-p, --port　　　　　[default:8000]  
-w, --workers　　　[default:1]  
--reload　　　　　　auto-reloader  



#### 

#### 模版项目说明

首先先进入到项目的根目录

cd ./yourproject

##### 项目配置

大部分的配置项都在core/config.py文件中，如：数据库配置，token过期时间，跨域配置等等。

main.py中可以配置中间件，日志相关，根路由



##### models配置

数据库的模型都存放在models文件夹下，共有两个类可以被使用，分别是Base和UserBase

###### base_class

base_class文件里共有两个类，UserBase和Base

UserBase相比Base仅仅增加了一个\_groups字段，是为了配合认证中间件的分组功能。

Base class默认有id，create_at, update_at, deleted这几个常用字段，如果编写类的时候没有指定\_\_tablename\_\_ ，Base将会自动指定改模型的表名为当前类名的小写格式；base默认会指定使用InnoDB引擎。这些配置都直接放在db/base_class.py, 随时不满意这些设置可以直接做修改，并不会受到限制

###### base.py

这个文件夹是用来给alembic识别所有模型的一个文件，其实这个文件夹有点鸡肋了。

###### models

models里面的模型都可以继承Base或着UserBase, 可以简化开发，但是有一个需要注意的是：编写类后请将其导入到models/\_\_init\_\_.py。生成的项目里有一个User示例类，可以做参照，User如果不需要大可直接删除。

###### db/session.py

这里可以看到redis和sqlalchemy的会话如何被获取，可以在这里调整sqlalchemy的线程池(pool_size)默认是8



##### 接口编写

接口的编写都放在api/endpoints文件夹里，里面可以按照个人需求进行接口的划分，示例中有一个user.py文件

里面只导入了一些常用的包，并定义了router对象。

示例接口:

```python
@router.get("/", summary='get_all_user')
async def get_all_user(*, utils: UtilsObject = Depends(Utils(False)),) -> Any:
    user = ["A", "B", "C"]
    return user
```

- 路由

	路由文件在/api/api_v1/api.py文件中，里边有所有的接口的路由

- 查询过程：

通过utils.db.session就可以拿到session，并且会自动管理session的生命周期，在接口调用结束的时候自动归还session。

```python
@router.get("/", summary='get_all_user')
def get_all_user(*, utils: UtilsObject = Depends(Utils(False)),) -> Any:
    session = utils.db.session  # get session
    users = session.query(models.User).filter_by(username="hello").all()  # query
    return users
```

拿到session之后就可以做之前sqlalchemy做的任何事情了。

Utils(False) 声明了改接口并不需要进行认证，如果需要认证只需将其改为True即可，并且可以指定允许的分组(List[str])，指定分组后不在该分组中的的用户也将被拒绝访问。

- 认证：

只需要认证成功就可以登陆（token校验通过且并没有过期）

**在设置Utils为True之前(在开启认证之前)，需要实现登陆接口，并在config.py中注册API_LOGIN_URL**

```python
@router.get("/", summary='get_all_user')
def get_all_user(*, utils: UtilsObject = Depends(Utils(True)),) -> Any:
    return "hello"
```

需要认证成功且jwt中的group在指定的scpes中

```python
@router.get("/", summary='get_all_user')
def get_all_user(*, utils: UtilsObject = Depends(Utils(True, ['admin', 'superadmin'])),) -> Any:
    return "hello"
```

utils对象可以理解成是Request对象，只是utils多了一个db对象，是request的超集。

- 获取一个jwt

	一般用在用户登陆的时候，为用户创建身份标识（jwt）

	```python
	@router.get("/login", summary="login")
	def login(*, utils: UtilsObject = Depends(Utils(False)),) -> Any:
	    user_id = "12345678"  # Unique label: int
	    jwt = create_access_token(user_id, ["admin"])
	    return jwt
	    """
	    access_token: str
	    token_type: str
	    """
	```

- password hash & verify_password

	```python
	from libs.security import get_password_hash, verify_password
	hashed_password = get_password_hash("my_password")
	result: bool = verify_password("my_password", hashed_password)
	```

	get_password_hash 一般用在增加用户的时候，将用户密码哈希后放到数据库中

	verify_password一般用在登陆的时候，校验用户密码是否与数据库中的哈希密码一致



- 分页插件 pagination

	这个插件在执行count的性能并不太好。

	引入Pagination依赖后，会自动增加两个查询参数： page, page_size 代表页数和每页的数量，当page_size 超过max_page_size后，将会引发status_code=400异常.

	

	使用方法： 默认每页的最大数量是400

	```python
	@router.get("/", summary='get_all_user')
	def get_all_user(*, utils: UtilsObject = Depends(Utils(True, ['admin', 'superadmin'])),
	                 pagination: Pagination = Depends()) -> Any:
	    session = utils.db.session
	    pagination.queryset = session.query(models.User).filter_by(is_active=True)
	    return pagination.get_page()
	```

	如果需要修改每页的最大数量，可以这样：

	```python
	@router.get("/", summary='get_all_user')
	def get_all_user(*, utils: UtilsObject = Depends(Utils(True, ['admin', 'superadmin'])),
	                 pagination: Pagination = Depends(Pagination(5000))) -> Any:
	    session = utils.db.session
	    pagination.queryset = session.query(models.User).filter_by(is_active=True)
	    return pagination.get_page()
	```

##### middleware和libs 的说明

- middleware

	- authentication 认证中间件，默认添加，添加该中间件后，Utils()将能够用来控制用户是否需要认证，不添加也是可以的，但是如果设置Utils(True)将会抛出异常提醒没有可用的中间件

	- auto_db_session 将用来提供utils中的db对象，它负责在需要用到session的地方创建获取session，在接口调用结束归还session，是一个自动管理sessoin的中间件

		**这个中间件性能并不好，因为starlette的的BaseHTTPMiddleware性能不太好，而auto_db_session继承了该类，本地测试每添加一个BaseHTTPMiddleware的子类，并发都将有一个较大幅度的下降，计划改进。**

	- rate_limit 限流中间件，用来限制每个用户的访问速度，整合了asgi-ratelimit，具体使用可以查看https://pypi.org/project/asgi-ratelimit/ 

- libs

	- dependencies 实现了utils对象，utils的逻辑都在这里
	- pagination 分页工具，封装了一个分页工具。
	- security  安全类，实现了jwt生成，密码哈希，密码校验的方法

##### schemas

该文件夹可以理解成django的序列化器(serializers.py)，**添加完序列化器推荐将该类导入schemas/\_\_init\_\_.py中， 可以简化之后的导入**

用来存放所有序列化器对象

具体用法和官方文档无异

##### tasks

用来放置一些异步任务，使用celery封装而成，用法跟celery基本一致，只是文件的路径做了定制。相关的后端配置也是在config中。

##### test

测试文件夹

##### 启动文件

start-celery.py 用来启动tasks任务

start-gunicorn用来启动住进程，使用gunicorn守护



##### 目前的问题

- sqlalchemy已经发布了1.4版本，提供了异步支持，本来的想法是能够通过config.py中SQLALCHEMY_DATABASE_URI变量里使用的驱动库识别出是否是异步驱动库来实现同步session和异步sessino的切换，但是这么做之后，自动补全就乱套了，没有一个比较好的想法 

- auto_db_session 目前的性能并不理想，需要脱离BaseHTTPMiddleware依赖，目前还没有实现。。


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 版本说明
##### 0.7.2
- 增加了github仓库
##### 0.7.1
- 增加了alembic依赖,在安装fastapi-manage时自动安装
##### 0.7.0
- 修改了生成密码hash的方式，可自定义调整加盐的次数
- 修复了在windows系统下使用serializer的兼容问题

##### 0.8.0
- 调整了目录结构，增加了常用中间件，以及一个工具类  
- 整合了aredis，redisbloom，使用db/session/redis_session(x)即可调用  
- 修改了core/config 中的数据库字段，与旧版本不兼容，可手动修改字段名称实现兼容  
- 增加了对spug运维平台的支持，可云端配置项目  