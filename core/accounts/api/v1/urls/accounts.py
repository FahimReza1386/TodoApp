from django.urls import path , include
from .. import views


urlpatterns = [
    #  Registration With Api
    path('registration/' , views.RegistrationApi.as_view() , name="Registration With Api"),

    #  Login and Logout With Api Token

    path('token/login/' , views.CustomObtainAuthToken.as_view() , name="Login-Token"),
    path('token/logout/' , views.CustomDiscardAuthToken.as_view() , name="Logout-Token"),


]