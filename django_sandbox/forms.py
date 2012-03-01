from django import forms
from django.contrib.auth.models import User
import re

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class DetailsForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    
class RegisterForm(forms.Form):
    username=forms.CharField()
#    headpic=forms.ImageField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput,label="Password")
    password2=forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if not re.match("^[a-zA-Z_]*$", username):
            raise forms.ValidationError("Username can only contain characters and Underscore ( _ )")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists")
    
    def clean_password2(self):
        password1=self.cleaned_data.get('password1','')
        password2=self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("The two password fields must match")
        return password2
class ChangePassForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    
    def clean_confirm_password(self):
        password1=self.cleaned_data.get('new_password','')
        password2=self.cleaned_data['confirm_password']
        if password1 !=password2:
            raise forms.ValidationError("New password and Confirm Password fields do not match")
        return password2
#    
#    def clean_old_password(self):
#        password=self.cleaned_data['old_password']
#        try:
#            User.objects.get()
        
    