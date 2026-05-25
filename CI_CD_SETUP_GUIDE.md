# 🚀 Guide de Configuration CI/CD - BryShop

Ce guide vous explique comment configurer le pipeline CI/CD complet pour BryShop (Parties II et III).

---

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Partie II : Dockerisation](#partie-ii--dockerisation)
3. [Partie III : Pipeline CI/CD](#partie-iii--pipeline-cicd)
4. [Configuration des Secrets](#configuration-des-secrets)
5. [Configuration SonarQube](#configuration-sonarqube)
6. [Déploiement O2Switch](#déploiement-o2switch)
7. [Tests et Validation](#tests-et-validation)

---

## 🔧 Prérequis

### Outils Nécessaires

- ✅ Docker Desktop installé
- ✅ Compte GitHub
- ✅ Compte Docker Hub
- ✅ Compte SonarCloud (ou instance SonarQube)
- ✅ Accès SSH à O2Switch

### Vérifications

```bash
# Vérifier Docker
docker --version
docker-compose --version

# Vérifier Git
git --version

# Vérifier Python
python --version
```

---

## 🐳 PARTIE II : Dockerisation

### Étape 1 : Configuration PostgreSQL Locale (Optionnel)

Si vous voulez tester localement sans Docker :

```bash
# Installer PostgreSQL
# Windows: Télécharger depuis https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Créer la base de données
psql -U postgres
CREATE DATABASE "BryshopDB";
CREATE USER bryshop WITH PASSWORD 'bryshop123';
GRANT ALL PRIVILEGES ON DATABASE "BryshopDB" TO bryshop;
\q
```

### Étape 2 : Installer les Dépendances Python

```bash
pip install -r requirement.txt
```

### Étape 3 : Tester l'Application Localement

```bash
# Exécuter les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Étape 4 : Build de l'Image Docker

```bash
# Build l'image
docker build -t bryshop:latest .

# Ou utiliser le script PowerShell
.\build-docker.ps1

# Vérifier l'image
docker images bryshop
```

### Étape 5 : Tester avec Docker Compose

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Vérifier que tout fonctionne
curl http://localhost:8000

# Arrêter les services
docker-compose down
```

### ✅ Validation Partie II

- [ ] Image Docker construite avec succès
- [ ] Taille de l'image < 500 MB
- [ ] Application démarre sans erreur
- [ ] Utilisateur non-root vérifié : `docker exec bryshop_web whoami`
- [ ] Healthcheck fonctionne : `docker inspect bryshop_web | grep -A 10 Health`

---

## 🔄 PARTIE III : Pipeline CI/CD

### Architecture du Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Stage 1: Lint & Test                                        │
│  ├─ Flake8 (Linting)                                         │
│  ├─ Tests unitaires (90 tests)                               │
│  └─ Coverage report                                          │
│                                                               │
│  Stage 2: Code Quality (SonarQube)                           │
│  ├─ Analyse statique du code                                 │
│  ├─ Détection de vulnérabilités                              │
│  └─ Quality Gate (≥80% coverage)                             │
│                                                               │
│  Stage 3: Build & Push Docker Hub                            │
│  ├─ Build image Docker                                       │
│  ├─ Tag avec SHA + latest                                    │
│  └─ Push vers Docker Hub                                     │
│                                                               │
│  Stage 4: Deploy to O2Switch                                 │
│  ├─ Connexion SSH sécurisée                                  │
│  ├─ Pull de la nouvelle image                                │
│  ├─ Redémarrage de l'application                             │
│  └─ Vérification du déploiement                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Configuration des Secrets

### Secrets GitHub à Configurer

Allez dans **Settings > Secrets and variables > Actions** de votre repository GitHub.

#### 1. Docker Hub

```
DOCKER_USERNAME=votre-username-dockerhub
DOCKER_PASSWORD=votre-token-dockerhub
```

**Comment obtenir le token Docker Hub :**
1. Connectez-vous à https://hub.docker.com
2. Allez dans **Account Settings > Security**
3. Cliquez sur **New Access Token**
4. Donnez un nom (ex: "github-actions")
5. Copiez le token généré

#### 2. SonarQube/SonarCloud

```
SONAR_TOKEN=votre-token-sonarqube
SONAR_HOST_URL=https://sonarcloud.io (ou votre instance)
```

**Comment obtenir le token SonarCloud :**
1. Connectez-vous à https://sonarcloud.io
2. Allez dans **My Account > Security**
3. Générez un nouveau token
4. Copiez le token

#### 3. O2Switch SSH

```
O2SWITCH_SSH_KEY=votre-clé-privée-ssh
O2SWITCH_HOST=votre-domaine.o2switch.net
O2SWITCH_USER=votre-username
O2SWITCH_PATH=/home/username/bryshop
```

**Comment générer une clé SSH :**

```bash
# Générer une paire de clés SSH
ssh-keygen -t ed25519 -C "github-actions@bryshop" -f ~/.ssh/o2switch_deploy

# Copier la clé publique sur O2Switch
ssh-copy-id -i ~/.ssh/o2switch_deploy.pub user@o2switch.net

# Copier la clé privée pour GitHub
cat ~/.ssh/o2switch_deploy
# Copiez tout le contenu (y compris BEGIN et END)
```

### Résumé des Secrets

| Secret | Description | Exemple |
|--------|-------------|---------|
| `DOCKER_USERNAME` | Nom d'utilisateur Docker Hub | `johndo` |
| `DOCKER_PASSWORD` | Token d'accès Docker Hub | `dckr_pat_xxx...` |
| `SONAR_TOKEN` | Token SonarCloud/SonarQube | `sqp_xxx...` |
| `SONAR_HOST_URL` | URL de SonarQube | `https://sonarcloud.io` |
| `O2SWITCH_SSH_KEY` | Clé privée SSH | `-----BEGIN OPENSSH...` |
| `O2SWITCH_HOST` | Hôte O2Switch | `ssh.o2switch.net` |
| `O2SWITCH_USER` | Utilisateur SSH | `username` |
| `O2SWITCH_PATH` | Chemin de l'application | `/home/user/bryshop` |

---

## 📊 Configuration SonarQube

### Option 1 : SonarCloud (Recommandé - Gratuit pour projets publics)

1. **Créer un compte** sur https://sonarcloud.io
2. **Importer votre projet GitHub**
   - Cliquez sur "+" > "Analyze new project"
   - Sélectionnez votre repository
3. **Configurer le Quality Gate**
   - Allez dans **Quality Gates**
   - Créez un nouveau gate ou utilisez "Sonar way"
   - Ajoutez la condition : `Coverage < 80%` → FAILED
   - Ajoutez la condition : `Vulnerabilities (High) > 0` → FAILED
4. **Récupérer le token**
   - Allez dans **My Account > Security**
   - Générez un token
   - Ajoutez-le dans les secrets GitHub

### Option 2 : SonarQube Local (Pour tests)

```bash
# Démarrer SonarQube avec Docker
docker run -d --name sonarqube \
  -p 9000:9000 \
  sonarqube:latest

# Accéder à http://localhost:9000
# Login: admin / admin (changez le mot de passe)

# Créer un projet
# Générer un token
# Configurer le Quality Gate
```

### Configuration du Quality Gate

Le Quality Gate doit échouer si :
- ✅ Couverture de code < 80%
- ✅ Vulnérabilités de niveau High détectées
- ✅ Code Smells critiques > 0
- ✅ Duplications > 3%

---

## 🚀 Déploiement O2Switch

### Prérequis sur O2Switch

1. **Accès SSH activé**
2. **Docker installé** (ou demander à O2Switch)
3. **Docker Compose installé**

### Configuration sur O2Switch

```bash
# Se connecter en SSH
ssh user@o2switch.net

# Créer le répertoire de l'application
mkdir -p ~/bryshop
cd ~/bryshop

# Cloner le repository (ou créer docker-compose.yml)
git clone https://github.com/votre-username/bryshop.git .

# Créer le fichier .env
cp .env.example .env
nano .env  # Éditer avec vos valeurs

# Tester le déploiement manuel
docker-compose up -d

# Vérifier
docker ps
curl http://localhost:8000
```

### Script de Déploiement

Le pipeline exécute automatiquement :

```bash
# Pull de la nouvelle image
docker pull username/bryshop:SHA

# Arrêt de l'ancien conteneur
docker-compose down

# Démarrage du nouveau conteneur
docker-compose up -d

# Vérification
docker ps | grep bryshop_web
```

---

## ✅ Tests et Validation

### Tester le Pipeline Localement

#### Stage 1 : Lint & Test

```bash
# Installer flake8
pip install flake8

# Linter le code
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Exécuter les tests
python manage.py test

# Générer le coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage xml
```

#### Stage 2 : SonarQube (Local)

```bash
# Installer sonar-scanner
# Windows: Télécharger depuis https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
# Mac: brew install sonar-scanner
# Linux: apt-get install sonar-scanner

# Lancer l'analyse
sonar-scanner \
  -Dsonar.projectKey=bryshop \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=votre-token
```

#### Stage 3 : Build Docker

```bash
# Build l'image
docker build -t bryshop:test .

# Tester l'image
docker run -d -p 8000:8000 --name test_bryshop bryshop:test

# Vérifier
curl http://localhost:8000

# Nettoyer
docker stop test_bryshop
docker rm test_bryshop
```

### Tester le Pipeline Complet

1. **Créer une branche de test**

```bash
git checkout -b test-pipeline
git add .
git commit -m "test: pipeline configuration"
git push origin test-pipeline
```

2. **Créer une Pull Request**
   - Le pipeline s'exécutera automatiquement
   - Vérifiez les 4 stages dans l'onglet "Actions"

3. **Merger dans main**
   - Le déploiement sur O2Switch se déclenchera automatiquement

### Vérifications Post-Déploiement

```bash
# Sur O2Switch
ssh user@o2switch.net

# Vérifier les conteneurs
docker ps

# Voir les logs
docker-compose logs -f

# Vérifier l'application
curl http://localhost:8000

# Vérifier la base de données
docker exec bryshop_db psql -U bryshop -d BryshopDB -c "\dt"
```

---

## 📈 Monitoring et Logs

### Voir les Logs du Pipeline

1. Allez dans **Actions** sur GitHub
2. Cliquez sur le workflow en cours
3. Consultez les logs de chaque stage

### Voir les Logs de l'Application

```bash
# Logs Docker Compose
docker-compose logs -f

# Logs d'un conteneur spécifique
docker logs bryshop_web -f

# Logs PostgreSQL
docker logs bryshop_db -f
```

### Métriques SonarQube

1. Connectez-vous à SonarCloud
2. Sélectionnez votre projet
3. Consultez :
   - Coverage
   - Bugs
   - Vulnerabilities
   - Code Smells
   - Duplications

---

## 🐛 Dépannage

### Problème : Le pipeline échoue au Stage 1 (Tests)

```bash
# Vérifier les tests localement
python manage.py test --verbosity=2

# Vérifier la connexion PostgreSQL
psql -U bryshop -d BryshopDB -h localhost
```

### Problème : Quality Gate échoue (Stage 2)

- Vérifiez la couverture de code : `coverage report`
- Corrigez les vulnérabilités détectées par SonarQube
- Ajoutez plus de tests si coverage < 80%

### Problème : Build Docker échoue (Stage 3)

```bash
# Tester le build localement
docker build -t bryshop:debug .

# Voir les logs détaillés
docker build --progress=plain -t bryshop:debug .
```

### Problème : Déploiement O2Switch échoue (Stage 4)

```bash
# Vérifier la connexion SSH
ssh user@o2switch.net

# Vérifier Docker sur O2Switch
docker --version
docker-compose --version

# Vérifier les logs
docker-compose logs
```

---

## 📚 Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

---

## ✅ Checklist Finale

### Partie II : Dockerisation

- [ ] Dockerfile multi-stage créé
- [ ] Image Docker < 500 MB
- [ ] Utilisateur non-root configuré
- [ ] docker-compose.yml fonctionnel
- [ ] PostgreSQL configuré (BryshopDB)
- [ ] Application démarre sans erreur
- [ ] Healthcheck fonctionne

### Partie III : Pipeline CI/CD

- [ ] Workflow GitHub Actions créé (`.github/workflows/main.yml`)
- [ ] Stage 1 : Tests passent (90 tests)
- [ ] Stage 2 : SonarQube configuré
- [ ] Stage 2 : Quality Gate défini (≥80% coverage)
- [ ] Stage 3 : Image Docker publiée sur Docker Hub
- [ ] Stage 3 : Tags SHA + latest appliqués
- [ ] Stage 4 : Déploiement O2Switch fonctionnel
- [ ] Secrets GitHub configurés (8 secrets)
- [ ] Pipeline complet testé et validé

---

**🎉 Félicitations ! Votre pipeline CI/CD est maintenant opérationnel !**
