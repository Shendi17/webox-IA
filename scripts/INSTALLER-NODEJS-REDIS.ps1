# Script d'installation Node.js et Redis
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           INSTALLATION NODE.JS & REDIS - WEBOX               ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Vérification des installations..." -ForegroundColor Cyan
Write-Host ""

# Vérifier Node.js
Write-Host "🔍 Vérification de Node.js..." -ForegroundColor Cyan
$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "  ✅ Node.js déjà installé : $nodeVersion" -ForegroundColor Green
        $nodeInstalled = $true
    }
} catch {
    Write-Host "  ⚠️  Node.js non installé" -ForegroundColor Yellow
}

Write-Host ""

# Vérifier npm
if ($nodeInstalled) {
    try {
        $npmVersion = npm --version 2>$null
        Write-Host "  ✅ npm installé : v$npmVersion" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  npm non trouvé" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

if (-not $nodeInstalled) {
    Write-Host "📥 Installation de Node.js requise" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options d'installation :" -ForegroundColor Cyan
    Write-Host "  1. Téléchargement manuel (recommandé)" -ForegroundColor White
    Write-Host "     https://nodejs.org/en/download/" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Via Chocolatey (nécessite admin)" -ForegroundColor White
    Write-Host "     choco install nodejs" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "Voulez-vous installer via Chocolatey maintenant ? (O/N)"
    
    if ($choice -eq "O" -or $choice -eq "o") {
        Write-Host ""
        Write-Host "📦 Installation de Node.js via Chocolatey..." -ForegroundColor Cyan
        Write-Host "   (Cela peut prendre quelques minutes)" -ForegroundColor Yellow
        Write-Host ""
        
        try {
            choco install nodejs -y
            Write-Host ""
            Write-Host "✅ Node.js installé avec succès !" -ForegroundColor Green
            $nodeInstalled = $true
        } catch {
            Write-Host ""
            Write-Host "❌ Erreur lors de l'installation" -ForegroundColor Red
            Write-Host "   Installez manuellement depuis https://nodejs.org/" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "📝 Veuillez installer Node.js manuellement :" -ForegroundColor Yellow
        Write-Host "   1. Ouvrir https://nodejs.org/en/download/" -ForegroundColor White
        Write-Host "   2. Télécharger la version LTS (recommandée)" -ForegroundColor White
        Write-Host "   3. Installer le fichier .msi" -ForegroundColor White
        Write-Host "   4. Redémarrer PowerShell" -ForegroundColor White
        Write-Host ""
        pause
        exit
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""

# Vérifier Redis
Write-Host "🔍 Vérification de Redis..." -ForegroundColor Cyan
$redisInstalled = $false
try {
    $redisVersion = redis-server --version 2>$null
    if ($redisVersion) {
        Write-Host "  ✅ Redis déjà installé" -ForegroundColor Green
        $redisInstalled = $true
    }
} catch {
    Write-Host "  ⚠️  Redis non installé" -ForegroundColor Yellow
}

Write-Host ""

if (-not $redisInstalled) {
    Write-Host "📥 Installation de Redis requise" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⚠️  Note : Redis n'est pas officiellement supporté sur Windows" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options d'installation :" -ForegroundColor Cyan
    Write-Host "  1. Memurai (Redis pour Windows - recommandé)" -ForegroundColor White
    Write-Host "     https://www.memurai.com/" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Redis via WSL2 (Windows Subsystem for Linux)" -ForegroundColor White
    Write-Host ""
    Write-Host "  3. Via Chocolatey (version non officielle)" -ForegroundColor White
    Write-Host "     choco install redis-64" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  4. Utiliser un service cloud (Redis Labs, AWS ElastiCache)" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Voulez-vous installer via Chocolatey maintenant ? (O/N)"
    
    if ($choice -eq "O" -or $choice -eq "o") {
        Write-Host ""
        Write-Host "📦 Installation de Redis via Chocolatey..." -ForegroundColor Cyan
        Write-Host ""
        
        try {
            choco install redis-64 -y
            Write-Host ""
            Write-Host "✅ Redis installé avec succès !" -ForegroundColor Green
            $redisInstalled = $true
        } catch {
            Write-Host ""
            Write-Host "❌ Erreur lors de l'installation" -ForegroundColor Red
        }
    } else {
        Write-Host ""
        Write-Host "💡 Pour le développement, Redis n'est pas obligatoire" -ForegroundColor Cyan
        Write-Host "   Vous pouvez continuer sans Redis pour l'instant" -ForegroundColor Cyan
        Write-Host ""
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 Résumé de l'installation :" -ForegroundColor Cyan
Write-Host ""

if ($nodeInstalled) {
    Write-Host "  ✅ Node.js : Installé" -ForegroundColor Green
} else {
    Write-Host "  ❌ Node.js : Non installé" -ForegroundColor Red
}

if ($redisInstalled) {
    Write-Host "  ✅ Redis : Installé" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Redis : Non installé (optionnel)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Initialiser le projet frontend (React/Vue)" -ForegroundColor White
Write-Host "  2. Créer les schémas Pydantic" -ForegroundColor White
Write-Host "  3. Créer les routes API Chat" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
