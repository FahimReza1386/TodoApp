from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class PermissionPagination(PageNumberPagination):
    page_size = 3



    def get_paginated_response(self, data):
        return Response({
            'Link_Tasks': {
                'Next_Task': self.get_next_link(),
                'Previous': self.get_previous_link()
            },
            'Tasks_Count': self.page.paginator.count,
            'Total_Pages': self.page.paginator.num_pages,
            'The_Tasks_Information': data
    })