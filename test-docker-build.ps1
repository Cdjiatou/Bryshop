# Script de test du build Docker - BryShop
# Ce script vérifie que le build Docker fonctionne correctement

Write-Host "🐳 Test du Build Docker - BryShop" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Étape 1 : Vérifier que Docker est installé et démarré
Write-Host "📋 Étape 1/5 : Vérification de Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker installé : $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker n'est pas installé ou n'est pas démarré !" -ForegroundColor Red
    Write-Host "   Veuillez installer Docker Desktop et le démarrer." -ForegroundColor Red
    exit 1
}

# Vérifier que Docker daemon est accessible
try {
    docker ps | Out-Null
    Write-Host "✅ Docker daemon accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon n'est pas accessible !" -ForegroundColor Red
    Write-Host "   Veuillez démarrer Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Étape 2 : Nettoyer les anciennes images (optionnel)
Write-Host "📋 Étape 2/5 : Nettoyage des anciennes images..." -ForegroundColor Yellow
$oldImages = docker images bryshop -q
if ($oldImages) {
    Write-Host "🗑️  Suppression des anciennes images bryshop..." -ForegroundColor Yellow
    docker rmi -f $oldImages 2>$null
    Write-Host "✅ Anciennes images supprimées" -ForegroundColor Green
} else {
    Write-Host "✅ Aucune ancienne image à supprimer" -ForegroundColor Green
}

Write-Host ""

# Étape 3 : Build de l'image
Write-Host "📋 Étape 3/5 : Build de l'image Docker..." -ForegroundColor Yellow
Write-Host "⏳ Cela peut prendre 5-10 minutes la première fois..." -ForegroundColor Cyan
Write-Host ""

$buildStart = Get-Date

docker build -t bryshop:test .

if ($LASTEXITCODE -eq 0) {
    $buildEnd = Get-Date
    $buildDuration = ($buildEnd - $buildStart).TotalSeconds
    Write-Host ""
    Write-Host "✅ Build réussi en $([math]::Round($buildDuration, 2)) secondes !" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Le build a échoué !" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Étape 4 : Vérifier la taille de l'image
Write-Host "📋 Étape 4/5 : Vérification de la taille de l'image..." -ForegroundColor Yellow

$imageInfo = docker images bryshop:test --format "{{.Size}}"
Write-Host "📊 Taille de l'image : $imageInfo" -ForegroundColor Cyan

# Extraire la taille en MB
$sizeValue = [regex]::Match($imageInfo, '(\d+\.?\d*)').Value
$sizeUnit = [regex]::Match($imageInfo, '[A-Z]+').Value

if ($sizeUnit -eq "GB") {
    $sizeMB = [double]$sizeValue * 1024
} elseif ($sizeUnit -eq "MB") {
    $sizeMB = [double]$sizeValue
} else {
    $sizeMB = 0
}

if ($sizeMB -gt 0 -and $sizeMB -lt 500) {
    Write-Host "✅ Taille OK (< 500 MB)" -ForegroundColor Green
} elseif ($sizeMB -ge 500) {
    Write-Host "⚠️  Attention : L'image dépasse 500 MB !" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Impossible de déterminer la taille" -ForegroundColor Yellow
}

Write-Host ""

# Étape 5 : Test de démarrage du conteneur
Write-Host "📋 Étape 5/5 : Test de démarrage du conteneur..." -ForegroundColor Yellow

# Arrêter et supprimer le conteneur de test s'il existe
docker stop bryshop_test 2>$null | Out-Null
docker rm bryshop_test 2>$null | Out-Null

Write-Host "🚀 Démarrage du conteneur de test..." -ForegroundColor Cyan

docker run -d `
    --name bryshop_test `
    -p 8001:8000 `
    -e DEBUG=True `
    -e DATABASE_HOST=localhost `
    -e DATABASE_NAME=BryshopDB `
    -e DATABASE_USER=postgres `
    -e DATABASE_PASSWORD= `
    bryshop:test

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Conteneur démarré avec succès" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "⏳ Attente de 10 secondes pour que l'application démarre..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    # Vérifier les logs
    Write-Host ""
    Write-Host "📋 Logs du conteneur (dernières 20 lignes) :" -ForegroundColor Yellow
    docker logs --tail 20 bryshop_test
    
    Write-Host ""
    Write-Host "🧹 Nettoyage du conteneur de test..." -ForegroundColor Yellow
    docker stop bryshop_test | Out-Null
    docker rm bryshop_test | Out-Null
    Write-Host "✅ Conteneur de test supprimé" -ForegroundColor Green
} else {
    Write-Host "❌ Échec du démarrage du conteneur" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ TOUS LES TESTS SONT PASSÉS !" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Résumé :" -ForegroundColor Yellow
Write-Host "   - Image créée : bryshop:test" -ForegroundColor White
Write-Host "   - Taille : $imageInfo" -ForegroundColor White
Write-Host "   - Temps de build : $([math]::Round($buildDuration, 2))s" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Prochaines étapes :" -ForegroundColor Yellow
Write-Host "   1. Tester avec docker-compose : docker-compose up -d" -ForegroundColor White
Write-Host "   2. Accéder à l'application : http://localhost:8000" -ForegroundColor White
Write-Host "   3. Pousser vers GitHub pour déclencher le CI/CD" -ForegroundColor White
Write-Host ""
