from typing import Optional

from fastapi import HTTPException, Query
from sqlalchemy.orm import Query as QueryType


"""
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


class Pagination:
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def __init__(self, max_page_size: int = 400):
        self._queryset: Optional[QueryType] = None
        self.max_page_size = max_page_size

    def __call__(self, page: int = Query(1, alias=page_query_param, ge=1,
                                         description='Client can control the page using this query parameter.'),
                 page_size: int = Query(10, alias=page_size_query_param, ge=1,
                                        description='Client can control the page size using this query parameter.')):
        if page_size > self.max_page_size:
            raise HTTPException(detail=f'The maximum number of page_size cannot exceed {str(self.max_page_size)}',
                                status_code=400)
        self.page = page
        self.page_size = page_size
        return self

    @property
    def queryset(self):
        return self._queryset

    @queryset.setter
    def queryset(self, queryset: QueryType):
        if not isinstance(queryset, QueryType):
            raise ValueError('queryset must be of QueryType')
        self._queryset = queryset

    def get_page(self, num_pages: int = None):
        """
        Returns a valid query set. If no page argument is available, the query parameter passed in is used.
        :param num_pages: page number
        :return: queryset
        """
        if not isinstance(self.queryset, QueryType):
            raise NameError('queryset must be set before it can be used')
        if not num_pages:
            num_pages = self.page
        if num_pages < 1:
            raise ValueError('Incorrect page number')
        if not self.queryset:
            raise UnboundLocalError('QuerySet is uninitialized')
        return self._get_page(num_pages)

    def _get_page(self, num_pages: int):
        skip = (num_pages - 1) * self.page_size
        return self.queryset.offset(skip).limit(self.page_size).all()

    def count(self):
        """ Return the total number of pages. This method is inefficient """
        # session.query(func.count(MODELS.id)).filter_by(xxx).all()
        if not isinstance(self.queryset, QueryType):
            raise NameError('queryset must be set before it can be used')
        return self.queryset.count()
