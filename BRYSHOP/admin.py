# BRYSHOP/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum, Count
from .models import Category, Product, Commande, Order, Cart, CartItem

# ===================================
# PERSONNALISATION DU SITE ADMIN
# ===================================
admin.site.site_header = "🛍️ BryShop Administration"
admin.site.site_title = "BryShop Admin"
admin.site.index_title = "Tableau de bord - Gérez votre boutique"


# ===================================
# ADMIN CATEGORY
# ===================================
@admin.register(Category)
class AdminCategorie(admin.ModelAdmin):
    list_display = ['category_icon', 'name', 'product_count', 'date_added_formatted', 'actions_column']
    search_fields = ['name']
    list_per_page = 25
    ordering = ['-date_added']
    
    # Icône catégorie
    def category_icon(self, obj):
        return format_html(
            '<div style="width: 40px; height: 40px; background: linear-gradient(135deg, #2ecc71, #56c596); '
            'border-radius: 10px; display: flex; align-items: center; justify-content: center; '
            'color: white; font-weight: bold; font-size: 16px;">{}</div>',
            obj.name[0].upper()
        )
    category_icon.short_description = '📁'
    
    # Nombre de produits
    def product_count(self, obj):
        count = obj.product_set.count()
        url = reverse('admin:BRYSHOP_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html(
            '<a href="{}" style="background: #3498db; color: white; padding: 6px 14px; '
            'border-radius: 14px; font-size: 12px; font-weight: bold; text-decoration: none;">'
            '📦 {} produits</a>',
            url, count
        )
    product_count.short_description = 'Produits'
    
    # Date formatée
    def date_added_formatted(self, obj):
        return obj.date_added.strftime('%d/%m/%Y à %H:%M')
    date_added_formatted.short_description = 'Date de création'
    
    # Actions
    def actions_column(self, obj):
        return format_html(
            '<a href="{}" style="color: #3498db; text-decoration: none;">✏️ Modifier</a>',
            reverse('admin:BRYSHOP_category_change', args=[obj.pk])
        )
    actions_column.short_description = 'Actions'


