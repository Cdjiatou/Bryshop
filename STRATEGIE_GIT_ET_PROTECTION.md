# Stratégie de Versioning et Protection de Dépôt (Partie I)

## 1. Stratégie Gitflow Adaptée
Pour notre équipe de 3 développeurs, nous utilisons une version allégée de **Gitflow** :

- **`main` (ou `master`)** : Branche de production. Le code sur cette branche doit toujours être stable et déployable.
- **`develop`** : Branche d'intégration principale. C'est ici que les nouvelles fonctionnalités se rejoignent avant d'être envoyées en production (`main`).
- **`feature/*`** (ex: `feature/api-delivery`) : Branches créées depuis `develop` pour développer de nouvelles fonctionnalités de manière isolée. Une fois terminées, elles sont fusionnées dans `develop` via une Pull Request.

## 2. Règles de Protection de la Branche Principale (`main`)
Afin d'assurer la stabilité du dépôt et de respecter les consignes de traçabilité, les règles suivantes doivent être configurées sur les paramètres du dépôt distant (GitHub/GitLab) pour la branche `main` :

1. **Interdiction du Force Push** : Personne ne peut réécrire l'historique de la branche `main`.
2. **Obligation de Pull Request (PR) / Merge Request (MR)** : Aucun commit direct sur `main` n'est autorisé. Tout changement doit passer par une PR depuis `develop`.
3. **Approbation par les pairs requise** : Chaque PR vers `main` doit être validée par au moins un autre développeur de l'équipe (Code Review).
4. **Réussite des statuts CI/CD obligatoire** : La fusion n'est possible que si le pipeline CI/CD de GitHub Actions est au vert (linting, tests unitaires avec >80% de couverture, passage du Quality Gate SonarQube, et absence de vulnérabilités critiques via Trivy).
