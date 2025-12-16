# Vue pour les vrais paiements (même en développement)
@login_required
def real_payment(request):
    """Vue pour effectuer de vrais paiements avec Notch Pay (même en développement)"""
    from django.conf import settings
    import uuid
    import time

    context = {
        'payment_methods': [
            ('orange_money', 'Orange Money'),
            ('mtn_money', 'MTN Mobile Money'),
            ('carte_bancaire', 'Carte Bancaire'),
            ('paypal', 'PayPal'),
        ],
        'currencies': ['XAF', 'USD', 'EUR'],
        'default_values': {
            'email': request.user.email or 'client@example.com',
            'amount': 5000,
            'currency': 'XAF',
            'payment_method': 'orange_money',
            'description': 'Paiement réel - BryShop'
        }
    }

    if request.method == 'POST':
        try:
            # Récupération des données du formulaire
            email = request.POST.get('email', request.user.email)
            amount = int(request.POST.get('amount', 5000))
            currency = request.POST.get('currency', 'XAF')
            payment_method = request.POST.get('payment_method', 'orange_money')
            description = request.POST.get('description', 'Paiement réel - BryShop')

            # Validation
            if amount < 100:
                messages.error(request, 'Le montant minimum est de 100 XAF.')
                return render(request, 'html/real_payment.html', context)

            if not email or '@' not in email:
                messages.error(request, 'Veuillez saisir un email valide.')
                return render(request, 'html/real_payment.html', context)

            # Génération d'une référence unique
            timestamp = int(time.time())
            unique_id = str(uuid.uuid4().hex[:8]).upper()
            reference = f"REAL-{timestamp}-{unique_id}"

            # APPEL RÉEL À NOTCH PAY (toujours, même en développement)
            try:
                from .utils import initialize_notch_payment

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

                    # Redirection vers Notch Pay
                    payment_url = payment_result.get('payment_url')
                    if payment_url:
                        return redirect(payment_url)
                    else:
                        messages.error(request, 'URL de paiement non reçue de Notch Pay.')
                        return render(request, 'html/real_payment.html', context)
                else:
                    messages.error(request, f'Erreur lors de l\'initialisation: {payment_result.get("message", "Erreur inconnue")}')
                    return render(request, 'html/real_payment.html', context)

            except Exception as e:
                messages.error(request, f'Erreur technique: {str(e)}')
                return render(request, 'html/real_payment.html', context)

        except ValueError as e:
            messages.error(request, f'Erreur de valeur: {str(e)}')
            return render(request, 'html/real_payment.html', context)
        except Exception as e:
            messages.error(request, f'Erreur inattendue: {str(e)}')
            return render(request, 'html/real_payment.html', context)

    return render(request, 'html/real_payment.html', context)