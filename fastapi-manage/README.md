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

### 项目详细使用说明

![image-20210312104602483](C:\Users\8201260\AppData\Roaming\Typora\typora-user-images\image-20210312104602483.png)

#### 1. alembic  & alembic.ini

数据库版本管理工具自动生成的目录，对数据库做的变更都会在这个文件夹里的versions记录，这里面的配置由fastapi-manage自动完成

#### 2. api  存放接口逻辑

- api_v1  版本控制
  - endpoints  存放接口逻辑的包
    - user.py 存放user相关的接口
  - api.py  存放路由

- \_\_init_\_.py

- common.py

> 用来存放一些接口会调用到的通用方法

#### 3. core  项目配置中心

> 项目的配置中心，如数据库配置，时区，密码强度，日志等级，jwt过期时间等等

#### 4. db  数据库相关

- base.py 		   文件里保存着所有需要被识别的模型信息， 基类，模型对象
- base_class.py  存放数据库模型的基类, 之后的模型都应该继承这个类，包含了常用四字段， id, create_at, update_at, deleted
- init_db.py         存放对数据库的初始化操作，如初始数据等。
- session.py        对数据库引擎的配置，会话工厂的创建

#### 5.libs  其他包

- dependencies.py    Utils对象的位置
- pagination.py          分页器的位置
- security.py              安全组件, 有 jwt的生成，密码哈希， 密码验证的方法

#### 6.middleware 中间件

- authentication.py        验证中间件 在传入请求前对请求做验证
- auto_db_session.py    数据库会话管理中间件  会话延迟加载, 负责将会话对象注入request对象，而Utils继承request对象
- rate_limit.py                限流中间件

#### 7.models  数据库模型

- \_\_init_\_.py 

- user.py             # 存放用户相关的模型

- machine.py      # 存放机台相关的模型

- etc...

  > 每个模型都需要在\_\_init_\_.py中注册
  >
  > 注册例子:``` from .user import User```
  >
  > 导入例子: ```  import models; models.User```

#### 8.schemas  序列化器

- _\_init_\_.py 

- user.py        # 用户相关的序列化器

  > 跟models一致，但是不强制，可以直接在_\_init_\_中注册类对象
  >
  > 注册后的导入方式: ```  import schemas; schemas.User```

#### 9.tasks  异步任务

- config.py   # celery的配置项
- tasks.py    # 默认创建， 用于存放任务，可自行修改，修改后在config.py中的include引用即可

#### 10.test  测试目录

> 放置测试用例

#### 11.main.py

> 项目从这里启动, 里面可配置中间件, 版本号, 文档路径等

#### 12.manage.py 

> 项目管理器

#### 13. README.md



#### 14. 框架详解

- 接口例子：

/api/endpoints/user.py

```python
from fastapi import APIRouter, Depends

import models
import schemas
from libs import security
from libs.dependencies import Utils

router = APIRouter()  # 定义当前文件里的app对象

@router.post('user', summary='创建用户')  # 第一个参数是url path, summary是接口的概要
def create_user(*, utils:Utils(True, 'admin') = Depends(),
               user: schemas.UserCreate):
    session = utils.db.session  # 获取会话 需要加载数据库会话管理中间件
    hashed_pwd = security.get_password_hash(user.password)  # 获取密码哈希值
    user_dict = user.dict(exclude={'password'})  # 排除password
    user_dict.update({'hashed_password': hashed_pwd})
    user_obj = models.User(**user_dict)  # 创建一个User对象
    session.add(user_obj)  # 添加对象
    session.commit()  # 提交事务
    obj = session.flush(user_obj)  # 刷新对象
    # session.close()  由数据库会话管理中间件自动归还, 未开启时需要手动关闭会话
    return obj
```

/schemas/user.py  (部分源码)

```python
from pydantic import BaseModel


# 序列化器
class UserCreate(BaseModel):
    userid: str
    username: Optional[str] = ''
    email: Optional[str] = ''
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
```

tip: 获取数据库会话的另一种方式

```python
from fastapi import Depends

from api.common import get_session

@router.get('/user', summary='获取所有用户')
def get_all_user(session: Session = Depends(get_session)):
    session.query(xxxx)
    # session.close()  无需调用, 由get_session在接口调用完成后触发close
```

/api/common.py  (部分源码)

```python
def get_session() -> Generator:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
```

- **配置中心：**

core/config.py  (部分源码)

