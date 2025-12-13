# Script pour maintenir le service WSL actif pendant l'installation
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     MAINTIEN DU SERVICE WSL ACTIF                              " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le script est exécuté en tant qu'administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur !" -ForegroundColor Red
    exit
}

Write-Host "Ce script va maintenir le service LxssManager actif" -ForegroundColor Yellow
Write-Host "pendant que vous installez Ubuntu." -ForegroundColor Yellow
Write-Host ""
Write-Host "INSTRUCTIONS :" -ForegroundColor Cyan
Write-Host "  1. Laissez cette fenêtre OUVERTE" -ForegroundColor White
Write-Host "  2. Ouvrez le menu Démarrer" -ForegroundColor White
Write-Host "  3. Lancez Ubuntu" -ForegroundColor White
Write-Host "  4. Attendez l'installation" -ForegroundColor White
Write-Host "  5. Revenez ici et appuyez sur Ctrl+C pour arrêter" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour démarrer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Surveillance du service en cours..." -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arrêter" -ForegroundColor Yellow
Write-Host ""

$count = 0
while ($true) {
    $count++
    
    # Vérifier le service
    $service = Get-Service -Name LxssManager -ErrorAction SilentlyContinue
    
    if ($service.Status -ne "Running") {
        Write-Host "[$count] Service arrêté - Redémarrage..." -ForegroundColor Red
        
        # Redémarrer le service
        sc.exe start LxssManager 2>$null
        Start-Sleep -Seconds 1
        
        $service = Get-Service -Name LxssManager
        if ($service.Status -eq "Running") {
            Write-Host "      ✅ Service redémarré" -ForegroundColor Green
        } else {
            Write-Host "      ❌ Échec du redémarrage" -ForegroundColor Red
        }
    } else {
        Write-Host "[$count] Service actif ✅" -ForegroundColor Green
    }
    
    # Attendre 2 secondes
    Start-Sleep -Seconds 2
}
