from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User
 
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'password')