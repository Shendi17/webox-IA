# ============================================
# SETUP COMPLET IA - AUTOMATIQUE
# ============================================
# Ce script fait tout automatiquement :
# 1. Installe les packages
# 2. Configure Gemini Pro (gratuit)
# 3. Démarre le serveur
# 4. Teste les IA
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLET IA - WEBOX STUDIO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Ce script va :" -ForegroundColor Yellow
Write-Host "1. Installer tous les packages IA" -ForegroundColor White
Write-Host "2. Te guider pour configurer Gemini Pro (GRATUIT)" -ForegroundColor White
Write-Host "3. Démarrer le serveur" -ForegroundColor White
Write-Host "4. Tester les IA" -ForegroundColor White
Write-Host ""
Write-Host "Veux-tu continuer ? (O/N)" -ForegroundColor Yellow
$continue = Read-Host

if ($continue -ne "O" -and $continue -ne "o") {
    Write-Host "✗ Annulé." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ÉTAPE 1/4 : INSTALLATION DES PACKAGES" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Exécuter INSTALLER-IA.ps1
& ".\INSTALLER-IA.ps1"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ÉTAPE 2/4 : CONFIGURATION GEMINI PRO" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Veux-tu configurer Gemini Pro maintenant ? (GRATUIT, recommandé)" -ForegroundColor Yellow
Write-Host "(Tu pourras ajouter d'autres IA plus tard)" -ForegroundColor Gray
$configGemini = Read-Host "(O/N)"

if ($configGemini -eq "O" -or $configGemini -eq "o") {
    & ".\CONFIGURER-GEMINI.ps1"
} else {
    Write-Host "⚠️  Gemini Pro non configuré." -ForegroundColor Yellow
    Write-Host "Tu peux le faire plus tard avec : .\CONFIGURER-GEMINI.ps1" -ForegroundColor Gray
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ÉTAPE 3/4 : DÉMARRAGE DU SERVEUR" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Veux-tu démarrer le serveur maintenant ? (O/N)" -ForegroundColor Yellow
$startServer = Read-Host

if ($startServer -eq "O" -or $startServer -eq "o") {
    Write-Host ""
    Write-Host "Démarrage du serveur..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python main.py"
    Write-Host "✓ Serveur démarré dans une nouvelle fenêtre !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Attends 5 secondes que le serveur démarre..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
} else {
    Write-Host "⚠️  Serveur non démarré." -ForegroundColor Yellow
    Write-Host "Démarre-le manuellement avec : python main.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  ÉTAPE 4/4 : TEST DES IA" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Veux-tu tester les IA maintenant ? (O/N)" -ForegroundColor Yellow
$testAI = Read-Host

if ($testAI -eq "O" -or $testAI -eq "o") {
    Write-Host ""
    Start-Sleep -Seconds 2
    & ".\TESTER-IA.ps1"
} else {
    Write-Host ""
    Write-Host "✓ Setup terminé !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour tester plus tard : .\TESTER-IA.ps1" -ForegroundColor Gray
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SETUP TERMINÉ !" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tu peux maintenant utiliser le Studio Web IA :" -ForegroundColor Cyan
Write-Host "http://localhost:8000/projects/2/editor" -ForegroundColor White
Write-Host ""
Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
