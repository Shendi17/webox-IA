# Script pour réinitialiser PostgreSQL avec un mot de passe simple
# Date : 31 Octobre 2025

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     REINITIALISATION POSTGRESQL - WEBOX                        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Ce script va :" -ForegroundColor Yellow
Write-Host "  1. Changer le mot de passe de webox_user en 'admin123'" -ForegroundColor White
Write-Host "  2. Recréer la base de données avec encodage UTF-8" -ForegroundColor White
Write-Host "  3. Créer les tables" -ForegroundColor White
Write-Host "  4. Créer l'utilisateur admin" -ForegroundColor White
Write-Host ""

$postgresPassword = Read-Host "Entrez le mot de passe de l'utilisateur 'postgres'"

Write-Host ""
Write-Host "Étape 1 : Suppression de l'ancienne base..." -ForegroundColor Cyan

$env:PGPASSWORD = $postgresPassword
psql -U postgres -c "DROP DATABASE IF EXISTS webox_db;" 2>$null
psql -U postgres -c "DROP USER IF EXISTS webox_user;" 2>$null

Write-Host "✅ Nettoyage terminé" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 2 : Création du nouvel utilisateur..." -ForegroundColor Cyan
psql -U postgres -c "CREATE USER webox_user WITH PASSWORD 'admin123';"

Write-Host "✅ Utilisateur créé" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 3 : Création de la base de données..." -ForegroundColor Cyan
psql -U postgres -c "CREATE DATABASE webox_db WITH OWNER webox_user ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"

Write-Host "✅ Base de données créée" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 4 : Attribution des privilèges..." -ForegroundColor Cyan
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE webox_db TO webox_user;"
psql -U postgres -d webox_db -c "GRANT ALL ON SCHEMA public TO webox_user;"

Write-Host "✅ Privilèges attribués" -ForegroundColor Green
Write-Host ""

Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "Nouvelles informations de connexion :" -ForegroundColor Cyan
Write-Host "  Host     : localhost" -ForegroundColor White
Write-Host "  Port     : 5432" -ForegroundColor White
Write-Host "  Database : webox_db" -ForegroundColor White
Write-Host "  User     : webox_user" -ForegroundColor White
Write-Host "  Password : admin123" -ForegroundColor White
Write-Host ""
Write-Host "Prochaine étape : Créer les tables et l'utilisateur admin" -ForegroundColor Yellow
Write-Host ""

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
