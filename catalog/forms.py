from django import forms
from catalog.models import Product
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#create models here

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'photo')

class SignupForm(UserCreationForm):
    class Meta:
        model= User
        fields= ('username','password1','password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    