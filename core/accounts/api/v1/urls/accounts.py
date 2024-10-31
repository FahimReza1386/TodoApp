from django.urls import path , include
from .. import views
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView , TokenVerifyView # type: ignore


urlpatterns = [
    #  Registration With Api
    path('registration/' , views.RegistrationApi.as_view() , name="Registration With Api"),

    #  Login and Logout With Api Token

    path('token/login/' , views.CustomObtainAuthToken.as_view() , name="Login-Token"),
    path('token/logout/' , views.CustomDiscardAuthToken.as_view() , name="Logout-Token"),


    # Create And Refresh And Verify with json web token (jwt)

    path('jwt/create/' , views.CustomTokenObtainPairView.as_view() , name="Create-jwt"),
    path('jwt/refresh/' , views.CustomTokenRefreshView.as_view() , name="refresh-jwt"),
    path('jwt/verify/' , views.CustomTokenVerifyView.as_view() , name="verify-jwt"),


    # Test Send email Static
    path('test-email/' , views.TestEmailSend.as_view() , name="Test-Email"),

]