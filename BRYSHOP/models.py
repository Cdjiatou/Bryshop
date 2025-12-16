from django.db import models
from django.db.models.fields.related import ForeignKey
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)
    
    #class pour ranger les produits par ordre d'ajout
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):  #fonction qui retourne l'element par son mom
        return self.name   
        
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    date_added= models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return self.title
    
    def est_disponible(self):
        return self.stock > 0
    
    def peut_commander(self, quantite):
        return self.stock >= quantite 
    
    
class Commande(models.Model):
    items = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_commande']
        
    def __str__(self):
        return self.nom 
    
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    notch_pay_id = models.CharField(max_length=100, null=True, blank=True, help_text="ID unique de la transaction Notch Pay")
    reference = models.CharField(max_length=100, unique=True, help_text="Notre référence unique de commande")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="XAF")
    status = models.CharField(max_length=50) # complete, pending, failed, canceled
    customer_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    user_card = models.ForeignKey('UserCard', on_delete=models.SET_NULL, null=True, blank=True, help_text="Carte bancaire utilisée pour le paiement")
    created_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True, help_text="Réponse brute JSON de Notch Pay")

    def __str__(self):
        return f"Paiement {self.reference} - {self.status}"


class UserCard(models.Model):
    """Modèle pour stocker les cartes bancaires des utilisateurs de manière sécurisée"""
    CARD_TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
        ('other', 'Autre'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_cards')
    card_token = models.CharField(max_length=255, unique=True, help_text="Token sécurisé fourni par le gateway de paiement")
    last_four_digits = models.CharField(max_length=4, help_text="4 derniers chiffres de la carte")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, default='other')
    expiry_month = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    expiry_year = models.PositiveIntegerField(validators=[MinValueValidator(2024), MaxValueValidator(2050)])
    cardholder_name = models.CharField(max_length=100, help_text="Nom du titulaire de la carte")
    is_default = models.BooleanField(default=False, help_text="Carte par défaut pour les paiements")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        unique_together = ['user', 'card_token']

    def __str__(self):
        return f"{self.card_type.title()} ****{self.last_four_digits} - {self.cardholder_name}"

    def clean(self):
        # Validation personnalisée
        if self.expiry_year < 2024 or (self.expiry_year == 2024 and self.expiry_month < 12):
            raise ValidationError("La carte bancaire a expiré.")

        # S'assurer qu'il n'y a qu'une seule carte par défaut par utilisateur
        if self.is_default:
            UserCard.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)

    @property
    def is_expired(self):
        """Vérifie si la carte a expiré"""
        from datetime import date
        today = date.today()
        return (self.expiry_year < today.year) or (self.expiry_year == today.year and self.expiry_month < today.month)

    @property
    def masked_number(self):
        """Retourne le numéro masqué pour affichage"""
        return f"**** **** **** {self.last_four_digits}"

    @property
    def expiry_date_display(self):
        """Retourne la date d'expiration formatée"""
        return f"{self.expiry_month:02d}/{self.expiry_year}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} (x{self.quantity})"


class Order(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traitement', 'En traitement'),
        ('expedie', 'Expédié'),
        ('livre', 'Livré'),
        ('annule', 'Annulé'),
    ]
    
    MODE_PAIEMENT_CHOICES = [
        ('livraison', 'Paiement à la livraison'),
        ('orange_money', 'Orange Money'),
        ('mtn_money', 'MTN Mobile Money'),
        ('carte_bancaire', 'Carte bancaire'),
    ]
    
    STATUT_PAIEMENT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('echoue', 'Échoué'),
    ]
    
    numero_commande = models.CharField(max_length=50, unique=True, editable=False, default='CMD-###')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, default='livraison')
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT_CHOICES, default='en_attente')
    nom = models.CharField(max_length=150, default='')
    email = models.EmailField(default='')
    address = models.CharField(max_length=200, default='')
    ville = models.CharField(max_length=200, default='')
    pays = models.CharField(max_length=300, default='')
    zipcode = models.CharField(max_length=300, default='')
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero_commande:
            import uuid
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().hex[:6]).upper()
            self.numero_commande = f"CMD-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def calculer_frais_livraison(self):
        """Calcule les frais de livraison selon le pays"""
        frais_par_pays = {
            'Cameroun': 1500,
            'France': 5000,
            'Côte d\'Ivoire': 2000,
            'Sénégal': 2500,
            'Gabon': 3000,
        }
        return frais_par_pays.get(self.pays, 2000)
    
    def total_commande(self):
        """Calcule le total avec frais de livraison"""
        return (self.product.price * self.quantity) + self.frais_livraison

    def __str__(self):
        return f"{self.numero_commande} - {self.user.username}"