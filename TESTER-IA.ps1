# ============================================
# SCRIPT DE TEST DES IA
# ============================================
# Ce script teste si les clés API fonctionnent
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  TEST DES CLÉS API IA - WEBOX" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le serveur est démarré
Write-Host "Vérification du serveur..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -Method GET -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Serveur démarré sur http://localhost:8000" -ForegroundColor Green
} catch {
    Write-Host "✗ Serveur non démarré !" -ForegroundColor Red
    Write-Host "  Démarre le serveur avec : python main.py" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "Test des modèles IA..." -ForegroundColor Yellow
Write-Host ""

# Liste des modèles à tester
$models = @(
    @{name="GPT-4o"; id="gpt-4o"; provider="OpenAI"},
    @{name="Claude 3.5 Sonnet"; id="claude-3.5-sonnet"; provider="Anthropic"},
    @{name="Gemini Pro"; id="gemini-pro"; provider="Google"},
    @{name="GPT-3.5 Turbo"; id="gpt-3.5-turbo"; provider="OpenAI"}
)

$successCount = 0
$failCount = 0

foreach ($model in $models) {
    Write-Host "Test de $($model.name) ($($model.provider))..." -ForegroundColor Cyan
    
    try {
        $body = @{
            message = "Bonjour, réponds juste 'OK' pour confirmer que tu fonctionnes."
            model = $model.id
            context = @{}
            project_id = 2
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/ai/chat" `
            -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -TimeoutSec 30
        
        # Vérifier la réponse
        if ($response.response -match "⚠️|❌") {
            Write-Host "  ✗ $($model.name) : $($response.response)" -ForegroundColor Red
            $failCount++
        } else {
            Write-Host "  ✓ $($model.name) : Fonctionne !" -ForegroundColor Green
            $successCount++
        }
    } catch {
        Write-Host "  ✗ $($model.name) : Erreur de connexion" -ForegroundColor Red
        $failCount++
    }
    
    Write-Host ""
    Start-Sleep -Milliseconds 500
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  RÉSULTATS" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Modèles fonctionnels : $successCount" -ForegroundColor Green
Write-Host "Modèles non configurés : $failCount" -ForegroundColor Red
Write-Host ""

if ($successCount -eq 0) {
    Write-Host "⚠️  Aucun modèle ne fonctionne !" -ForegroundColor Red
    Write-Host ""
    Write-Host "Actions à faire :" -ForegroundColor Yellow
    Write-Host "1. Obtenir au moins une clé API (Gemini Pro est gratuit)" -ForegroundColor White
    Write-Host "2. Ajouter la clé dans le fichier .env" -ForegroundColor White
    Write-Host "3. Redémarrer le serveur : python main.py" -ForegroundColor White
    Write-Host "4. Relancer ce test : .\TESTER-IA.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Consulte CONFIGURATION_IA.md pour les détails !" -ForegroundColor Cyan
} elseif ($successCount -lt $models.Count) {
    Write-Host "✓ Certains modèles fonctionnent !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour activer les autres modèles :" -ForegroundColor Yellow
    Write-Host "1. Obtenir les clés API manquantes" -ForegroundColor White
    Write-Host "2. Ajouter dans .env" -ForegroundColor White
    Write-Host "3. Redémarrer le serveur" -ForegroundColor White
} else {
    Write-Host "🎉 Tous les modèles fonctionnent parfaitement !" -ForegroundColor Green
    Write-Host ""
    Write-Host "Tu peux maintenant utiliser le Studio Web IA :" -ForegroundColor Cyan
    Write-Host "http://localhost:8000/projects/2/editor" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
