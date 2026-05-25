#!/bin/bash
set -e

echo "🚀 Starting BryShop Application..."

# Attendre que la base de données PostgreSQL soit prête
echo "⏳ Waiting for PostgreSQL database..."
until pg_isready -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "✅ PostgreSQL is ready!"

# Exécuter les migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Créer un superuser si nécessaire (optionnel)
# echo "👤 Creating superuser..."
# python manage.py createsuperuser --noinput --username admin --email admin@bryshop.com || true

echo "✅ Application is ready!"

# Démarrer le serveur
exec "$@"
