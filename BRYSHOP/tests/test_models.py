from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from BRYSHOP.models import (
    Category, Product, Cart, CartItem, Order, 
    Payment, Wishlist, WishlistItem, Commande
)

User = get_user_model()


class CategoryModelTest(TestCase):
    """Tests pour le modèle Category"""
    
    def setUp(self):
        """Créer une catégorie de test"""
        self.category = Category.objects.create(
            name='Électronique'
        )
    
    def test_category_creation(self):
        """Test que la catégorie est créée correctement"""
        self.assertEqual(self.category.name, 'Électronique')
        self.assertIsNotNone(self.category.date_added)
    
    def test_category_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.category), 'Électronique')
    
    def test_category_ordering(self):
        """Test que les catégories sont ordonnées par date décroissante"""
        cat1 = Category.objects.create(name='Vêtements')
        cat2 = Category.objects.create(name='Livres')
        
        categories = Category.objects.all()
        self.assertEqual(categories[0], cat2)
        self.assertEqual(categories[1], cat1)


class ProductModelTest(TestCase):
    """Tests pour le modèle Product"""
    
    def setUp(self):
        """Créer une catégorie et un produit de test"""
        self.category = Category.objects.create(name='Smartphones')
        self.product = Product.objects.create(
            title='iPhone 15 Pro',
            price=999.99,
            description='Le dernier iPhone avec puce A17',
            category=self.category,
            stock=10
        )
    
    def test_product_creation(self):
        """Test que le produit est créé correctement"""
        self.assertEqual(self.product.title, 'iPhone 15 Pro')
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.description, 'Le dernier iPhone avec puce A17')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.stock, 10)
    
    def test_product_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.product), 'iPhone 15 Pro')
    
    def test_product_est_disponible_true(self):
        """Test que est_disponible retourne True quand stock > 0"""
        self.assertTrue(self.product.est_disponible())
    
    def test_product_est_disponible_false(self):
        """Test que est_disponible retourne False quand stock = 0"""
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.est_disponible())
    
    def test_product_peut_commander_true(self):
        """Test que peut_commander retourne True si stock suffisant"""
        self.assertTrue(self.product.peut_commander(5))
        self.assertTrue(self.product.peut_commander(10))
    
    def test_product_peut_commander_false(self):
        """Test que peut_commander retourne False si stock insuffisant"""
        self.assertFalse(self.product.peut_commander(11))
        self.assertFalse(self.product.peut_commander(100))
    
    def test_product_category_relation(self):
        """Test de la relation avec Category"""
        self.assertEqual(self.product.category, self.category)
        self.assertIn(self.product, self.category.categorie.all())
    
    def test_product_ordering(self):
        """Test que les produits sont ordonnés par date décroissante"""
        prod1 = Product.objects.create(
            title='Product 1',
            price=100,
            description='Test',
            category=self.category,
            stock=5
        )
        prod2 = Product.objects.create(
            title='Product 2',
            price=200,
            description='Test',
            category=self.category,
            stock=5
        )
        
        products = Product.objects.all()
        self.assertEqual(products[0], prod2)
        self.assertEqual(products[1], prod1)


class CartModelTest(TestCase):
    """Tests pour le modèle Cart"""
    
    def setUp(self):
        """Créer un utilisateur et un panier de test"""
        self.user = User.objects.create_user(
            username='cartuser',
            password='pass123'
        )
        self.cart = Cart.objects.create(user=self.user)
    
    def test_cart_creation(self):
        """Test que le panier est créé correctement"""
        self.assertEqual(self.cart.user, self.user)
        self.assertIsNotNone(self.cart.created_at)
    
    def test_cart_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.cart), 'Panier de cartuser')


class CartItemModelTest(TestCase):
    """Tests pour le modèle CartItem"""
    
    def setUp(self):
        """Créer les données de test"""
        self.user = User.objects.create_user(
            username='itemuser',
            password='pass123'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            title='Test Product',
            price=50.00,
            description='Test',
            category=self.category,
            stock=10
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
    
    def test_cart_item_creation(self):
        """Test que l'item du panier est créé correctement"""
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
    
    def test_cart_item_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.cart_item), 'Test Product (x2)')
    
    def test_cart_item_related_name(self):
        """Test du related_name pour accéder aux items d'un panier"""
        self.assertIn(self.cart_item, self.cart.items.all())


