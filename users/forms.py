from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    ## Registration form for the custom email-based user model
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]