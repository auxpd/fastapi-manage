

class Pagination:
    """
    分页对象
    """
    def __init__(self, request, queryset, per_page):
        self.request = request
        self.queryset = queryset


    def get_paginated_response(self, data):
        return {
            'count': None,
            'data': None
        }

