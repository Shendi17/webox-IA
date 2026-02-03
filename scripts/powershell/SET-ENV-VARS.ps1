# Script pour définir les variables d'environnement système
# Date : 31 Octobre 2025

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     CONFIGURATION VARIABLES D'ENVIRONNEMENT - WEBOX            " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Définir les variables d'environnement pour la session PowerShell actuelle
$env:PGCLIENTENCODING = "UTF8"
$env:PGPASSWORD = "VotreMotDePasseSecurise123!"
$env:PGUSER = "webox_user"
$env:PGDATABASE = "webox_db"
$env:PGHOST = "localhost"
$env:PGPORT = "5432"

Write-Host "Variables d'environnement PostgreSQL définies :" -ForegroundColor Green
Write-Host "  PGCLIENTENCODING = UTF8" -ForegroundColor White
Write-Host "  PGUSER = webox_user" -ForegroundColor White
Write-Host "  PGDATABASE = webox_db" -ForegroundColor White
Write-Host "  PGHOST = localhost" -ForegroundColor White
Write-Host "  PGPORT = 5432" -ForegroundColor White
Write-Host ""

# Lancer le backend
Write-Host "Lancement du backend FastAPI..." -ForegroundColor Cyan
Write-Host ""

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
