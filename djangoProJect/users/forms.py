from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # there's a (required) argument that accepts a bool val
    # ^ the def: True (an email is required)
    class Meta:
        model = User
        # ^specifying the model that we want the form to interact with
        fields = ['username', 'email', 'password1', 'password2']
        # ^ fields that gonna be shown in the the order given        
        # ^ class Mehta gives us a nested namespace for configurations 
        # and keeps the configurations in one place 
        # and within the configuration we're saying that the model 
        # that will be affected is the user model 
        # so for example when we do a form dot save it's going to 
        # save it to this user model and the fields that we have 
        # here in this list are the fields that we want in the form 
        # and in what order

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image']