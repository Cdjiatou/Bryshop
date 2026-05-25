from django.test import TestCase
from BRYSHOP.forms import CategoryForm, ProductForm
from BRYSHOP.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile

class CategoryFormTest(TestCase):
    """Tests pour le formulaire CategoryForm"""
    
    def test_category_form_valid(self):
        """Test qu'un formulaire valide est accepté"""
        form_data = {
            'name': 'Électronique'
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_category_form_empty_name(self):
        """Test qu'un nom vide est rejeté"""
        form_data = {
            'name': ''
        }
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_category_form_save(self):
        """Test que le formulaire sauvegarde correctement"""
        form_data = {
            'name': 'Vêtements'
        }
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertEqual(category.name, 'Vêtements')
        self.assertEqual(Category.objects.count(), 1)


class ProductFormTest(TestCase):
    """Tests pour le formulaire ProductForm"""
    
    def setUp(self):
        """Créer une catégorie pour les tests"""
        self.category = Category.objects.create(name='Smartphones')
    

    
    def test_product_form_empty_title(self):
        """Test qu'un titre vide est rejeté"""
        form_data = {
            'title': '',
            'price': 999.99,
            'description': 'Description',
            'category': self.category.id,
            'stock': 10
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_product_form_negative_price(self):
        """Test qu'un prix négatif est rejeté"""
        form_data = {
            'title': 'Test Product',
            'price': -50.00,
            'description': 'Description',
            'category': self.category.id,
            'stock': 10
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_product_form_empty_description(self):
        """Test qu'une description vide est rejetée"""
        form_data = {
            'title': 'Test Product',
            'price': 100.00,
            'description': '',
            'category': self.category.id,
            'stock': 10
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
    
    def test_product_form_no_category(self):
        """Test qu'une catégorie est requise"""
        form_data = {
            'title': 'Test Product',
            'price': 100.00,
            'description': 'Description',
            'stock': 10
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
    
    def test_product_form_negative_stock(self):
        """Test qu'un stock négatif est rejeté"""
        form_data = {
            'title': 'Test Product',
            'price': 100.00,
            'description': 'Description',
            'category': self.category.id,
            'stock': -5
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_product_form_fields(self):
        """Test que tous les champs requis sont présents"""
        form = ProductForm()
        expected_fields = ['title', 'price', 'description', 'category', 'image', 'stock']
        for field in expected_fields:
            self.assertIn(field, form.fields)
