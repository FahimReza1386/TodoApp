from rest_framework import serializers # type: ignore
from ...models import *
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore

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
    

class CustomObtainAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email') , write_only=True)
    password = serializers.CharField(label=_('Password') , style={'input_type': 'password'},trim_whitespace=False, write_only=True)
    token = serializers.CharField(label=_('Token') , read_only=True)


    def validate(self , attrs):
        username = attrs.get('email')
        password = attrs.get('password')


        if username and password :
            user = authenticate(request=self.context.get('request'),username=username , password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({'detail':'user is not verified .'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    


class CustomTokenObtainPairViewSerializer(TokenObtainPairSerializer):

    def validate(self , attrs):
        validated_data=super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({'detail':'your account is not verified.'})
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        
        return validated_data