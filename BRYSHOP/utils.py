import requests
from django.conf import settings

def initialize_notch_payment(email, amount, description, reference, payment_method=None, currency="XAF"):
    """
    Initialize payment with Notch Pay API
    Args:
        email: Customer email
        amount: Payment amount
        description: Payment description
        reference: Unique payment reference
        payment_method: Payment method (optional)
        currency: Currency code (default: XAF)
    """
    headers = {
        "Authorization": f"Bearer {settings.NOTCH_PAY_PUBLIC_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = {
        "email": email,
        "amount": int(amount),  # Ensure it's integer
        "currency": currency,
        "description": description,
        "reference": reference,
    }

    # Add payment method if specified
    if payment_method:
        data["payment_method"] = payment_method

    # Add callback URL if available
    callback_url = getattr(settings, 'NOTCH_PAY_CALLBACK_URL', None)
    if callback_url:
        data["callback"] = callback_url

    try:
        # Timeout de 30 secondes pour éviter le blocage
        response = requests.post(settings.NOTCH_PAY_URL, json=data, headers=headers, timeout=30)

        # Debug logging
        print(f"Notch Pay Request: {data}")
        print(f"Notch Pay Response Status: {response.status_code}")
        print(f"Notch Pay Response: {response.text}")

        response.raise_for_status()
        result = response.json()

        # Check if the response indicates success
        if result.get('status') == 'success' or 'payment_url' in result:
            return {
                "status": "success",
                "payment_url": result.get('payment_url'),
                "reference": reference,
                "data": result
            }
        else:
            return {
                "status": "error",
                "message": "Réponse invalide de Notch Pay",
                "details": result
            }

    except requests.exceptions.RequestException as e:
        print(f"Notch Pay Error: {e}")
        error_details = ""
        if hasattr(e, 'response') and e.response:
            error_details = e.response.text

        return {
            "status": "error",
            "message": str(e),
            "details": error_details
        }

def verify_notch_transaction(reference):
    """
    Verify payment transaction with Notch Pay API
    """
    headers = {
        "Authorization": f"Bearer {settings.NOTCH_PAY_PUBLIC_KEY}",
        "Accept": "application/json",
    }

    url = f"{settings.NOTCH_PAY_VERIFY_URL}{reference}"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Notch Pay Verification Error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
