# Script pour vérifier la configuration système
# Date : 31 Octobre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     VÉRIFICATION SYSTÈME - WSL & VIRTUALISATION                " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "1. Version de Windows" -ForegroundColor Cyan
Write-Host "   " -NoNewline
$osInfo = Get-CimInstance -ClassName Win32_OperatingSystem
Write-Host "$($osInfo.Caption) - Build $($osInfo.BuildNumber)" -ForegroundColor White
Write-Host ""

Write-Host "2. Édition de Windows" -ForegroundColor Cyan
Write-Host "   " -NoNewline
Write-Host "$($osInfo.OperatingSystemSKU)" -ForegroundColor White
$isHome = $osInfo.Caption -like "*Home*"
if ($isHome) {
    Write-Host "   ⚠️  Windows Home détecté - Hyper-V non disponible" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ Édition compatible avec Hyper-V" -ForegroundColor Green
}
Write-Host ""

Write-Host "3. Virtualisation" -ForegroundColor Cyan
$cpu = Get-CimInstance -ClassName Win32_Processor
$virtEnabled = $cpu.VirtualizationFirmwareEnabled
Write-Host "   " -NoNewline
if ($virtEnabled) {
    Write-Host "✅ Virtualisation activée dans le BIOS" -ForegroundColor Green
} else {
    Write-Host "❌ Virtualisation DÉSACTIVÉE dans le BIOS" -ForegroundColor Red
    Write-Host "   Vous devez activer VT-x/AMD-V dans le BIOS" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "4. Service LxssManager (WSL)" -ForegroundColor Cyan
$lxssService = Get-Service -Name LxssManager -ErrorAction SilentlyContinue
if ($lxssService) {
    Write-Host "   État : $($lxssService.Status)" -ForegroundColor White
    Write-Host "   Démarrage : $($lxssService.StartType)" -ForegroundColor White
    
    if ($lxssService.StartType -eq "Disabled") {
        Write-Host "   ❌ Service DÉSACTIVÉ" -ForegroundColor Red
    } elseif ($lxssService.Status -eq "Running") {
        Write-Host "   ✅ Service en cours d'exécution" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Service arrêté mais pas désactivé" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Service NON INSTALLÉ" -ForegroundColor Red
}
Write-Host ""

Write-Host "5. Fonctionnalités Windows" -ForegroundColor Cyan

# WSL
$wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -ErrorAction SilentlyContinue
Write-Host "   WSL : " -NoNewline
if ($wslFeature -and $wslFeature.State -eq "Enabled") {
    Write-Host "✅ Activé" -ForegroundColor Green
} else {
    Write-Host "❌ Désactivé" -ForegroundColor Red
}

# VM Platform
$vmFeature = Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -ErrorAction SilentlyContinue
Write-Host "   VM Platform : " -NoNewline
if ($vmFeature -and $vmFeature.State -eq "Enabled") {
    Write-Host "✅ Activé" -ForegroundColor Green
} else {
    Write-Host "❌ Désactivé" -ForegroundColor Red
}

# Hyper-V
$hvFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue
Write-Host "   Hyper-V : " -NoNewline
if ($hvFeature -and $hvFeature.State -eq "Enabled") {
    Write-Host "✅ Activé" -ForegroundColor Green
} elseif ($isHome) {
    Write-Host "⚠️  Non disponible (Windows Home)" -ForegroundColor Yellow
} else {
    Write-Host "❌ Désactivé" -ForegroundColor Red
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

# Recommandations
Write-Host "RECOMMANDATIONS :" -ForegroundColor Cyan
Write-Host ""

if (-not $virtEnabled) {
    Write-Host "❌ BLOQUANT : Virtualisation désactivée dans le BIOS" -ForegroundColor Red
    Write-Host "   Solution : Redémarrer et activer VT-x/AMD-V dans le BIOS" -ForegroundColor Yellow
    Write-Host ""
}

if ($isHome) {
    Write-Host "⚠️  Windows Home détecté" -ForegroundColor Yellow
    Write-Host "   WSL 2 fonctionne sur Home, mais pas Hyper-V complet" -ForegroundColor White
    Write-Host "   Docker Desktop devrait fonctionner avec WSL 2" -ForegroundColor White
    Write-Host ""
}

$hasIssues = $false

if ($lxssService -and $lxssService.StartType -eq "Disabled") {
    Write-Host "⚠️  Service WSL désactivé" -ForegroundColor Yellow
    Write-Host "   Solution : Exécuter FIX-WSL-SERVICE.ps1" -ForegroundColor White
    $hasIssues = $true
}

if ($wslFeature -and $wslFeature.State -ne "Enabled") {
    Write-Host "⚠️  Fonctionnalité WSL désactivée" -ForegroundColor Yellow
    Write-Host "   Solution : Exécuter FIX-WSL-SERVICE.ps1" -ForegroundColor White
    $hasIssues = $true
}

if ($vmFeature -and $vmFeature.State -ne "Enabled") {
    Write-Host "⚠️  Plateforme VM désactivée" -ForegroundColor Yellow
    Write-Host "   Solution : Exécuter FIX-WSL-SERVICE.ps1" -ForegroundColor White
    $hasIssues = $true
}

if (-not $hasIssues -and $virtEnabled) {
    Write-Host "✅ Système correctement configuré pour WSL/Docker !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaine étape : wsl --install -d Ubuntu" -ForegroundColor Cyan
}

if (-not $virtEnabled -or ($hasIssues -and -not $isHome)) {
    Write-Host ""
    Write-Host "ALTERNATIVE : Utiliser SQLite au lieu de PostgreSQL Docker" -ForegroundColor Yellow
    Write-Host "   Avantage : Fonctionne sans virtualisation" -ForegroundColor White
    Write-Host "   Temps : 2 minutes de configuration" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
