from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import CartItem, Product, Commande, Category, Cart, Order
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse


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

    # Vérifier le stock avant de créer les commandes
    for item in cart_items:
        if not item.product.peut_commander(item.quantity):
            messages.error(request, f"Stock insuffisant pour '{item.product.title}'. Stock disponible : {item.product.stock}")
            return redirect('cart')

    # Créer les commandes et déduire le stock
    for item in cart_items:
        Order.objects.create(
            user=user,
            product=item.product,
            quantity=item.quantity,
            nom=f"{user.first_name} {user.last_name}",
            email=user.email,
            address=user.customuser.ville if hasattr(user, 'customuser') else '',
            ville=user.customuser.ville if hasattr(user, 'customuser') else '',
            pays=user.customuser.pays if hasattr(user, 'customuser') else '',
        )
        # Déduire le stock
        item.product.stock -= item.quantity
        item.product.save()

    # Calcul du total
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Préparer le message e-mail
    subject = "✅ Confirmation de votre commande - BryShop"
    message = f"Bonjour {user.first_name},\n\n"
    message += "Merci pour votre commande sur BryShop ! Voici un résumé de vos achats :\n\n"

    for item in cart_items:
        message += f"- {item.product.title} x {item.quantity} = {item.product.price * item.quantity} XAF\n"

    message += f"\nTotal : {total} XAF\n\n"
    message += "Nous traiterons votre commande dans les plus brefs délais.\n\nMerci pour votre confiance.\n\nL'équipe BryShop"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )

    # Vider le panier après la commande
    cart.items.all().delete()

    # Message de confirmation à l'utilisateur dans l'interface
    messages.success(request, "🎉 Merci pour votre commande ! Un email de confirmation vous a été envoyé.")

    return redirect('confirmation')


@login_required
def mes_commandes(request):
    commandes = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'html/mes_commandes.html', {'commandes': commandes})

