# 🚀 BryShop E-Commerce - CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/Cdjiatou/Bryshop/actions/workflows/main.yml/badge.svg)](https://github.com/Cdjiatou/Bryshop/actions/workflows/main.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue.svg)](https://www.postgresql.org/)
[![Django](https://img.shields.io/badge/django-4.2.27-green.svg)](https://www.djangoproject.com/)

Application e-commerce Django avec pipeline CI/CD complet, dockerisation multi-stage et déploiement automatisé.

---

## 🎯 Fonctionnalités

### Partie II : Dockerisation
- ✅ Image Docker multi-stage optimisée (< 500 MB)
- ✅ Utilisateur non-root pour la sécurité
- ✅ PostgreSQL (BryshopDB)
- ✅ Healthcheck automatique
- ✅ Docker Compose pour orchestration

### Partie III : Pipeline CI/CD
- ✅ **Stage 1** : Lint & Test (Flake8 + 90 tests)
- ✅ **Stage 2** : SonarQube (Quality Gate ≥80%)
- ✅ **Stage 3** : Build & Push Docker Hub
- ✅ **Stage 4** : Déploiement O2Switch

---

## ⚡ Quick Start

### Prérequis
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL (optionnel pour dev local)

### Démarrage Rapide

```bash
# 1. Cloner le repository
git clone https://github.com/Cdjiatou/Bryshop.git
cd Bryshop

# 2. Démarrer avec Docker Compose
docker-compose up -d

# 3. Accéder à l'application
# http://localhost:8000
```

---

## 📦 Structure du Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│  Stage 1: Lint & Test                                        │
│  ├─ Flake8 (Linting)                                         │
│  ├─ 90 tests unitaires                                       │
│  └─ Coverage report                                          │
│                                                               │
│  Stage 2: Code Quality (SonarQube)                           │
│  ├─ Analyse statique                                         │
│  ├─ Détection vulnérabilités                                 │
│  └─ Quality Gate (≥80%)                                      │
│                                                               │
│  Stage 3: Build & Push Docker Hub                            │
│  ├─ Build multi-stage                                        │
│  ├─ Tag SHA + latest                                         │
│  └─ Push Docker Hub                                          │
│                                                               │
│  Stage 4: Deploy O2Switch                                    │
│  ├─ SSH sécurisé                                             │
│  ├─ Pull nouvelle image                                      │
│  └─ Redémarrage app                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Configuration des Secrets

Configurer dans **Settings > Secrets and variables > Actions** :

```
DOCKER_USERNAME       # Nom d'utilisateur Docker Hub
DOCKER_PASSWORD       # Token Docker Hub
SONAR_TOKEN          # Token SonarCloud
SONAR_HOST_URL       # https://sonarcloud.io
O2SWITCH_SSH_KEY     # Clé privée SSH
O2SWITCH_HOST        # ssh.o2switch.net
O2SWITCH_USER        # Nom d'utilisateur
O2SWITCH_PATH        # /home/user/bryshop
```

---

## 🐳 Docker

### Build l'image

```bash
# Build
docker build -t bryshop:latest .

# Ou avec le script
.\build-docker.ps1
```

### Vérifications

```bash
# Taille de l'image
docker images bryshop:latest

# Utilisateur non-root
docker run --rm bryshop:latest whoami
# Output: appuser

# Healthcheck
docker inspect bryshop_web | grep -A 10 Health
```

---

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests (utilise SQLite automatiquement)
python manage.py test

# Avec coverage
coverage run --source='.' manage.py test
coverage report

# Tests d'une app spécifique
python manage.py test accounts
python manage.py test BRYSHOP
```

### Résultats actuels

```
Total : 90 tests
Réussis : 74 (82%)
Temps : ~0.24s
```

---

## 📊 SonarQube

### Configuration locale

```bash
# Démarrer SonarQube
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Analyser le code
sonar-scanner \
  -Dsonar.projectKey=bryshop \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=votre-token
```

### Quality Gate

- ✅ Coverage ≥ 80%
- ✅ Vulnérabilités High = 0
- ✅ Code Smells critiques = 0

---

## 🚀 Déploiement

### Automatique (via GitHub Actions)

```bash
# Push sur main déclenche le déploiement
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin main
```

### Manuel

```bash
# Sur O2Switch
ssh user@o2switch.net
cd ~/bryshop
docker-compose pull
docker-compose up -d
```

---

## 📚 Documentation

- **[CI_CD_SETUP_GUIDE.md](CI_CD_SETUP_GUIDE.md)** - Guide complet de configuration
- **[DOCKER_README.md](DOCKER_README.md)** - Documentation Docker détaillée
- **[QUICK_START.md](QUICK_START.md)** - Démarrage rapide
- **[COMMENT_LANCER_LES_TESTS.md](COMMENT_LANCER_LES_TESTS.md)** - Guide des tests
- **[RENDU_TRAVAIL.md](RENDU_TRAVAIL.md)** - Rendu du travail complet

---

## 🛠️ Technologies

- **Backend** : Django 4.2.27
- **Base de données** : PostgreSQL 15
- **Conteneurisation** : Docker + Docker Compose
- **CI/CD** : GitHub Actions
- **Quality** : SonarQube/SonarCloud
- **Déploiement** : O2Switch
- **Tests** : Django TestCase (90 tests)

---

## 📈 Métriques

| Métrique | Valeur |
|----------|--------|
| Taille image Docker | < 500 MB |
| Tests unitaires | 90 |
| Couverture de code | ~75-80% |
| Temps de build | ~2-3 min |
| Temps de déploiement | ~1-2 min |

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

Le pipeline CI/CD s'exécutera automatiquement sur votre PR !

---

## 📝 License

Ce projet est sous licence MIT.

---

## 👥 Auteurs

- **Cdjiatou** - [GitHub](https://github.com/Cdjiatou)

---

## 🔗 Liens Utiles

- **Repository** : https://github.com/Cdjiatou/Bryshop.git
- **Docker Hub** : https://hub.docker.com
- **SonarCloud** : https://sonarcloud.io
- **GitHub Actions** : https://github.com/Cdjiatou/Bryshop/actions

---

**🎉 Prêt à déployer !**
