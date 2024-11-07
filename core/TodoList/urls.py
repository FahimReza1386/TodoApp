from django.urls import path,include
from . import views


app_name="TodoList"

urlpatterns = [
    path('' , views.Task.as_view() , name= 'Task'),
    path('add/' , views.New_Task.as_view() , name= 'New_Task'),
    path('delete/<int:pk>/' , views.Delete_Task.as_view() , name= 'Delete_Task'),
    path('update/<int:pk>/' , views.Update_Task.as_view() , name= 'Update_Task'),
    path('ticked/<int:pk>/' , views.Ticked.as_view() , name= 'Ticked'),
    path('api/v1/' , include('TodoList.api.v1.urls')),

]
