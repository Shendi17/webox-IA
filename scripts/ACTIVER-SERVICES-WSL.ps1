# Script pour activer les services WSL
# Date : 31 Octobre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     ACTIVATION DES SERVICES WSL                                " -ForegroundColor Cyan
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

Write-Host "✅ Script exécuté en tant qu'administrateur" -ForegroundColor Green
Write-Host ""

# Activer les services nécessaires
Write-Host "Activation des services WSL..." -ForegroundColor Cyan
Write-Host ""

# Service LxssManager (WSL)
Write-Host "1. Activation du service LxssManager..." -ForegroundColor Yellow
Set-Service -Name LxssManager -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service -Name LxssManager -ErrorAction SilentlyContinue

# Service vmcompute (Hyper-V)
Write-Host "2. Activation du service vmcompute..." -ForegroundColor Yellow
Set-Service -Name vmcompute -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service -Name vmcompute -ErrorAction SilentlyContinue

# Service HvHost (Hyper-V Host)
Write-Host "3. Activation du service HvHost..." -ForegroundColor Yellow
Set-Service -Name HvHost -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service -Name HvHost -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "✅ Services activés" -ForegroundColor Green
Write-Host ""

# Activer les fonctionnalités Windows
Write-Host "Activation des fonctionnalités Windows..." -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Activation de WSL..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

Write-Host ""
Write-Host "2. Activation de la plateforme de machine virtuelle..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Write-Host ""
Write-Host "3. Activation de Hyper-V..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Configuration terminée !" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  VOUS DEVEZ REDÉMARRER WINDOWS MAINTENANT" -ForegroundColor Yellow
Write-Host ""
Write-Host "Après le redémarrage :" -ForegroundColor Cyan
Write-Host "  1. Ouvrir PowerShell en administrateur" -ForegroundColor White
Write-Host "  2. Exécuter : wsl --install -d Ubuntu" -ForegroundColor White
Write-Host "  3. Attendre l'installation (5-10 min)" -ForegroundColor White
Write-Host "  4. Créer un utilisateur Linux quand demandé" -ForegroundColor White
Write-Host "  5. Lancer Docker Desktop" -ForegroundColor White
Write-Host ""

$reboot = Read-Host "Voulez-vous redémarrer maintenant ? (O/N)"

if ($reboot -eq "O" -or $reboot -eq "o") {
    Write-Host ""
    Write-Host "Redémarrage dans 10 secondes..." -ForegroundColor Yellow
    Write-Host "Appuyez sur Ctrl+C pour annuler" -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    Restart-Computer -Force
} else {
    Write-Host ""
    Write-Host "N'oubliez pas de redémarrer Windows avant de continuer !" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
