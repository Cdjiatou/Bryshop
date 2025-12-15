from django.contrib import admin
from .models import Category, Product, Commande, Order, Cart, CartItem

# Register your models here.
#personalisation de la partie administrateur du site
admin.site.site_header = "E-COMMERCE BRYSHOP"
admin.site.site_title = "BRYAN Shop"
admin.site.index_title = "Manager"


# class pour personnaliser la partie admin sous forme de tableau
class AdminCategorie(admin.ModelAdmin):
    list_display = ('name', 'date_added')
    
    
class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category', 'date_added')
    search_fields = ('title',)
    list_editable = ('price', 'stock', 'category')
    list_filter = ('category',)
    
class AdminCommande(admin.ModelAdmin):
    list_display = ('items', 'nom', 'email', 'address', 'ville', 'pays', 'total', 'zipcode', 'date_commande')

class AdminOrder(admin.ModelAdmin):
    list_display = ('numero_commande', 'user', 'product', 'quantity', 'statut', 'ville', 'pays', 'date_ordered')
    list_filter = ('statut', 'date_ordered', 'pays')
    search_fields = ('numero_commande', 'user__username', 'product__title', 'email')
    list_editable = ('statut',)
    readonly_fields = ('numero_commande', 'date_ordered')
    ordering = ('-date_ordered',)

class AdminCart(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

class AdminCartItem(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product__title',)

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(Commande, AdminCommande)
admin.site.register(Order, AdminOrder)
admin.site.register(Cart, AdminCart)
admin.site.register(CartItem, AdminCartItem)