from django.urls import path, include
from rest_framework import generics , status  # type: ignore
from .serializers import *
from rest_framework.response import Response # type: ignore
from rest_framework.authtoken.views import ObtainAuthToken # type: ignore
from rest_framework.authtoken.models import Token # type: ignore

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

class CustomDiscardAuthToken(generics.GenericAPIView):
    pass