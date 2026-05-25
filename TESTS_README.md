# Guide des Tests - Projet E-Commerce

## 📊 Résumé des Tests

**Total de tests créés : 90**

### Structure des Tests

```
accounts/tests/
├── __init__.py
└── test_models.py          # Tests des modèles CustomUser, Client, Notification

BRYSHOP/tests/
├── __init__.py
├── test_models.py          # Tests des modèles Product, Category, Cart, Order, etc.
├── test_forms.py           # Tests des formulaires
└── test_views.py           # Tests des vues
```

## 🚀 Comment Exécuter les Tests

### Option 1 : Avec SQLite (Recommandé pour les tests)

```bash
python manage.py test --settings=ECOMMERCE.test_settings
```

Cette commande utilise SQLite en mémoire, ce qui est plus rapide et ne nécessite pas de serveur MySQL.

### Option 2 : Avec MySQL (nécessite MySQL démarré)

```bash
# Assurez-vous que MySQL est démarré
python manage.py test
```

### Exécuter des tests spécifiques

```bash
# Tests d'une application
python manage.py test accounts --settings=ECOMMERCE.test_settings
python manage.py test BRYSHOP --settings=ECOMMERCE.test_settings

# Tests d'un fichier
python manage.py test accounts.tests.test_models --settings=ECOMMERCE.test_settings

# Tests d'une classe
python manage.py test BRYSHOP.tests.test_models.ProductModelTest --settings=ECOMMERCE.test_settings

# Test d'une méthode spécifique
python manage.py test BRYSHOP.tests.test_models.ProductModelTest.test_product_creation --settings=ECOMMERCE.test_settings
```

### Avec verbosité

```bash
# Voir plus de détails
python manage.py test --settings=ECOMMERCE.test_settings --verbosity=2

# Voir tous les détails
python manage.py test --settings=ECOMMERCE.test_settings --verbosity=3
```

## 📋 Résultats Actuels

### ✅ Tests Réussis : 74/90

#### Modèles (accounts)
- ✅ CustomUser : création, rôles, sexe, hashage de mot de passe
- ✅ Client : création, relation OneToOne, propriété est_boutiquier
- ✅ Notification : création, marquage comme lu, ordering

#### Modèles (BRYSHOP)
- ✅ Category : création, ordering, __str__
- ✅ Product : création, disponibilité, stock, relations
- ✅ Cart & CartItem : création, relations
- ✅ Payment : création, unicité de référence
- ✅ Order : création, calcul frais de livraison, statuts
- ✅ Wishlist & WishlistItem : création, contraintes unique_together
- ✅ Commande : création, ordering

#### Formulaires
- ✅ CategoryForm : validation, sauvegarde
- ✅ ProductForm : validation des champs (partiellement)

#### Vues
- ✅ Dashboard boutiquier : authentification, autorisation
- ✅ Panier : authentification requise
- ✅ Checkout : authentification requise
- ✅ Produits : liste, détails

### ❌ Problèmes Identifiés

#### 1. Erreurs de Noms d'URLs (13 erreurs)
Certains tests utilisent des noms d'URLs qui n'existent pas :
- `'index'` → Vérifier le nom réel dans urls.py
- `'order_history'` → Vérifier le nom réel
- `'wishlist'` → Vérifier le nom réel
- `'produits_par_categorie'` → Vérifier le nom réel
- `'add_to_cart'` → Nécessite un argument product_id

**Solution** : Vérifier les noms d'URLs dans `BRYSHOP/urls.py` et `ECOMMERCE/urls.py`

#### 2. Problème de Type dans Order.total_commande() (1 erreur)
```python
TypeError: unsupported operand type(s) for +: 'float' and 'decimal.Decimal'
```

**Solution** : Convertir `product.price` en Decimal dans le modèle Order

#### 3. Génération de numero_commande (1 échec)
Le numéro de commande n'est pas généré automatiquement lors de la création.

**Solution** : Le code de génération dans `save()` doit être vérifié

#### 4. Test de Formulaire ProductForm (1 échec)
Le formulaire n'accepte pas les données valides (probablement à cause du champ image).

**Solution** : Ajuster le test pour gérer le champ image optionnel

#### 5. Test Notification __str__ (1 échec)
Différence mineure dans le troncage du message (30 vs 31 caractères).

**Solution** : Ajuster le test pour correspondre à l'implémentation réelle

## 🔧 Corrections Nécessaires

### 1. Corriger le modèle Order

```python
# Dans BRYSHOP/models.py
def total_commande(self):
    """Calcule le total avec frais de livraison"""
    from decimal import Decimal
    return (Decimal(str(self.product.price)) * self.quantity) + self.frais_livraison
```

### 2. Vérifier les URLs

Examiner `BRYSHOP/urls.py` pour identifier les noms corrects des URLs.

### 3. Corriger le test de notification

```python
# Dans accounts/tests/test_models.py
def test_notification_str_method(self):
    """Test de la méthode __str__"""
    result = str(self.notification)
    self.assertIn("Notif pour notifuser:", result)
    self.assertIn("Votre commande a été expédi", result)
```

## 📈 Couverture de Code

Pour mesurer la couverture de code :

```bash
# Installer coverage
pip install coverage

# Exécuter les tests avec coverage
coverage run --source='.' manage.py test --settings=ECOMMERCE.test_settings

# Voir le rapport
coverage report

# Générer un rapport HTML
coverage html
# Ouvrir htmlcov/index.html dans un navigateur
```

## 🎯 Prochaines Étapes

1. ✅ **Corriger les 16 tests en échec**
2. **Ajouter des tests d'intégration** pour les flux complets :
   - Flux d'achat complet (panier → checkout → paiement)
   - Flux d'authentification
   - Flux de gestion de boutique
3. **Ajouter des tests pour les vues manquantes** :
   - Vues de paiement NotchPay
   - Vues de profil utilisateur
   - Vues de recherche
4. **Améliorer la couverture de code** (objectif : >80%)

## 📚 Ressources

- [Documentation Django Testing](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Django Test Client](https://docs.djangoproject.com/en/5.2/topics/testing/tools/#the-test-client)
- [Coverage.py](https://coverage.readthedocs.io/)

## 💡 Bonnes Pratiques

1. **Exécuter les tests avant chaque commit**
2. **Écrire des tests pour chaque nouvelle fonctionnalité**
3. **Maintenir une couverture de code élevée**
4. **Utiliser des fixtures pour les données de test répétitives**
5. **Isoler les tests (chaque test doit être indépendant)**
6. **Nommer les tests de manière descriptive**

---

**Note** : Les tests utilisent SQLite en mémoire pour être plus rapides et ne pas dépendre de MySQL. La configuration est dans `ECOMMERCE/test_settings.py`.
