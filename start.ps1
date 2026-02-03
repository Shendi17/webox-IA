#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script de démarrage rapide pour WeBox Multi-IA

.DESCRIPTION
    Active l'environnement virtuel Python 3.11 et démarre le serveur uvicorn
    sur http://webox.local:8000

.EXAMPLE
    .\start.ps1
#>

Write-Host "🚀 Démarrage de WeBox Multi-IA..." -ForegroundColor Cyan
Write-Host ""

# Vérifier que le .venv existe
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Erreur: Environnement virtuel .venv introuvable" -ForegroundColor Red
    Write-Host "Exécutez d'abord: py -3.11 -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Activer l'environnement virtuel
Write-Host "📦 Activation de l'environnement virtuel..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

# Vérifier la version Python
$pythonVersion = python --version
Write-Host "🐍 $pythonVersion" -ForegroundColor Green

# Vérifier que les dépendances sont installées
Write-Host "🔍 Vérification des dépendances..." -ForegroundColor Green
$uvicornInstalled = python -c "import uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Dépendances manquantes. Installation en cours..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erreur lors de l'installation des dépendances" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Tout est prêt!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Démarrage du serveur sur:" -ForegroundColor Cyan
Write-Host "   - http://webox.local:8000/" -ForegroundColor White
Write-Host "   - http://localhost:8000/" -ForegroundColor White
Write-Host "   - http://127.0.0.1:8000/" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation API: http://webox.local:8000/docs" -ForegroundColor Cyan
Write-Host "🏥 Health check: http://webox.local:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur CTRL+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

# Démarrer uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
