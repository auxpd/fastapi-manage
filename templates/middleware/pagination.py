from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class PaginationMiddleware(BaseHTTPMiddleware):
    """
    分页中间件
    """
    def __init__(self, app, page_query_param: str = 'page',
                 page_size_query_param: str = 'page_size',):
        super().__init__(app)
        self.page_query_param = page_query_param
        self.page_size_query_param = page_size_query_param

    async def dispatch(self, request, call_next):
        request.state.num_pages = request.query_params.get(self.page_query_param, 1)
        if not isinstance(request.state.num_pages, int) or request.state.num_pages < 1:
            raise HTTPException(detail=f'invalid number of {self.page_query_param}',
                                status_code=status.HTTP_400_BAD_REQUEST)

        request.state.page_size = request.query_params.get(self.page_size_query_param, None)
        if not isinstance(request.state.page_size, int) or request.state.page_size < 1:
            raise HTTPException(detail=f'invalid number of {self.page_size_query_param}',
                                status_code=status.HTTP_400_BAD_REQUEST)
        response = await call_next(request)
        return response
