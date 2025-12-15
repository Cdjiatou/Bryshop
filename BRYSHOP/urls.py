from django.urls import path, include
from BRYSHOP.views import index, detail, checkout, confirmation, product_by_category, nos_produits,contact_views
from . import views
urlpatterns = [
    path('', index, name='Accueil'),
    path('<int:myid>', detail, name="detail"),
    path('confirmation', confirmation, name="confirmation"),
    path('categorie/<int:id>/', product_by_category, name='product_by_category'),
    path('accounts/', include('accounts.urls')),
    path('nos-produits/', views.nos_produits, name='nos_produits'),
    path('contact/', views.contact_views, name='contact'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_views, name='cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('cart/update/<int:cart_item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),





]

