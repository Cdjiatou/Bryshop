# ================================
# VUES DE TEST DE PAIEMENT AVANCÉES
# ================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseForbidden
import uuid
import time

def payment_test_suite(request):
    """Suite complète de tests de paiement"""
    return render(request, 'html/payment_test_suite.html', {
        'title': 'Suite de Test de Paiement',
        'description': 'Testez tous les scénarios de paiement Notch Pay'
    })

def test_successful_payment(request):
    """Test un paiement réussi"""
    return _process_payment_test(request, scenario='success')

def test_failed_payment(request):
    """Test un paiement échoué"""
    return _process_payment_test(request, scenario='failure')

def test_cancelled_payment(request):
    """Test un paiement annulé"""
    return _process_payment_test(request, scenario='cancelled')

def test_paypal_payment(request):
    """Test spécifique pour PayPal via Notch Pay"""
    return _process_payment_test(request, scenario='paypal')

def test_large_amount_payment(request):
    """Test avec un montant élevé"""
    return _process_payment_test(request, scenario='large_amount')

def _process_payment_test(request, scenario):
    """Fonction utilitaire pour traiter les tests de paiement"""

    # Configuration des scénarios de test
    scenarios = {
        'success': {
            'amount': 5000,
            'description': 'Paiement réussi - Test',
            'expected_result': 'success'
        },
        'failure': {
            'amount': 1500,  # Montant qui pourrait échouer
            'description': 'Paiement échoué - Test',
            'expected_result': 'failure'
        },
        'cancelled': {
            'amount': 3000,
            'description': 'Paiement annulé - Test',
            'expected_result': 'cancelled'
        },
        'paypal': {
            'amount': 10000,
            'description': 'Paiement PayPal - Test',
            'payment_method': 'paypal',
            'expected_result': 'paypal_success'
        },
        'large_amount': {
            'amount': 100000,  # Montant élevé
            'description': 'Paiement gros montant - Test',
            'expected_result': 'large_amount_success'
        }
    }

    config = scenarios.get(scenario, scenarios['success'])

    context = {
        'scenario': scenario,
        'scenario_name': config['description'],
        'expected_result': config['expected_result'],
        'payment_methods': [
            ('orange_money', 'Orange Money'),
            ('mtn_money', 'MTN Mobile Money'),
            ('carte_bancaire', 'Carte Bancaire'),
            ('paypal', 'PayPal'),
        ],
        'currencies': ['XAF', 'USD', 'EUR'],
        'default_values': {
            'email': 'test@example.com',
            'amount': config['amount'],
            'currency': 'XAF',
            'payment_method': config.get('payment_method', 'orange_money'),
            'description': config['description']
        }
    }

    if request.method == 'POST':
        try:
            # Récupération des données du formulaire
            email = request.POST.get('email', 'test@example.com')
            amount = int(request.POST.get('amount', config['amount']))
            currency = request.POST.get('currency', 'XAF')
            payment_method = request.POST.get('payment_method', config.get('payment_method', 'orange_money'))
            description = request.POST.get('description', config['description'])

            # Validation basique
            if amount < 100:
                messages.error(request, 'Le montant minimum est de 100 XAF.')
                return render(request, 'html/payment_test_result.html', context)

            if not email or '@' not in email:
                messages.error(request, 'Veuillez saisir un email valide.')
                return render(request, 'html/payment_test_result.html', context)

            # Génération d'une référence unique avec timestamp
            timestamp = int(time.time())
            unique_id = str(uuid.uuid4().hex[:8]).upper()
            reference = f"TEST-{timestamp}-{unique_id}"

            # Simulation de l'initialisation du paiement (en développement)
            if settings.DEBUG:
                # En mode développement, on simule le paiement
                payment_data = {
                    'reference': reference,
                    'amount': amount,
                    'currency': currency,
                    'email': email,
                    'payment_method': payment_method,
                    'description': description,
                    'status': 'simulated',
                    'payment_url': f'/payment/simulate/{reference}/',
                    'scenario': scenario
                }

                # Stockage temporaire des données de paiement (simulation)
                request.session[f'payment_{reference}'] = payment_data

                messages.success(request, f'Paiement simulé créé avec succès. Référence: {reference}')
                context.update({
                    'payment_data': payment_data,
                    'test_mode': True
                })

                return render(request, 'html/payment_test_result.html', context)

            else:
                # En production, utiliser l'API réelle Notch Pay
                try:
                    from BRYSHOP.utils import initialize_notch_payment

                    payment_result = initialize_notch_payment(
                        amount=amount,
                        currency=currency,
                        email=email,
                        reference=reference,
                        description=description,
                        payment_method=payment_method
                    )

                    if payment_result.get('status') == 'success':
                        messages.success(request, f'Paiement initialisé avec succès. Référence: {reference}')
                        context.update({
                            'payment_data': payment_result,
                            'test_mode': False
                        })
                        return render(request, 'html/payment_test_result.html', context)
                    else:
                        messages.error(request, f'Erreur lors de l\'initialisation: {payment_result.get("message", "Erreur inconnue")}')
                        return render(request, 'html/payment_test_result.html', context)

                except Exception as e:
                    messages.error(request, f'Erreur technique: {str(e)}')
                    return render(request, 'html/payment_test_result.html', context)

        except ValueError as e:
            messages.error(request, f'Erreur de valeur: {str(e)}')
            return render(request, 'html/payment_test_result.html', context)
        except Exception as e:
            messages.error(request, f'Erreur inattendue: {str(e)}')
            return render(request, 'html/payment_test_result.html', context)

    return render(request, 'html/payment_test_form.html', context)

