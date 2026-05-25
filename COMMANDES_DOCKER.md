# 🐳 Commandes Docker - Guide Rapide BryShop

## 🚀 Démarrage Rapide (3 commandes)

```powershell
# 1. Builder l'image
docker-compose build

# 2. Démarrer tous les services
docker-compose up -d

# 3. Vérifier que tout fonctionne
docker-compose ps
```

**Accès** : http://localhost:8000

---

## 📋 Commandes Essentielles

### **Build**

```powershell
# Build simple
docker build -t bryshop:latest .

# Build avec docker-compose
docker-compose build

# Build sans cache (si problèmes)
docker-compose build --no-cache

# Build avec le script PowerShell
.\build-docker.ps1
```

---

### **Démarrage**

```powershell
# Démarrer tous les services
docker-compose up -d

# Démarrer avec rebuild
docker-compose up -d --build

# Démarrer et voir les logs
docker-compose up

# Avec le script PowerShell
.\start-bryshop.ps1

# Avec rebuild
.\start-bryshop.ps1 -Build

# Avec nettoyage complet
.\start-bryshop.ps1 -Clean -Build
```

---

### **Arrêt**

```powershell
# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker-compose down -v

# Arrêter un service spécifique
docker-compose stop web
```

---

### **Logs**

```powershell
# Voir tous les logs
docker-compose logs

# Suivre les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f web

# Dernières 50 lignes
docker-compose logs --tail=50 web

# Avec le script PowerShell
.\start-bryshop.ps1 -Logs
```

---

### **État et Monitoring**

```powershell
# Voir l'état des services
docker-compose ps

# Voir les processus dans un conteneur
docker-compose top web

# Statistiques en temps réel
docker stats

# Inspecter un conteneur
docker inspect bryshop_web
```

---

### **Exécution de Commandes**

```powershell
# Entrer dans le conteneur web
docker-compose exec web bash

# Exécuter une commande Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Exécuter les tests
docker-compose exec web python manage.py test
```

---

### **Redémarrage**

```powershell
# Redémarrer tous les services
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart web

# Redémarrer avec rebuild
docker-compose down
docker-compose up -d --build
```

---

## 🧪 Tests et Vérification

### **Test du Build**

```powershell
# Tester le build complet
.\test-docker-build.ps1

# Vérifier la taille de l'image
docker images bryshop
```

---

### **Test de l'Application**

```powershell
# Démarrer l'application
docker-compose up -d

# Attendre 15 secondes
Start-Sleep -Seconds 15

# Tester l'endpoint
Invoke-WebRequest -Uri http://localhost:8000

# Ou avec curl
curl http://localhost:8000
```

---

### **Test de la Base de Données**

```powershell
# Entrer dans le conteneur PostgreSQL
docker-compose exec db psql -U postgres -d BryshopDB

# Lister les tables
\dt

# Quitter
\q
```

---

## 🧹 Nettoyage

### **Nettoyage Léger**

```powershell
# Supprimer les conteneurs arrêtés
docker container prune

# Supprimer les images non utilisées
docker image prune

# Supprimer les volumes non utilisés
docker volume prune
```

---

### **Nettoyage Complet** (⚠️ Attention)

```powershell
# Arrêter et supprimer tout (BryShop)
docker-compose down -v

# Supprimer toutes les images BryShop
docker rmi $(docker images bryshop -q)

# Nettoyage complet de Docker (TOUT)
docker system prune -a --volumes
```

---

## 🔍 Dépannage

### **Problème : Port déjà utilisé**

```powershell
# Trouver le processus sur le port 8000
netstat -ano | findstr :8000

# Arrêter les conteneurs
docker-compose down

# Changer le port dans docker-compose.yml
# ports:
#   - "8001:8000"  # Au lieu de 8000:8000
```

---

### **Problème : Conteneur ne démarre pas**

```powershell
# Voir les logs d'erreur
docker-compose logs web

# Voir les logs complets
docker logs bryshop_web

# Redémarrer avec rebuild
docker-compose down
docker-compose up -d --build
```

