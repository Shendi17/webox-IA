# Script pour démarrer le service WSL
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     DÉMARRAGE SERVICE WSL                                      " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "✅ Virtualisation activée détectée" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 1 : Configuration du service LxssManager..." -ForegroundColor Cyan

# Configurer le service en automatique
try {
    Set-Service -Name LxssManager -StartupType Automatic
    Write-Host "✅ Service configuré en Automatique" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Erreur lors de la configuration : $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Étape 2 : Démarrage du service..." -ForegroundColor Cyan

# Démarrer le service
try {
    Start-Service -Name LxssManager
    Write-Host "✅ Service démarré" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Erreur lors du démarrage : $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Étape 3 : Vérification..." -ForegroundColor Cyan

$service = Get-Service -Name LxssManager
Write-Host "   État : $($service.Status)" -ForegroundColor White
Write-Host "   Type de démarrage : $($service.StartType)" -ForegroundColor White

Write-Host ""

if ($service.Status -eq "Running") {
    Write-Host "✅ Service WSL en cours d'exécution !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Vous pouvez maintenant :" -ForegroundColor Cyan
    Write-Host "  1. Installer Ubuntu : wsl --install -d Ubuntu" -ForegroundColor White
    Write-Host "  2. Ou lancer Docker Desktop directement" -ForegroundColor White
} else {
    Write-Host "❌ Le service n'a pas pu démarrer" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vérifiez les logs d'événements Windows pour plus d'infos" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative : Utiliser SQLite au lieu de PostgreSQL Docker" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
