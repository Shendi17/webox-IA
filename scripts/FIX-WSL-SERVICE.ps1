# Script pour forcer l'activation du service WSL
# Date : 31 Octobre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     FIX SERVICE WSL - ACTIVATION FORCÉE                        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "Étape 1 : Vérification des services..." -ForegroundColor Cyan
Write-Host ""

# Vérifier le service LxssManager
$lxssService = Get-Service -Name LxssManager -ErrorAction SilentlyContinue

if ($lxssService) {
    Write-Host "Service LxssManager trouvé - État : $($lxssService.Status)" -ForegroundColor Yellow
    Write-Host "Type de démarrage : $($lxssService.StartType)" -ForegroundColor Yellow
    
    if ($lxssService.StartType -eq "Disabled") {
        Write-Host "Activation du service..." -ForegroundColor Cyan
        Set-Service -Name LxssManager -StartupType Manual
        Write-Host "✅ Service configuré en Manuel" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  Service LxssManager non trouvé" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Étape 2 : Activation via Registry..." -ForegroundColor Cyan
Write-Host ""

# Activer via le registre
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LxssManager"
if (Test-Path $regPath) {
    Set-ItemProperty -Path $regPath -Name "Start" -Value 3 -Force
    Write-Host "✅ Registre modifié (Start = 3 = Manuel)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Clé de registre non trouvée" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Étape 3 : Vérification des fonctionnalités Windows..." -ForegroundColor Cyan
Write-Host ""

# Vérifier si WSL est installé
$wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -ErrorAction SilentlyContinue

if ($wslFeature) {
    Write-Host "WSL Feature - État : $($wslFeature.State)" -ForegroundColor Yellow
    
    if ($wslFeature.State -ne "Enabled") {
        Write-Host "Activation de WSL..." -ForegroundColor Cyan
        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart
        Write-Host "✅ WSL activé" -ForegroundColor Green
    } else {
        Write-Host "✅ WSL déjà activé" -ForegroundColor Green
    }
}

# Vérifier la plateforme VM
$vmFeature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -ErrorAction SilentlyContinue

if ($vmFeature) {
    Write-Host "VM Platform - État : $($vmFeature.State)" -ForegroundColor Yellow
    
    if ($vmFeature.State -ne "Enabled") {
        Write-Host "Activation de la plateforme VM..." -ForegroundColor Cyan
        Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
        Write-Host "✅ VM Platform activé" -ForegroundColor Green
    } else {
        Write-Host "✅ VM Platform déjà activé" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Configuration terminée" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  REDÉMARRAGE OBLIGATOIRE" -ForegroundColor Yellow
Write-Host ""
Write-Host "Après le redémarrage, essayez :" -ForegroundColor Cyan
Write-Host "  wsl --install -d Ubuntu" -ForegroundColor White
Write-Host ""
Write-Host "Si ça ne fonctionne toujours pas, nous passerons à SQLite." -ForegroundColor Yellow
Write-Host ""

$reboot = Read-Host "Redémarrer maintenant ? (O/N)"

if ($reboot -eq "O" -or $reboot -eq "o") {
    Write-Host ""
    Write-Host "Redémarrage dans 10 secondes..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    Restart-Computer -Force
} else {
    Write-Host ""
    Write-Host "Redémarrez manuellement puis réessayez wsl --install" -ForegroundColor Yellow
    Write-Host ""
}
