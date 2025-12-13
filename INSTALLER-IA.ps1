# ============================================
# SCRIPT D'INSTALLATION DES PACKAGES IA
# ============================================
# Ce script installe tous les packages nécessaires
# pour utiliser les modèles IA dans WeBox Studio
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION DES PACKAGES IA - WEBOX" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Python est installé
Write-Host "[1/5] Vérification de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python trouvé : $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python n'est pas installé !" -ForegroundColor Red
    Write-Host "  Installez Python depuis : https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Installer OpenAI
Write-Host "[2/5] Installation OpenAI (GPT-4o, GPT-4)..." -ForegroundColor Yellow
try {
    pip install openai --quiet
    Write-Host "✓ OpenAI installé avec succès" -ForegroundColor Green
} catch {
    Write-Host "✗ Erreur lors de l'installation d'OpenAI" -ForegroundColor Red
}

Write-Host ""

# Installer Anthropic
Write-Host "[3/5] Installation Anthropic (Claude 3.5 Sonnet)..." -ForegroundColor Yellow
try {
    pip install anthropic --quiet
    Write-Host "✓ Anthropic installé avec succès" -ForegroundColor Green
} catch {
    Write-Host "✗ Erreur lors de l'installation d'Anthropic" -ForegroundColor Red
}

Write-Host ""

# Installer Google Generative AI
Write-Host "[4/5] Installation Google Generative AI (Gemini Pro)..." -ForegroundColor Yellow
try {
    pip install google-generativeai --quiet
    Write-Host "✓ Google Generative AI installé avec succès" -ForegroundColor Green
} catch {
    Write-Host "✗ Erreur lors de l'installation de Google Generative AI" -ForegroundColor Red
}

Write-Host ""

# Installer Mistral AI
Write-Host "[5/5] Installation Mistral AI..." -ForegroundColor Yellow
try {
    pip install mistralai --quiet
    Write-Host "✓ Mistral AI installé avec succès" -ForegroundColor Green
} catch {
    Write-Host "✗ Erreur lors de l'installation de Mistral AI" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION TERMINÉE !" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier les packages installés
Write-Host "Packages installés :" -ForegroundColor Yellow
Write-Host ""
pip list | Select-String -Pattern "openai|anthropic|google-generativeai|mistralai"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PROCHAINES ÉTAPES" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Obtenir les clés API :" -ForegroundColor White
Write-Host "   - OpenAI    : https://platform.openai.com/api-keys" -ForegroundColor Gray
Write-Host "   - Anthropic : https://console.anthropic.com/" -ForegroundColor Gray
Write-Host "   - Google    : https://makersuite.google.com/app/apikey" -ForegroundColor Gray
Write-Host "   - Mistral   : https://console.mistral.ai/" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Ajouter les clés dans le fichier .env :" -ForegroundColor White
Write-Host "   OPENAI_API_KEY=sk-..." -ForegroundColor Gray
Write-Host "   ANTHROPIC_API_KEY=sk-ant-..." -ForegroundColor Gray
Write-Host "   GOOGLE_API_KEY=AIza..." -ForegroundColor Gray
Write-Host "   MISTRAL_API_KEY=..." -ForegroundColor Gray
Write-Host ""
Write-Host "3. Redémarrer le serveur :" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Tester sur :" -ForegroundColor White
Write-Host "   http://localhost:8000/projects/2/editor" -ForegroundColor Gray
Write-Host ""
Write-Host "Consulte CONFIGURATION_IA.md pour plus de détails !" -ForegroundColor Cyan
Write-Host ""

# Pause pour lire les instructions
Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
