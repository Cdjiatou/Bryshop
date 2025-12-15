---
description: Guide d'intégration et de test du paiement Notch Pay
---

# Flux de Paiement Notch Pay

Ce workflow décrit comment utiliser, tester et maintenir intégration de paiement Notch Pay dans le projet eCommerce.

## 1. Configuration requise

S'assurer que `ECOMMERCE/settings.py` contient les clés API :
```python
NOTCH_PAY_PUBLIC_KEY = 'pk_...'
NOTCH_PAY_PRIVATE_KEY = 'sk_...'
NOTCH_PAY_URL = 'https://api.notchpay.co/payments/initialize'
NOTCH_PAY_VERIFY_URL = 'https://api.notchpay.co/payments/'
```

## 2. Tester le paiement (Dev)

Pour valider l'intégration technique sans passer par le panier d'achat :

1.  Lancer le serveur : `python manage.py runserver`
2.  Accéder à l'URL : `http://127.0.0.1:8000/test-payment/`
3.  Effectuer un paiement (mode test ou réel selon vos clés).
4.  Vérifier le résultat :
    - Vous devez être redirigé vers la page de confirmation (ou d'erreur).
    - Dans la base de données (table `bryshop_payment`), le statut doit être passé à `complete`.

## 3. Flux Utilisateur Réel

1.  L'utilisateur remplit son panier.
2.  Il clique sur **Commander** (`/checkout/`).
3.  La vue `place_order` initialise le paiement et redirige vers Notch Pay.
4.  Au retour (`/payment/callback/`), si le paiement est valide :
    - Une commande (`Order`) est créée.
    - Un email est envoyé.
    - Le panier est vidé.

## 4. Dépannage

Si le paiement reste "pending" ou échoue :
- Vérifier les logs du terminal pour les erreurs HTTP (`requests.exceptions`).
- Vérifier que l'URL de callback est accessible (localhost fonctionne en local, mais en production il faut un vrai domaine).
