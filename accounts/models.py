from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



# Create your models here.
class CustomUser(AbstractUser):
    sexe_choices = [('M', 'Masculin'), ('F', 'Féminin')]
    role_choices = [
        ('client', 'Client'),
        ('boutiquier', 'Boutiquier'),
        ('admin', 'Admin'),
    ]
    telephone = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=sexe_choices)
    role = models.CharField(max_length=20, choices=role_choices, default='client')


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sexe = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')])
    telephone = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

