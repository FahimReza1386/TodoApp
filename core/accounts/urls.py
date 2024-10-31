from django.urls import path , include
from . import views


urlpatterns = [
    path('' , views.index , name=["index"]),
    path('api/v1/' , include('accounts.api.v1.urls')),
]