# 🔒 PARTIE IV : Sécurisation du Pipeline et Traçabilité (C25)

## 📋 Vue d'ensemble

Cette partie implémente les mesures de sécurité et de traçabilité pour le pipeline CI/CD de BryShop.

---

## 1. 🔐 Gestion des Secrets

### Secrets GitHub Configurés

Tous les secrets sensibles sont stockés de manière sécurisée dans GitHub Secrets et ne sont jamais exposés dans le code.

| Secret | Usage | Type |
|--------|-------|------|
| `DOCKER_USERNAME` | Authentification Docker Hub | Credentials |
| `DOCKER_PASSWORD` | Token Docker Hub | Token |
| `SONAR_TOKEN` | Authentification SonarQube | Token |
| `SONAR_HOST_URL` | URL SonarQube | URL |
| `O2SWITCH_SSH_KEY` | Clé privée SSH pour déploiement | Private Key |
| `O2SWITCH_HOST` | Hôte O2Switch | Hostname |
| `O2SWITCH_USER` | Utilisateur SSH | Username |
| `O2SWITCH_PATH` | Chemin de l'application | Path |

### Justification par Écrit

**Absence totale de données sensibles dans le code :**

✅ **Clés d'API** : Aucune clé d'API n'est présente dans le code source. Toutes les clés (Notch Pay, Email, etc.) sont gérées via des variables d'environnement ou des secrets GitHub.

✅ **Mots de passe de base de données** : 
- PostgreSQL en développement : Sans mot de passe (trust mode)
- PostgreSQL en production : Mot de passe géré via variables d'environnement
- Aucun mot de passe hardcodé dans `settings.py` ou `docker-compose.yml`

✅ **Tokens Docker Hub** : Utilisés uniquement via `${{ secrets.DOCKER_PASSWORD }}` dans le workflow GitHub Actions.

✅ **Clés SSH O2Switch** : La clé privée SSH est stockée dans GitHub Secrets et injectée uniquement au moment du déploiement via `webfactory/ssh-agent`.

✅ **Fichiers de configuration** :
- `.env.example` : Template sans valeurs réelles
- `.gitignore` : Exclut `.env`, `*.key`, `*.pem`, `id_rsa*`
- Aucun fichier `.env` avec des vraies valeurs n'est commité

### Vérification

```bash
# Vérifier qu'aucun secret n'est présent dans le code
git grep -i "password\|secret\|api_key\|token" --exclude-dir=.git

# Vérifier le .gitignore
cat .gitignore | grep -E "\.env|\.key|\.pem|id_rsa"
```

---

## 2. 🛡️ Analyse de Vulnérabilités des Images Docker

### Outil Utilisé : Trivy

**Trivy** est un scanner de vulnérabilités open-source pour conteneurs, développé par Aqua Security.

### Implémentation dans le Pipeline

Le scan de sécurité est intégré comme **Stage 3.5** dans le workflow GitHub Actions :

```yaml
security-scan:
  name: 🔒 Security Vulnerability Scan
  runs-on: ubuntu-latest
  needs: build-and-push
  
  steps:
    - name: 🛡️ Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.DOCKER_IMAGE }}:${{ github.sha }}
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'
```

### Fonctionnalités du Scan

1. **Scan SARIF** : Résultats uploadés vers GitHub Security
   - Visible dans l'onglet "Security" > "Code scanning alerts"
   - Intégration native avec GitHub Advanced Security

2. **Scan Table** : Affichage formaté dans les logs
   - Vulnérabilités CRITICAL, HIGH, MEDIUM
   - Facile à lire dans les logs du workflow

3. **Scan JSON** : Rapport détaillé téléchargeable
   - Conservé pendant 30 jours
   - Analyse programmatique possible

4. **Vérification Automatique** :
   ```bash
   CRITICAL_COUNT=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' trivy-report.json)
   HIGH_COUNT=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity=="HIGH")] | length' trivy-report.json)
   ```

### Blocage du Push vers Docker Hub

**Configuration actuelle** : `exit-code: '0'` (mode warning)
- Le scan ne bloque PAS le pipeline
- Les vulnérabilités sont signalées comme warnings
- Permet de continuer le déploiement tout en étant informé

**Pour bloquer si vulnérabilités critiques** :
```yaml
- name: 🛡️ Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.DOCKER_IMAGE }}:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'  # ⚠️ Bloque le pipeline si vulnérabilités détectées
```

### Exemple de Résultat

```
🔍 Vulnerability Summary:
   CRITICAL: 0
   HIGH: 2

⚠️ WARNING: 2 high vulnerabilities found!
::warning::2 high vulnerabilities detected in Docker image

┌─────────────────────────────────────────────────────────────┐
│ Library    │ Vulnerability │ Severity │ Installed │ Fixed   │
├─────────────────────────────────────────────────────────────┤
│ openssl    │ CVE-2023-1234 │ HIGH     │ 1.1.1     │ 1.1.2   │
│ libcrypto  │ CVE-2023-5678 │ HIGH     │ 1.1.1     │ 1.1.2   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 📊 Traçabilité

### Logs de Déploiement

Chaque déploiement est tracé dans un fichier `deployment.log` sur le serveur O2Switch :

```bash
# Création du log
echo "$(date): Deploying ${{ github.sha }}" >> deployment.log

