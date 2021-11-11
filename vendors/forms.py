from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import VendorProfile


class VendorCreationForm(UserCreationForm):
  
  first_name = forms.CharField(max_length=50, required=True,
    widget=forms.TextInput(attrs={'placeholder': '*Name of business'}))
  last_name = forms.CharField(max_length=50, required=False,
    widget=forms.TextInput(attrs={'placeholder': '*Name of business'}))
  username = forms.EmailField(max_length=254, required=True, 
    widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
  password1 = forms.CharField(
    widget=forms.PasswordInput(attrs={'placeholder': '*Password..', 'class': 'password'}))
  password2 = forms.CharField(
    widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password..', 'class': 'password'}))

  #reCAPTCHA token
  token = forms.CharField(
    widget=forms.HiddenInput())
  
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
  
  
class VendorAuthForm(AuthenticationForm):
  
  username = forms.EmailField(max_length=254, required=True,
    widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
  password = forms.CharField(
    widget = forms.PasswordInput(attrs={'placeholder': '*Password..', 'class': 'password'}))
  
  class Meta:
    model = User
    fields= ('username', 'password', )
  
  
class VendorProfileForm(forms.ModelForm):
  
  company_name = forms.CharField(max_length=100, required= True, widget=forms.HiddenInput())
  address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
  city = forms.CharField(max_length=100, required= True, widget = forms.HiddenInput())
  state = forms.CharField(max_length=100, required= True, widget = forms.HiddenInput())
  zip_code = forms.CharField(max_length=9, required=True, widget = forms.HiddenInput())
  country = forms.CharField(max_length=50, required= True, widget = forms.HiddenInput())
  longitude = forms.CharField(max_length=50, required= True, widget = forms.HiddenInput())
  latitude = forms.CharField(max_length=50, required= True, widget = forms.HiddenInput())
  
  class Meta:
    model = VendorProfile
    fields = ('company_name', 'address', 'city', 'state', 'zip_code', 'country', 'longitude', 'latitude', )











