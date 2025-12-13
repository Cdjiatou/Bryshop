from django.contrib import admin
from .models import Category, Product, Commande

# Register your models here.
#personalisation de la partie administrateur du site
admin.site.site_header = "E-COMMERCE BRYSHOP"
admin.site.site_title = "BRYAN Shop"
admin.site.index_title = "Manager"


# class pour personnaliser la partie admin sous forme de tableau
class AdminCategorie(admin.ModelAdmin):
    list_display = ('name', 'date_added')
    
    
class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added')
    search_fields = ('title',)
    list_editable = ('price','category',)
    
class AdminCommande(admin.ModelAdmin):
    list_display = ('items', 'nom', 'email', 'address', 'ville', 'pays', 'total', 'zipcode', 'date_commande')

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(Commande, AdminCommande)