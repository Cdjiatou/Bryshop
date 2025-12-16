from django.urls import path, include
from BRYSHOP.views import index, detail, checkout, confirmation, product_by_category, nos_produits,contact_views, dashboard_boutiquier, ajouter_categorie, ajouter_produit, modifier_profil, changer_mot_de_passe, mes_cartes
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
    path('payment/callback/', views.payment_callback, name='payment_callback'),

    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('mes-cartes/', mes_cartes, name='mes_cartes'),
    path('test-payment/', views.test_payment, name='test_payment'),



    # Dashboard administrateur (boutiquier)
    path('dashboard/', dashboard_boutiquier, name='dashboard_boutiquier'),

    # Ajout catégorie et produit
    path('dashboard/ajouter-categorie/', ajouter_categorie, name='ajouter_categorie'),
    path('dashboard/ajouter-produit/', ajouter_produit, name='ajouter_produit'),

    # Modification profil et mot de passe
    path('dashboard/modifier-profil/', modifier_profil, name='modifier_profil'),
    path('dashboard/changer-mot-de-passe/', changer_mot_de_passe, name='changer_mot_de_passe'),

]