def simulate_payment_callback(request, reference):
    """Simulation du callback de paiement pour les tests"""
    if not settings.DEBUG:
        return HttpResponseForbidden("Cette fonctionnalité est seulement disponible en mode développement.")

    # Récupération des données de paiement simulées
    payment_data = request.session.get(f'payment_{reference}')
    if not payment_data:
        messages.error(request, 'Données de paiement non trouvées.')
        return redirect('payment_test_suite')

    # Simulation des différents scénarios
    scenario = payment_data.get('scenario', 'success')

    if scenario == 'success':
        payment_data['status'] = 'completed'
        payment_data['transaction_id'] = f"TXN-{reference}"
        messages.success(request, 'Paiement simulé avec succès !')

    elif scenario == 'failure':
        payment_data['status'] = 'failed'
        payment_data['error'] = 'Paiement refusé par le fournisseur'
        messages.error(request, 'Paiement simulé comme échoué.')

    elif scenario == 'cancelled':
        payment_data['status'] = 'cancelled'
        messages.warning(request, 'Paiement simulé comme annulé.')

    elif scenario == 'paypal_success':
        payment_data['status'] = 'completed'
        payment_data['transaction_id'] = f"PAYPAL-{reference}"
        messages.success(request, 'Paiement PayPal simulé avec succès !')

    elif scenario == 'large_amount_success':
        payment_data['status'] = 'completed'
        payment_data['transaction_id'] = f"LARGE-{reference}"
        messages.success(request, 'Paiement de gros montant simulé avec succès !')

    # Mise à jour des données en session
    request.session[f'payment_{reference}'] = payment_data

    return render(request, 'html/payment_callback_result.html', {
        'payment_data': payment_data,
        'scenario': scenario
    })

def run_payment_tests(request):
    """Exécute une batterie de tests automatisés"""
    if not settings.DEBUG:
        return HttpResponseForbidden("Les tests automatisés sont seulement disponibles en mode développement.")

    from django.test import Client

    results = {
        'total_tests': 0,
        'passed': 0,
        'failed': 0,
        'tests': []
    }

    client = Client()

    # Test 1: Formulaire de test accessible
    try:
        response = client.get('/payment-tests/')
        if response.status_code == 200:
            results['tests'].append({'name': 'Page de test accessible', 'status': 'passed'})
            results['passed'] += 1
        else:
            results['tests'].append({'name': 'Page de test accessible', 'status': 'failed', 'error': f'Status: {response.status_code}'})
            results['failed'] += 1
    except Exception as e:
        results['tests'].append({'name': 'Page de test accessible', 'status': 'failed', 'error': str(e)})
        results['failed'] += 1

    # Test 2: Soumission de formulaire valide
    try:
        data = {
            'email': 'test@example.com',
            'amount': '5000',
            'currency': 'XAF',
            'payment_method': 'orange_money',
            'description': 'Test automatique',
            'csrfmiddlewaretoken': 'dummy'
        }
        response = client.post('/test-payment/', data)
        if response.status_code in [200, 302]:  # Redirection ou succès
            results['tests'].append({'name': 'Soumission formulaire valide', 'status': 'passed'})
            results['passed'] += 1
        else:
            results['tests'].append({'name': 'Soumission formulaire valide', 'status': 'failed', 'error': f'Status: {response.status_code}'})
            results['failed'] += 1
    except Exception as e:
        results['tests'].append({'name': 'Soumission formulaire valide', 'status': 'failed', 'error': str(e)})
        results['failed'] += 1

    # Test 3: Validation des données
    try:
        invalid_data = {
            'email': 'invalid-email',
            'amount': '50',  # Trop petit
            'currency': 'XAF',
            'payment_method': 'orange_money',
            'description': 'Test validation',
            'csrfmiddlewaretoken': 'dummy'
        }
        response = client.post('/test-payment/', invalid_data)
        if response.status_code == 200:  # Devrait retourner au formulaire avec erreurs
            results['tests'].append({'name': 'Validation des données', 'status': 'passed'})
            results['passed'] += 1
        else:
            results['tests'].append({'name': 'Validation des données', 'status': 'failed', 'error': f'Status inattendu: {response.status_code}'})
            results['failed'] += 1
    except Exception as e:
        results['tests'].append({'name': 'Validation des données', 'status': 'failed', 'error': str(e)})
        results['failed'] += 1

    results['total_tests'] = len(results['tests'])

    return render(request, 'html/payment_test_results.html', {
        'results': results,
        'title': 'Résultats des Tests Automatisés'
    })