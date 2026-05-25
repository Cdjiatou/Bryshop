# 🚀 Quick Start - BryShop CI/CD

## ⚡ Démarrage Rapide (5 minutes)

### 1. Tester Localement avec Docker

```bash
# Démarrer l'application avec PostgreSQL
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Accéder à l'application
# http://localhost:8000
```

### 2. Configurer les Secrets GitHub

Allez dans **Settings > Secrets and variables > Actions** :

```
DOCKER_USERNAME=votre-username
DOCKER_PASSWORD=votre-token-dockerhub
SONAR_TOKEN=votre-token-sonarcloud
SONAR_HOST_URL=https://sonarcloud.io
O2SWITCH_SSH_KEY=votre-clé-privée
O2SWITCH_HOST=ssh.o2switch.net
O2SWITCH_USER=votre-username
O2SWITCH_PATH=/home/user/bryshop
```

### 3. Pousser sur GitHub

```bash
git add .
git commit -m "feat: add CI/CD pipeline"
git push origin main
```

Le pipeline se déclenchera automatiquement ! 🎉

---

## 📊 Pipeline CI/CD

```
Push to GitHub
     ↓
Stage 1: Lint & Test (90 tests)
     ↓
Stage 2: SonarQube (Quality Gate ≥80%)
     ↓
Stage 3: Build & Push Docker Hub
     ↓
Stage 4: Deploy to O2Switch
     ↓
✅ Application déployée !
```

---

## 🔧 Commandes Utiles

```bash
# Tests
python manage.py test

# Build Docker
docker build -t bryshop:latest .

# Run Docker
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📚 Documentation Complète

- **CI_CD_SETUP_GUIDE.md** : Guide complet de configuration
- **DOCKER_README.md** : Documentation Docker détaillée
- **COMMENT_LANCER_LES_TESTS.md** : Guide des tests

---

## ✅ Checklist

- [ ] Docker installé et fonctionnel
- [ ] PostgreSQL configuré (BryshopDB)
- [ ] Tests passent (90 tests)
- [ ] Image Docker < 500 MB
- [ ] Secrets GitHub configurés
- [ ] SonarCloud configuré
- [ ] Pipeline GitHub Actions actif
- [ ] Déploiement O2Switch testé

---

**🎉 Prêt à déployer !**
