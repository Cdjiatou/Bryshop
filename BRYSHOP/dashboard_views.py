from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.models import Client # Importez le modèle Client
from BRYSHOP.models import Order, Product 
from django.db.models import Sum, Count, F,Min, Max, Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce
from accounts.models import Client


User = get_user_model()


# # Fonction de test pour vérifier si l'utilisateur est un superutilisateur (admin)
# def is_shop_owner(user):
#     return user.is_authenticated and user.is_superuser
# Fonction de test pour vérifier si l'utilisateur est un boutiquier ou un superutilisateur
def is_shop_owner(user):
    if not user.is_authenticated:
        return False
    
    # 1. Vérifie si l'utilisateur est Superutilisateur (accès complet)
    if user.is_superuser:
        return True
    
    # 2. Vérifie si l'utilisateur a un profil Client et si ce profil est marqué comme boutiquier
    try:
        # Tente d'accéder au profil Client lié
        return user.client.is_shop_owner
    except Client.DoesNotExist:
        # Si aucun profil Client n'existe, il n'est pas un boutiquier
        return False

# Vue du tableau de bord sécurisée
@login_required(login_url='login') # Assure que l'utilisateur est connecté
@user_passes_test(is_shop_owner, login_url='Accueil') # Redirige s'il n'est pas superuser
def admin_dashboard(request):
    # 1. Statistiques Clés (Exemple)
    total_orders = Order.objects.count()
    total_revenue = Order.objects.annotate(
        item_total=F('product__price') * F('quantity')
    ).aggregate(Sum('item_total'))['item_total__sum'] or 0
    total_clients = User.objects.filter(is_superuser=False).count() # Compte les utilisateurs non-admin

    # 2. Article le plus vendu
    best_seller = Order.objects.values('product__title').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity').first()

    # 3. Meilleur Client (celui qui a le plus de commandes)
    top_customer = Order.objects.values('user__username').annotate(
        num_orders=Count('id')
    ).order_by('-num_orders').first()
    
    # Récupérer les 5 dernières commandes
    recent_orders = Order.objects.select_related('user', 'product').order_by('-date_ordered')[:5]

    context = {
        # Données du tableau de bord
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2),
        'total_clients': total_clients,
        'best_seller': best_seller,
        'top_customer': top_customer,
        'recent_orders': recent_orders,
    }
    return render(request, 'html/admin_dashboard.html', context)




@login_required(login_url='login')
@user_passes_test(is_shop_owner, login_url='Accueil')
def manage_clients(request):
    # Récupérer tous les utilisateurs qui ne sont PAS des superutilisateurs (les clients)
    # Utilisez .select_related('client') pour charger les infos Client en même temps
    client_list = User.objects.filter(is_superuser=False).select_related('client').order_by('date_joined')
    
    # Gestion de la recherche
    query = request.GET.get('q')
    if query:
        client_list = client_list.filter(
    Q(username__icontains=query) |
    Q(first_name__icontains=query) |
    Q(last_name__icontains=query) |
    Q(email__icontains=query)
)
        
    # Gestion de la pagination (afficher par exemple 10 clients par page)
    paginator = Paginator(client_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'html/admin_manage_clients.html', context)