---

### **Problème : Base de données non accessible**

```powershell
# Vérifier que PostgreSQL est démarré
docker-compose ps db

# Voir les logs de la base de données
docker-compose logs db

# Redémarrer la base de données
docker-compose restart db

# Attendre que la base soit prête
docker-compose exec db pg_isready -U postgres
```

---

### **Problème : Migrations non appliquées**

```powershell
# Appliquer les migrations manuellement
docker-compose exec web python manage.py migrate

# Voir l'état des migrations
docker-compose exec web python manage.py showmigrations
```

---

### **Problème : Fichiers statiques manquants**

```powershell
# Collecter les fichiers statiques
docker-compose exec web python manage.py collectstatic --noinput

# Vérifier les fichiers
docker-compose exec web ls -la /app/staticfiles
```

---

## 📊 Monitoring et Observabilité

### **Accès aux Dashboards**

- **Application** : http://localhost:8000
- **Kibana** : http://localhost:5601
- **Grafana** : http://localhost:3000 (admin/admin)
- **Prometheus** : http://localhost:9090

---

### **Vérifier les Services de Monitoring**

```powershell
# Vérifier Elasticsearch
Invoke-WebRequest -Uri http://localhost:9200

# Vérifier Prometheus
Invoke-WebRequest -Uri http://localhost:9090

# Voir les logs Kibana
docker-compose logs kibana

# Voir les logs Grafana
docker-compose logs grafana
```

---

## 🚀 Workflow de Développement

### **Workflow Standard**

```powershell
# 1. Faire des modifications dans le code
# ...

# 2. Rebuild et redémarrer
docker-compose up -d --build

# 3. Voir les logs
docker-compose logs -f web

# 4. Tester
Invoke-WebRequest -Uri http://localhost:8000

# 5. Si OK, commit et push
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin develop
```

---

### **Workflow avec Tests**

```powershell
# 1. Exécuter les tests dans le conteneur
docker-compose exec web python manage.py test

# 2. Voir la couverture
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report

# 3. Si tests OK, commit
git add .
git commit -m "test: ajout de tests"
git push
```

---

## 🔐 Push vers Docker Hub

```powershell
# 1. Se connecter à Docker Hub
docker login

# 2. Tagger l'image
docker tag bryshop:latest VOTRE_USERNAME/bryshop:latest

# 3. Pousser l'image
docker push VOTRE_USERNAME/bryshop:latest

# 4. Vérifier sur Docker Hub
# https://hub.docker.com/r/VOTRE_USERNAME/bryshop
```

---

## 📝 Commandes Utiles Supplémentaires

```powershell
# Voir la taille des images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Voir l'utilisation disque de Docker
docker system df

# Voir les réseaux Docker
docker network ls

# Voir les volumes Docker
docker volume ls

# Inspecter un volume
docker volume inspect bryshop_postgres_data

# Sauvegarder une image
docker save bryshop:latest -o bryshop-backup.tar

# Charger une image
docker load -i bryshop-backup.tar
```

---

## ✅ Checklist Avant Production

- [ ] Build réussi sans erreur
- [ ] Taille de l'image < 500 MB
- [ ] Tous les tests passent
- [ ] Migrations appliquées
- [ ] Fichiers statiques collectés
- [ ] Healthcheck fonctionne
- [ ] Logs accessibles
- [ ] Variables d'environnement configurées
- [ ] Secrets configurés dans GitHub
- [ ] Pipeline CI/CD testé

---

## 🆘 Aide

Si vous rencontrez des problèmes :

1. Vérifiez les logs : `docker-compose logs -f`
2. Vérifiez l'état : `docker-compose ps`
3. Redémarrez : `docker-compose restart`
4. Rebuild : `docker-compose up -d --build`
5. Nettoyage : `docker-compose down -v && docker-compose up -d --build`

---

**Documentation complète** : Voir `GUIDE_BUILD_DOCKER.md`
