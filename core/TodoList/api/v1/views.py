from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerPermissions
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import PermissionPagination
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models import Todo


class TaskModelView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwnerPermissions] 
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_fields = ['Ticked']
    search_fields = ['Text']
    ordering_fields = ['Ticked']
    # pagination_class = PermissionPagination

    def get_queryset(self): 
        query= Todo.objects.filter(user = self.request.user)
        return query

    @action(methods=['get'],detail=False)
    def get_user_id(self , request):
        id = request.user.id
        return Response({'Your Id :':str(id)})