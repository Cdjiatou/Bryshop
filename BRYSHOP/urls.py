from django.urls import path, include
from BRYSHOP import dashboard_views
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

    path('dashboard/', dashboard_views.admin_dashboard, name='admin_dashboard'), 
    path('historique-commandes/', views.order_history, name='order_history'), 
    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('dashboard/clients/', dashboard_views.manage_clients, name='admin_manage_clients'), 



]

