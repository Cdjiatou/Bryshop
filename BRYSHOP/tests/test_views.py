from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from BRYSHOP.models import Category, Product, Cart, CartItem, Order, Wishlist, WishlistItem
from decimal import Decimal

User = get_user_model()




class ProductListViewTest(TestCase):
    """Tests pour la vue liste des produits"""
    
    def setUp(self):
        """Créer des produits de test"""
        self.client = Client()
        self.category = Category.objects.create(name='Electronics')
        
        # Créer plusieurs produits
        for i in range(5):
            Product.objects.create(
                title=f'Product {i}',
                price=100.00 + i,
                description=f'Description {i}',
                category=self.category,
                stock=10
            )
    
    def test_product_list_view_status_code(self):
        """Test que la page des produits retourne 200"""
        response = self.client.get(reverse('nos_produits'))
        self.assertEqual(response.status_code, 200)
    
    def test_product_list_view_contains_products(self):
        """Test que la vue contient les produits"""
        response = self.client.get(reverse('nos_produits'))
        self.assertContains(response, 'Product 0')
        self.assertContains(response, 'Product 1')


class BoutiquierViewsTest(TestCase):
    """Tests pour les vues du boutiquier"""
    
    def setUp(self):
        """Créer un boutiquier et un client normal"""
        self.client = Client()
        
        # Créer un boutiquier
        self.boutiquier = User.objects.create_user(
            username='boutiquier',
            password='pass123',
            role='boutiquier'
        )
        
        # Créer un client normal
        self.normal_user = User.objects.create_user(
            username='client',
            password='pass123',
            role='client'
        )
        
        self.category = Category.objects.create(name='Test')
    
    def test_dashboard_boutiquier_requires_login(self):
        """Test que le dashboard nécessite une connexion"""
        response = self.client.get(reverse('dashboard_boutiquier'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_dashboard_boutiquier_requires_boutiquier_role(self):
        """Test que seul un boutiquier peut accéder au dashboard"""
        # Connexion en tant que client normal
        self.client.login(username='client', password='pass123')
        response = self.client.get(reverse('dashboard_boutiquier'))
        self.assertEqual(response.status_code, 302)  # Redirection
    
    def test_dashboard_boutiquier_access_with_boutiquier_role(self):
        """Test qu'un boutiquier peut accéder au dashboard"""
        self.client.login(username='boutiquier', password='pass123')
        response = self.client.get(reverse('dashboard_boutiquier'))
        self.assertEqual(response.status_code, 200)
    
    def test_ajouter_categorie_requires_boutiquier(self):
        """Test que seul un boutiquier peut ajouter une catégorie"""
        # Sans connexion
        response = self.client.get(reverse('ajouter_categorie'))
        self.assertEqual(response.status_code, 302)
        
        # Avec client normal
        self.client.login(username='client', password='pass123')
        response = self.client.get(reverse('ajouter_categorie'))
        self.assertEqual(response.status_code, 302)
    
    def test_ajouter_categorie_post_valid(self):
        """Test de l'ajout d'une catégorie avec données valides"""
        self.client.login(username='boutiquier', password='pass123')
        response = self.client.post(reverse('ajouter_categorie'), {
            'name': 'Nouvelle Catégorie'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après succès
        self.assertTrue(Category.objects.filter(name='Nouvelle Catégorie').exists())
    
    def test_ajouter_produit_requires_boutiquier(self):
        """Test que seul un boutiquier peut ajouter un produit"""
        # Sans connexion
        response = self.client.get(reverse('ajouter_produit'))
        self.assertEqual(response.status_code, 302)
        
        # Avec client normal
        self.client.login(username='client', password='pass123')
        response = self.client.get(reverse('ajouter_produit'))
        self.assertEqual(response.status_code, 302)


class CartViewsTest(TestCase):
    """Tests pour les vues du panier"""
    
    def setUp(self):
        """Créer des données de test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='cartuser',
            password='pass123'
        )
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            title='Test Product',
            price=50.00,
            description='Test',
            category=self.category,
            stock=10
        )
    
    def test_cart_view_requires_login(self):
        """Test que la vue panier nécessite une connexion"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login
    
    def test_cart_view_authenticated_user(self):
        """Test que l'utilisateur connecté peut voir son panier"""
        self.client.login(username='cartuser', password='pass123')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
    




class OrderViewsTest(TestCase):
    """Tests pour les vues de commande"""
    
    def setUp(self):
        """Créer des données de test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='orderuser',
            password='pass123',
            email='order@example.com'
        )
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            title='Order Product',
            price=25000.00,
            description='Test',
            category=self.category,
            stock=10
        )
    
    def test_checkout_view_requires_login(self):
        """Test que le checkout nécessite une connexion"""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login
    
    def test_checkout_view_authenticated_user(self):
        """Test que l'utilisateur connecté peut accéder au checkout"""
        self.client.login(username='orderuser', password='pass123')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
    
    def test_mes_commandes_requires_login(self):
        """Test que l'historique des commandes nécessite une connexion"""
        response = self.client.get(reverse('mes_commandes'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login
    
    def test_mes_commandes_authenticated_user(self):
        """Test que l'utilisateur connecté peut voir son historique"""
        self.client.login(username='orderuser', password='pass123')
        response = self.client.get(reverse('mes_commandes'))
        self.assertEqual(response.status_code, 200)
    
    def test_mes_commandes_shows_user_orders(self):
        """Test que l'historique affiche les commandes de l'utilisateur"""
        self.client.login(username='orderuser', password='pass123')
        
        # Créer une commande
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            nom='Test User',
            email='order@example.com',
            address='123 Test St',
            ville='Douala',
            pays='Cameroun',
            zipcode='12345'
        )
        
        response = self.client.get(reverse('mes_commandes'))
        self.assertContains(response, order.numero_commande)


class ProductDetailViewTest(TestCase):
    """Tests pour la vue détail du produit"""
    
    def setUp(self):
        """Créer un produit de test"""
        self.client = Client()
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            title='Detail Product',
            price=150.00,
            description='Detailed description',
            category=self.category,
            stock=8
        )
    
    def test_product_detail_view_status_code(self):
        """Test que la page détail du produit retourne 200"""
        response = self.client.get(reverse('detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_view_contains_product_info(self):
        """Test que la vue contient les informations du produit"""
        response = self.client.get(reverse('detail', args=[self.product.id]))
        self.assertContains(response, 'Detail Product')
        self.assertContains(response, '150')
        self.assertContains(response, 'Detailed description')
    
    def test_product_detail_view_404_for_invalid_id(self):
        """Test qu'un ID invalide retourne 404"""
        response = self.client.get(reverse('detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class CategoryProductsViewTest(TestCase):
    """Tests pour la vue produits par catégorie"""
    
    def setUp(self):
        """Créer des catégories et produits de test"""
        self.client = Client()
        self.category1 = Category.objects.create(name='Electronics')
        self.category2 = Category.objects.create(name='Books')
        
        # Produits de la catégorie 1
        Product.objects.create(
            title='Phone',
            price=500.00,
            description='Smartphone',
            category=self.category1,
            stock=5
        )
        Product.objects.create(
            title='Laptop',
            price=1000.00,
            description='Computer',
            category=self.category1,
            stock=3
        )
        
        # Produit de la catégorie 2
        Product.objects.create(
            title='Book',
            price=20.00,
            description='Novel',
            category=self.category2,
            stock=10
        )
    
    def test_category_products_view_status_code(self):
        """Test que la page catégorie retourne 200"""
        response = self.client.get(reverse('product_by_category', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
    

