from rest_framework import viewsets # type: ignore
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly # type: ignore
from .permissions import IsOwnerPermissions
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from .paginations import PermissionPagination
from rest_framework.filters import SearchFilter , OrderingFilter # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from ...models import Todo


class TaskModelView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerPermissions] 
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
    
    def perform_create(self, serializer):  
        serializer.save(user=self.request.user)  