# ===================================
# ADMIN PRODUCT
# ===================================
@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['image_thumbnail', 'title', 'price_formatted', 'stock_badge', 
                    'category_link', 'date_added_formatted', 'actions_column']
    search_fields = ['title', 'description']
    list_filter = ['category', 'date_added']
    list_per_page = 20
    ordering = ['-date_added']
    date_hierarchy = 'date_added'
    
    fieldsets = (
        ('📦 Informations Produit', {
            'fields': ('title', 'description', 'price', 'stock', 'category')
        }),
        ('🖼️ Image', {
            'fields': ('image',)
        }),
        ('📅 Dates', {
            'fields': ('date_added',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['date_added']
    
    # Actions personnalisées
    actions = ['augmenter_stock', 'reduire_stock', 'marquer_rupture']
    
    # Miniature image
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius: 8px; '
                'box-shadow: 0 2px 8px rgba(0,0,0,0.1); object-fit: cover;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 60px; height: 60px; background: #e0e0e0; '
            'border-radius: 8px; display: flex; align-items: center; '
            'justify-content: center; font-size: 24px;">📦</div>'
        )
    image_thumbnail.short_description = 'Image'
    
    # Prix formaté
    def price_formatted(self, obj):
        return format_html(
            '<span style="color: #2ecc71; font-weight: bold; font-size: 15px;">'
            '{:,.0f} XAF</span>',
            obj.price
        )
    price_formatted.short_description = 'Prix'
    price_formatted.admin_order_field = 'price'
    
    # Badge stock
    def stock_badge(self, obj):
        if obj.stock == 0:
            color = '#e74c3c'
            icon = '❌'
            text = 'RUPTURE'
        elif obj.stock < 10:
            color = '#f39c12'
            icon = '⚠️'
            text = f'{obj.stock} restants'
        else:
            color = '#2ecc71'
            icon = '✅'
            text = f'{obj.stock} en stock'
        
        return format_html(
            '<span style="background: {}; color: white; padding: 6px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold; '
            'display: inline-block;">{} {}</span>',
            color, icon, text
        )
    stock_badge.short_description = 'Stock'
    stock_badge.admin_order_field = 'stock'
    
    # Lien catégorie
    def category_link(self, obj):
        if obj.category:
            url = reverse('admin:BRYSHOP_category_change', args=[obj.category.pk])
            return format_html(
                '<a href="{}" style="color: #9b59b6; font-weight: 600;">📁 {}</a>',
                url, obj.category.name
            )
        return '—'
    category_link.short_description = 'Catégorie'
    
    # Date formatée
    def date_added_formatted(self, obj):
        return obj.date_added.strftime('%d/%m/%Y')
    date_added_formatted.short_description = 'Ajouté le'
    date_added_formatted.admin_order_field = 'date_added'
    
    # Actions
    def actions_column(self, obj):
        return format_html(
            '<a href="{}" style="color: #3498db; text-decoration: none;">✏️ Modifier</a>',
            reverse('admin:BRYSHOP_product_change', args=[obj.pk])
        )
    actions_column.short_description = 'Actions'
    
    # Actions en masse
    def augmenter_stock(self, request, queryset):
        for product in queryset:
            product.stock += 10
            product.save()
        self.message_user(request, f"✅ Stock augmenté de 10 pour {queryset.count()} produit(s)")
    augmenter_stock.short_description = "📈 Augmenter le stock (+10)"
    
    def reduire_stock(self, request, queryset):
        for product in queryset:
            if product.stock >= 5:
                product.stock -= 5
                product.save()
        self.message_user(request, f"✅ Stock réduit de 5 pour {queryset.count()} produit(s)")
    reduire_stock.short_description = "📉 Réduire le stock (-5)"
    
    def marquer_rupture(self, request, queryset):
        queryset.update(stock=0)
        self.message_user(request, f"⚠️ {queryset.count()} produit(s) marqué(s) en rupture", level='WARNING')
    marquer_rupture.short_description = "❌ Marquer en rupture de stock"


# ===================================
# ADMIN COMMANDE
# ===================================
@admin.register(Commande)
class AdminCommande(admin.ModelAdmin):
    list_display = ['order_number', 'customer_info', 'items_preview', 'total_formatted', 
                    'location', 'date_commande_formatted', 'order_status']
    search_fields = ['nom', 'email', 'ville', 'pays']
    list_filter = ['ville', 'pays', 'date_commande']
    list_per_page = 25
    date_hierarchy = 'date_commande'
    ordering = ['-date_commande']
    
    fieldsets = (
        ('👤 Informations Client', {
            'fields': ('nom', 'prenom', 'email', 'phone')
        }),
        ('📦 Commande', {
            'fields': ('items', 'total')
        }),
        ('📍 Adresse de Livraison', {
            'fields': ('address', 'ville', 'pays', 'zipcode')
        }),
        ('📅 Date', {
            'fields': ('date_commande',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['date_commande']
    
    # Numéro commande
    def order_number(self, obj):
        return format_html(
            '<span style="background: #34495e; color: white; padding: 6px 12px; '
            'border-radius: 6px; font-family: monospace; font-size: 11px; font-weight: bold;">'
            '#{}</span>',
            obj.id
        )
    order_number.short_description = 'N°'
    
    # Info client
    def customer_info(self, obj):
        return format_html(
            '<div><strong style="color: #2c3e50;">👤 {}</strong><br>'
            '<small style="color: #7f8c8d;">📧 {}</small></div>',
            obj.nom, obj.email
        )
    customer_info.short_description = 'Client'
    
    # Aperçu items
    def items_preview(self, obj):
        items = obj.items[:50] + '...' if len(obj.items) > 50 else obj.items
        return format_html(
            '<span style="color: #7f8c8d; font-size: 12px;">📦 {}</span>',
            items
        )
    items_preview.short_description = 'Articles'
    
    # Total formaté
    def total_formatted(self, obj):
        return format_html(
            '<span style="color: #e74c3c; font-weight: bold; font-size: 14px;">'
            '{} XAF</span>',
            obj.total
        )
    total_formatted.short_description = 'Total'
    total_formatted.admin_order_field = 'total'
    
    # Localisation
    def location(self, obj):
        return format_html(
            '<span style="color: #3498db;">📍 {}, {}</span>',
            obj.ville, obj.pays
        )
    location.short_description = 'Localisation'
    
    # Date formatée
    def date_commande_formatted(self, obj):
        return obj.date_commande.strftime('%d/%m/%Y %H:%M')
    date_commande_formatted.short_description = 'Date'
    date_commande_formatted.admin_order_field = 'date_commande'
    
    # Statut
    def order_status(self, obj):
        return format_html(
            '<span style="background: #f39c12; color: white; padding: 6px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">⏳ EN COURS</span>'
        )
    order_status.short_description = 'Statut'


# ===================================
# ADMIN ORDER
# ===================================
@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['order_number', 'user_link', 'product_link', 'quantity', 
                    'total_order', 'status_badge', 'payment_badge', 
                    'payment_method', 'date_ordered_formatted']
    list_filter = ['statut', 'statut_paiement', 'mode_paiement', 'date_ordered', 'pays', 'ville']
    search_fields = ['numero_commande', 'user__username', 'user__email', 'product__title', 'email', 'telephone']
    list_per_page = 25
    date_hierarchy = 'date_ordered'
    ordering = ['-date_ordered']
    
    fieldsets = (
        ('📋 Informations Commande', {
            'fields': ('numero_commande', 'user', 'product', 'quantity', 'date_ordered')
        }),
        ('💳 Paiement', {
            'fields': ('mode_paiement', 'statut_paiement', 'frais_livraison')
        }),
        ('📦 Livraison', {
            'fields': ('statut', 'adresse', 'ville', 'pays', 'code_postal', 'telephone', 'email')
        }),
        ('💰 Résumé Financier', {
            'fields': ('order_summary',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['numero_commande', 'date_ordered', 'order_summary']
    
    # Actions en masse
    actions = ['marquer_expedie', 'marquer_livre', 'marquer_paye', 'marquer_traitement', 'annuler_commande']
    
    # Numéro commande
    def order_number(self, obj):
        return format_html(
            '<span style="background: #34495e; color: white; padding: 6px 12px; '
            'border-radius: 6px; font-family: monospace; font-size: 11px; font-weight: bold;">{}</span>',
            obj.numero_commande
        )
    order_number.short_description = 'N° Commande'
    
    # Lien utilisateur
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}" style="color: #3498db; font-weight: 600; text-decoration: none;">'
            '👤 {}</a>',
            url, obj.user.username
        )
    user_link.short_description = 'Client'
    
    # Lien produit
    def product_link(self, obj):
        url = reverse('admin:BRYSHOP_product_change', args=[obj.product.pk])
        title = obj.product.title[:30] + '...' if len(obj.product.title) > 30 else obj.product.title
        return format_html(
            '<a href="{}" style="color: #2ecc71; text-decoration: none;">📦 {}</a>',
            url, title
        )
    product_link.short_description = 'Produit'
    
    # Total commande
    def total_order(self, obj):
        total = (obj.product.price * obj.quantity) + obj.frais_livraison
        return format_html(
            '<div style="text-align: right;">'
            '<span style="color: #e74c3c; font-weight: bold; font-size: 14px;">'
            '{:,.0f} XAF</span><br>'
            '<small style="color: #7f8c8d;">+ {:,.0f} XAF livraison</small>'
            '</div>',
            total, obj.frais_livraison
        )
    total_order.short_description = 'Montant Total'
    
    # Badge statut
    def status_badge(self, obj):
        status_config = {
            'en_attente': ('#f39c12', '⏳', 'En attente'),
            'traitement': ('#3498db', '⚙️', 'En traitement'),
            'expedie': ('#9b59b6', '🚚', 'Expédié'),
            'livre': ('#2ecc71', '✅', 'Livré'),
            'annule': ('#e74c3c', '❌', 'Annulé')
        }
        config = status_config.get(obj.statut, ('#95a5a6', '❓', obj.statut))
        return format_html(
            '<span style="background: {}; color: white; padding: 6px 14px; '
            'border-radius: 14px; font-size: 11px; font-weight: bold; '
            'display: inline-block; min-width: 100px; text-align: center;">{} {}</span>',
            config[0], config[1], config[2]
        )
    status_badge.short_description = 'Statut Livraison'
    status_badge.admin_order_field = 'statut'
    
    # Badge paiement
    def payment_badge(self, obj):
        payment_config = {
            'en_attente': ('#f39c12', '⏳', 'En attente'),
            'paye': ('#2ecc71', '✅', 'Payé'),
            'echoue': ('#e74c3c', '❌', 'Échoué')
        }
        config = payment_config.get(obj.statut_paiement, ('#95a5a6', '❓', obj.statut_paiement))
        return format_html(
            '<span style="background: {}; color: white; padding: 6px 14px; '
            'border-radius: 14px; font-size: 11px; font-weight: bold; '
            'display: inline-block; min-width: 80px; text-align: center;">{} {}</span>',
            config[0], config[1], config[2]
        )
    payment_badge.short_description = 'Paiement'
    payment_badge.admin_order_field = 'statut_paiement'
    
    # Mode paiement
    def payment_method(self, obj):
        icons = {
            'livraison': ('💵', '#2c3e50'),
            'orange_money': ('🟠', '#ff6b00'),
            'mtn_money': ('🟡', '#ffcb05'),
            'carte_bancaire': ('💳', '#3498db')
        }
        icon, color = icons.get(obj.mode_paiement, ('💰', '#95a5a6'))
        return format_html(
            '<span style="color: {}; font-weight: 600;">{} {}</span>',
            color, icon, obj.get_mode_paiement_display()
        )
    payment_method.short_description = 'Mode de paiement'
    
    # Date formatée
    def date_ordered_formatted(self, obj):
        return obj.date_ordered.strftime('%d/%m/%Y %H:%M')
    date_ordered_formatted.short_description = 'Date'
    date_ordered_formatted.admin_order_field = 'date_ordered'
    
    # Résumé commande
    def order_summary(self, obj):
        subtotal = obj.product.price * obj.quantity
        total = subtotal + obj.frais_livraison
        return format_html(
            '<div style="background: linear-gradient(135deg, #f8f9fa, #e8f5e9); '
            'padding: 25px; border-radius: 12px; border-left: 4px solid #2ecc71;">'
            '<h3 style="color: #2c3e50; margin-bottom: 20px; font-size: 18px;">📊 Résumé de la commande</h3>'
            '<table style="width: 100%; border-collapse: collapse;">'
            '<tr><td style="padding: 10px; border-bottom: 1px solid #e0e0e0;"><strong>Produit:</strong></td>'
            '<td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{}</td></tr>'
            '<tr><td style="padding: 10px; border-bottom: 1px solid #e0e0e0;"><strong>Prix unitaire:</strong></td>'
            '<td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{:,.0f} XAF</td></tr>'
            '<tr><td style="padding: 10px; border-bottom: 1px solid #e0e0e0;"><strong>Quantité:</strong></td>'
            '<td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">× {}</td></tr>'
            '<tr><td style="padding: 10px; border-bottom: 1px solid #e0e0e0;"><strong>Sous-total:</strong></td>'
            '<td style="padding: 10px; border-bottom: 1px solid #e0e0e0;">{:,.0f} XAF</td></tr>'
            '<tr><td style="padding: 10px; border-bottom: 2px solid #2ecc71;"><strong>Frais de livraison:</strong></td>'
            '<td style="padding: 10px; border-bottom: 2px solid #2ecc71;">{:,.0f} XAF</td></tr>'
            '<tr><td style="padding: 12px; font-size: 16px;"><strong>TOTAL:</strong></td>'
            '<td style="padding: 12px; color: #2ecc71; font-weight: bold; font-size: 18px;">{:,.0f} XAF</td></tr>'
            '</table>'
            '<div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e0e0e0;">'
            '<p style="margin: 5px 0;"><strong>📞 Téléphone:</strong> {}</p>'
            '<p style="margin: 5px 0;"><strong>📧 Email:</strong> {}</p>'
            '<p style="margin: 5px 0;"><strong>📍 Adresse:</strong> {}, {}, {} - {}</p>'
            '</div></div>',
            obj.product.title, obj.product.price, obj.quantity, subtotal, 
            obj.frais_livraison, total, obj.telephone, obj.email,
            obj.adresse, obj.ville, obj.pays, obj.code_postal
        )
    order_summary.short_description = 'Détails Complets'
    
    # Actions en masse
    def marquer_traitement(self, request, queryset):
        updated = queryset.update(statut='traitement')
        self.message_user(request, f"⚙️ {updated} commande(s) en cours de traitement")
    marquer_traitement.short_description = "⚙️ Marquer en traitement"
    
    def marquer_expedie(self, request, queryset):
        updated = queryset.update(statut='expedie')
        self.message_user(request, f"🚚 {updated} commande(s) expédiée(s)")
    marquer_expedie.short_description = "🚚 Marquer comme expédié"
    
    def marquer_livre(self, request, queryset):
        updated = queryset.update(statut='livre')
        self.message_user(request, f"✅ {updated} commande(s) livrée(s)")
    marquer_livre.short_description = "✅ Marquer comme livré"
    
    def marquer_paye(self, request, queryset):
        updated = queryset.update(statut_paiement='paye')
        self.message_user(request, f"💰 {updated} paiement(s) confirmé(s)")
    marquer_paye.short_description = "💰 Confirmer le paiement"
    
    def annuler_commande(self, request, queryset):
        updated = queryset.update(statut='annule')
        self.message_user(request, f"❌ {updated} commande(s) annulée(s)", level='WARNING')
    annuler_commande.short_description = "❌ Annuler la commande"


# ===================================
# ADMIN CART
# ===================================
@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['cart_id', 'user_link', 'items_count', 'created_at_formatted', 'cart_status']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    # ID Panier
    def cart_id(self, obj):
        return format_html(
            '<span style="background: #9b59b6; color: white; padding: 4px 10px; '
            'border-radius: 6px; font-family: monospace; font-size: 11px;">🛒 #{}</span>',
            obj.id
        )
    cart_id.short_description = 'Panier'
    
    # Lien utilisateur
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}" style="color: #3498db; font-weight: 600;">👤 {}</a>',
            url, obj.user.username
        )
    user_link.short_description = 'Client'
    
    # Nombre d'items
    def items_count(self, obj):
        count = obj.cartitem_set.count()
        return format_html(
            '<span style="background: #3498db; color: white; padding: 6px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">📦 {} articles</span>',
            count
        )
    items_count.short_description = 'Articles'
    
    # Date formatée
    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    created_at_formatted.short_description = 'Créé le'
    created_at_formatted.admin_order_field = 'created_at'
    
    # Statut
    def cart_status(self, obj):
        return format_html(
            '<span style="background: #f39c12; color: white; padding: 6px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">⏳ ACTIF</span>'
        )
    cart_status.short_description = 'Statut'


# ===================================
# ADMIN CART ITEM
# ===================================
@admin.register(CartItem)
class AdminCartItem(admin.ModelAdmin):
    list_display = ['item_id', 'cart_link', 'product_link', 'quantity_badge', 
                    'unit_price', 'total_price', 'item_actions']
    search_fields = ['product__title', 'cart__user__username']
    list_filter = ['cart__created_at']
    list_per_page = 25
    
    # ID Item
    def item_id(self, obj):
        return format_html(
            '<span style="background: #95a5a6; color: white; padding: 4px 8px; '
            'border-radius: 4px; font-size: 10px;">#{}</span>',
            obj.id
        )
    item_id.short_description = 'ID'
    
    # Lien panier
    def cart_link(self, obj):
        url = reverse('admin:BRYSHOP_cart_change', args=[obj.cart.pk])
        return format_html(
            '<a href="{}" style="color: #9b59b6;">🛒 Panier #{}</a>',
            url, obj.cart.id
        )
    cart_link.short_description = 'Panier'
    
    # Lien produit
    def product_link(self, obj):
        url = reverse('admin:BRYSHOP_product_change', args=[obj.product.pk])
        return format_html(
            '<a href="{}" style="color: #2ecc71; font-weight: 600;">📦 {}</a>',
            url, obj.product.title[:30]
        )
    product_link.short_description = 'Produit'
    
    # Badge quantité
    def quantity_badge(self, obj):
        return format_html(
            '<span style="background: #3498db; color: white; padding: 6px 12px; '
            'border-radius: 12px; font-size: 12px; font-weight: bold;">× {}</span>',
            obj.quantity
        )
    quantity_badge.short_description = 'Qté'
    
    # Prix unitaire
    def unit_price(self, obj):
        return format_html(
            '<span style="color: #7f8c8d;">{:,.0f} XAF</span>',
            obj.product.price
        )
    unit_price.short_description = 'Prix Unit.'
    
    # Prix total
    def total_price(self, obj):
        total = obj.product.price * obj.quantity
        return format_html(
            '<span style="color: #e74c3c; font-weight: bold; font-size: 14px;">'
            '{:,.0f} XAF</span>',
            total
        )
    total_price.short_description = 'Total'
    
    # Actions
    def item_actions(self, obj):
        return format_html(
            '<a href="{}" style="color: #3498db; text-decoration: none;">✏️ Modifier</a>',
            reverse('admin:BRYSHOP_cartitem_change', args=[obj.pk])
        )
    item_actions.short_description = 'Actions'