> ```
> PROJECT_NAME: str = "test-project"  # 项目名称
> 
> LOG_LEVEL: str = 'DEBUG'  # TRACE, INFO, SUCCESS, WARNING, ERROR, CRITICAL ...  # 日志等级
> 
> API_V1_STR: str = "/api/v1"  # 接口版本控制，http://localhost/api/v1/xxx
> 
> SECRET_KEY: str = "jymxRSTcLK7Y0AJrYVT12BGQ7HO7IvhXx5HM5_z55Xo"  # 密钥，每个项目会单独生成一个随机密钥, 可用于jwt的加解密
> SALT_ROUNDS: int = 4  # 加盐次数, 决定密码哈希值的强度
> 
> # JWT过期时间 单位: 分钟
> ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
> 
> # 时区设置
> TIMEZONE: str = 'Asia/Shanghai'
> 
> # 分页器, 用到分页器时需要配置
> PAGE_QUERY_PARAM: str = ''
> PAGE_SIZE_QUERY_PARAM: str = ''
> 
> # 跨域配置 默认允许全部
> BACKEND_CORS_ORIGINS: List = ["*"]
> 
> # mysql数据库的配置， 其他关系型数据库也可直接修改此处，然后选择该数据库的引擎即可
> MYSQL_USER: str = "test_user"
> MYSQL_PASS: str = "123456"
> MYSQL_HOST: str = "127.0.0.1"
> MYSQL_DB: str = "test_db"
> MYSQL_PORT: str = "3306"
> SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
> 
> # Redis配置， 需要使用到时配置
> REDIS_STORAGE_HOST: str = '127.0.0.1'
> REDIS_STORAGE_PORT: str = '6379'
> REDIS_STORAGE_PASS: str = ''
> REDIS_STORAGE = f"redis://{REDIS_STORAGE_HOST}:{REDIS_STORAGE_PORT}/?password={REDIS_STORAGE_PASS}"
> 
> # 限流中间件后端
> RATE_LIMIT_REDIS_BACKEND_HOST: str = 'localhost'
> RATE_LIMIT_REDIS_BACKEND_PORT: str = '6379'
> RATE_LIMIT_REDIS_BACKEND_DB: str = '12'
> RATE_LIMIT_REDIS_BACKEND_PASS: str = 'Aa1234'
> 
> # Celery 中间人和后端的配置，主要用在异步任务
> CELERY_BROKER: str = 'redis://:Aa1234@127.0.0.1:6379/7'
> CELERY_BACKEND: str = 'redis://:Aa1234@127.0.0.1:6379/8'
> 
> 
> class Config:
>     case_sensitive = True
> ```

- **异步任务：**

tasks/config.py  部分源码

```python
# 默认include自动生成的tasks.py文件， 如果有新增的py文件，创建后，在这边添加引用即可。
include = ['tasks.tasks']
```

tasks.py

```python
from . import app


@app.task()
def say_hello(name: str) -> None:
    print('hello world')
```

异步任务的调用

```python
from tasks.tasks import say_hello

say_hello.delay('xiaoming')  # 即可将任务添加到消息队列中，等待celery去处理
# 可达到异步执行的效果，在不要求消息强一致性，又是较耗时的操作时，考虑使用，需要考虑消息的可靠性，重复消费，顺序消费等问题。
```

- **主文件：**

main.py   (部分源码)

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    docs_url='/docs',
    redoc_url='/redoc',
) # 文档地址配置等

# 中间件的加载
app.add_middleware(BearerAuthenticationMiddleware)  # 认证中间件
app.add_middleware(DBSessionMiddleware)  # 自动数据库会话管理中间件
if settings.BACKEND_CORS_ORIGINS:  # 跨域中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,  # 允许携带验证信息，如cookies之类的
        allow_methods=["*"],  # 跨域-允许所有方法
        allow_headers=["*"],  # 跨域-允许所有请求头
    )
 
# log配置
logger.remove(handler_id=None)
logger.add(sink=f'logs/{settings.PROJECT_NAME}-{{time:YYYY-MM-DD}}.log',
           format="{time:YYYY-MM-DD HH:mm:ss}-{level}-{name}:{function}:{line}-{level}-{message}",  # 日志格式
           level=settings.LOG_LEVEL,
           enqueue=True,
           diagnose=True,  # 显示详细的错误，可能会泄漏敏感数据
           retention="10 days",  # 清理几天前的日志
           rotation="24h",  # log文件在记录24小时后，就会新建一个新的文件来记录
           encoding='utf-8',
           # compression='zip'  # 启用压缩
           )

''' 开启diagnose后的异常显示：
File "test.py", line 4, in func
    return a / b
           │   └ 0
           └ 5
'''

# 启动事件
@app.on_event('startup')
async def startup_event():
    print('startup_event')


# 版本选择
# app.include_router(api_router)
# V1
app.include_router(api_router, prefix=settings.API_V1_STR)

```

#### 15. 项目例子

1. 安装框架

   ```shell
   pip install fastapi-manage
   ```

2. 生成项目

   ```shell
   fastapi-manage startproject t-project
   cd ./t-project
   ```

3. 项目的初始配置

   - config的配置

4. 数据库模型的构建

   - 编写models
   - 生成迁移版本
   - 应用数据库迁移

5. 接口编写

   - 设置路由
   - 编写序列化器
   - 编写业务逻辑



**restful风格接口**  get post put delete ...

假设需要设计一个用户管理系统

- **数据库设计**
  - 用户基础信息表 (user)
    - userid, username, gender, birthday, mobile, email, etc...
  - 部门信息表(department)
    - name, tel, func, staff, ...
  - 用户拓展信息表(user_extra)
    - client_id, client_name, device_name, device_id, ...



- **接口设计**
  - 登陆模块
    - 用户登陆  --> post		->  def login()	-> username, password
  - 用户模块
    - 用户注册  **-->** post  **->** def create_user()	**->**  UserInfo   ->  User
    - 修改用户  **-->** put    **->** def update_user()   **->**  UserInfo  ->  User
    - 查询用户  **-->** get     **->** def get_user()/get_users()     **->** userid /  None-> User/Users
    - 删除用户  **-->** delete  **->** def delete_user()   **->**  userid    -> None