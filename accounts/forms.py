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



# Nouveau Formulaire 1: Pour les champs du modèle User (Nom, Prénom, Email)
class UserUpdateForm(forms.ModelForm):
    # Rendre l'email facultatif pour la MAJ si vous le souhaitez, ou obligatoire
    email = forms.EmailField(required=True) 

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# Nouveau Formulaire 2: Pour les champs du modèle Client
class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        # Assurez-vous d'utiliser les mêmes champs que dans votre modèle Client
        fields = ['telephone', 'sexe', 'ville', 'pays'] 
        widgets = {
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}), # Utiliser Select pour les choix
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
        }