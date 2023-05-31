from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    
# Define a class for the UserRegistrationForm
class UserRegistrationForm(forms.ModelForm):
    # Create two password fields, labeled 'Password' and 'Password Confirmation'
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    
    # Define the meta class to specify the model and fields to use for the form
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    # Define the clean_password2 method to validate that the passwords match
    def clean_password2(self):
        cleaned_data = self.cleaned_data
        # Check if the passwords don't match and raise a validation error
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        # Return the password2 field if the validation passes
        return cleaned_data['password2']
    
    # Define the clean_email method to validate that the email isn't already in use
    def clean_email(self):
        data = self.cleaned_data['email']
        # Check if the email already exists in the database and raise a validation error
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use')
        # Return the email if the validation passes
        return data

class UserEditForm(forms.ModelForm):
    # Define the meta class to specify the model class and fields to use for form
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def clean_email(self):
        # Get the email data from the cleaned_data dictionary
        data = self.cleaned_data['email']
    
        # Exclude the current instance of the User model (to allow editing the email address)
        # and filter the User model for any instances that have the same email
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
    
        # If there's already a User instance with that email address, raise a validation error
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
    
        # Return the email data
        return data
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }
