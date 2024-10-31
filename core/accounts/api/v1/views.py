from django.urls import path, include
from django.shortcuts import get_object_or_404
from rest_framework import generics , status  # type: ignore
from .serializers import *
from rest_framework.response import Response # type: ignore
from rest_framework.authtoken.views import ObtainAuthToken # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView , TokenVerifyView # type: ignore
from django.core.mail import send_mail
from mail_templated import EmailMessage # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from .utils import EmailThread


class RegistrationApi(generics.GenericAPIView):
    serializer_class = RegistrationApiSerializer


    def post(self , request , *args , **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email' : email 
            }

            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomObtainAuthTokenSerializer
    
    def post(self , request , *args , **kwargs):
        serializer = self.serializer_class(data = request.data , context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token , created = Token.objects.get_or_create(user = user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })

class CustomDiscardAuthToken(APIView):
    permission_class = [IsAuthenticated]

    def post(self , request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairViewSerializer


class CustomTokenRefreshView(TokenRefreshView):
    pass

class CustomTokenVerifyView(TokenVerifyView):
    pass



class TestEmailSend(generics.GenericAPIView):

    def get(self , request , *args ,**kwargs):
        self.email = "Fahim@gmail.com"
        user_obj = get_object_or_404(User , email = self.email)
        token = self.get_tokens_for_user(user_obj)


    #  Send Mail with console .

    # send_mail(
    #     "Subject here",
    #     "Here is the message.",
    #     "from@example.com",
    #     ["Fahimreza20200@gmail.com"],
    #     fail_silently=False,
    # )
    
        # Send Email By Html With smtp4dev
        # messages = EmailMessage('email/hi.tpl' ,  {'token':token} , 'fahimreza20200@gmail.com' , to=['fahimreza2200@gmail.com'])
        # messages.send()

        email_obj = EmailMessage('email/hi.tpl' ,  {'token':token} , 'fahimreza20200@gmail.com' , to=['fahimreza2200@gmail.com'])
        EmailThread(email_obj).start()

        return Response('Email Send.')


    def get_tokens_for_user(self , user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
