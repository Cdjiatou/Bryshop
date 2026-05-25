# 📦 PARTIE I : Gestion de Dépôt et Stratégie de Versioning (C21/C22)

## 📋 Vue d'ensemble

Cette partie documente la stratégie Git et les politiques de protection du repository BryShop.

**Repository GitHub** : https://github.com/Cdjiatou/Bryshop.git

---

## 1. 🔄 Initialisation et Flux Git

### Repository GitHub

- **Plateforme** : GitHub
- **URL** : https://github.com/Cdjiatou/Bryshop.git
- **Visibilité** : Privé (recommandé) ou Public
- **Type** : Dépôt Git privé

### Stratégie de Branches (GitFlow Adapté)

Nous utilisons une stratégie de branches **GitFlow adaptée** pour une équipe de 3 développeurs :

```
main (production)
  ↑
  └── develop (intégration)
       ↑
       ├── feature/user-authentication
       ├── feature/payment-integration
       └── feature/api-delivery
```

#### Structure des Branches

1. **`main`** (branche principale)
   - Code en production
   - Toujours stable et déployable
   - Protégée contre les push directs
   - Déploiement automatique vers O2Switch

2. **`develop`** (branche de développement)
   - Intégration continue des features
   - Tests automatiques via CI/CD
   - Base pour créer les features

3. **`feature/*`** (branches de fonctionnalités)
   - Format : `feature/nom-de-la-fonctionnalite`
   - Exemples :
     - `feature/user-authentication`
     - `feature/payment-notchpay`
     - `feature/order-management`
     - `feature/api-delivery`

#### Workflow de Développement

```bash
# 1. Créer une branche feature depuis develop
git checkout develop
git pull origin develop
git checkout -b feature/user-authentication

# 2. Développer et commiter
git add .
git commit -m "feat: add user authentication system"

# 3. Pousser la branche
git push origin feature/user-authentication

# 4. Créer une Pull Request vers develop
# Via l'interface GitHub

# 5. Après review et tests, merger dans develop
# Via l'interface GitHub

# 6. Quand develop est stable, merger dans main
git checkout main
git pull origin main
git merge develop
git push origin main
```

### Convention de Nommage des Commits

Nous utilisons la convention **Conventional Commits** :

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

#### Types de Commits

| Type | Description | Exemple |
|------|-------------|---------|
| `feat` | Nouvelle fonctionnalité | `feat: add user login` |
| `fix` | Correction de bug | `fix: resolve payment error` |
| `docs` | Documentation | `docs: update README` |
| `style` | Formatage, style | `style: format code with black` |
| `refactor` | Refactoring | `refactor: simplify cart logic` |
| `test` | Ajout de tests | `test: add order model tests` |
| `chore` | Tâches diverses | `chore: update dependencies` |
| `ci` | CI/CD | `ci: add GitHub Actions workflow` |
| `perf` | Performance | `perf: optimize database queries` |

#### Exemples de Commits

```bash
# Feature
git commit -m "feat(auth): add user registration with email verification"

# Bug fix
git commit -m "fix(payment): resolve NotchPay callback error"

# Documentation
git commit -m "docs: add Docker setup instructions"

# Tests
git commit -m "test(models): add Product model unit tests"

# CI/CD
git commit -m "ci: add Trivy security scan to pipeline"
```

---

## 2. 🔒 Politique de Traçabilité et Protection

### Protection de la Branche `main`

#### Configuration GitHub

Aller dans **Settings > Branches > Branch protection rules** pour `main` :

✅ **Règles de Protection Configurées** :

1. **Require a pull request before merging**
   - ✅ Interdiction du force push
   - ✅ Obligation de passer par une Pull Request
   - ✅ Require approvals: 1 (au moins 1 approbation)

2. **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - ✅ Status checks requis :
     - `lint-and-test` (Stage 1)
     - `code-quality` (Stage 2 - SonarQube)
     - `build-and-push` (Stage 3)
     - `security-scan` (Stage 3.5 - Trivy)

