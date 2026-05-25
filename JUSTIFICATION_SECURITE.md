# Justification de l'absence de données sensibles "hardcodées"

Conformément aux bonnes pratiques de sécurité et aux exigences du projet, aucune donnée sensible (clés d'API, mots de passe de base de données, tokens Docker Hub, clés SSH) n'est "hardcodée" (écrite en dur) dans les scripts, le code source ou les Dockerfiles de l'application BryShop.

## 1. Mots de passe de Base de Données
Dans le fichier `docker-compose.yml`, la connexion à la base de données PostgreSQL locale utilise la méthode d'authentification `trust` (`POSTGRES_HOST_AUTH_METHOD: trust`) uniquement pour le développement local. Aucun mot de passe n'est stocké dans ce fichier.

En environnement de production (via CI/CD), les identifiants de base de données sont injectés via des variables d'environnement (`DATABASE_USER`, `DATABASE_PASSWORD`, etc.), qui sont récupérées de manière sécurisée (par exemple, depuis des secrets GitHub ou un gestionnaire de secrets).

## 2. Secrets CI/CD (GitHub Actions)
Dans les workflows `.github/workflows/main.yml` et `main-secure.yml`, aucun token ou clé n'est écrit en clair. Tous les accès sensibles utilisent le mécanisme sécurisé `secrets` de GitHub Actions :

- **Docker Hub** : Les identifiants sont appelés via `${{ secrets.DOCKER_USERNAME }}` et `${{ secrets.DOCKER_PASSWORD }}`.
- **SonarQube** : Le token est appelé via `${{ secrets.SONAR_TOKEN }}`.
- **Déploiement O2Switch (SSH)** : La clé SSH privée et les informations de connexion sont injectées via `${{ secrets.O2SWITCH_SSH_KEY }}`, `${{ secrets.O2SWITCH_HOST }}`, `${{ secrets.O2SWITCH_USER }}`, et `${{ secrets.O2SWITCH_PATH }}`.

## 3. Clés d'API (Notch Pay, etc.)
De même, toutes les clés d'API (comme celles de Notch Pay pour les paiements) sont gérées via le fichier `.env` en local (lequel est ignoré par Git via `.gitignore`) et via des variables d'environnement sur le serveur de production. Le code utilise `os.getenv('VARIABLE_NAME')` ou la configuration Django pour les lire.

## Conclusion
Cette approche garantit qu'aucune fuite de données critiques ne peut survenir en cas d'accès non autorisé au dépôt de code source. Le code source est découplé de la configuration sensible.
