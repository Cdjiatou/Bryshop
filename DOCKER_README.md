# 🐳 Guide de Dockerisation - BryShop E-Commerce

## 📋 Vue d'ensemble

Ce projet utilise Docker avec une approche **multi-stage build** pour créer une image optimisée et sécurisée.

### ✨ Caractéristiques

- ✅ **Multi-stage build** : Réduction de la taille de l'image (~70% plus petite)
- ✅ **Utilisateur non-root** : Sécurité renforcée
- ✅ **Image optimisée** : Basée sur `python:3.11-slim`
- ✅ **Healthcheck** : Surveillance automatique de l'application
- ✅ **Cache Docker** : Build plus rapide grâce au cache des layers

## 🚀 Démarrage Rapide

### Option 1 : Avec Docker Compose (Recommandé)

```bash
# Démarrer tous les services (DB + Application)
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

L'application sera accessible sur : http://localhost:8000

### Option 2 : Build et Run Manuel

```bash
# 1. Builder l'image
docker build -t bryshop:latest .

# 2. Créer un réseau Docker
docker network create bryshop_network

# 3. Démarrer MySQL
docker run -d \
  --name bryshop_db \
  --network bryshop_network \
  -e MYSQL_DATABASE=ecommerce \
  -e MYSQL_ROOT_PASSWORD=root \
  -p 3306:3306 \
  mysql:8.0

# 4. Attendre que MySQL soit prêt (environ 30 secondes)
sleep 30

# 5. Démarrer l'application
docker run -d \
  --name bryshop_web \
  --network bryshop_network \
  -e DATABASE_HOST=bryshop_db \
  -e DATABASE_PORT=3306 \
  -e DATABASE_NAME=ecommerce \
  -e DATABASE_USER=root \
  -e DATABASE_PASSWORD=root \
  -p 8000:8000 \
  bryshop:latest
```

## 📦 Structure du Dockerfile

### Stage 1 : Builder
- Installation des dépendances de compilation
- Création d'un environnement virtuel Python
- Installation des packages Python

### Stage 2 : Runtime
- Image finale légère (sans outils de compilation)
- Copie de l'environnement virtuel depuis le builder
- Création d'un utilisateur non-root
- Configuration de l'application

## 🔧 Commandes Utiles

### Gestion des conteneurs

```bash
# Voir les conteneurs en cours d'exécution
docker ps

# Voir tous les conteneurs
docker ps -a

# Voir les logs d'un conteneur
docker logs bryshop_web
docker logs -f bryshop_web  # Suivre les logs en temps réel

# Accéder au shell d'un conteneur
docker exec -it bryshop_web bash

# Redémarrer un conteneur
docker restart bryshop_web

# Arrêter un conteneur
docker stop bryshop_web

# Supprimer un conteneur
docker rm bryshop_web
```

### Gestion des images

```bash
# Lister les images
docker images

# Supprimer une image
docker rmi bryshop:latest

# Nettoyer les images non utilisées
docker image prune -a

# Voir la taille des layers
docker history bryshop:latest
```

### Commandes Django dans le conteneur

```bash
# Exécuter les migrations
docker exec bryshop_web python manage.py migrate

# Créer un superuser
docker exec -it bryshop_web python manage.py createsuperuser

# Collecter les fichiers statiques
docker exec bryshop_web python manage.py collectstatic --noinput

# Exécuter les tests
docker exec bryshop_web python manage.py test

# Accéder au shell Django
docker exec -it bryshop_web python manage.py shell
```

## 📊 Optimisations Appliquées

### 1. Multi-stage Build
- **Avant** : ~1.2 GB
- **Après** : ~350 MB
- **Gain** : ~70% de réduction

### 2. Utilisateur Non-Root
```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### 3. Cache Docker
Les dépendances sont installées avant de copier le code source, permettant de réutiliser le cache lors des builds suivants.

### 4. .dockerignore
Exclusion des fichiers inutiles pour réduire le contexte de build.

## 🔒 Sécurité

### Bonnes Pratiques Appliquées

1. ✅ **Utilisateur non-root** : L'application s'exécute avec un utilisateur limité
2. ✅ **Image de base officielle** : `python:3.11-slim` maintenue par Docker
3. ✅ **Pas de secrets dans l'image** : Utilisation de variables d'environnement
4. ✅ **Healthcheck** : Détection automatique des problèmes
5. ✅ **Dépendances minimales** : Seulement ce qui est nécessaire en runtime

### Scanner l'image pour les vulnérabilités

```bash
# Avec Docker Scout (intégré à Docker Desktop)
docker scout cves bryshop:latest

# Avec Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image bryshop:latest
```

## 🌐 Variables d'Environnement

Créer un fichier `.env` basé sur `.env.example` :

```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

### Variables Principales

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DEBUG` | Mode debug Django | `False` |
| `SECRET_KEY` | Clé secrète Django | `your-secret-key` |
| `DATABASE_HOST` | Hôte de la base de données | `db` |
| `DATABASE_NAME` | Nom de la base de données | `ecommerce` |
| `DATABASE_USER` | Utilisateur DB | `bryshop` |
| `DATABASE_PASSWORD` | Mot de passe DB | `bryshop123` |

## 🐛 Dépannage

### Problème : Le conteneur ne démarre pas

```bash
# Voir les logs détaillés
docker logs bryshop_web

# Vérifier le statut
docker ps -a
```

### Problème : Erreur de connexion à la base de données

```bash
# Vérifier que MySQL est prêt
docker exec bryshop_db mysqladmin ping -h localhost

# Vérifier les variables d'environnement
docker exec bryshop_web env | grep DATABASE
```

### Problème : Les fichiers statiques ne se chargent pas

```bash
# Recollect les fichiers statiques
docker exec bryshop_web python manage.py collectstatic --noinput
```

### Problème : L'image est trop grande

```bash
# Analyser les layers
docker history bryshop:latest

# Vérifier le .dockerignore
cat .dockerignore
```

## 📈 Monitoring

### Healthcheck

Le Dockerfile inclut un healthcheck qui vérifie toutes les 30 secondes si l'application répond :

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000', timeout=5)" || exit 1
```

### Voir le statut de santé

```bash
docker ps
# La colonne STATUS affiche "healthy" ou "unhealthy"

# Inspecter le healthcheck
docker inspect --format='{{json .State.Health}}' bryshop_web | jq
```

## 🚢 Déploiement en Production

### 1. Build pour production

```bash
docker build -t bryshop:v1.0.0 .
```

### 2. Tag pour Docker Hub

```bash
docker tag bryshop:v1.0.0 votre-username/bryshop:v1.0.0
docker tag bryshop:v1.0.0 votre-username/bryshop:latest
```

### 3. Push vers Docker Hub

```bash
docker login
docker push votre-username/bryshop:v1.0.0
docker push votre-username/bryshop:latest
```

### 4. Pull et Run sur le serveur

```bash
docker pull votre-username/bryshop:latest
docker run -d \
  --name bryshop_web \
  -p 8000:8000 \
  -e DATABASE_HOST=your-db-host \
  -e DATABASE_NAME=ecommerce \
  -e DATABASE_USER=your-user \
  -e DATABASE_PASSWORD=your-password \
  votre-username/bryshop:latest
```

## 📚 Ressources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

---

**Note** : Ce Dockerfile est optimisé pour la production. Pour le développement local, vous pouvez continuer à utiliser `python manage.py runserver`.
