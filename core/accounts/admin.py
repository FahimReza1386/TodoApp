from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile
from django.contrib.auth.forms import UserChangeForm , UserCreationForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User 
    list_display=('email' , 'is_staff' , 'is_active' , 'is_superuser')
    list_filter=('is_staff','is_superuser' , 'is_active')
    searching_fields = ('email',)
    ordering=('email',)
    fieldsets=(
        ('Authentications', {
            "fields" : (
                "email" , 'password'
            )
        }),
        ('Permission', {
            "fields" : (
                "is_staff" , 'is_superuser' , 'is_active' 
            )
        }),
        ('group Permission', {
            "fields" : (
                'groups' , 'user_permissions'
            )
        }),
        ('important date', {
            "fields" : (
                'last_login' ,
            )
        }),
    )

    add_fieldsets= (
        (None , {
            'classes' : ('wide',),
            'fields' : ('email' , 'password1' , 'password2' ,'is_staff' , 'is_active' , 'is_superuser')
        }),
    )




admin.site.register(Profile)
admin.site.register(User , CustomUserAdmin)