from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Vendor
from inventory.models import BrewProduct, BrewProductImage


# class CustomUserCreationForm(UserCreationForm):
  
#   first_name = forms.CharField(max_length=50, required=True,
#     widget=forms.TextInput(attrs={'placeholder': 'Name of Business'}))
#   last_name = forms.CharField(max_length=50, required=False,
#     widget=forms.TextInput(attrs={'placeholder': 'Slogan'}))
#   username = forms.EmailField(max_length=254, required=True, 
#     widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#   password1 = forms.CharField(
#     widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'password'}))
#   password2 = forms.CharField(
#     widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'password'}))
 
#   class Meta:
#     model = User
#     fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )
  
# class SignupForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)  
  
# class LoginForm(AuthenticationForm):
  
#   username = forms.EmailField(max_length=254, required=True,
#     widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#   password = forms.CharField(
#     widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'password'}))
  
#   class Meta:
#     model = User
#     fields= ('username', 'password', )
  
class BrewProductForm(ModelForm):
    class Meta:
        model = BrewProduct
        fields = ['brewcategory', 'title', 'description', 'price', 'image']

class BrewProductImageForm(ModelForm):
    class Meta:
        model = BrewProductImage
        fields = ['image']
# class VendorProfileForm(forms.ModelForm):
  
#   company_name = forms.CharField(max_length=100, required= False, widget = forms.HiddenInput())
#   address = forms.CharField(max_length=100, required=True, widget = forms.HiddenInput())
#   locality = forms.CharField(max_length=100, required= True, widget = forms.HiddenInput())
#   state = forms.CharField(max_length=100, required= True, widget = forms.HiddenInput())
#   postal_code = forms.CharField(max_length=9, required=True, widget = forms.HiddenInput())
#   country = forms.CharField(max_length=50, required= True, widget = forms.HiddenInput())
#   longitude = forms.CharField(max_length=50, required= True, widget = forms.HiddenInput())
#   latitude = forms.CharField(max_length=50, required= True, widget = forms.HiddenInput())
  
#   class Meta:
#     model = User
#     fields = ('company_name', 'address', 'locality', 'state', 'postal_code', 'country', 'longitude', 'latitude', )


# Upload image for vendor
# class VendorProfilePictureForm(ModelForm):

#     class Meta:
#         model = VendorProfile
#         fields = ('image',)


# class VendorCreatePostForm (ModelForm):
#     title = forms.CharField(max_length=100, required=True, label="", widget=forms.TextInput(attrs={'placeholder': 'Brew Name', 'class': 'modal-form-input',}))
#     description = forms.CharField(max_length=5000, required=True, label="", widget=forms.TextInput(attrs={'placeholder': 'Description', 'class': 'modal-form-input',}))
    
#     class Meta:
#         model: PostInventory
#         fields = ('title', 'description', 'image')






