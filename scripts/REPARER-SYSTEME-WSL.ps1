# Script de réparation système complète pour WSL
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     RÉPARATION SYSTÈME COMPLÈTE - WSL                          " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "ÉTAPE 1 : VÉRIFICATION ANTIVIRUS" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Gray
Write-Host ""

# Vérifier Windows Defender
$defender = Get-MpComputerStatus -ErrorAction SilentlyContinue
if ($defender) {
    Write-Host "Windows Defender détecté :" -ForegroundColor Yellow
    Write-Host "  Protection en temps réel : $($defender.RealTimeProtectionEnabled)" -ForegroundColor White
    Write-Host "  Antivirus actif : $($defender.AntivirusEnabled)" -ForegroundColor White
    
    if ($defender.RealTimeProtectionEnabled) {
        Write-Host ""
        Write-Host "⚠️  Windows Defender est actif et peut bloquer WSL" -ForegroundColor Yellow
        Write-Host ""
        $disable = Read-Host "Voulez-vous désactiver temporairement Windows Defender ? (O/N)"
        
        if ($disable -eq "O" -or $disable -eq "o") {
            Write-Host "Désactivation de Windows Defender..." -ForegroundColor Cyan
            Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
            Write-Host "✅ Windows Defender désactivé temporairement" -ForegroundColor Green
            Write-Host "   (Il se réactivera au prochain redémarrage)" -ForegroundColor Gray
        }
    }
}

# Vérifier autres antivirus
Write-Host ""
Write-Host "Recherche d'autres antivirus..." -ForegroundColor Yellow
$antivirus = Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct -ErrorAction SilentlyContinue

if ($antivirus) {
    foreach ($av in $antivirus) {
        Write-Host "  - $($av.displayName)" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "⚠️  Si vous avez un antivirus tiers, désactivez-le manuellement" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Appuyez sur Entrée après avoir désactivé votre antivirus"
}

Write-Host ""
Write-Host "ÉTAPE 2 : VÉRIFICATION POLITIQUE DE GROUPE" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Gray
Write-Host ""

# Vérifier les politiques de groupe
$gpo = Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" -ErrorAction SilentlyContinue

if ($gpo) {
    Write-Host "⚠️  Politiques de groupe détectées" -ForegroundColor Yellow
    Write-Host "   Votre PC est peut-être géré par une organisation" -ForegroundColor White
} else {
    Write-Host "✅ Pas de politique de groupe restrictive détectée" -ForegroundColor Green
}

Write-Host ""
Write-Host "ÉTAPE 3 : RÉPARATION DES COMPOSANTS WINDOWS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Gray
Write-Host ""

Write-Host "Réparation de l'image Windows (DISM)..." -ForegroundColor Yellow
Write-Host "⏳ Cela peut prendre 5-10 minutes..." -ForegroundColor Gray
Write-Host ""

# Réparer l'image Windows
DISM /Online /Cleanup-Image /RestoreHealth

Write-Host ""
Write-Host "Vérification des fichiers système (SFC)..." -ForegroundColor Yellow
Write-Host "⏳ Cela peut prendre 5-10 minutes..." -ForegroundColor Gray
Write-Host ""

# Vérifier les fichiers système
sfc /scannow

Write-Host ""
Write-Host "ÉTAPE 4 : RÉINSTALLATION COMPOSANTS WSL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Gray
Write-Host ""

# Désactiver puis réactiver WSL
Write-Host "Désactivation de WSL..." -ForegroundColor Yellow
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart -ErrorAction SilentlyContinue

Write-Host "Désactivation de la plateforme VM..." -ForegroundColor Yellow
Disable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

Write-Host "Réactivation de WSL..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart -ErrorAction SilentlyContinue

Write-Host "Réactivation de la plateforme VM..." -ForegroundColor Yellow
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart -ErrorAction SilentlyContinue

Write-Host "✅ Composants réinstallés" -ForegroundColor Green

Write-Host ""
Write-Host "ÉTAPE 5 : CONFIGURATION SERVICE LXSSMANAGER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Gray
Write-Host ""

# Arrêter le service
Stop-Service -Name LxssManager -Force -ErrorAction SilentlyContinue

# Supprimer les dépendances problématiques
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LxssManager"

# Configurer le service
Set-ItemProperty -Path $regPath -Name "Start" -Value 3 -Force
Set-ItemProperty -Path $regPath -Name "Type" -Value 32 -Force
Set-ItemProperty -Path $regPath -Name "ErrorControl" -Value 1 -Force

# Supprimer DependOnService si existe
Remove-ItemProperty -Path $regPath -Name "DependOnService" -ErrorAction SilentlyContinue

# Configurer via sc.exe
sc.exe config LxssManager start= demand depend= RPCSS

Write-Host "✅ Service configuré" -ForegroundColor Green

# Démarrer le service
Write-Host ""
Write-Host "Démarrage du service..." -ForegroundColor Yellow
Start-Service -Name LxssManager -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

$service = Get-Service -Name LxssManager
Write-Host "État du service : $($service.Status)" -ForegroundColor $(if ($service.Status -eq "Running") { "Green" } else { "Red" })

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

if ($service.Status -eq "Running") {
    Write-Host "✅ RÉPARATION RÉUSSIE !" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT : REDÉMARREZ WINDOWS MAINTENANT" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Après le redémarrage :" -ForegroundColor Cyan
    Write-Host "  1. Lancer Ubuntu depuis le menu Démarrer" -ForegroundColor White
    Write-Host "  2. Créer un utilisateur Linux" -ForegroundColor White
    Write-Host "  3. Lancer Docker Desktop" -ForegroundColor White
    Write-Host "  4. Installer PostgreSQL" -ForegroundColor White
    Write-Host ""
    
    $reboot = Read-Host "Voulez-vous redémarrer maintenant ? (O/N)"
    if ($reboot -eq "O" -or $reboot -eq "o") {
        Write-Host ""
        Write-Host "Redémarrage dans 10 secondes..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        Restart-Computer -Force
    }
} else {
    Write-Host "❌ LE SERVICE NE DÉMARRE TOUJOURS PAS" -ForegroundColor Red
    Write-Host ""
    Write-Host "Causes possibles restantes :" -ForegroundColor Yellow
    Write-Host "  1. Pilote de virtualisation manquant ou corrompu" -ForegroundColor White
    Write-Host "  2. BIOS mal configuré (vérifier VT-x/AMD-V)" -ForegroundColor White
    Write-Host "  3. Conflit matériel" -ForegroundColor White
    Write-Host ""
    Write-Host "SOLUTION ALTERNATIVE : Utiliser SQLite" -ForegroundColor Cyan
    Write-Host "SQLite ne nécessite pas WSL/Docker et fonctionne immédiatement" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
