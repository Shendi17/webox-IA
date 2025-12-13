# Script d'initialisation du frontend React
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           INITIALISATION FRONTEND REACT - WEBOX              ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎨 Création du projet React avec Vite..." -ForegroundColor Cyan
Write-Host ""

# Vérifier si le dossier frontend existe déjà
if (Test-Path "frontend") {
    Write-Host "⚠️  Le dossier 'frontend' existe déjà" -ForegroundColor Yellow
    $choice = Read-Host "Voulez-vous le supprimer et recréer ? (O/N)"
    
    if ($choice -eq "O" -or $choice -eq "o") {
        Remove-Item -Recurse -Force "frontend"
        Write-Host "✅ Dossier supprimé" -ForegroundColor Green
    } else {
        Write-Host "❌ Opération annulée" -ForegroundColor Red
        pause
        exit
    }
}

Write-Host ""
Write-Host "📦 Création du projet avec Vite..." -ForegroundColor Cyan
Write-Host "   (Cela peut prendre quelques minutes)" -ForegroundColor Yellow
Write-Host ""

# Créer le projet React avec Vite
npm create vite@latest frontend -- --template react

Write-Host ""
Write-Host "✅ Projet React créé !" -ForegroundColor Green
Write-Host ""

# Installer les dépendances
Write-Host "📦 Installation des dépendances..." -ForegroundColor Cyan
Set-Location frontend
npm install

Write-Host ""
Write-Host "📦 Installation des dépendances supplémentaires..." -ForegroundColor Cyan

# Installer TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Installer les bibliothèques utiles
npm install axios react-router-dom lucide-react

Write-Host ""
Write-Host "✅ Dépendances installées !" -ForegroundColor Green
Write-Host ""

Set-Location ..

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Frontend React initialisé avec succès !" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Technologies installées :" -ForegroundColor Cyan
Write-Host "  - React 18" -ForegroundColor White
Write-Host "  - Vite (build tool)" -ForegroundColor White
Write-Host "  - TailwindCSS (styling)" -ForegroundColor White
Write-Host "  - Axios (HTTP client)" -ForegroundColor White
Write-Host "  - React Router (navigation)" -ForegroundColor White
Write-Host "  - Lucide React (icons)" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Configurer TailwindCSS" -ForegroundColor White
Write-Host "  2. Créer les composants Chat" -ForegroundColor White
Write-Host "  3. Configurer Axios pour l'API" -ForegroundColor White
Write-Host "  4. Lancer le serveur de développement" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
