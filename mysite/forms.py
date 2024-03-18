# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from CustomAdmin.models import CustomAdmin


class CustomAdminRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    password1 = forms.CharField(max_length=8, required=True)
    password2 = forms.CharField(max_length=8, required=True)

    class Meta:
        model = CustomAdmin
        fields = ['username', 'email', 'password1', 'password2']


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
        
    class Meta:
        model = CustomAdmin
        fields = ['username', 'password']
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    password1 = forms.CharField(max_length=8, required=True)
    password2 = forms.CharField(max_length=8, required=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2']


class CheckoutForm(forms.Form):
    Shipping_address = forms.CharField(label='Address', max_length=100, widget=forms.TextInput(attrs={'required': True}))
    phone_number = forms.CharField(label='Phone Number', max_length=12, widget=forms.TextInput(attrs={'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}', 'required': True}))

