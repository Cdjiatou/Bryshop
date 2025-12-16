from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings




# Définition des choix pour le sexe (utilisé dans CustomUser)
USER_SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]

# Définition des choix pour le sexe (utilisé dans Client)
CLIENT_SEXE_CHOICES = [('Homme', 'Homme'), ('Femme', 'Femme')]


# Modèle Utilisateur Personnalisé
class CustomUser(AbstractUser):
<<<<<<< HEAD
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
=======
   
    telephone = models.CharField(max_length=20, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    # Utilisation correcte de la variable définie
    sexe = models.CharField(max_length=1, choices=USER_SEXE_CHOICES, blank=True, null=True)

    # Note : Le champ is_staff de Django est hérité de AbstractUser
    
    def __str__(self):
        return self.username
>>>>>>> aa2d42933048647c932f91eaddfba79a6349a236


# Modèle Client (Profil étendu)
class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # RÔLE : Ajout du champ is_shop_owner
    is_shop_owner = models.BooleanField(default=False) 
    
    # Champs redondants avec CustomUser (maintenus pour l'adaptation)
    # Utilisation correcte de la variable définie
    sexe = models.CharField(max_length=10, choices=CLIENT_SEXE_CHOICES, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # Utilise le nom complet de l'utilisateur CustomUser
        return f"{self.user.first_name} {self.user.last_name}"
    
    # Propriété utilitaire pour récupérer le statut du rôle
    @property
    def est_boutiquier(self):
        return self.is_shop_owner or self.user.is_superuser


# Nouveau Modèle : Notification
class Notification(models.Model):
    # L'utilisateur destinataire
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    
    # Message de la notification
    message = models.CharField(max_length=255)
    
    # Lien vers l'objet concerné (ex: une commande)
    url = models.CharField(max_length=255, blank=True, null=True) 
    
    # Indicateur si la notification a été lue
    is_read = models.BooleanField(default=False)
    
    # Horodatage
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notif pour {self.user.username}: {self.message[:30]}..."