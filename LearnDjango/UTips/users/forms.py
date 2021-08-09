from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Adding additional fields to the User Registration page
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        