class PaymentModelTest(TestCase):
    """Tests pour le modèle Payment"""
    
    def setUp(self):
        """Créer un utilisateur et un paiement de test"""
        self.user = User.objects.create_user(
            username='payuser',
            password='pass123'
        )
        self.payment = Payment.objects.create(
            user=self.user,
            notch_pay_id='NP123456',
            reference='REF-001',
            amount=Decimal('50000.00'),
            currency='XAF',
            status='complete',
            customer_id='CUST-001',
            payment_method='orange_money'
        )
    
    def test_payment_creation(self):
        """Test que le paiement est créé correctement"""
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.notch_pay_id, 'NP123456')
        self.assertEqual(self.payment.reference, 'REF-001')
        self.assertEqual(self.payment.amount, Decimal('50000.00'))
        self.assertEqual(self.payment.currency, 'XAF')
        self.assertEqual(self.payment.status, 'complete')
    
    def test_payment_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.payment), 'Paiement REF-001 - complete')
    
    def test_payment_reference_unique(self):
        """Test que la référence est unique"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                user=self.user,
                reference='REF-001',  # Même référence
                amount=Decimal('1000.00'),
                status='pending'
            )


class OrderModelTest(TestCase):
    """Tests pour le modèle Order"""
    
    def setUp(self):
        """Créer les données de test"""
        self.user = User.objects.create_user(
            username='orderuser',
            password='pass123'
        )
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            title='Test Product',
            price=25000.00,
            description='Test',
            category=self.category,
            stock=10
        )
        self.order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            nom='Dupont',
            email='dupont@example.com',
            address='123 Rue Test',
            ville='Douala',
            pays='Cameroun',
            zipcode='12345',
            statut='en_attente',
            mode_paiement='orange_money',
            statut_paiement='en_attente'
        )
    
    def test_order_creation(self):
        """Test que la commande est créée correctement"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.product, self.product)
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.nom, 'Dupont')
        self.assertEqual(self.order.email, 'dupont@example.com')
        self.assertEqual(self.order.statut, 'en_attente')
    
    def test_order_numero_commande_auto_generated(self):
        """Test que le numéro de commande est généré automatiquement"""
        self.assertIsNotNone(self.order.numero_commande)
        self.assertTrue(self.order.numero_commande.startswith('CMD-'))
        self.assertNotEqual(self.order.numero_commande, 'CMD-###')
    
    def test_order_numero_commande_unique(self):
        """Test que chaque commande a un numéro unique"""
        order2 = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            nom='Martin',
            email='martin@example.com',
            address='456 Rue Test',
            ville='Yaoundé',
            pays='Cameroun',
            zipcode='54321'
        )
        self.assertNotEqual(self.order.numero_commande, order2.numero_commande)
    
    def test_order_calculer_frais_livraison_cameroun(self):
        """Test du calcul des frais de livraison pour le Cameroun"""
        self.order.pays = 'Cameroun'
        frais = self.order.calculer_frais_livraison()
        self.assertEqual(frais, 1500)
    
    def test_order_calculer_frais_livraison_france(self):
        """Test du calcul des frais de livraison pour la France"""
        self.order.pays = 'France'
        frais = self.order.calculer_frais_livraison()
        self.assertEqual(frais, 5000)
    
    def test_order_calculer_frais_livraison_default(self):
        """Test du calcul des frais de livraison pour un pays non listé"""
        self.order.pays = 'Belgique'
        frais = self.order.calculer_frais_livraison()
        self.assertEqual(frais, 2000)
    
    def test_order_total_commande(self):
        """Test du calcul du total de la commande"""
        self.order.frais_livraison = Decimal('1500.00')
        total = self.order.total_commande()
        expected = (Decimal('25000.00') * 2) + Decimal('1500.00')
        self.assertEqual(total, expected)
    
    def test_order_str_method(self):
        """Test de la méthode __str__"""
        expected = f"{self.order.numero_commande} - orderuser"
        self.assertEqual(str(self.order), expected)
    
    def test_order_statut_choices(self):
        """Test des différents statuts de commande"""
        statuts = ['en_attente', 'traitement', 'expedie', 'livre', 'annule']
        for statut in statuts:
            self.order.statut = statut
            self.order.save()
            self.assertEqual(self.order.statut, statut)
    
    def test_order_mode_paiement_choices(self):
        """Test des différents modes de paiement"""
        modes = ['livraison', 'orange_money', 'mtn_money', 'carte_bancaire']
        for mode in modes:
            self.order.mode_paiement = mode
            self.order.save()
            self.assertEqual(self.order.mode_paiement, mode)


