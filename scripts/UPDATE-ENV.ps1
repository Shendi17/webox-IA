# Script pour mettre à jour le fichier .env
Write-Host "🔧 Mise à jour du fichier .env..." -ForegroundColor Cyan

$envPath = ".env"
$envExamplePath = ".env.example"

# Vérifier si .env.example existe
if (-not (Test-Path $envExamplePath)) {
    Write-Host "❌ Erreur: .env.example n'existe pas" -ForegroundColor Red
    exit 1
}

# Sauvegarder l'ancien .env si il existe
if (Test-Path $envPath) {
    $backupPath = ".env.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "💾 Sauvegarde de l'ancien .env vers $backupPath" -ForegroundColor Yellow
    Copy-Item $envPath $backupPath
}

# Copier .env.example vers .env
Write-Host "📋 Copie de .env.example vers .env..." -ForegroundColor Cyan
Copy-Item $envExamplePath $envPath -Force

Write-Host "✅ Fichier .env mis à jour avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  N'oubliez pas de remplir vos clés API dans .env" -ForegroundColor Yellow
Write-Host "   Au minimum: OPENAI_API_KEY" -ForegroundColor Yellow
Write-Host ""
Write-Host "📚 Documentation: CONFIGURATION_API.md" -ForegroundColor Cyan
