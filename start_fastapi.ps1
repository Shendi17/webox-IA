# Script de démarrage FastAPI pour WeBox Multi-IA

Write-Host "🚀 Démarrage de WeBox Multi-IA (FastAPI)..." -ForegroundColor Cyan

# Arrêter les anciens processus
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "✅ Processus nettoyés" -ForegroundColor Green

# Démarrer FastAPI
Write-Host "🌐 Lancement du serveur sur http://localhost:8000" -ForegroundColor Yellow

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

Write-Host "`n💡 Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Cyan
