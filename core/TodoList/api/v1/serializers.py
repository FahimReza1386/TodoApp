from rest_framework import serializers
from ...models import Todo
from accounts.models import User , Profile



class TaskSerializer(serializers.ModelSerializer):

    absolute_url = serializers.SerializerMethodField()


    class Meta:
        model = Todo
        fields = ["id" , 'user',"Text" , "Ticked",'absolute_url']
        read_only_fields=['user']



    def get_absolute_url(self , obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self , instance):
        reps = super().to_representation(instance)

        request = self.context.get('request')
        if request.parser_context.get('kwargs').get('pk'):
            reps.pop('absolute_url')

        return reps

            