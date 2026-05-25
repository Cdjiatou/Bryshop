# Guide de Contribution (CONTRIBUTING.md)

Merci de contribuer au projet **BryShop** (Kaba-Delivery) ! 

Pour garantir une qualité de code et une lisibilité de l'historique Git optimales, nous utilisons la convention **Conventional Commits**.

## Convention de Nommage des Commits

Chaque message de commit doit respecter la structure suivante :
```
<type>(<portée optionnelle>): <description courte>

[corps optionnel]

[pied de page optionnel]
```

### Types Autorisés
- **feat** : Ajout d'une nouvelle fonctionnalité (ex: intégration de Notch Pay).
- **fix** : Correction d'un bug.
- **docs** : Modifications de la documentation uniquement (ex: README, CONTRIBUTING).
- **style** : Changements qui n'affectent pas le sens du code (espaces, formatage, etc.).
- **refactor** : Modification du code qui ne corrige ni bug ni n'ajoute de fonctionnalité.
- **perf** : Amélioration des performances.
- **test** : Ajout ou correction de tests.
- **chore** : Mise à jour des tâches de build, gestionnaire de paquets, CI/CD, etc.

### Exemples
- `feat(api): ajout de la route pour le paiement en ligne`
- `fix(db): correction de la connexion à la base de données`
- `docs: mise à jour du plan d'implémentation`
- `chore(ci): intégration de Trivy dans le pipeline`

## Processus de Contribution
1. Créez une branche depuis `develop` : `git checkout -b feature/nom-de-votre-fonctionnalite`
2. Effectuez vos commits en respectant la convention ci-dessus.
3. Poussez votre branche sur le dépôt distant.
4. Ouvrez une **Pull Request (PR)** vers la branche `develop`.
5. Attendez la validation (Code Review + tests CI/CD) avant la fusion.
