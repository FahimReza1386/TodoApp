from django.urls import path, include
from django.shortcuts import get_object_or_404
from rest_framework import generics , status  # type: ignore
from .serializers import *
from rest_framework.response import Response# type: ignore
from django.http import HttpResponse , JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView , TokenVerifyView # type: ignore
from django.core.mail import send_mail
from mail_templated import EmailMessage # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from .utils import EmailThread
from django.conf import settings
import jwt # type: ignore
from jwt.exceptions import ExpiredSignatureError , InvalidSignatureError # type: ignore
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework import viewsets # type: ignore
from rest_framework.decorators import api_view # type:ignore
import requests
import random

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
            user_obj = get_object_or_404(User , email = email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl' ,  {'token':token} , 'fahimreza20200@gmail.com' , to=['fahimreza2200@gmail.com'])
            EmailThread(email_obj).start()

            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    

    def get_tokens_for_user(self ,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    

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
    


class ActivationApiView(APIView):
    def get(self , request , token , *args , **kwargs):
        # DECODE -> ID User
        try:
            token = jwt.decode(token , settings.SECRET_KEY , algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({'details':'Token Has Been Expired .'} , status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'details':'Token Is Not Valid .'} , status=status.HTTP_400_BAD_REQUEST)
        
        # Get object by id
        user_obj = get_object_or_404(User , pk=user_id)
        if user_obj.is_verified:
            return Response({'details' : 'your account is verified .'})
        else :
            user_obj.is_verified = True
            user_obj.save()
            return Response({'details' : 'your account have been verified and activated successfully .'})


class ActivationResentApiView(generics.GenericAPIView):
    serializer_class = ActivationResentApiSerializer

    def post(self , request , *args , **kwargs):
      
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl' ,  {'token':token} , 'fahimreza20200@gmail.com' , to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response({"details" : 'user activation resent successfully .'} , status=status.HTTP_200_OK)



    def get_tokens_for_user(self , user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset , user=self.request.user)
        return obj
    


@cache_page(1200)
@api_view(["GET"])
def get_weather(request):
    content = {"user_feed": request.user.email}
    API_KEY = '8f74ae0e2b6622ee9f7910440e3f8a82'  
    city = 'Tehran'  
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'  
    response = requests.get(url)
    rdm = random.choice(['True','False','Hi','How','Hello'])
    return Response([content,rdm,response.json()])
