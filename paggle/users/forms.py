from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    code = forms.CharField(required=True)

    # gives us a nested name field for configurations
    class Meta:
        model = User
        fields = ['username', 'email', 'code', 'password1', 'password2']