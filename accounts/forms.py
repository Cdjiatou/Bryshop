from django import forms
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['sexe', 'telephone', 'ville', 'pays']
