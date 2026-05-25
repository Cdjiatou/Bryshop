# ============================================
# STAGE 1: Builder - Installation des dépendances
# ============================================
FROM python:3.11-slim AS builder

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour la compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements pour profiter du cache Docker
COPY requirements.txt requirements-docker.txt ./

# Installer les dépendances Python dans un environnement virtuel
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-docker.txt


# ============================================
# STAGE 2: Runtime - Image finale optimisée
# ============================================
FROM python:3.11-slim

# Métadonnées de l'image
LABEL maintainer="BryShop App"
LABEL description="BryShop E-Commerce Application "


# Variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Installer uniquement les dépendances runtime nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Définir le répertoire de travail
WORKDIR /app

# Copier l'environnement virtuel depuis le stage builder
COPY --from=builder /opt/venv /opt/venv

# Copier le code de l'application
COPY --chown=appuser:appuser . .

# Créer les répertoires nécessaires avec les bonnes permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput || true

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port 8000
EXPOSE 8000

# Healthcheck pour vérifier que l'application fonctionne
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000', timeout=5)" || exit 1

# Commande par défaut pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "ECOMMERCE.wsgi:application"]
