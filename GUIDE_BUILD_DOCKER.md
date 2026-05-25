# 🐳 Guide de Build des Images Docker - BryShop

## Prérequis

Avant de commencer, assurez-vous d'avoir :
- ✅ Docker Desktop installé et démarré
- ✅ Git installé (pour les métadonnées de version)
- ✅ Connexion Internet (pour télécharger les images de base)

## 📋 Méthodes de Build

### **Méthode 1 : Build Simple (Recommandé pour débuter)**

```bash
# Build l'image avec le tag 'latest'
docker build -t bryshop:latest .
```

**Temps estimé** : 5-10 minutes (première fois)

---

### **Méthode 2 : Build avec Script (Recommandé)**

#### Sur Windows (PowerShell) :
```powershell
# Donner les permissions d'exécution (première fois seulement)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Builder l'image
.\build-docker.ps1

# Ou avec une version spécifique
.\build-docker.ps1 -Version "v1.0.0"
```

#### Sur Linux/Mac (Bash) :
```bash
# Donner les permissions d'exécution (première fois seulement)
chmod +x build-docker.sh

# Builder l'image
./build-docker.sh

# Ou avec une version spécifique
./build-docker.sh v1.0.0
```

---

### **Méthode 3 : Build avec Docker Compose (Recommandé pour production)**

```bash
# Build toutes les images définies dans docker-compose.yml
docker-compose build

# Build avec cache désactivé (build propre)
docker-compose build --no-cache

# Build et démarrer tous les services
docker-compose up -d --build
```

---

## 🚀 Démarrer l'Application

### **Option A : Avec Docker Compose (Recommandé)**

```bash
# Démarrer tous les services (web + db + monitoring)
docker-compose up -d

# Vérifier que les conteneurs sont démarrés
docker-compose ps

# Voir les logs
docker-compose logs -f web

# Arrêter tous les services
docker-compose down
```

L'application sera accessible sur : **http://localhost:8000**

---

### **Option B : Avec Docker seul (sans base de données)**

```bash
# Démarrer uniquement l'application web
docker run -d \
  --name bryshop_web \
  -p 8000:8000 \
  -e DEBUG=True \
  -e DATABASE_HOST=host.docker.internal \
  -e DATABASE_NAME=BryshopDB \
  -e DATABASE_USER=postgres \
  -e DATABASE_PASSWORD= \
  bryshop:latest

# Voir les logs
docker logs -f bryshop_web

# Arrêter le conteneur
docker stop bryshop_web
docker rm bryshop_web
```

---

## 🔍 Vérification du Build

### **1. Vérifier que l'image est créée**

```bash
docker images bryshop
```

**Résultat attendu** :
```
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
bryshop      latest    abc123def456   2 minutes ago    450MB
```

✅ **Taille cible** : < 500 MB

---

### **2. Inspecter l'image**

```bash
# Voir les détails de l'image
docker inspect bryshop:latest

# Voir l'historique des layers
docker history bryshop:latest
```

---

### **3. Tester l'image localement**

```bash
# Démarrer avec docker-compose
docker-compose up -d

# Attendre 10 secondes que l'application démarre
Start-Sleep -Seconds 10  # PowerShell
# sleep 10  # Bash

# Tester l'endpoint de santé
curl http://localhost:8000

# Ou avec PowerShell
Invoke-WebRequest -Uri http://localhost:8000
```

---

## 🐛 Dépannage

### **Problème 1 : "Cannot connect to Docker daemon"**

**Solution** :
- Vérifiez que Docker Desktop est démarré
- Sur Windows : Redémarrez Docker Desktop
- Sur Linux : `sudo systemctl start docker`

---

### **Problème 2 : "Build failed" ou erreurs de dépendances**

**Solution** :
```bash
# Build sans cache
docker build --no-cache -t bryshop:latest .

# Ou avec docker-compose
docker-compose build --no-cache
```

---

### **Problème 3 : "Port 8000 already in use"**

**Solution** :
```bash
# Trouver le processus qui utilise le port
netstat -ano | findstr :8000  # Windows
# lsof -i :8000  # Linux/Mac

# Arrêter les conteneurs existants
docker-compose down
docker stop $(docker ps -q)  # Arrêter tous les conteneurs
```

---

### **Problème 4 : L'image est trop grande (> 500 MB)**

**Solution** :
- Vérifiez que le multi-stage build fonctionne correctement
- Vérifiez que `.dockerignore` est présent et configuré
- Nettoyez les caches Docker :

```bash
# Nettoyer les images non utilisées
docker image prune -a

# Nettoyer tout (attention : supprime tout)
docker system prune -a --volumes
```

---

## 📊 Commandes Utiles

### **Gestion des images**

```bash
# Lister toutes les images
docker images

# Supprimer une image
docker rmi bryshop:latest

# Supprimer toutes les images non utilisées
docker image prune -a
```

---

### **Gestion des conteneurs**

```bash
# Lister les conteneurs en cours d'exécution
docker ps

# Lister tous les conteneurs (y compris arrêtés)
docker ps -a

# Voir les logs d'un conteneur
docker logs bryshop_web
docker logs -f bryshop_web  # Suivre les logs en temps réel

# Entrer dans un conteneur
docker exec -it bryshop_web bash

# Arrêter un conteneur
docker stop bryshop_web

# Supprimer un conteneur
docker rm bryshop_web
```

---

### **Gestion avec Docker Compose**

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Voir les logs de tous les services
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f web

# Redémarrer un service
docker-compose restart web

# Reconstruire et redémarrer
docker-compose up -d --build
```

---

## 🔐 Push vers Docker Hub (Optionnel)

Si vous voulez pousser votre image vers Docker Hub :

```bash
# 1. Se connecter à Docker Hub
docker login

# 2. Tagger l'image avec votre nom d'utilisateur
docker tag bryshop:latest VOTRE_USERNAME/bryshop:latest

# 3. Pousser l'image
docker push VOTRE_USERNAME/bryshop:latest
```

---

## 📈 Monitoring et Observabilité

Après avoir démarré avec `docker-compose up -d`, vous aurez accès à :

- **Application Django** : http://localhost:8000
- **Kibana (Logs)** : http://localhost:5601
- **Grafana (Métriques)** : http://localhost:3000 (admin/admin)
- **Prometheus** : http://localhost:9090

---

## ✅ Checklist de Vérification

Avant de considérer le build comme réussi :

- [ ] L'image est créée avec succès (`docker images bryshop`)
- [ ] La taille de l'image est < 500 MB
- [ ] Le conteneur démarre sans erreur (`docker-compose up -d`)
- [ ] L'application est accessible sur http://localhost:8000
- [ ] Les migrations de base de données s'exécutent correctement
- [ ] Les fichiers statiques sont collectés
- [ ] Le healthcheck passe (vérifier avec `docker ps`)

---

## 🎯 Prochaines Étapes

Une fois le build local réussi :

1. ✅ Commitez vos changements sur Git
2. ✅ Poussez vers GitHub (branche `develop` ou `main`)
3. ✅ Le pipeline CI/CD GitHub Actions se déclenchera automatiquement
4. ✅ L'image sera buildée et poussée vers Docker Hub
5. ✅ Le déploiement sur O2Switch se fera automatiquement (si branche `main`)

---

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

---

**Besoin d'aide ?** Consultez les logs avec `docker-compose logs -f` ou `docker logs bryshop_web`
