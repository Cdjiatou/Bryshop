# 🧪 Guide de Test des Paiements BryShop

## Vue d'ensemble

BryShop dispose maintenant d'un système complet de test des paiements Notch Pay avec simulation de différents scénarios. Ce guide explique comment utiliser toutes les fonctionnalités de test.

## 🚀 Démarrage Rapide

### 1. Accès aux Tests
- **URL principale:** `http://127.0.0.1:8000/payment-tests/`
- **Test simple:** `http://127.0.0.1:8000/test-payment/`

### 2. Scénarios Disponibles

#### ✅ Paiement Réussi
- **URL:** `/test-successful-payment/`
- **Description:** Test d'un paiement qui se déroule normalement
- **Montant:** 5,000 XAF
- **Résultat attendu:** Succès

#### ❌ Paiement Échoué
- **URL:** `/test-failed-payment/`
- **Description:** Test d'un paiement refusé par le fournisseur
- **Montant:** 1,500 XAF
- **Résultat attendu:** Échec

#### ⏸️ Paiement Annulé
- **URL:** `/test-cancelled-payment/`
- **Description:** Test d'un paiement annulé par l'utilisateur
- **Montant:** 3,000 XAF
- **Résultat attendu:** Annulé

#### 💰 PayPal
- **URL:** `/test-paypal-payment/`
- **Description:** Test spécifique de PayPal via Notch Pay
- **Montant:** 10,000 XAF
- **Résultat attendu:** Succès PayPal

#### 💸 Gros Montant
- **URL:** `/test-large-amount/`
- **Description:** Test avec un montant élevé
- **Montant:** 100,000 XAF
- **Résultat attendu:** Succès

#### 🤖 Tests Automatisés
- **URL:** `/run-payment-tests/`
- **Description:** Exécute une batterie de tests automatisés

## 📋 Fonctionnement des Tests

### Mode Développement
Tous les tests sont **simulés** en mode développement :
- ✅ Aucune transaction réelle
- ✅ Pas de frais bancaires
- ✅ Données stockées en session
- ✅ Simulation du callback de paiement

### Processus de Test

1. **Sélection du scénario** depuis la suite de tests
2. **Remplissage du formulaire** avec les données de test
3. **Soumission** du formulaire de paiement
4. **Simulation du callback** en cliquant sur le lien fourni
5. **Vérification du résultat** dans l'interface

## 🎯 Méthodes de Paiement Testées

| Méthode | Description | Disponibilité |
|---------|-------------|---------------|
| Orange Money | Mobile Money Orange | ✅ Simulé |
| MTN Money | Mobile Money MTN | ✅ Simulé |
| Carte Bancaire | Cartes de crédit/débit | ✅ Simulé |
| PayPal | Via Notch Pay | ✅ Simulé |

## 📊 Résultats des Tests

### États Possibles
- **✅ Completed:** Paiement réussi
- **❌ Failed:** Paiement échoué
- **⏸️ Cancelled:** Paiement annulé
- **🔄 Simulated:** En attente de callback

### Informations Affichées
- Référence unique du paiement
- Montant et devise
- Méthode de paiement utilisée
- Email du client
- Statut de la transaction
- ID de transaction (si applicable)

## 🔧 Tests Automatisés

### Tests Inclus
- ✅ Accessibilité des pages de test
- ✅ Soumission de formulaires valides
- ✅ Validation des données d'entrée
- ✅ Gestion des erreurs

### Métriques
- **Total des tests** exécutés
- **Tests réussis** (en vert)
- **Tests échoués** (en rouge)
- **Taux de succès** en pourcentage

## 🛠️ Utilisation Avancée

### Simulation du Callback
```python
# URL de simulation
/payment/simulate/{reference}/

# Exemple
/payment/simulate/TEST-1703123456-ABC123/
```

### Données de Session
Les données de paiement sont stockées en session :
```python
request.session[f'payment_{reference}'] = payment_data
```

### Debug Mode
En mode développement (`DEBUG=True`), des informations supplémentaires sont affichées.

## 🚨 Dépannage

### Erreur "Page non trouvée"
- Vérifiez que le serveur Django fonctionne
- Assurez-vous que les URLs sont correctement configurées

### Erreur "Méthode non autorisée"
- Les tests automatisés ne fonctionnent qu'en mode développement
- Vérifiez le setting `DEBUG=True`

### Callback non simulé
- Cliquez sur le lien "Simuler le Callback de Paiement"
- Vérifiez que la référence existe en session

## 📁 Structure des Fichiers

```
BRYSHOP/
├── test_payment_views.py           # Vues avancées de test
├── templates/html/
│   ├── payment_test_suite.html     # Suite principale de tests
│   ├── payment_test_form.html      # Formulaire de test
│   ├── payment_test_result.html    # Résultats individuels
│   ├── payment_test_results.html   # Résultats automatisés
│   └── payment_callback_result.html # Callback simulé
└── urls.py                         # URLs de test ajoutées
```

## 🔄 Migration vers Production

### Quand passer en production :
1. Modifier `DEBUG=False` dans `settings.py`
2. Remplacer les simulations par l'API réelle Notch Pay
3. Configurer les clés API de production
4. Tester avec de vraies transactions (montants minimaux)

### Code de production :
```python
# Remplacer la simulation par :
payment_result = initialize_notch_payment(
    amount=amount,
    currency=currency,
    email=email,
    reference=reference,
    description=description,
    payment_method=payment_method
)
```

## 📞 Support

Pour toute question concernant les tests de paiement :
- Vérifiez les logs du serveur Django
- Consultez les données de session
- Utilisez le mode debug pour plus d'informations

---

**🎉 Le système de test de paiement est maintenant opérationnel !**

Testez tous les scénarios pour valider l'intégration Notch Pay avant le déploiement en production.