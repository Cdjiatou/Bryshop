from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
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
from .models import CartItem, Product, Commande, Category, Cart, Order, Payment, Wishlist, WishlistItem
from .forms_profil import ProfilBoutiquierForm, PasswordChangeCustomForm

# Import des vues de test de paiement
from .test_payment_views import (
    payment_test_suite,
    test_successful_payment,
    test_failed_payment,
    test_cancelled_payment,
    test_paypal_payment,
    test_large_amount_payment,
    simulate_payment_callback,
    run_payment_tests
)
from django.contrib.auth import update_session_auth_hash,get_user_model
from .forms import CategoryForm, ProductForm


# Vérifie si l'utilisateur est boutiquier ou superuser
def is_boutiquier(user):
    return user.is_superuser or (hasattr(user, 'role') and user.role == 'boutiquier')

# Vue pour modifier le profil du boutiquier
@login_required
@user_passes_test(is_boutiquier, login_url='login')
def modifier_profil(request):
    user = request.user
    if request.method == 'POST':
        form = ProfilBoutiquierForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('dashboard_boutiquier')
    else:
        form = ProfilBoutiquierForm(instance=user)
    return render(request, 'html/modifier_profil.html', {'form': form})

# Vue pour changer le mot de passe
@login_required
@user_passes_test(is_boutiquier, login_url='login')
def changer_mot_de_passe(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if not user.check_password(old_password):
                form.add_error('old_password', 'Ancien mot de passe incorrect.')
            elif new_password1 != new_password2:
                form.add_error('new_password2', 'Les mots de passe ne correspondent pas.')
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mot de passe changé avec succès !')
                return redirect('dashboard_boutiquier')
    else:
        form = PasswordChangeCustomForm()
    return render(request, 'html/changer_mot_de_passe.html', {'form': form})


# Vérifie si l'utilisateur est boutiquier ou superuser
def is_boutiquier(user):
    return user.is_superuser or (hasattr(user, 'role') and user.role == 'boutiquier')

# Vue pour ajouter une catégorie
@login_required
@user_passes_test(is_boutiquier, login_url='login')
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie ajoutée avec succès !')
            return redirect('dashboard_boutiquier')
    else:
        form = CategoryForm()
    return render(request, 'html/ajouter_categorie.html', {'form': form})

# Vue pour ajouter un produit
@login_required
@user_passes_test(is_boutiquier, login_url='login')
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit ajouté avec succès !')
            return redirect('dashboard_boutiquier')
    else:
        form = ProductForm()
    return render(request, 'html/ajouter_produit.html', {'form': form})

@login_required
@user_passes_test(is_boutiquier, login_url='login')
def dashboard_boutiquier(request):
    user = request.user
    # Statistiques
    total_commandes = Order.objects.count()
    total_produits = Product.objects.count()
    User = get_user_model()
    total_clients = User.objects.count()
    commandes = Order.objects.all().order_by('-date_ordered')
    categories = Category.objects.all()
    produits = Product.objects.all()
    # Notifications fictives (à améliorer)
    notifications = [
        {'message': 'Nouvelle commande reçue !'},
        {'message': 'Stock faible sur certains produits.'},
    ]
    return render(request, 'html/dashboard_boutiquier.html', {
        'user': user,
        'total_commandes': total_commandes,
        'total_produits': total_produits,
        'total_clients': total_clients,
        'commandes': commandes,
        'categories': categories,
        'produits': produits,
        'notifications': notifications,
    })

import uuid
from django.utils import timezone
from datetime import datetime
from .utils import initialize_notch_payment, verify_notch_transaction
from .models import CartItem, Product, Commande, Category, Cart, Order, Payment, Wishlist, WishlistItem






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

    if not product.est_disponible():
        messages.error(request, f"Le produit '{product.title}' est en rupture de stock.")
        return redirect('Accueil')

    cart, created = Cart.objects.get_or_create(user=user)
    existing_item = cart.items.filter(product=product).first()

    if existing_item:
        nouvelle_quantite = existing_item.quantity + 1
        if not product.peut_commander(nouvelle_quantite):
            messages.warning(request, f"Stock insuffisant pour '{product.title}'. Stock disponible : {product.stock}")
            return redirect('cart')
        existing_item.quantity = nouvelle_quantite
        existing_item.save()
    else:
        CartItem.objects.create(product=product, quantity=1, cart=cart)

    messages.success(request, f"'{product.title}' ajouté au panier.")
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
        nouvelle_quantite = cart_item.quantity + 1
        if not cart_item.product.peut_commander(nouvelle_quantite):
            messages.warning(request, f"Stock insuffisant pour '{cart_item.product.title}'. Stock disponible : {cart_item.product.stock}")
            return redirect('cart')
        cart_item.quantity = nouvelle_quantite
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
        
        # Calculer frais de livraison
        pays = request.user.customuser.pays if hasattr(request.user, 'customuser') else ''
        frais_par_pays = {
            'Cameroun': 1500,
            'France': 5000,
            'Côte d\'Ivoire': 2000,
            'Sénégal': 2500,
            'Gabon': 3000,
        }
        frais_livraison = frais_par_pays.get(pays, 2000)
        total_avec_livraison = total_price + frais_livraison
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0
        frais_livraison = 0
        total_avec_livraison = 0

    return render(request, 'html/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'frais_livraison': frais_livraison,
        'total_avec_livraison': total_avec_livraison
    })
    



