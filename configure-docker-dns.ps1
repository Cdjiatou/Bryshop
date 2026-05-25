# Script de configuration DNS pour Docker Desktop
# Ce script aide à résoudre le problème "Could not resolve deb.debian.org"

Write-Host "🔧 Configuration DNS pour Docker Desktop" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que Docker est installé
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker installé : $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker n'est pas installé !" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Diagnostic du problème..." -ForegroundColor Yellow
Write-Host ""

# Test 1 : Vérifier la résolution DNS depuis un conteneur
Write-Host "Test 1 : Résolution DNS de google.com..." -ForegroundColor Cyan
try {
    $result = docker run --rm alpine nslookup google.com 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ google.com résolu avec succès" -ForegroundColor Green
    } else {
        Write-Host "❌ Échec de résolution de google.com" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Impossible d'exécuter le test" -ForegroundColor Red
}

Write-Host ""

# Test 2 : Vérifier la résolution DNS de deb.debian.org
Write-Host "Test 2 : Résolution DNS de deb.debian.org..." -ForegroundColor Cyan
try {
    $result = docker run --rm alpine nslookup deb.debian.org 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ deb.debian.org résolu avec succès" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎉 Votre configuration DNS fonctionne !" -ForegroundColor Green
        Write-Host "   Vous pouvez maintenant builder l'image avec :" -ForegroundColor White
        Write-Host "   docker build -t bryshop:latest ." -ForegroundColor Yellow
        exit 0
    } else {
        Write-Host "❌ Échec de résolution de deb.debian.org" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Impossible d'exécuter le test" -ForegroundColor Red
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔧 Configuration DNS Requise" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Pour résoudre ce problème, suivez ces étapes :" -ForegroundColor White
Write-Host ""
Write-Host "1️⃣  Ouvrez Docker Desktop" -ForegroundColor Cyan
Write-Host "   - Cliquez sur l'icône Docker dans la barre des tâches" -ForegroundColor White
Write-Host "   - Cliquez sur l'icône ⚙️ (Settings)" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣  Allez dans 'Docker Engine'" -ForegroundColor Cyan
Write-Host ""

Write-Host "3️⃣  Ajoutez cette configuration dans le JSON :" -ForegroundColor Cyan
Write-Host ""
Write-Host '   {' -ForegroundColor Yellow
Write-Host '     "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"]' -ForegroundColor Yellow
Write-Host '   }' -ForegroundColor Yellow
Write-Host ""
Write-Host "   ⚠️  Si d'autres configurations existent, ajoutez juste la ligne dns" -ForegroundColor Yellow
Write-Host ""

Write-Host "4️⃣  Cliquez sur 'Apply & Restart'" -ForegroundColor Cyan
Write-Host ""

Write-Host "5️⃣  Attendez que Docker redémarre (30 secondes)" -ForegroundColor Cyan
Write-Host ""

Write-Host "6️⃣  Relancez ce script pour vérifier : .\configure-docker-dns.ps1" -ForegroundColor Cyan
Write-Host ""

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Proposer d'ouvrir le fichier de documentation
Write-Host "📚 Pour plus de détails, consultez : fix-docker-dns.md" -ForegroundColor Cyan
Write-Host ""

$openDoc = Read-Host "Voulez-vous ouvrir la documentation complète ? (O/N)"
if ($openDoc -eq "O" -or $openDoc -eq "o") {
    if (Test-Path "fix-docker-dns.md") {
        Start-Process "fix-docker-dns.md"
    } else {
        Write-Host "❌ Fichier fix-docker-dns.md introuvable" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🆘 Besoin d'aide ?" -ForegroundColor Yellow
Write-Host "   - Consultez fix-docker-dns.md pour toutes les solutions" -ForegroundColor White
Write-Host "   - Redémarrez votre ordinateur après configuration DNS" -ForegroundColor White
Write-Host "   - Vérifiez que votre pare-feu autorise Docker Desktop" -ForegroundColor White
Write-Host ""
