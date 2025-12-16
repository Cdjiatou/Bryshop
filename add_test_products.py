"""
Script pour ajouter des produits de test a la base de donnees
"""
import os
import django
from django.core.files.base import ContentFile
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ECOMMERCE.settings')
django.setup()

from BRYSHOP.models import Product, Category

print("Creation de produits de test...")

# Creer une categorie de test si elle n'existe pas
category, created = Category.objects.get_or_create(
    name="Electronique"
)
print(f"Categorie: {category.name} ({'creee' if created else 'existante'})")

# Liste de produits de test SANS images (pour tester la correction)
test_products = [
    {
        'title': 'Smartphone Galaxy',
        'description': 'Smartphone derniere generation avec ecran AMOLED',
        'price': 250000,
        'stock': 10,
    },
    {
        'title': 'Laptop Pro',
        'description': 'Ordinateur portable haute performance',
        'price': 450000,
        'stock': 5,
    },
    {
        'title': 'Casque Bluetooth',
        'description': 'Casque sans fil avec reduction de bruit',
        'price': 35000,
        'stock': 20,
    },
]

created_count = 0
for product_data in test_products:
    # Verifier si le produit existe deja
    if not Product.objects.filter(title=product_data['title']).exists():
        product = Product.objects.create(
            title=product_data['title'],
            description=product_data['description'],
            price=product_data['price'],
            stock=product_data['stock'],
            category=category
        )
        created_count += 1
        print(f"Produit cree: {product.title} (SANS image - pour tester le placeholder)")
    else:
        print(f"Produit existe deja: {product_data['title']}")

print(f"\n{created_count} nouveau(x) produit(s) cree(s) SANS images")
print(f"Total produits dans la base: {Product.objects.count()}")
print("\nCes produits n'ont PAS d'images, donc ils afficheront l'image placeholder.")
print("Verifiez que les placeholders s'affichent correctement sur la page d'accueil!")
