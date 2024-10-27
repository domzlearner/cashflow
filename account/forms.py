
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    # security_question = forms.CharField(max_length=255, help_text='Enter a security question.')
    # security_answer = forms.CharField(max_length=255, help_text='Enter the answer to your security question.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        # fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'security_question', 'security_answer')

class SignInForm(AuthenticationForm):
    username = forms.EmailField(label='Email')