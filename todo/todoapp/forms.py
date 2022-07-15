from django import forms
from django.forms import ModelForm
from .models import Todo


class TodoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add new task'}))

    class Meta:
        model = Todo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(TodoForm, self).__init__(*args, **kwargs)
