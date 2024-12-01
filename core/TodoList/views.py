from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render,get_object_or_404,HttpResponse
from django.views.generic import ListView,CreateView,DeleteView,UpdateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin 
from .models import Todo
from .forms import TaskForm , TickedForm
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .tasks import del_ticked_task

# Create your views here.


class Task(LoginRequiredMixin,ListView):
    template_name='TodoList/todo_list.html'
    context_object_name = 'todo'
    paginate_by = 7
    ordering = ['id']


    def get_queryset(self):
        user = self.request.user
        queryset = Todo.objects.filter(user = user)
        return queryset

    


class New_Task(LoginRequiredMixin , CreateView):
    """
        Create The Task Of Todo Model
    """
    template_name='TodoList/todo_list.html'
    model = Todo
    form_class=TaskForm
    success_url = '/'



    def form_valid(self , form ):
        form.instance.user = self.request.user
        return super().form_valid(form)



class Delete_Task(LoginRequiredMixin , DeleteView):
    model = Todo
    success_url = '/'
    template_name = 'TodoList/todo_del.html'


class Update_Task(LoginRequiredMixin , UpdateView):
    model = Todo
    success_url = '/'
    form_class = TaskForm
    template_name='TodoList/todo_form.html'
    


class Ticked(LoginRequiredMixin, UpdateView):  
    model = Todo  
    template_name = 'TodoList/todo_form.html'  # نام قالب خود را اینجا قرار دهید  
    form_class = TickedForm
    success_url = '/'