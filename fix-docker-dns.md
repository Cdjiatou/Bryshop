# 🔧 Fix Docker DNS - Résolution du problème "Could not resolve deb.debian.org"

## Problème
Le build Docker échoue avec l'erreur :
```
Could not resolve 'deb.debian.org'
E: Unable to fetch some archives
```

## Causes Possibles
1. Problème de DNS dans Docker
2. Pare-feu ou proxy bloquant les connexions
3. Configuration réseau de Docker Desktop

---

## ✅ Solution 1 : Configurer les DNS dans Docker Desktop (Windows)

### Étape 1 : Ouvrir Docker Desktop

1. Cliquez sur l'icône Docker dans la barre des tâches
2. Cliquez sur l'icône ⚙️ (Settings)

### Étape 2 : Configurer les DNS

1. Allez dans **Docker Engine**
2. Ajoutez cette configuration dans le JSON :

```json
{
  "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
}
```

**Exemple complet** :
```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
  "experimental": false
}
```

3. Cliquez sur **Apply & Restart**
4. Attendez que Docker redémarre (30 secondes)

### Étape 3 : Tester

```powershell
# Tester la résolution DNS
docker run --rm alpine ping -c 3 deb.debian.org

# Si ça fonctionne, rebuilder l'image
docker build -t bryshop:latest .
```

---

## ✅ Solution 2 : Utiliser --network=host (Temporaire)

```powershell
# Build avec le réseau de l'hôte
docker build --network=host -t bryshop:latest .
```

⚠️ **Note** : Cette solution est temporaire et ne fonctionne que sur Linux. Sur Windows, utilisez la Solution 1.

---

## ✅ Solution 3 : Ajouter DNS dans le Dockerfile

Modifiez le `Dockerfile` pour ajouter des DNS explicites :

```dockerfile
# Au début du Dockerfile, après FROM
FROM python:3.11-slim as builder

# Configurer les DNS
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# Reste du Dockerfile...
```

⚠️ **Note** : Cette solution n'est pas recommandée car elle modifie le Dockerfile.

---

## ✅ Solution 4 : Vérifier le Pare-feu / Antivirus

Certains pare-feu ou antivirus bloquent les connexions Docker.

### Windows Defender Firewall

1. Ouvrez **Windows Defender Firewall**
2. Cliquez sur **Autoriser une application via le pare-feu**
3. Vérifiez que **Docker Desktop** est autorisé pour les réseaux privés et publics

### Antivirus Tiers

Si vous utilisez un antivirus (Avast, Norton, etc.) :
1. Ajoutez Docker Desktop aux exceptions
2. Autorisez les connexions réseau de Docker

---

## ✅ Solution 5 : Réinitialiser Docker Desktop

Si rien ne fonctionne :

1. Ouvrez Docker Desktop
2. Allez dans **Troubleshoot** (icône 🐛)
3. Cliquez sur **Reset to factory defaults**
4. Attendez la réinitialisation
5. Reconfigurez les DNS (Solution 1)

---

## ✅ Solution 6 : Utiliser un Proxy (Si vous êtes derrière un proxy d'entreprise)

### Configurer le Proxy dans Docker Desktop

1. Ouvrez Docker Desktop → Settings
2. Allez dans **Resources** → **Proxies**
3. Activez **Manual proxy configuration**
4. Entrez vos paramètres proxy :
   - HTTP Proxy: `http://proxy.entreprise.com:8080`
   - HTTPS Proxy: `http://proxy.entreprise.com:8080`
5. Cliquez sur **Apply & Restart**

---

## 🧪 Tester la Connexion Réseau

### Test 1 : Ping depuis un conteneur

```powershell
# Tester la résolution DNS
docker run --rm alpine nslookup deb.debian.org

# Tester la connectivité
docker run --rm alpine ping -c 3 deb.debian.org

# Tester wget
docker run --rm alpine wget -O- http://deb.debian.org
```

### Test 2 : Vérifier les DNS de Docker

```powershell
# Voir la configuration Docker
docker info | Select-String -Pattern "DNS"
```

---

## 🔍 Diagnostic Complet

Exécutez ces commandes pour diagnostiquer le problème :

```powershell
# 1. Vérifier que Docker fonctionne
docker --version
docker ps

# 2. Tester la résolution DNS
docker run --rm alpine nslookup google.com
docker run --rm alpine nslookup deb.debian.org

# 3. Tester la connectivité Internet
docker run --rm alpine ping -c 3 8.8.8.8
docker run --rm alpine ping -c 3 google.com

# 4. Voir les logs Docker
# Dans Docker Desktop → Troubleshoot → View logs
```

---

## 📋 Checklist de Résolution

- [ ] Docker Desktop est démarré
- [ ] DNS configurés dans Docker Engine (8.8.8.8, 8.8.4.4, 1.1.1.1)
- [ ] Docker Desktop redémarré après configuration
- [ ] Pare-feu autorise Docker Desktop
- [ ] Antivirus n'interfère pas avec Docker
- [ ] Test de résolution DNS réussi (`docker run --rm alpine nslookup deb.debian.org`)
- [ ] Test de connectivité réussi (`docker run --rm alpine ping -c 3 deb.debian.org`)
- [ ] Build Docker réussi (`docker build -t bryshop:latest .`)

---

## 🚀 Après la Résolution

Une fois le problème résolu :

```powershell
# 1. Nettoyer les builds échoués
docker builder prune -a

# 2. Rebuilder l'image
docker build -t bryshop:latest .

# 3. Ou avec docker-compose
docker-compose build --no-cache

# 4. Démarrer l'application
docker-compose up -d
```

---

## 🆘 Si Rien ne Fonctionne

1. **Redémarrez votre ordinateur** (parfois nécessaire après configuration DNS)
2. **Réinstallez Docker Desktop** (en dernier recours)
3. **Vérifiez votre connexion Internet** (essayez de naviguer sur deb.debian.org dans votre navigateur)
4. **Contactez votre administrateur réseau** (si vous êtes dans un réseau d'entreprise)

---

## 📚 Ressources

- [Docker DNS Configuration](https://docs.docker.com/config/daemon/#configure-the-docker-daemon)
- [Docker Network Troubleshooting](https://docs.docker.com/network/troubleshoot/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
