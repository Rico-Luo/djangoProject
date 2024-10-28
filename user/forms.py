from django import forms
from .models import User

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email']