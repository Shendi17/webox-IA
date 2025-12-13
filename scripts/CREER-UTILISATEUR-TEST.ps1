# Script pour creer un utilisateur de test
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "           CREATION UTILISATEUR TEST - WEBOX                    " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$password = Read-Host "Entrez le mot de passe de 'webox_user'"

Write-Host ""
Write-Host "Creation de l'utilisateur de test..." -ForegroundColor Cyan
Write-Host ""

# Executer le script SQL
$env:PGPASSWORD = $password
psql -U webox_user -d webox_db -f create_user.sql

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "Informations de connexion :" -ForegroundColor Cyan
Write-Host "  Email    : admin@webox.com" -ForegroundColor White
Write-Host "  Password : admin123" -ForegroundColor White
Write-Host "  Username : admin" -ForegroundColor White
Write-Host "  Role     : admin" -ForegroundColor White
Write-Host ""
Write-Host "Tu peux maintenant te connecter avec ces identifiants !" -ForegroundColor Green
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