3. **Require conversation resolution before merging**
   - ✅ Tous les commentaires doivent être résolus

4. **Do not allow bypassing the above settings**
   - ✅ Même les admins doivent suivre les règles

5. **Restrict who can push to matching branches**
   - ✅ Seuls les mainteneurs peuvent merger

#### Commandes pour Configurer (via GitHub CLI)

```bash
# Installer GitHub CLI
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: apt install gh

# Se connecter
gh auth login

# Protéger la branche main
gh api repos/Cdjiatou/Bryshop/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["lint-and-test","code-quality","build-and-push","security-scan"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

### Protection de la Branche `develop`

Configuration similaire mais moins stricte :

✅ **Règles de Protection** :

1. **Require a pull request before merging**
   - ✅ Require approvals: 1

2. **Require status checks to pass before merging**
   - ✅ `lint-and-test` doit passer

3. **Allow force pushes** (pour les rebases)
   - ⚠️ Autorisé uniquement pour les mainteneurs

### Merge Request / Pull Request

#### Template de Pull Request

Créer `.github/PULL_REQUEST_TEMPLATE.md` :

```markdown
## 📝 Description

<!-- Décrivez les changements apportés -->

## 🎯 Type de changement

- [ ] 🐛 Bug fix
- [ ] ✨ Nouvelle fonctionnalité
- [ ] 📝 Documentation
- [ ] 🔧 Configuration
- [ ] ♻️ Refactoring
- [ ] 🧪 Tests

## 🧪 Tests

- [ ] Les tests passent localement
- [ ] J'ai ajouté des tests pour mes changements
- [ ] La couverture de code est maintenue/améliorée

## 📋 Checklist

- [ ] Mon code suit les conventions du projet
- [ ] J'ai commenté les parties complexes
- [ ] J'ai mis à jour la documentation
- [ ] Aucun warning dans les tests
- [ ] Les migrations sont incluses (si nécessaire)

## 🔗 Issues liées

<!-- Référencez les issues : Closes #123 -->

## 📸 Screenshots (si applicable)

<!-- Ajoutez des captures d'écran -->
```

#### Workflow de Pull Request

```
1. Développeur crée une PR
   ↓
2. CI/CD s'exécute automatiquement
   ↓
3. Review par un pair (1 approbation minimum)
   ↓
4. Tous les checks passent (tests, SonarQube, Trivy)
   ↓
5. Merge dans develop ou main
```

### Traçabilité des Changements

#### 1. Commits Signés (Recommandé)

```bash
# Configurer GPG
git config --global user.signingkey YOUR_GPG_KEY
git config --global commit.gpgsign true

# Commiter avec signature
git commit -S -m "feat: add secure payment"
```

#### 2. Tags de Version

```bash
# Créer un tag pour une release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Lister les tags
git tag -l

# Voir les détails d'un tag
git show v1.0.0
```

#### 3. Changelog Automatique

Utiliser **conventional-changelog** :

```bash
# Installer
npm install -g conventional-changelog-cli

# Générer le CHANGELOG
conventional-changelog -p angular -i CHANGELOG.md -s

# Exemple de CHANGELOG.md généré :
```

```markdown
# Changelog

## [1.0.0] - 2026-05-25

### Features
- **auth**: add user registration with email verification
- **payment**: integrate NotchPay payment gateway
- **ci**: add GitHub Actions pipeline with 4 stages

### Bug Fixes
- **cart**: fix quantity update issue
- **order**: resolve numero_commande generation

### Documentation
- **docker**: add comprehensive Docker documentation
- **ci-cd**: add CI/CD setup guide
```

---

## 3. 📊 Visualisation du Flux Git

### Diagramme GitFlow

```
main ────●────────────●────────────●──────> (production)
         │            │            │
         │            │            │
develop ─┴─●──●──●──●─┴─●──●──●──●─┴──●───> (intégration)
           │  │  │  │    │  │  │  │
           │  │  │  │    │  │  │  │
feature/A ─┴──●──●──┘    │  │  │  │
                         │  │  │  │
feature/B ───────────────┴──●──●──┘
                               │
