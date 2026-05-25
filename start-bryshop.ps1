# Script de démarrage rapide - BryShop
# Ce script démarre l'application complète avec Docker Compose

param(
    [switch]$Build,
    [switch]$Clean,
    [switch]$Logs
)

Write-Host "🚀 Démarrage de BryShop" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que Docker est démarré
try {
    docker ps | Out-Null
} catch {
    Write-Host "❌ Docker n'est pas démarré !" -ForegroundColor Red
    Write-Host "   Veuillez démarrer Docker Desktop." -ForegroundColor Red
    exit 1
}

# Option : Nettoyage complet
if ($Clean) {
    Write-Host "🧹 Nettoyage des conteneurs et volumes..." -ForegroundColor Yellow
    docker-compose down -v
    Write-Host "✅ Nettoyage terminé" -ForegroundColor Green
    Write-Host ""
}

# Option : Build avant de démarrer
if ($Build) {
    Write-Host "🔨 Build des images Docker..." -ForegroundColor Yellow
    docker-compose build --no-cache
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Le build a échoué !" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Build terminé" -ForegroundColor Green
    Write-Host ""
}

# Démarrer les services
Write-Host "🚀 Démarrage des services..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Services démarrés avec succès !" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "⏳ Attente de 15 secondes pour que les services démarrent..." -ForegroundColor Cyan
    Start-Sleep -Seconds 15
    
    Write-Host ""
    Write-Host "📊 État des services :" -ForegroundColor Yellow
    docker-compose ps
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "✅ BryShop est démarré !" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 Accès aux services :" -ForegroundColor Yellow
    Write-Host "   - Application Django : http://localhost:8000" -ForegroundColor White
    Write-Host "   - Kibana (Logs)      : http://localhost:5601" -ForegroundColor White
    Write-Host "   - Grafana (Métriques): http://localhost:3000 (admin/admin)" -ForegroundColor White
    Write-Host "   - Prometheus         : http://localhost:9090" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Commandes utiles :" -ForegroundColor Yellow
    Write-Host "   - Voir les logs      : docker-compose logs -f" -ForegroundColor White
    Write-Host "   - Voir logs web      : docker-compose logs -f web" -ForegroundColor White
    Write-Host "   - Arrêter            : docker-compose down" -ForegroundColor White
    Write-Host "   - Redémarrer         : docker-compose restart" -ForegroundColor White
    Write-Host ""
    
    # Option : Afficher les logs
    if ($Logs) {
        Write-Host "📋 Logs en temps réel (Ctrl+C pour quitter) :" -ForegroundColor Yellow
        Write-Host ""
        docker-compose logs -f
    }
} else {
    Write-Host "❌ Échec du démarrage des services !" -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 Logs d'erreur :" -ForegroundColor Yellow
    docker-compose logs
    exit 1
}
