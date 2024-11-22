from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'phone', 'address')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User