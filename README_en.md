### introduce  
Fastapi template generation, database version management tools

fastapi+sqlalchemy

This project includes template directory (./templates) and template application tool (/ serializer.py ）It provides a tool for developers to customize and modify  

### instructions

Templates : holds the template file. Support developers to modify custom models

serializer.py : Responsible for writing template files to main.py To be a variable.
  Support developers to modify or develop new templates

conf.py : Contains configurable template parameters

main.py : Responsible for providing all functions, creating projects, performing migrations, etc

### use of fastapi-manage
#### install
```shell
pip install fastapi-manage
```
#### usage
##### startproject
Create a fastapi project in the current directory, 
the directory name is the project name currently entered
```shell
fastapi-manage startproject yourproject
```

##### makemigrations
Create a migration for the project
```shell
cd ./yourproject
python manage.py makemigrations
```
##### migrate
Apply the migration to the database
```shell
cd ./yourproject
python mangage.py migrate
```

##### runserver
Start a web service
```shell
cd ./yourproject
python manage.py runserver
```
> ```shell fastapi-manage --help ```  # View the help of fastapi-manage command  
> Options:  
-h, --host　　　　　[default:127.0.0.1]  
-p, --port　　　　　[default:8000]  
-w, --workers　　　[default:1]  
--reload　　　　　　auto-reloader  

#### Template project description

cd ./yourproject

##### Project configuration

Most of the configuration items are in the core/config.py file, 
such as: database configuration, token expiration time, cross-domain configuration and so on.

Middleware, log related, root routing can be configured in main.py



##### models configuration

The models of the database are stored in the models folder, 
and there are two classes that can be used, namely Base and User Base

###### base_class

There are two classes in the base class file, User Base and Base

Compared with Base, User Base only adds a \_groups field to cooperate with the grouping function of the authentication middleware.

Base class has id, create_at, update_at, deleted by default. 
If you do not specify \_\_tablename\_\_ when writing the class, 
Base will automatically specify the table name of the modified model in lowercase format of the current class name. 
 Base will specify the InnoDB engine by default. These configurations are placed directly in dbbase_class.py, 
if you are not satisfied with these settings at any time, you can modify them directly without restriction

###### base.py

This folder is a file used to identify all models for alembic. In fact, this folder is a bit tasteless.

###### models

Models in models can inherit Base or UserBase, which can simplify development, 
but there is one thing to note: After writing the class, please import it into models\_\_init\_\_.py. 
There is a User sample class in the generated project, which can be used as a reference, 
and User can be deleted directly if it is not needed.

###### db/session.py

Here you can see how the sessions of redis and sqlalchemy are obtained. 
You can adjust the sqlalchemy thread pool (pool size) by default to 8.



##### Interface writing

The compilation of the interface is placed in the apiendpoints folder, 
which can be divided according to personal needs. There is a user.py file in the example

Only some commonly used packages are imported in user.py, and router objects are defined.

Example:

```python
@router.get("/", summary='get_all_user')
async def get_all_user(*, utils: UtilsObject = Depends(Utils(False)),) -> Any:
    user = ["A", "B", "C"]
    return user
```

- query process：

The session can be obtained through utils.db.session, and the life cycle of the session will be automatically managed, 
and the session will be automatically returned at the end of the interface call.

```python
@router.get("/", summary='get_all_user')
def get_all_user(*, utils: UtilsObject = Depends(Utils(False)),) -> Any:
    session = utils.db.session  # type: sqlalchemy.orm.Session
    users = session.query(models.User).filter_by(username="hello").all()  # query
    return users
```

After getting the session, you can do anything that sqlalchemy did before.

Utils(False) declares that the interface does not need to be authenticated. 
If authentication is required, just change it to True, and you can specify the allowed group (List[str]). 
After specifying the group, the ones that are not in the group The user will also be denied access.

- Authentication：

You can log in as long as the authentication is successful (the token is verified and has not expired)

**Before setting Utils to True (before enabling authentication), 
you need to implement the login interface and register the API LOGIN URL in config.py**

```python
@router.get("/", summary='get_all_user')
def get_all_user(*, utils: UtilsObject = Depends(Utils(True)),) -> Any:
    return "hello"
```

Need to be authenticated successfully, and the group in jwt is in the specified scopes

```python
@router.get("/", summary='get_all_user')
def get_all_user(*, utils: UtilsObject = Depends(Utils(True, ['admin', 'superadmin'])),) -> Any:
    return "hello"
```

The utils object can be understood as a Request object, but utils has an additional db object, which is a superset of request.

- get jwt

	Generally used when the user logs in, to create an identity for the user (jwt)

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

	get_password_hash -> Generally used when adding users, hash the user password and put it in the database

	verify_password -> Generally used when logging in to verify whether the user password is consistent 
    with the hashed password in the database



- Paging plugin pagination

	The performance of this plugin in executing count is not very good.

	引入Pagination依赖后，会自动增加两个查询参数： page, page_size 代表页数和每页的数量，当page_size 超过max_page_size后，将会引发status_code=400异常.
    After the Pagination dependency is introduced, two query parameters will be automatically added: 
    page, page_size represent the number of pages and the number of each page, 
    when page_size exceeds max_page_size, status_code=400 exception will be raised.
	

    The default maximum number per page is 400

	```python
	@router.get("/", summary='get_all_user')
	def get_all_user(*, utils: UtilsObject = Depends(Utils(True, ['admin', 'superadmin'])),
	                 pagination: Pagination = Depends()) -> Any:
	    session = utils.db.session
	    pagination.queryset = session.query(models.User).filter_by(is_active=True)
	    return pagination.get_page()
	```

	If you need to modify the maximum number of each page, you can do this:

	```python
	@router.get("/", summary='get_all_user')
	def get_all_user(*, utils: UtilsObject = Depends(Utils(True, ['admin', 'superadmin'])),
	                 pagination: Pagination = Depends(Pagination(5000))) -> Any:
	    session = utils.db.session
	    pagination.queryset = session.query(models.User).filter_by(is_active=True)
	    return pagination.get_page()
	```

##### middleware & libs

- middleware

	- authentication Authentication middleware is added by default. After adding this middleware, Utils() will be able to control whether the user needs authentication. It is also possible not to add it, but if Utils(True) will throw an exception to remind that there is no middleware available

	- auto_db_session It will be used to provide the db object in utils. It is responsible for creating and acquiring session where the session is needed, and returning the session at the end of the interface call. It is a middleware that automatically manages sessoin.

		**The performance of this middleware is not good, because the performance of Starlette's Base HTTP Middleware is not very good, and auto db session inherits this class. Every time a subclass of Base HTTP Middleware is added to the local test, there will be a larger concurrency. Decline, plan to improve.**

	- rate_limit The current limiting middleware is used to limit the access speed of each user and integrates asgi-ratelimit. For specific use, please refer to https:pypi.orgprojectasgi-ratelimit

- libs

	- dependencies The utils object is implemented, and the logic of utils is here
	- pagination Paging tool encapsulates a paging tool.
	- security  Security class, which implements the methods of jwt generation, password hashing, and password verification

##### schemas

This folder can be understood as django's serializer (serializers.py)，**After adding the serializer, it is recommended to import this class into schemes\_\_init\_\_.py, which can simplify the subsequent import**

Used to store all serializer objects

The specific usage is the same as the official documents

##### tasks

Used to place some asynchronous tasks, encapsulated by celery, the usage is basically the same as celery, but the file path is customized. The related back-end configuration is also in config.
##### test

testFolder

##### startup file

start-celery.py 

start-gunicorn Start the live process, use gunicorn to guard



##### Current problem

- Sqlalchemy has released version 1.4, which provides asynchronous support. original idea was to be able to identify whether it is an asynchronous drive library through the SQLALCHEMY DATABASE URI variable in config.py to identify whether it is an asynchronous drive library to switch between synchronous session and asynchronous sessino, but After doing this, the auto-completion will be messed up, and there is no better idea.
- auto_db_session The current performance is not ideal, and it needs to be separated from the Base HTTP Middleware dependency, which has not been implemented yet. .

##### Contribution
1. Fork the repository
2. Create Feat_xxx branch
3. Commit your code
4. Create Pull Request