@login_required
def place_order(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        mode_paiement = request.POST.get('mode_paiement', 'livraison')

        if not cart or not cart.items.exists():
            messages.warning(request, "Votre panier est vide.")
            return redirect('checkout')

        cart_items = cart.items.all()

        # 1. Vérification du Stock (Logique Collaborateur)
        for item in cart_items:
            if not item.product.peut_commander(item.quantity):
                messages.error(request, f"Stock insuffisant pour '{item.product.title}'. Stock disponible : {item.product.stock}")
                return redirect('cart')

        # 2. Calcul des totaux et frais (Logique Collaborateur)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Calcul frais de livraison (identique à checkout)
        pays = request.user.customuser.pays if hasattr(request.user, 'customuser') else ''
        frais_par_pays = {'Cameroun': 1500, 'France': 5000, 'Côte d\'Ivoire': 2000, 'Sénégal': 2500, 'Gabon': 3000}
        frais_livraison = frais_par_pays.get(pays, 2000)
        
        total_a_payer = total_price + frais_livraison

        # 3. Branchement selon le mode de paiement
        if mode_paiement == 'livraison':
            # --- CAS PAIEMENT À LA LIVRAISON (Logique Collaborateur) ---
            frais_livraison_total = 0 # Variable pour l'email
            total_calcul_email = 0

            for item in cart_items:
                order = Order(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    mode_paiement=mode_paiement,
                    statut_paiement='en_attente', # Livraison = on attend l'argent
                    nom=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    address=user.customuser.ville if hasattr(user, 'customuser') else '',
                    ville=user.customuser.ville if hasattr(user, 'customuser') else '',
                    pays=user.customuser.pays if hasattr(user, 'customuser') else '',
                )
                order.frais_livraison = order.calculer_frais_livraison()
                order.save()
                
                # Déduire le stock
                item.product.stock -= item.quantity
                item.product.save()
                
                total_calcul_email += item.product.price * item.quantity
                frais_livraison_total += order.frais_livraison

            # Email et message
            subject = " Confirmation de votre commande - BryShop"
            message_email = f"Bonjour {user.first_name},\n\nMerci pour votre commande sur BryShop !\n\n..."
            # (Simplification du message pour le merge)
            
            try:
                send_mail(subject, message_email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
            except:
                pass

            cart.items.all().delete()
            messages.success(request, "🎉 Merci pour votre commande ! Vous paierez à la livraison.")
            return redirect('confirmation')

        else:
            # --- CAS PAIEMENT EN LIGNE (Notch Pay) ---
            # On initialise Notch Pay avec le total incluant la livraison
            
            reference = str(uuid.uuid4())
            description = f"Commande {user.username} - {total_a_payer} XAF (Livraison incluse)"
            callback_url = request.build_absolute_uri(reverse('payment_callback')) + f"?reference={reference}"
            
            # Initialiser le paiement
            response = initialize_notch_payment(user.email, int(total_a_payer), description, reference, callback_url)

            if response and response.get('status') == 'Accepted':
                # Créer le paiement en attente
                notch_id = response.get('transaction', {}).get('id', '')
                Payment.objects.create(
                    user=user,
                    notch_pay_id=notch_id,
                    reference=reference,
                    amount=total_a_payer,
                    status='pending',
                    raw_response=response,
                    payment_method=mode_paiement # On garde trace que c'était Orange/MTN/Carte
                )
                return redirect(response.get('authorization_url'))
            else:
                messages.error(request, "Erreur lors de l'initialisation du paiement Notch Pay.")
                return redirect('checkout')

    return redirect('checkout')


@login_required
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return redirect('cart')

    verification = verify_notch_transaction(reference)

    if verification and verification.get('status') == 'complete':
        # Mise à jour du Paiement
        payment = Payment.objects.filter(reference=reference).first()
        if payment:
            payment.status = 'complete'
            payment.save()

        # Création des commandes et déduction du stock
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart: return redirect('Accueil') # Panier déjà vidé ?

        cart_items = cart.items.all()
        
        # On refait la vérification de stock par sécurité
        for item in cart_items:
             if not item.product.peut_commander(item.quantity):
                 messages.error(request, f"Stock épuisé entre temps pour {item.product.title}")
                 return redirect('cart')

        for item in cart_items:
            order = Order(
                user=user,
                product=item.product,
                quantity=item.quantity,
                payment=payment, # Lien Notch Pay
                mode_paiement=payment.payment_method or 'online',
                statut_paiement='paye',
                statut='traitement',
                nom=f"{user.first_name} {user.last_name}",
                email=user.email,
                # On remplit les nouvelles infos adresse
                address=user.customuser.ville if hasattr(user, 'customuser') else '', 
                 # Note: Idéalement il faudrait récupérer ces infos du checkout form et les stocker en session
                 # Pour simplifier ici on reprend du profil user
            )
            order.frais_livraison = order.calculer_frais_livraison()
            order.save()
            
            # Déduire le stock
            item.product.stock -= item.quantity
            item.product.save()

        cart.items.all().delete()
        messages.success(request, "🎉 Paiement validé ! Votre commande est confirmée.")
        return redirect('confirmation')
    
    else:
        messages.error(request, "Paiement non validé.")
        return redirect('checkout')


@login_required
def mes_commandes(request):
    commandes = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'html/mes_commandes.html', {'commandes': commandes})


def test_payment(request):
    """Vue de test pour les paiements - accessible seulement en développement"""
    from django.conf import settings
    import uuid

    context = {
        'payment_methods': [
            ('orange_money', 'Orange Money'),
            ('mtn_money', 'MTN Mobile Money'),
            ('carte_bancaire', 'Carte Bancaire'),
        ],
        'currencies': ['XAF'],
        'default_values': {
            'email': 'test@example.com',
            'amount': 5000,
            'currency': 'XAF',
            'payment_method': 'orange_money',
            'description': 'Test de paiement - BryShop'
        }
    }

    if request.method == 'POST':
        # Récupération des données du formulaire
        email = request.POST.get('email', 'test@example.com')
        amount = int(request.POST.get('amount', 5000))
        currency = request.POST.get('currency', 'XAF')
        payment_method = request.POST.get('payment_method', 'orange_money')
        description = request.POST.get('description', 'Test de paiement - BryShop')

        # Génération d'une référence unique
        reference = str(uuid.uuid4())
        callback_url = request.build_absolute_uri(reverse('payment_callback')) + f"?reference={reference}"

        print(f"[TEST PAYMENT] Email: {email}, Amount: {amount} {currency}")
        print(f"[TEST PAYMENT] Reference: {reference}")
        print(f"[TEST PAYMENT] Callback URL: {callback_url}")

        # Initialisation du paiement avec Notch Pay
        response = initialize_notch_payment(email, amount, description, reference, callback_url)

        if response and response.get('status') == 'Accepted':
            # Création de l'enregistrement Payment en base
            try:
                payment = Payment.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    notch_pay_id=response.get('transaction', {}).get('id', ''),
                    reference=reference,
                    amount=amount,
                    currency=currency,
                    status='pending',
                    payment_method=payment_method,
                    raw_response=response,
                )
                print(f"[TEST PAYMENT] Payment créé en base: ID {payment.id}")

                # Succès - redirection vers Notch Pay
                messages.success(request, f"Paiement initialisé avec succès ! ID: {payment.id}")
                return redirect(response.get('authorization_url'))

            except Exception as e:
                print(f"[TEST PAYMENT] Erreur création Payment: {e}")
                messages.error(request, f"Erreur lors de la création du paiement: {e}")
        else:
            # Erreur lors de l'initialisation
            error_msg = response.get('message', 'Erreur inconnue') if response else 'Pas de réponse'
            details = response.get('details', '') if response else ''
            print(f"[TEST PAYMENT] Erreur Notch Pay: {error_msg} - {details}")

            messages.error(request, f"Erreur d'initialisation: {error_msg}")
            if details:
                messages.error(request, f"Détails: {details}")

        # En cas d'erreur, on reste sur la page avec les erreurs
        context.update({
            'form_data': {
                'email': email,
                'amount': amount,
                'currency': currency,
                'payment_method': payment_method,
                'description': description,
            },
            'response': response,
        })

    return render(request, 'html/test_payment.html', context)

# historique des commandes (clients)
@login_required
def order_history(request):
    # Récupère toutes les commandes passées par l'utilisateur connecté
    user_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    # Vous pouvez regrouper les articles par date ou par un champ 'numéro_commande' si vous en ajoutez un.
    
    return render(request, 'html/order_history.html', {'user_orders': user_orders})

@login_required
def mes_cartes(request):
    """Vue pour afficher les cartes bancaires de l'utilisateur"""
    # Pour l'instant, on affiche une page simple
    # TODO: Implémenter la gestion complète des cartes bancaires
    return render(request, 'html/mes_cartes.html', {
        'title': 'Mes Cartes Bancaires',
        'message': 'Fonctionnalité en cours de développement.'
    })

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
