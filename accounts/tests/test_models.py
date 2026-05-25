from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Client, Notification

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Tests pour le modèle CustomUser"""
    
    def setUp(self):
        """Créer un utilisateur de test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            telephone='+237612345678',
            ville='Douala',
            pays='Cameroun',
            sexe='M',
            role='client'
        )
    
    def test_user_creation(self):
        """Test que l'utilisateur est créé correctement"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.telephone, '+237612345678')
        self.assertEqual(self.user.ville, 'Douala')
        self.assertEqual(self.user.pays, 'Cameroun')
        self.assertEqual(self.user.sexe, 'M')
        self.assertEqual(self.user.role, 'client')
    
    def test_user_password_is_hashed(self):
        """Test que le mot de passe est hashé"""
        self.assertNotEqual(self.user.password, 'testpass123')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_user_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.user), 'testuser')
    
    def test_user_role_choices(self):
        """Test des différents rôles"""
        # Client
        client_user = User.objects.create_user(
            username='client',
            password='pass123',
            role='client'
        )
        self.assertEqual(client_user.role, 'client')
        
        # Boutiquier
        boutiquier_user = User.objects.create_user(
            username='boutiquier',
            password='pass123',
            role='boutiquier'
        )
        self.assertEqual(boutiquier_user.role, 'boutiquier')
        
        # Admin
        admin_user = User.objects.create_user(
            username='admin',
            password='pass123',
            role='admin'
        )
        self.assertEqual(admin_user.role, 'admin')
    
    def test_user_sexe_choices(self):
        """Test des choix de sexe"""
        male_user = User.objects.create_user(
            username='male',
            password='pass123',
            sexe='M'
        )
        self.assertEqual(male_user.sexe, 'M')
        
        female_user = User.objects.create_user(
            username='female',
            password='pass123',
            sexe='F'
        )
        self.assertEqual(female_user.sexe, 'F')


class ClientModelTest(TestCase):
    """Tests pour le modèle Client"""
    
    def setUp(self):
        """Créer un utilisateur et un client de test"""
        self.user = User.objects.create_user(
            username='clientuser',
            email='client@example.com',
            password='pass123',
            first_name='Jean',
            last_name='Dupont'
        )
        
        self.client_profile = Client.objects.create(
            user=self.user,
            sexe='Homme',
            telephone='+237612345678',
            ville='Yaoundé',
            pays='Cameroun',
            is_shop_owner=False
        )
    
    def test_client_creation(self):
        """Test que le profil client est créé correctement"""
        self.assertEqual(self.client_profile.user, self.user)
        self.assertEqual(self.client_profile.sexe, 'Homme')
        self.assertEqual(self.client_profile.telephone, '+237612345678')
        self.assertEqual(self.client_profile.ville, 'Yaoundé')
        self.assertEqual(self.client_profile.pays, 'Cameroun')
        self.assertFalse(self.client_profile.is_shop_owner)
    
    def test_client_str_method(self):
        """Test de la méthode __str__"""
        self.assertEqual(str(self.client_profile), 'Jean Dupont')
    
    def test_client_one_to_one_relation(self):
        """Test de la relation OneToOne avec User"""
        self.assertEqual(self.user.client, self.client_profile)
    
    def test_est_boutiquier_property_false(self):
        """Test que est_boutiquier retourne False pour un client normal"""
        self.assertFalse(self.client_profile.est_boutiquier)
    
    def test_est_boutiquier_property_true_shop_owner(self):
        """Test que est_boutiquier retourne True pour un propriétaire de boutique"""
        self.client_profile.is_shop_owner = True
        self.client_profile.save()
        self.assertTrue(self.client_profile.est_boutiquier)
    
    def test_est_boutiquier_property_true_superuser(self):
        """Test que est_boutiquier retourne True pour un superuser"""
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        admin_client = Client.objects.create(
            user=superuser,
            is_shop_owner=False
        )
        self.assertTrue(admin_client.est_boutiquier)


class NotificationModelTest(TestCase):
    """Tests pour le modèle Notification"""
    
    def setUp(self):
        """Créer un utilisateur et une notification de test"""
        self.user = User.objects.create_user(
            username='notifuser',
            password='pass123'
        )
        
        self.notification = Notification.objects.create(
            user=self.user,
            message='Votre commande a été expédiée',
            url='/orders/123/',
            is_read=False
        )
    
    def test_notification_creation(self):
        """Test que la notification est créée correctement"""
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, 'Votre commande a été expédiée')
        self.assertEqual(self.notification.url, '/orders/123/')
        self.assertFalse(self.notification.is_read)
    

    
    def test_notification_ordering(self):
        """Test que les notifications sont ordonnées par date décroissante"""
        notif1 = Notification.objects.create(
            user=self.user,
            message='Première notification'
        )
        notif2 = Notification.objects.create(
            user=self.user,
            message='Deuxième notification'
        )
        
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0], notif2)
        self.assertEqual(notifications[1], notif1)
    
    def test_notification_mark_as_read(self):
        """Test du marquage d'une notification comme lue"""
        self.assertFalse(self.notification.is_read)
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(self.notification.is_read)
    
    def test_notification_related_name(self):
        """Test du related_name pour accéder aux notifications d'un utilisateur"""
        Notification.objects.create(
            user=self.user,
            message='Notification 2'
        )
        
        user_notifications = self.user.notifications.all()
        self.assertEqual(user_notifications.count(), 2)
