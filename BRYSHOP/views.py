
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms_profil import ProfilBoutiquierForm, PasswordChangeCustomForm
from django.contrib.auth import update_session_auth_hash,get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
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
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse
from .models import CartItem, Product, Commande, Category, Cart, Order, Wishlist, WishlistItem 






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

        # Vérifier le stock avant de créer les commandes
        for item in cart_items:
            if not item.product.peut_commander(item.quantity):
                messages.error(request, f"Stock insuffisant pour '{item.product.title}'. Stock disponible : {item.product.stock}")
                return redirect('cart')

        # Créer les commandes et déduire le stock
        total = 0
        frais_livraison_total = 0
        for item in cart_items:
            order = Order(
                user=user,
                product=item.product,
                quantity=item.quantity,
                mode_paiement=mode_paiement,
                statut_paiement='paye' if mode_paiement == 'livraison' else 'en_attente',
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
            
            total += item.product.price * item.quantity
            frais_livraison_total += order.frais_livraison

        # Préparer le message e-mail
        subject = "✅ Confirmation de votre commande - BryShop"
        message_email = f"Bonjour {user.first_name},\n\n"
        message_email += "Merci pour votre commande sur BryShop ! Voici un résumé de vos achats :\n\n"

        for item in cart_items:
            message_email += f"- {item.product.title} x {item.quantity} = {item.product.price * item.quantity} XAF\n"

        message_email += f"\nSous-total : {total} XAF\n"
        message_email += f"Frais de livraison : {frais_livraison_total} XAF\n"
        message_email += f"Total : {total + frais_livraison_total} XAF\n\n"
        message_email += "Nous traiterons votre commande dans les plus brefs délais.\n\nMerci pour votre confiance.\n\nL'équipe BryShop"

        send_mail(
            subject,
            message_email,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

        # Vider le panier après la commande
        cart.items.all().delete()

        # Message de confirmation à l'utilisateur dans l'interface
        if mode_paiement == 'livraison':
            messages.success(request, "🎉 Merci pour votre commande ! Vous paierez à la livraison. Un email de confirmation vous a été envoyé.")
        else:
            messages.info(request, f"🎉 Commande enregistrée ! Paiement {order.get_mode_paiement_display()} en attente de confirmation.")

        return redirect('confirmation')
    
    return redirect('checkout')


@login_required
def mes_commandes(request):
    commandes = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'html/mes_commandes.html', {'commandes': commandes})



# historique des commandes (clients)
@login_required
def order_history(request):
    # Récupère toutes les commandes passées par l'utilisateur connecté
    user_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    # Vous pouvez regrouper les articles par date ou par un champ 'numéro_commande' si vous en ajoutez un.
    
    return render(request, 'html/order_history.html', {'user_orders': user_orders})









# -------------------------------------------
# Vues pour la Wishlist
# -------------------------------------------

@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # 1. Récupérer ou créer la Wishlist pour l'utilisateur
    wishlist, created = Wishlist.objects.get_or_create(user=user)

    # 2. Vérifier si l'article existe déjà
    try:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f"✨ {product.title} a été ajouté à votre liste de souhaits.")
    except Exception:
        # Gère le cas où l'article existe déjà (dû à unique_together)
        messages.info(request, f"ℹ️ {product.title} est déjà dans votre liste de souhaits.")
        
    # Redirige vers la page d'où l'utilisateur vient, ou vers la wishlist
    return redirect(request.META.get('HTTP_REFERER', 'wishlist_view'))


@login_required
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist_items = wishlist.items.all()
    except Wishlist.DoesNotExist:
        wishlist_items = []

    return render(request, 'html/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist(request, item_id):
    # Cherche l'élément dans la wishlist de l'utilisateur connecté
    item = get_object_or_404(
        WishlistItem, 
        id=item_id, 
        wishlist__user=request.user # Sécurité: s'assure que l'élément appartient bien à l'utilisateur
    )
    
    product_title = item.product.title
    item.delete()
    
    messages.success(request, f"🗑️ {product_title} a été retiré de votre liste de souhaits.")
    return redirect('wishlist_view')



