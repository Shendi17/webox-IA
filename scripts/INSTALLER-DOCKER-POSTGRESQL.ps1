# Script pour installer PostgreSQL avec Docker
# Date : 31 Octobre 2025

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     INSTALLATION POSTGRESQL DOCKER - WEBOX                     " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Docker Desktop est en cours d'exécution
Write-Host "Vérification de Docker Desktop..." -ForegroundColor Cyan
$dockerRunning = docker ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Docker Desktop n'est pas démarré !" -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez :" -ForegroundColor Yellow
    Write-Host "  1. Ouvrir Docker Desktop" -ForegroundColor White
    Write-Host "  2. Attendre qu'il démarre complètement" -ForegroundColor White
    Write-Host "  3. Relancer ce script" -ForegroundColor White
    Write-Host ""
    Write-Host "Appuyez sur une touche pour ouvrir Docker Desktop..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Essayer d'ouvrir Docker Desktop
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    Write-Host ""
    Write-Host "Docker Desktop en cours de démarrage..." -ForegroundColor Yellow
    Write-Host "Attendez 30 secondes puis relancez ce script." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "✅ Docker Desktop est en cours d'exécution" -ForegroundColor Green
Write-Host ""

# Arrêter et supprimer l'ancien conteneur s'il existe
Write-Host "Nettoyage des anciens conteneurs..." -ForegroundColor Cyan
docker stop webox-postgres 2>$null
docker rm webox-postgres 2>$null

# Créer et démarrer le conteneur PostgreSQL
Write-Host ""
Write-Host "Création du conteneur PostgreSQL..." -ForegroundColor Cyan
Write-Host ""

docker run --name webox-postgres `
  -e POSTGRES_USER=webox_user `
  -e POSTGRES_PASSWORD=admin123 `
  -e POSTGRES_DB=webox_db `
  -e POSTGRES_INITDB_ARGS="--encoding=UTF8 --locale=C" `
  -p 5432:5432 `
  -d postgres:16

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ PostgreSQL Docker créé avec succès !" -ForegroundColor Green
    Write-Host ""
    
    # Attendre que PostgreSQL soit prêt
    Write-Host "Attente du démarrage de PostgreSQL..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Informations de connexion :" -ForegroundColor Cyan
    Write-Host "  Host     : localhost" -ForegroundColor White
    Write-Host "  Port     : 5432" -ForegroundColor White
    Write-Host "  Database : webox_db" -ForegroundColor White
    Write-Host "  User     : webox_user" -ForegroundColor White
    Write-Host "  Password : admin123" -ForegroundColor White
    Write-Host ""
    Write-Host "Commandes utiles :" -ForegroundColor Cyan
    Write-Host "  Démarrer  : docker start webox-postgres" -ForegroundColor White
    Write-Host "  Arrêter   : docker stop webox-postgres" -ForegroundColor White
    Write-Host "  Logs      : docker logs webox-postgres" -ForegroundColor White
    Write-Host ""
    Write-Host "Prochaine étape : Créer les tables et l'utilisateur admin" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors de la création du conteneur" -ForegroundColor Red
    Write-Host ""
}

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
