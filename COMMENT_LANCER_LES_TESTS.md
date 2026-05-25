# 🧪 Comment Lancer les Tests

## ✅ Configuration Terminée !

Les tests sont maintenant configurés pour utiliser **SQLite automatiquement** quand tu lances les tests.  
**Tu n'as plus besoin de démarrer MySQL pour les tests !**

## 🚀 Commande Simple

```bash
python manage.py test
```

C'est tout ! Les tests vont :
- ✅ Utiliser SQLite en mémoire (pas besoin de MySQL)
- ✅ S'exécuter très rapidement
- ✅ Ne pas toucher à ta base de données MySQL de développement

## 📊 Résultats Actuels

**90 tests créés** :
- ✅ **74 tests réussis** (82%)
- ❌ **16 tests à corriger** (18%)

### Tests qui fonctionnent ✅

- **Modèles** : CustomUser, Client, Notification, Product, Category, Cart, Order, Payment, Wishlist
- **Formulaires** : CategoryForm (validation complète)
- **Vues** : Dashboard boutiquier, authentification, panier, checkout

### Tests à corriger ❌

Les erreurs sont principalement dues à :
1. Noms d'URLs incorrects dans les tests
2. Un bug dans le calcul du total de commande (float vs Decimal)
3. Génération du numéro de commande

## 📁 Structure des Tests

```
accounts/tests/
├── test_models.py       # Tests des modèles utilisateurs

BRYSHOP/tests/
├── test_models.py       # Tests des modèles e-commerce
├── test_forms.py        # Tests des formulaires
└── test_views.py        # Tests des vues
```

## 🎯 Commandes Utiles

```bash
# Tous les tests
python manage.py test

# Tests d'une application
python manage.py test accounts
python manage.py test BRYSHOP

# Tests avec plus de détails
python manage.py test --verbosity=2

# Tests d'un fichier spécifique
python manage.py test BRYSHOP.tests.test_models

# Test d'une classe spécifique
python manage.py test BRYSHOP.tests.test_models.ProductModelTest

# Test d'une méthode spécifique
python manage.py test BRYSHOP.tests.test_models.ProductModelTest.test_product_creation
```

## 💡 Comment ça marche ?

Le fichier `ECOMMERCE/settings.py` détecte automatiquement quand tu lances les tests et utilise SQLite :

```python
# Dans settings.py
TESTING = 'test' in sys.argv

if TESTING:
    # SQLite pour les tests
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
else:
    # MySQL pour le développement
    DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', ...}}
```

## 🔧 Pour le Développement Normal

Quand tu lances ton serveur Django normalement, il utilise toujours MySQL :

```bash
python manage.py runserver  # Utilise MySQL
```

Seule la commande `test` utilise SQLite !

---

**Note** : Les tests sont indépendants de ta base de données MySQL. Tu peux les lancer à tout moment sans risque !
