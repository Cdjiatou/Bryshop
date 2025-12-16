#!/usr/bin/env python
"""
Script de test pour vérifier que les vues de paiement fonctionnent
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ECOMMERCE.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser

def test_payment_views():
    """Test des vues de paiement"""
    print("Test des vues de paiement...")

    try:
        # Tester simplement l'import des vues
        from BRYSHOP.test_payment_views import payment_test_suite, test_successful_payment
        print("SUCCES: Import des vues de test réussi")

        # Tester l'import depuis views.py
        from BRYSHOP.views import payment_test_suite as pts
        print("SUCCES: Import depuis views.py réussi")

        # Tester que les fonctions sont callables
        if callable(payment_test_suite):
            print("SUCCES: Fonction payment_test_suite est callable")
        else:
            print("ERREUR: Fonction payment_test_suite n'est pas callable")

        # Vérifier que les templates existent
        import os
        template_path = os.path.join('BRYSHOP', 'templates', 'html', 'payment_test_suite.html')
        if os.path.exists(template_path):
            print("SUCCES: Template payment_test_suite.html existe")
        else:
            print("ERREUR: Template payment_test_suite.html n'existe pas")

    except ImportError as e:
        print(f"ERREUR d'import: {e}")
    except Exception as e:
        print(f"ERREUR generale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_payment_views()