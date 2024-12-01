from faker import Faker  # type: ignore
from django.core.management.base import BaseCommand
from accounts.models import User,Profile
from TodoList.models import Todo
import random

class Command(BaseCommand):

    help = 'inserting Tasks Fake .'

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fake=Faker()


    def handle(self , *args , **kwargs):
        # Create The User By Faker
        user = User.objects.create_user(email = self.fake.email() , password=self.fake.password())
        user.is_verified = True
        user.save()

        # Change and Save The User Profile By Faker
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.save()
        print(profile)


        # Create Tasks By Faker 
        for _ in range(5):
            Todo.objects.create(
                user=user,
                Text=self.fake.paragraph(nb_sentences=5),
                Ticked=random.choice([True,False]),
            )




