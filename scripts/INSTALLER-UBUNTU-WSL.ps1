# Script pour installer Ubuntu WSL avec service forcé
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     INSTALLATION UBUNTU WSL - SERVICE FORCÉ                    " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "Étape 1 : Forcer le démarrage du service LxssManager..." -ForegroundColor Cyan

# Forcer via sc.exe
sc.exe config LxssManager start= demand
sc.exe start LxssManager

Start-Sleep -Seconds 2

# Vérifier
$service = Get-Service -Name LxssManager -ErrorAction SilentlyContinue
Write-Host "   État du service : $($service.Status)" -ForegroundColor White

if ($service.Status -ne "Running") {
    Write-Host "   Tentative de démarrage via PowerShell..." -ForegroundColor Yellow
    Start-Service -Name LxssManager -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    $service = Get-Service -Name LxssManager
}

if ($service.Status -eq "Running") {
    Write-Host "✅ Service LxssManager démarré" -ForegroundColor Green
} else {
    Write-Host "❌ Impossible de démarrer le service" -ForegroundColor Red
    Write-Host ""
    Write-Host "Le service est peut-être bloqué par une politique système." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Solution alternative : Télécharger Ubuntu depuis le Microsoft Store" -ForegroundColor Cyan
    Write-Host "   1. Ouvrir le Microsoft Store" -ForegroundColor White
    Write-Host "   2. Rechercher 'Ubuntu'" -ForegroundColor White
    Write-Host "   3. Installer 'Ubuntu 22.04 LTS' ou 'Ubuntu'" -ForegroundColor White
    Write-Host "   4. Lancer Ubuntu depuis le menu Démarrer" -ForegroundColor White
    Write-Host "   5. Créer un utilisateur Linux" -ForegroundColor White
    Write-Host ""
    
    $openStore = Read-Host "Voulez-vous ouvrir le Microsoft Store maintenant ? (O/N)"
    if ($openStore -eq "O" -or $openStore -eq "o") {
        Start-Process "ms-windows-store://pdp/?ProductId=9PN20MSR04DW"
    }
    
    exit
}

Write-Host ""
Write-Host "Étape 2 : Installation d'Ubuntu via wsl --install..." -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ Installation en cours (5-10 minutes)..." -ForegroundColor Yellow
Write-Host ""

# Installer Ubuntu
$installOutput = wsl --install -d Ubuntu --no-launch 2>&1

if ($LASTEXITCODE -eq 0 -or $installOutput -like "*déjà installé*" -or $installOutput -like "*already installed*") {
    Write-Host ""
    Write-Host "✅ Ubuntu WSL installé !" -ForegroundColor Green
    Write-Host ""
    
    # Configurer WSL 2
    Write-Host "Étape 3 : Configuration WSL 2..." -ForegroundColor Cyan
    wsl --set-default-version 2 2>$null
    Write-Host "✅ WSL 2 configuré" -ForegroundColor Green
    Write-Host ""
    
    # Lister les distributions
    Write-Host "Distributions WSL installées :" -ForegroundColor Cyan
    wsl --list --verbose
    Write-Host ""
    
    Write-Host "================================================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ INSTALLATION RÉUSSIE !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaines étapes :" -ForegroundColor Cyan
    Write-Host "  1. Lancer Docker Desktop" -ForegroundColor White
    Write-Host "  2. Docker va créer ses distributions WSL automatiquement" -ForegroundColor White
    Write-Host "  3. Attendre que Docker soit prêt (icône verte)" -ForegroundColor White
    Write-Host "  4. Exécuter : .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Voulez-vous lancer Docker Desktop maintenant ? (O/N)"
    if ($launch -eq "O" -or $launch -eq "o") {
        Write-Host ""
        Write-Host "Lancement de Docker Desktop..." -ForegroundColor Cyan
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        Write-Host "✅ Docker Desktop lancé" -ForegroundColor Green
        Write-Host ""
        Write-Host "⏳ Attendez 1-2 minutes que Docker démarre..." -ForegroundColor Yellow
    }
    
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors de l'installation" -ForegroundColor Red
    Write-Host ""
    Write-Host "Message d'erreur :" -ForegroundColor Yellow
    Write-Host $installOutput
    Write-Host ""
    Write-Host "Solution alternative : Microsoft Store" -ForegroundColor Cyan
    Write-Host "   1. Ouvrir le Microsoft Store" -ForegroundColor White
    Write-Host "   2. Rechercher 'Ubuntu'" -ForegroundColor White
    Write-Host "   3. Installer 'Ubuntu 22.04 LTS'" -ForegroundColor White
    Write-Host ""
    
    $openStore = Read-Host "Voulez-vous ouvrir le Microsoft Store ? (O/N)"
    if ($openStore -eq "O" -or $openStore -eq "o") {
        Start-Process "ms-windows-store://pdp/?ProductId=9PN20MSR04DW"
    }
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
