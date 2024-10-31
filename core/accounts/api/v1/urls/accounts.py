from django.urls import path , include
from .. import views


urlpatterns = [
    path('registration/' , views.RegistrationApi.as_view() , name="Registration With Api")
]