# En cas de succès
echo "$(date): Deployment ${{ github.sha }} successful" >> deployment.log

# En cas d'échec
echo "$(date): Deployment ${{ github.sha }} failed" >> deployment.log
```

### Métadonnées de l'Image Docker

Chaque image Docker est taguée avec des métadonnées :

```yaml
build-args: |
  BUILD_DATE=${{ github.event.head_commit.timestamp }}
  VCS_REF=${{ github.sha }}
```

**Inspection de l'image** :
```bash
docker inspect bryshop:latest | jq '.[0].Config.Labels'
```

### GitHub Actions Summary

Un résumé de déploiement est créé automatiquement :

```markdown
## 🚀 Deployment Summary

- **Status**: success
- **Image**: `username/bryshop:abc123def`
- **Commit**: [abc123def](https://github.com/Cdjiatou/Bryshop/commit/abc123def)
- **Branch**: `main`
- **Timestamp**: `2026-05-25T14:30:00Z`
```

### Artifacts Conservés

| Artifact | Durée | Contenu |
|----------|-------|---------|
| `coverage-report` | Permanent | Rapport de couverture de code |
| `trivy-security-report` | 30 jours | Rapport de vulnérabilités JSON |
| GitHub Security Alerts | Permanent | Alertes SARIF dans l'onglet Security |

---

## 4. 🔍 Vérification de la Sécurité

### Checklist de Sécurité

- [x] Aucun secret dans le code source
- [x] Tous les secrets dans GitHub Secrets
- [x] `.gitignore` configuré pour exclure les fichiers sensibles
- [x] Scan de vulnérabilités avec Trivy
- [x] Résultats uploadés vers GitHub Security
- [x] Logs de déploiement tracés
- [x] Métadonnées dans les images Docker
- [x] Utilisateur non-root dans le conteneur
- [x] Connexion SSH sécurisée pour le déploiement

### Commandes de Vérification

```bash
# 1. Vérifier qu'aucun secret n'est commité
git log --all --full-history --source -- '*password*' '*secret*' '*.key' '*.pem'

# 2. Scanner l'image localement avec Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image bryshop:latest

# 3. Vérifier les secrets GitHub (via UI)
# https://github.com/Cdjiatou/Bryshop/settings/secrets/actions

# 4. Vérifier les alertes de sécurité
# https://github.com/Cdjiatou/Bryshop/security/code-scanning

# 5. Vérifier les logs de déploiement (sur O2Switch)
ssh user@o2switch.net "cat ~/bryshop/deployment.log"
```

---

## 5. 📈 Monitoring de Sécurité

### GitHub Security Tab

Toutes les vulnérabilités détectées par Trivy sont visibles dans :
- **Security** > **Code scanning** > **Trivy container scan**

### Notifications

GitHub envoie automatiquement des notifications :
- ✅ Par email aux mainteneurs
- ✅ Dans l'onglet Notifications
- ✅ Via webhooks (si configurés)

### Rapports Réguliers

Les scans Trivy s'exécutent :
- ✅ À chaque push sur `main` ou `develop`
- ✅ À chaque Pull Request
- ✅ Manuellement via "Run workflow"

---

## 6. 🛠️ Utilisation

### Workflow Principal

Le workflow sécurisé est dans `.github/workflows/main-secure.yml`

**Pour l'activer** :
```bash
# Renommer le workflow actuel
mv .github/workflows/main.yml .github/workflows/main-old.yml

# Activer le workflow sécurisé
mv .github/workflows/main-secure.yml .github/workflows/main.yml

# Commit et push
git add .github/workflows/
git commit -m "feat: activate secured pipeline with Trivy scan"
git push origin main
```

### Scanner une Image Localement

```bash
# Installer Trivy
# Windows: choco install trivy
# Mac: brew install trivy
# Linux: apt-get install trivy

# Scanner l'image
trivy image bryshop:latest

# Scanner avec sévérité spécifique
trivy image --severity CRITICAL,HIGH bryshop:latest

# Générer un rapport JSON
trivy image --format json --output trivy-report.json bryshop:latest
```

---

## 7. 📚 Ressources

- **Trivy Documentation** : https://aquasecurity.github.io/trivy/
- **GitHub Security** : https://docs.github.com/en/code-security
- **Docker Security Best Practices** : https://docs.docker.com/engine/security/
- **OWASP Container Security** : https://owasp.org/www-project-docker-top-10/

---

## ✅ Validation Partie IV

- [x] Gestion des secrets via GitHub Secrets (8 secrets)
- [x] Justification écrite de l'absence de données sensibles
- [x] Scan de vulnérabilités avec Trivy intégré
- [x] Résultats uploadés vers GitHub Security (SARIF)
- [x] Rapports JSON conservés (30 jours)
- [x] Traçabilité des déploiements (logs)
- [x] Métadonnées dans les images Docker
- [x] Documentation complète

---

**🎉 Partie IV : Sécurisation et Traçabilité - TERMINÉE !**
