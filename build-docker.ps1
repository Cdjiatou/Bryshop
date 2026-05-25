# Script de build Docker pour BryShop (Windows PowerShell)
# Usage: .\build-docker.ps1 [version]

param(
    [string]$Version = "latest"
)

$ImageName = "bryshop"
$BuildDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

try {
    $VcsRef = git rev-parse --short HEAD 2>$null
} catch {
    $VcsRef = "unknown"
}

Write-Host "🐳 Building Docker image: $ImageName:$Version" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Build l'image
docker build `
    --tag "${ImageName}:${Version}" `
    --tag "${ImageName}:latest" `
    --build-arg BUILD_DATE=$BuildDate `
    --build-arg VCS_REF=$VcsRef `
    .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Image details:" -ForegroundColor Yellow
    docker images $ImageName:$Version
    Write-Host ""
    Write-Host "🚀 To run the image:" -ForegroundColor Yellow
    Write-Host "   docker-compose up -d" -ForegroundColor White
    Write-Host ""
    Write-Host "   OR" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   docker run -d -p 8000:8000 --name bryshop_web ${ImageName}:${Version}" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
