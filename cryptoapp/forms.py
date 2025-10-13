from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# User Registration Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# Example User Input Form for Coin Search
class CoinSearchForm(forms.Form):
    coin_name = forms.CharField(label="Enter coin name", max_length=50)
