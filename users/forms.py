from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Your username",
        "class": "w-full py-4 px-6 rounded-xl",
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Your password",
        "class": "w-full py-4 px-6 rounded-xl",
    }))
