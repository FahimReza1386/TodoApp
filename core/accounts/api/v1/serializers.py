from rest_framework import serializers # type: ignore
from ...models import *
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class RegistrationApiSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250 , required=True , write_only=True)
    class Meta:
        model = User
        fields=['email'  , 'password' , 'password1']


    def validate(self , attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'details':'password dose not matched .'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        return super().validate(attrs=attrs)


    def create(self , validate_data):
        validate_data.pop('password1' , None)
        return User.objects.create_user(**validate_data)