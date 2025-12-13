# Script pour activer WSL (Windows Subsystem for Linux)
# Date : 31 Octobre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     ACTIVATION WSL - WINDOWS SUBSYSTEM FOR LINUX               " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pour exécuter en tant qu'administrateur :" -ForegroundColor Yellow
    Write-Host "  1. Clic droit sur PowerShell" -ForegroundColor White
    Write-Host "  2. Sélectionner 'Exécuter en tant qu'administrateur'" -ForegroundColor White
    Write-Host "  3. Naviguer vers le dossier scripts" -ForegroundColor White
    Write-Host "  4. Exécuter : .\ACTIVER-WSL.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "✅ Script exécuté en tant qu'administrateur" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 1 : Activation de WSL..." -ForegroundColor Cyan
Write-Host ""

# Activer WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

Write-Host ""
Write-Host "Étape 2 : Activation de la plateforme de machine virtuelle..." -ForegroundColor Cyan
Write-Host ""

# Activer la plateforme de machine virtuelle
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ WSL et la plateforme VM sont maintenant activés !" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANT : Vous DEVEZ redémarrer Windows maintenant" -ForegroundColor Yellow
Write-Host ""
Write-Host "Après le redémarrage :" -ForegroundColor Cyan
Write-Host "  1. Ouvrir PowerShell en administrateur" -ForegroundColor White
Write-Host "  2. Exécuter : wsl --install" -ForegroundColor White
Write-Host "  3. Redémarrer à nouveau" -ForegroundColor White
Write-Host "  4. Lancer Docker Desktop" -ForegroundColor White
Write-Host "  5. Exécuter le script INSTALLER-DOCKER-POSTGRESQL.ps1" -ForegroundColor White
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
