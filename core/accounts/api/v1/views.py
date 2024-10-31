from django.urls import path, include
from rest_framework import generics , status # type: ignore
from .serializers import *
from rest_framework.response import Response # type: ignore


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