from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from .models import CartItem, Product, Commande, Category, Cart, Order, Payment
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
import uuid
from django.utils import timezone
from datetime import datetime
from .utils import initialize_notch_payment, verify_notch_transaction


# Create your views here.

def index(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name:
        product_object = Product.objects.filter(title__icontains = item_name)
    else:
        product_object = Product.objects.all()
        
    
    paginator = Paginator(product_object, 4)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'html/index.html', {'product_object': product_object})

def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'html/detailProduit.htm', {'product': product_object})





@login_required
def confirmation(request):
    user = request.user
    nom = user.username
    email = user.email

    print(f"[DEBUG] Utilisateur : {nom} - Email : {email}")

    # 🛒 Récupérer le panier selon la méthode utilisée
    cart_id = request.session.get('cart_id')
    if cart_id:
        panier = CartItem.objects.filter(cart_id=cart_id)
    else:
        panier = CartItem.objects.none()

    # ✉️ Construire le message de confirmation
    message = f"Bonjour {nom},\n\nVoici le récapitulatif de votre commande sur BryShop :\n\n"
    total = 0
    for item in panier:
        ligne = f"- {item.product.title} (x{item.quantity}) - {item.product.price * item.quantity}€\n"
        message += ligne
        total += item.product.price * item.quantity
        print("[DEBUG] Ligne panier:", ligne.strip())  # Debug terminal

    message += f"\nTotal : {total}€\n\nMerci pour votre commande !\nL'équipe BryShop"

    try:
        send_mail(
            subject="Confirmation de votre commande - BryShop",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        print("[DEBUG] Email envoyé avec succès.")
    except Exception as e:
        print(f"[ERREUR ENVOI EMAIL] {e}")

    request.session['message'] = f"Merci pour votre commande, {nom} ! Un récapitulatif a été envoyé à votre adresse e-mail."

    return redirect('Accueil')



def home(request):
    message = request.session.pop('message', None)
    return render(request, 'html/index.html', {'message': message})


def product_by_category(request, id):
    categorie = get_object_or_404(Category, id=id)
    produits = Product.objects.filter(category=categorie)
    return render(request, 'html/produitsParCategorie.html', {
        'categorie': categorie,
        'produits': produits
    })
    
def nos_produits(request):
    produits = Product.objects.all()
    return render(request, 'html/nos_produits.html', {'produits': produits})


def contact_views(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        full_message = f"Message de: {name} ({email})\n\n{message}"
        
        send_mail(
            subject=subject,
            message=full_message,
            from_email=email,
            recipient_list=['djikissibryan@gmail.com'],
            fail_silently=False,
        )
        
        messages.success(request, "Votre message a bien été envoyé. Merci de nous avoir contactés !")
        return redirect('contact')
    
    return render(request, 'html/contact.html')


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    cart, created = Cart.objects.get_or_create(user=user)

    existing_item = cart.items.filter(product=product).first()

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        new_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

    return redirect('cart')


@login_required
def cart_views(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)  # <-- important ici
        total = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
    return render(request, 'html/cart.html', {'cart_items': cart_items, 'total': total})



@login_required
def update_cart_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    if action == "increment":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrement":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')



@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect(request, 'html/cart.html')



@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    return render(request, 'html/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
    

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Cart, Order

@login_required
def place_order(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect('checkout')

    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    # 1. Générer une référence unique
    reference = str(uuid.uuid4())

    # 2. Lien de retour (Callback)
    callback_url = request.build_absolute_uri(reverse('payment_callback')) + f"?reference={reference}"

    # 3. Description
    description = f"Commande de {user.username} - {total} XAF"
    
    # 4. Initialiser le paiement Notch Pay
    response = initialize_notch_payment(user.email, total, description, reference, callback_url)

    if response and response.get('status') == 'Accepted':
        # --- NOUVEAU : Sauvegarder le paiement en attente ---
        # Note : Notch Pay renvoie 'transaction' avec l'ID dans la réponse d'initialisation habituellement, 
        # mais la doc fournie ne montre que le webhook/verify. 
        # On va utiliser 'reference' comme clé principale pour retrouver ce paiement.
        # On essaie de récupérer l'ID Notch Pay s'il est dispo dans la réponse (souvent dans transaction.id)
        notch_id = response.get('transaction', {}).get('id', '') 
        
        Payment.objects.create(
            user=user,
            notch_pay_id=notch_id, # Peut être vide au début si pas renvoyé ici
            reference=reference,
            amount=total,
            status='pending',
            raw_response=response
        )
        
        authorization_url = response.get('authorization_url')
        return redirect(authorization_url)
    else:
        messages.error(request, "Erreur lors de l'initialisation du paiement.")
        return redirect('checkout')


@login_required
def payment_callback(request):
    reference = request.GET.get('reference') 
    
    if not reference:
        messages.error(request, "Référence de paiement manquante.")
        return redirect('cart')

    # Vérifier la transaction
    verification = verify_notch_transaction(reference)

    if verification and verification.get('status') == 'complete':
        # Mise à jour du Paiement en BDD
        # La réponse JSON correspond à l'exemple fourni par l'utilisateur
        
        payment = Payment.objects.filter(reference=reference).first()
        
        # On convertit les dates si présentes (format ISO 8601 probable)
        # Ex: "2023-01-01T12:00:00Z" -> datetime object
        created_at_str = verification.get('created_at')
        completed_at_str = verification.get('completed_at')
        
        # Fonction simple pour parser l'ISO 8601 basique (ajustez si besoin pour le timezone Z)
        def parse_iso(date_str):
            if date_str:
                return date_str.replace('Z', '+00:00') # Pour compatibilité Django fromisoformat
            return None

        if payment:
            payment.status = verification.get('status')
            payment.notch_pay_id = verification.get('id')
            payment.customer_id = verification.get('customer')
            payment.payment_method = verification.get('payment_method')
            payment.raw_response = verification
            if created_at_str:
                payment.created_at = datetime.fromisoformat(parse_iso(created_at_str))
            if completed_at_str:
                payment.completed_at = datetime.fromisoformat(parse_iso(completed_at_str))
            payment.save()
        else:
            # Fallback si le paiement n'a pas été créé à l'init (cas rare)
            payment = Payment.objects.create(
                user=request.user,
                notch_pay_id=verification.get('id'),
                reference=reference,
                amount=verification.get('amount'),
                status=verification.get('status'),
                raw_response=verification
            )


        # PAIEMENT RÉUSSI -> On crée les commandes liées à ce paiement
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        
        if not cart:
             return redirect('Accueil')

        cart_items = cart.items.all()
        
        for item in cart_items:
            Order.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,
                payment=payment # --- LIEN AVEC LE PAIEMENT ---
            )

        # Calcul du total pour l'email
        total = sum(item.product.price * item.quantity for item in cart_items)

        # Préparer le message e-mail
        subject = "Confirmation de votre commande - BryShop"
        message = f"Bonjour {user.first_name},\n\n..." 

        # Vider le panier
        cart.items.all().delete()

        messages.success(request, " Paiement validé et enregistré !")
        return redirect('confirmation')
    
    else:
        # Paiement échoué
        payment = Payment.objects.filter(reference=reference).first()
        if payment:
            payment.status = 'failed'
            payment.save()
            
        messages.error(request, "Le paiement a échoué.")
        return redirect('checkout')


def test_payment_view(request):
    """
    Vue de test simple pour vérifier l'intégration Notch Pay sans dépendre du Panier.
    """
  
    amount = 100  # 100 XAF pour le test
    email = request.user.email if request.user.is_authenticated else "test@example.com"
    reference = str(uuid.uuid4())
    description = "Test de paiement technique 100 XAF"
    
    # 2. Callback vers la vue standard (qui mettra à jour le statut)
    callback_url = request.build_absolute_uri(reverse('payment_callback')) + f"?reference={reference}"

    # 3. Initialisation API
    response = initialize_notch_payment(email, amount, description, reference, callback_url)

    if response and response.get('status') == 'Accepted':
        # 4. Créer l'objet Payment en base pour pouvoir vérifier ensuite
        Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            notch_pay_id=response.get('transaction', {}).get('id', ''),
            reference=reference,
            amount=amount,
            status='pending',
            raw_response=response
        )
        
        # 5. Redirection vars la page de paiement
        return redirect(response.get('authorization_url'))
    else:
        return HttpResponse(f"Erreur d'initialisation : {response}")

