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

#### 9.tasks  任务队列

- config.py   # celery的配置项
- tasks.py    # 默认创建， 用于存放任务，可自行修改，修改后在config.py中的include引用即可

#### 10.test  测试目录

> 放置测试用例

#### 11.main.py

> 项目从这里启动, 里面可配置中间件, 版本号, 文档路径等

#### 12.manage.py 

> 项目管理器

#### 13. README.md



接口例子：

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

