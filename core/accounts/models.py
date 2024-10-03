from django.db import models
from django.contrib.auth.models import (AbstractBaseUser ,BaseUserManager,PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class UserManager(BaseUserManager):

    """
        THe Create User and SuperUser
    """

    def create_user(self , email , password , **extra_fields):
        """
            Create and Save a User With The Given email and password , or extra data. 
        """
        if not email:
            raise ValueError(_('The Email Must Be Set'))
        email= self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self , email , password,**extra_fields):
        """
            Create and Save a SuperUser With The Given email and password , or extra data. 
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("is_staff must have is True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("is_superuser must have is True"))

        return self.create_user(email , password , **extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):

    """
        Custom User Model our App
    """

    email=models.EmailField(max_length=200 , unique=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    # is_verified=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    first_name=models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects=UserManager()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.email
    


class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(null=True , blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.user}'
    

@receiver(post_save , sender = User)
def post_save(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user = instance)