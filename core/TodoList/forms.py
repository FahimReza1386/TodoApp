from .models import Todo
from django import forms




class TaskForm(forms.ModelForm):
    Text = forms.CharField(max_length=200 , required=True , help_text='' , label='')

    class Meta:
        model = Todo
        fields=['Text']

class TickedForm(forms.ModelForm):
    Ticked = forms.BooleanField(required=False , help_text='' , label='')

    class Meta:
        model = Todo
        fields=['Ticked']
