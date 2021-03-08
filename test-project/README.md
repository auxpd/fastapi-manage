"""
libs/dependencies.py
在使用前需要在config.py中配置登陆接口 UTILS_LOGIN_PATH
之后直接导入即可 
"""

"""
libs/dependencies.py/Utils
工具类
返回Request对象, 额外包含db属性
utils.app  # app对象
utils.client  # 客户端的来源地址和端口
utils.method  # 请求方法
utils.headers  # 请求头
utils.cookies  # cookies
utils.query_params  # 查询参数(page=1&page_size=10)
utils.scope  # scope对象
utils.session
utils.user  # 包含is_authenticated, display_name 属性  需要添加authentication中间件！
utils.auth  # 包含scopes(用户所在的组 list)  需要添加authentication中间件！
utils.db.session  # 数据库会话对象  需要添加DBSessionMiddleware中间件！
...
"""

"""
libs/pagination.py
1. 写好查询集, 不加.all() 或 one(), first() 之类的触发查询的操作
2. 在接口中注入 pagination依赖(可设置最大每页数量 Pagination(300))
3. pagination.queryset = QuerySet  # 设置分页对象的查询集
4. pagination.get_page() 获取当前页的数据, pagination.count() 获取当前页的数据总数
例：
async def get_all_users(pagination: Pagination = Depends()) -> Any:
    queryset = session.query(models.User)  # 确定查询集
    pagination.queryset = queryset  # 传入查询集
    return pagination.get_page()  # 取分页数据, 不填参数默认取用户的查询参数作为页数
"""

"""
middleware/middleware.py
认证中间件
添加该中间件后，会解析用户请求头中的jwt, 根据载荷里的sub为用户唯一标识, group为用户组
request.auth.scopes 用户所在组(list)
request.user.is_authenticated 是否是认证用户(已登录)(bool)
使用Utils：
utils.auth.scopes 用户组
utils.user.is_authenticated 是否死后认证用户

BearerAuthBackend
    headers: 请求头中存放jwt的key
    auth_type： 认证类型
    user_id_flag： jwt载荷中存放用户唯一标识的key
    user_group_flag： jwt载荷中存放用户组信息的key
    
可以完善AuthUser中的obj 返回数据库中的用户对象, 之后可以utils.user.obj.用户属性 来获取到用户对象信息
"""

"""
middleware/rate_limit.py
1. 在config中配置rate后端RATE_LIMIT_BACKEND_HOST, RATE_LIMIT_BACKEND_PORT, RATE_LIMIT_BACKEND_DB, RATE_LIMIT_BACKEND_PASS
2. 确定如何取唯一标识的函数(auth_func)
3. 配置config参数, 也就是每个接口的访问频率限制 格式:  { r'^/hello': [Rule(minute=2, group='default'), Rule(group='admin')] }
4. 注册中间件 app.add_middleware(RateLimitMiddleware, config=config)
"""