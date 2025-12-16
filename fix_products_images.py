"""
Script pour corriger les produits sans images dans la base de donnees
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ECOMMERCE.settings')
django.setup()

from BRYSHOP.models import Product

print("Recherche des produits sans image...")
products = Product.objects.all()
print(f"Total produits: {products.count()}")

products_without_image = []
for product in products:
    try:
        # Tenter d'acceder a l'image
        if product.image and product.image.name:
            # Verifier que le fichier existe
            if not product.image.storage.exists(product.image.name):
                products_without_image.append(product)
                print(f"X Produit avec image manquante: ID={product.id}, Title={product.title}, Path={product.image.name}")
        else:
            products_without_image.append(product)
            print(f"X Produit sans image: ID={product.id}, Title={product.title}")
    except Exception as e:
        products_without_image.append(product)
        print(f"X Erreur sur produit ID={product.id}: {str(e)}")

if products_without_image:
    print(f"\n{len(products_without_image)} produit(s) avec probleme d'image trouve(s)")
    print("Suppression automatique des produits problematiques...")
    
    for product in products_without_image:
        print(f"Suppression: {product.title}")
        product.delete()
    print(f"{len(products_without_image)} produit(s) supprime(s)")
else:
    print("Tous les produits ont une image valide!")

print("\nEtat final:")
print(f"Produits restants: {Product.objects.count()}")

