from django.db import models
from django.db.models.fields.related import ForeignKey
from django.conf import settings
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
    date_added= models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return self.title 
    
    
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
    notch_pay_id = models.CharField(max_length=100, unique=True, help_text="ID unique de la transaction Notch Pay")
    reference = models.CharField(max_length=100, unique=True, help_text="Notre référence unique de commande")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="XAF")
    status = models.CharField(max_length=50) # complete, pending, failed, canceled
    customer_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True, help_text="Réponse brute JSON de Notch Pay")

    def __str__(self):
        return f"Paiement {self.reference} - {self.status}"

    
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.user} - {self.product.title}"