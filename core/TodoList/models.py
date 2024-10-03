from django.db import models
from django.contrib.auth import get_user_model 
# Create your models here.

User = get_user_model()

class Todo(models.Model):
    """
        Todo Model For User
    """
    
    
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    Text=models.TextField(max_length=500)

    def __str__(self):
        return f'{self.user}'