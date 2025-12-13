# Script de réparation complète WSL pour Docker
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     RÉPARATION COMPLÈTE WSL POUR DOCKER                        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    Write-Host ""
    Write-Host "Clic droit sur PowerShell → Exécuter en tant qu'administrateur" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "✅ Exécution en tant qu'administrateur" -ForegroundColor Green
Write-Host ""

# Étape 1 : Arrêter Docker Desktop
Write-Host "Étape 1 : Arrêt de Docker Desktop..." -ForegroundColor Cyan
Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "✅ Docker Desktop arrêté" -ForegroundColor Green
Write-Host ""

# Étape 2 : Arrêter tous les services WSL
Write-Host "Étape 2 : Arrêt des services WSL..." -ForegroundColor Cyan
Stop-Service -Name LxssManager -Force -ErrorAction SilentlyContinue
Stop-Service -Name vmcompute -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "✅ Services arrêtés" -ForegroundColor Green
Write-Host ""

# Étape 3 : Configurer les services
Write-Host "Étape 3 : Configuration des services..." -ForegroundColor Cyan

# LxssManager
Write-Host "   Configuration LxssManager..." -ForegroundColor Yellow
sc.exe config LxssManager start= demand
Set-Service -Name LxssManager -StartupType Manual -ErrorAction SilentlyContinue

# vmcompute
Write-Host "   Configuration vmcompute..." -ForegroundColor Yellow
sc.exe config vmcompute start= demand
Set-Service -Name vmcompute -StartupType Manual -ErrorAction SilentlyContinue

# HvHost
Write-Host "   Configuration HvHost..." -ForegroundColor Yellow
sc.exe config HvHost start= demand
Set-Service -Name HvHost -StartupType Manual -ErrorAction SilentlyContinue

Write-Host "✅ Services configurés" -ForegroundColor Green
Write-Host ""

# Étape 4 : Démarrer les services
Write-Host "Étape 4 : Démarrage des services..." -ForegroundColor Cyan

Write-Host "   Démarrage LxssManager..." -ForegroundColor Yellow
Start-Service -Name LxssManager -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "   Démarrage vmcompute..." -ForegroundColor Yellow
Start-Service -Name vmcompute -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "✅ Services démarrés" -ForegroundColor Green
Write-Host ""

# Étape 5 : Vérifier l'état
Write-Host "Étape 5 : Vérification..." -ForegroundColor Cyan
Write-Host ""

$lxss = Get-Service -Name LxssManager -ErrorAction SilentlyContinue
$vmcomp = Get-Service -Name vmcompute -ErrorAction SilentlyContinue

Write-Host "   LxssManager : " -NoNewline
if ($lxss.Status -eq "Running") {
    Write-Host "✅ Running" -ForegroundColor Green
} else {
    Write-Host "❌ $($lxss.Status)" -ForegroundColor Red
}

Write-Host "   vmcompute   : " -NoNewline
if ($vmcomp.Status -eq "Running") {
    Write-Host "✅ Running" -ForegroundColor Green
} else {
    Write-Host "❌ $($vmcomp.Status)" -ForegroundColor Red
}

Write-Host ""

# Étape 6 : Tester WSL
Write-Host "Étape 6 : Test WSL..." -ForegroundColor Cyan
$wslTest = wsl --status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ WSL fonctionne !" -ForegroundColor Green
    Write-Host ""
    Write-Host $wslTest
} else {
    Write-Host "⚠️  WSL ne répond pas encore" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""

if ($lxss.Status -eq "Running") {
    Write-Host "✅ RÉPARATION RÉUSSIE !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaines étapes :" -ForegroundColor Cyan
    Write-Host "  1. Attendre 10 secondes" -ForegroundColor White
    Write-Host "  2. Lancer Docker Desktop" -ForegroundColor White
    Write-Host "  3. Attendre que Docker démarre complètement" -ForegroundColor White
    Write-Host "  4. Exécuter : .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Voulez-vous lancer Docker Desktop maintenant ? (O/N)"
    if ($launch -eq "O" -or $launch -eq "o") {
        Write-Host ""
        Write-Host "Lancement de Docker Desktop..." -ForegroundColor Cyan
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        Write-Host "✅ Docker Desktop lancé" -ForegroundColor Green
        Write-Host ""
        Write-Host "Attendez que Docker soit complètement démarré (icône verte)" -ForegroundColor Yellow
        Write-Host "Puis exécutez : .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Le service LxssManager n'a pas démarré" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solutions alternatives :" -ForegroundColor Yellow
    Write-Host "  1. Redémarrer Windows et réessayer" -ForegroundColor White
    Write-Host "  2. Vérifier les logs : Observateur d'événements → Windows → System" -ForegroundColor White
    Write-Host "  3. Réinstaller WSL : wsl --unregister docker-desktop puis wsl --install" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
