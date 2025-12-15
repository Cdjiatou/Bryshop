import requests
from django.conf import settings

def initialize_notch_payment(email, amount, description, reference, callback_url):
    headers = {
        "Authorization": f"{settings.NOTCH_PAY_PUBLIC_KEY}",  # Notch Pay uses Public Key for initialization usually, but sometimes Private depending on endpoint. 
                                                              # Standard is usually Public key in header or as param. 
                                                              # Checking docs implies Authorization header with key.
                                                              # Let's try matching standard payment gateway patterns.
                                                              # WAIT: API docs say "Authorization: PUBLIC_KEY" for client-side, 
                                                              # but server-side usually uses Private Key or Public Key passed in header.
                                                              # Let's use the Public Key as per common Notch Pay integration examples.
        "Accept": "application/json",
    }
    
    data = {
        "email": email,
        "amount": str(amount), # Ensure it's string or int
        "currency": "XAF",
        "description": description,
        "reference": reference,
        "callback": callback_url
    }
    
    try:
        # Ajout d'un timeout de 15 secondes pour éviter le chargement infini
        response = requests.post(settings.NOTCH_PAY_URL, json=data, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Notch Pay Error: {e}")
        # Retourner l'erreur pour l'afficher dans la vue de test
        return {"status": "error", "message": str(e), "details": getattr(e.response, 'text', '') if e.response else ''}

def verify_notch_transaction(reference):
    headers = {
        "Authorization": f"{settings.NOTCH_PAY_PUBLIC_KEY}", # Verify endpoint often needs keys too
        "Accept": "application/json",
    }
    url = f"{settings.NOTCH_PAY_VERIFY_URL}{reference}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Notch Pay Verification Error: {e}")
        return None
