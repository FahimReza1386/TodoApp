from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse
from django.views.generic import ListView
from .models import Todo
# Create your views here.



class Task(ListView):
    template_name='list_todo.html'
    context_object_name = 'todo'
    paginate_by = 10
    ordering = ['id']


    def get_queryset(self):
        user = self.request.user
        queryset = Todo.objects.filter(user = user)
        return queryset