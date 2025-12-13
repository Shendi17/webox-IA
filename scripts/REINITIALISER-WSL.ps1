# Script pour réinitialiser complètement WSL
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     RÉINITIALISATION COMPLÈTE WSL                              " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "⚠️  ATTENTION : Ce script va réinitialiser complètement WSL" -ForegroundColor Yellow
Write-Host ""
Write-Host "Cela va :" -ForegroundColor White
Write-Host "  - Arrêter Docker Desktop" -ForegroundColor White
Write-Host "  - Supprimer toutes les distributions WSL existantes" -ForegroundColor White
Write-Host "  - Nettoyer les données Docker WSL" -ForegroundColor White
Write-Host "  - Installer Ubuntu WSL" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Voulez-vous continuer ? (O/N)"
if ($confirm -ne "O" -and $confirm -ne "o") {
    Write-Host "Opération annulée" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Étape 1 : Arrêt de Docker Desktop..." -ForegroundColor Cyan
Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Write-Host "✅ Docker Desktop arrêté" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 2 : Arrêt de toutes les distributions WSL..." -ForegroundColor Cyan
wsl --shutdown
Start-Sleep -Seconds 2
Write-Host "✅ WSL arrêté" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 3 : Liste des distributions WSL..." -ForegroundColor Cyan
$distros = wsl --list --quiet 2>$null
if ($distros) {
    Write-Host "Distributions trouvées :" -ForegroundColor Yellow
    $distros | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    Write-Host ""
    
    Write-Host "Suppression des distributions..." -ForegroundColor Cyan
    foreach ($distro in $distros) {
        $distroName = $distro.Trim()
        if ($distroName) {
            Write-Host "  Suppression de $distroName..." -ForegroundColor Yellow
            wsl --unregister $distroName 2>$null
        }
    }
    Write-Host "✅ Distributions supprimées" -ForegroundColor Green
} else {
    Write-Host "✅ Aucune distribution trouvée" -ForegroundColor Green
}
Write-Host ""

Write-Host "Étape 4 : Nettoyage des données Docker..." -ForegroundColor Cyan
$dockerData = "$env:LOCALAPPDATA\Docker\wsl"
if (Test-Path $dockerData) {
    Remove-Item -Path $dockerData -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Données Docker nettoyées" -ForegroundColor Green
} else {
    Write-Host "✅ Pas de données Docker à nettoyer" -ForegroundColor Green
}
Write-Host ""

Write-Host "Étape 5 : Installation d'Ubuntu WSL..." -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ Téléchargement et installation en cours..." -ForegroundColor Yellow
Write-Host "   Cela peut prendre 5-10 minutes" -ForegroundColor Yellow
Write-Host ""

wsl --install -d Ubuntu --no-launch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Ubuntu WSL installé !" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Étape 6 : Configuration de WSL 2..." -ForegroundColor Cyan
    wsl --set-default-version 2
    Write-Host "✅ WSL 2 défini par défaut" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "================================================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ RÉINITIALISATION TERMINÉE !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaines étapes :" -ForegroundColor Cyan
    Write-Host "  1. Lancer Docker Desktop" -ForegroundColor White
    Write-Host "  2. Docker va automatiquement configurer WSL" -ForegroundColor White
    Write-Host "  3. Attendre que Docker soit complètement démarré" -ForegroundColor White
    Write-Host "  4. Exécuter : .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Voulez-vous lancer Docker Desktop maintenant ? (O/N)"
    if ($launch -eq "O" -or $launch -eq "o") {
        Write-Host ""
        Write-Host "Lancement de Docker Desktop..." -ForegroundColor Cyan
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        Write-Host ""
        Write-Host "✅ Docker Desktop lancé" -ForegroundColor Green
        Write-Host ""
        Write-Host "⏳ Attendez 1-2 minutes que Docker configure WSL..." -ForegroundColor Yellow
        Write-Host "   L'icône Docker deviendra verte quand c'est prêt" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Puis exécutez :" -ForegroundColor Cyan
        Write-Host "   cd C:\Users\Anthony\CascadeProjects\webox" -ForegroundColor White
        Write-Host "   .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors de l'installation d'Ubuntu" -ForegroundColor Red
    Write-Host ""
    Write-Host "Essayez manuellement :" -ForegroundColor Yellow
    Write-Host "   wsl --install -d Ubuntu" -ForegroundColor White
    Write-Host ""
    Write-Host "Ou téléchargez Ubuntu depuis le Microsoft Store" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