class WishlistModelTest(TestCase):
    """Tests pour le modèle Wishlist"""
    
    def setUp(self):
        """Créer un utilisateur et une wishlist de test"""
        self.user = User.objects.create_user(
            username='wishuser',
            password='pass123'
        )
        self.wishlist = Wishlist.objects.create(user=self.user)
    
    def test_wishlist_creation(self):
        """Test que la wishlist est créée correctement"""
        self.assertEqual(self.wishlist.user, self.user)
        self.assertIsNotNone(self.wishlist.created_at)
    
    def test_wishlist_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.wishlist), 'Wishlist de wishuser')
    
    def test_wishlist_one_to_one_relation(self):
        """Test de la relation OneToOne avec User"""
        self.assertEqual(self.user.wishlist, self.wishlist)


class WishlistItemModelTest(TestCase):
    """Tests pour le modèle WishlistItem"""
    
    def setUp(self):
        """Créer les données de test"""
        self.user = User.objects.create_user(
            username='wishitemuser',
            password='pass123'
        )
        self.wishlist = Wishlist.objects.create(user=self.user)
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            title='Wishlist Product',
            price=100.00,
            description='Test',
            category=self.category,
            stock=5
        )
        self.wishlist_item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            product=self.product
        )
    
    def test_wishlist_item_creation(self):
        """Test que l'item de wishlist est créé correctement"""
        self.assertEqual(self.wishlist_item.wishlist, self.wishlist)
        self.assertEqual(self.wishlist_item.product, self.product)
        self.assertIsNotNone(self.wishlist_item.added_at)
    
    def test_wishlist_item_str_method(self):
        """Test de la méthode __str__"""
        expected = 'Wishlist Product dans wishlist de wishitemuser'
        self.assertEqual(str(self.wishlist_item), expected)
    
    def test_wishlist_item_unique_together(self):
        """Test que la contrainte unique_together fonctionne"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            WishlistItem.objects.create(
                wishlist=self.wishlist,
                product=self.product  # Même produit dans la même wishlist
            )
    
    def test_wishlist_item_related_name(self):
        """Test du related_name pour accéder aux items d'une wishlist"""
        self.assertIn(self.wishlist_item, self.wishlist.items.all())


class CommandeModelTest(TestCase):
    """Tests pour le modèle Commande (ancien modèle)"""
    
    def setUp(self):
        """Créer une commande de test"""
        self.commande = Commande.objects.create(
            items='iPhone 15 x2, AirPods x1',
            total=Decimal('2500.00'),
            nom='Martin',
            email='martin@example.com',
            address='789 Avenue Test',
            ville='Yaoundé',
            pays='Cameroun',
            zipcode='99999'
        )
    
    def test_commande_creation(self):
        """Test que la commande est créée correctement"""
        self.assertEqual(self.commande.items, 'iPhone 15 x2, AirPods x1')
        self.assertEqual(self.commande.total, Decimal('2500.00'))
        self.assertEqual(self.commande.nom, 'Martin')
        self.assertEqual(self.commande.email, 'martin@example.com')
    
    def test_commande_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.commande), 'Martin')
    
    def test_commande_ordering(self):
        """Test que les commandes sont ordonnées par date décroissante"""
        cmd1 = Commande.objects.create(
            items='Item 1',
            total=Decimal('100.00'),
            nom='User1',
            email='user1@example.com',
            address='Address 1',
            ville='Ville 1',
            pays='Pays 1',
            zipcode='11111'
        )
        cmd2 = Commande.objects.create(
            items='Item 2',
            total=Decimal('200.00'),
            nom='User2',
            email='user2@example.com',
            address='Address 2',
            ville='Ville 2',
            pays='Pays 2',
            zipcode='22222'
        )
        
        commandes = Commande.objects.all()
        self.assertEqual(commandes[0], cmd2)
        self.assertEqual(commandes[1], cmd1)
