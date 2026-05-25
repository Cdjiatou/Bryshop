"""
Configuration Django pour les tests
Utilise SQLite au lieu de MySQL pour faciliter l'exécution des tests
"""
from .settings import *

# Utiliser SQLite pour les tests (plus rapide et ne nécessite pas de serveur)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Base de données en mémoire pour les tests
    }
}

# Désactiver les migrations pour accélérer les tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# MIGRATION_MODULES = DisableMigrations()

# Désactiver le debug pour les tests
DEBUG = False

# Simplifier le hashage des mots de passe pour accélérer les tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Désactiver l'envoi d'emails pendant les tests
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
