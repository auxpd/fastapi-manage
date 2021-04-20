import sqlalchemy as __sqlalchemy
from sqlalchemy.engine import Engine as __Engine, create_engine as __create_engine
from sqlalchemy.orm import sessionmaker as __sessionmaker

__ASYNC_VERSION__ = "1.4.0"

from sqlalchemy.orm import Session as __Session


def __compared_version(ver1, ver2):
    """
    Compare the size of the two version numbers
    :param ver1: Version number 1
    :param ver2: Version number 2
    :return: ver1< = >ver2 Return separately -1/0/1
    """
    list1 = str(ver1).split(".")
    list2 = str(ver2).split(".")
    # 循环比较每一个小数点区间的数字
    for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
        if int(list1[i]) == int(list2[i]):
            pass
        elif int(list1[i]) < int(list2[i]):
            return -1
        else:
            return 1
    # 比较长度, 值相等的情况下 做长度比较
    if len(list1) == len(list2):
        return 0
    elif len(list1) < len(list2):
        return -1
    else:
        return 1


def __async_support() -> bool:
    """ 检测sqlalchemy是否支持异步 """
    return __compared_version(__sqlalchemy.__version__, __ASYNC_VERSION__) == 1


def auto_engine(uri, *args, **kwargs):
    """ 创建engine """
    sync_engine = __create_engine(uri, *args, **kwargs)
    if __async_support():
        from sqlalchemy.ext.asyncio import AsyncEngine
        if sync_engine.dialect.is_async:
            return AsyncEngine(sync_engine)
    return sync_engine


def auto_sessionmaker(bind=None, class_=__Session, autoflush=True, autocommit=False,
                      expire_on_commit=True, info=None, **kwargs) -> __sessionmaker:
    """ 创建会话工厂 """
    parameter = {"bind": bind, "autoflush": autoflush, "autocommit": autocommit, "expire_on_commit": expire_on_commit,
                 "info": info, "class_": class_}
    parameter.update(kwargs)
    if __async_support():
        from sqlalchemy.ext.asyncio import AsyncEngine as __AsyncEngine
        bind_type = type(bind)
        if bind_type == __Engine:
            pass
        elif bind_type == __AsyncEngine:
            if parameter.get('class_') == __Session:
                parameter['class_'] = __AsyncEngine
    return __sessionmaker(**kwargs)