feature/C ─────────────────────┴──●──●
```

### Exemple Concret pour BryShop

```
main ────●─────────────────────●──────> v1.0.0 (production)
         │                     │
         │                     │
develop ─┴─●──●──●──●──●──●──●─┴──●───> (tests)
           │  │  │     │  │  │
           │  │  │     │  │  │
feature/   │  │  │     │  │  │
user-auth ─┴──●──●─────┘  │  │
                           │  │
feature/                   │  │
payment ────────────────────┴──●──●
                                 │
feature/                         │
api-delivery ────────────────────┴──●
```

---

## 4. 🛠️ Configuration Pratique

### Fichier `.gitignore` (Déjà configuré)

```gitignore
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
*.log

# Django
db.sqlite3
*.sqlite3
media/
staticfiles/

# Environment variables
.env
.env.local
.env.*.local
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Coverage
.coverage
htmlcov/
coverage.xml
.pytest_cache/

# Docker
deta

# OS
Thumbs.db

# Secrets (ne jamais commiter)
*.pem
*.key
id_rsa*
*.ppk
```

### Fichier `.gitattributes`

Créer `.gitattributes` pour normaliser les fins de ligne :

```gitattributes
# Auto detect text files and normalize line endings to LF
* text=auto

# Python files
*.py text eol=lf

# Shell scripts
*.sh text eol=lf

# Windows scripts
*.bat text eol=crlf
*.ps1 text eol=crlf

# Docker files
Dockerfile text eol=lf
docker-compose*.yml text eol=lf

# YAML files
*.yml text eol=lf
*.yaml text eol=lf

# Markdown
*.md text eol=lf

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
```

---

## 5. ✅ Checklist de Validation

### Configuration Git

- [x] Repository GitHub créé : https://github.com/Cdjiatou/Bryshop.git
- [x] Branches `main` et `develop` créées
- [x] `.gitignore` configuré
- [ ] `.gitattributes` créé
- [ ] Protection de la branche `main` activée
- [ ] Protection de la branche `develop` activée
- [ ] Template de Pull Request créé

### Stratégie de Branches

- [x] GitFlow adapté documenté
- [x] Convention de nommage des commits (Conventional Commits)
- [x] Workflow de développement défini
- [ ] Tags de version configurés
- [ ] CHANGELOG.md initialisé

### Traçabilité

- [x] Commits avec messages descriptifs
- [ ] Commits signés (GPG) - Optionnel
- [ ] Tags de version pour les releases
- [ ] CHANGELOG automatique

---

## 6. 📚 Commandes Git Essentielles

### Configuration Initiale

```bash
# Cloner le repository
git clone https://github.com/Cdjiatou/Bryshop.git
cd Bryshop

# Configurer l'utilisateur
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"

# Voir la configuration
git config --list
```

### Workflow Quotidien

```bash
# Mettre à jour develop
git checkout develop
git pull origin develop

# Créer une feature
git checkout -b feature/ma-fonctionnalite

# Développer...
git add .
git commit -m "feat: add my feature"

# Pousser
git push origin feature/ma-fonctionnalite

# Créer une PR sur GitHub
# Via l'interface web
```

### Commandes Utiles

```bash
# Voir l'historique
git log --oneline --graph --all

# Voir les branches
git branch -a

# Supprimer une branche locale
git branch -d feature/ma-fonctionnalite

# Supprimer une branche distante
git push origin --delete feature/ma-fonctionnalite

# Annuler le dernier commit (local)
git reset --soft HEAD~1

# Voir les différences
git diff

# Voir le statut
git status
```

---

## 7. 📖 Ressources

- **Git Documentation** : https://git-scm.com/doc
- **GitFlow** : https://nvie.com/posts/a-successful-git-branching-model/
- **Conventional Commits** : https://www.conventionalcommits.org/
- **GitHub Flow** : https://guides.github.com/introduction/flow/
- **Branch Protection** : https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches

---

**🎉 Partie I : Gestion de Dépôt et Stratégie de Versioning - TERMINÉE !**
