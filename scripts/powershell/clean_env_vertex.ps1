# Script pour nettoyer le fichier .env et corriger le problème Vertex AI
# Supprime GOOGLE_APPLICATION_CREDENTIALS vide qui cause l'erreur "File was not found"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Nettoyage du fichier .env" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".env")) {
    Write-Host "❌ Fichier .env non trouvé" -ForegroundColor Red
    exit 1
}

Write-Host "Lecture du fichier .env..." -ForegroundColor Yellow
$envContent = Get-Content ".env"
$newContent = @()
$modified = $false

foreach ($line in $envContent) {
    # Supprimer ou commenter les lignes GOOGLE_APPLICATION_CREDENTIALS vides
    if ($line -match "^GOOGLE_APPLICATION_CREDENTIALS\s*=\s*$") {
        Write-Host "  Ligne problematique trouvee: $line" -ForegroundColor Yellow
        Write-Host "  Commentee automatiquement" -ForegroundColor Green
        $newContent += "# $line  # Commente automatiquement - non necessaire avec gcloud auth"
        $modified = $true
    }
    elseif ($line -match "^GOOGLE_APPLICATION_CREDENTIALS\s*=\s*['`"]?\s*['`"]?\s*$") {
        Write-Host "  Ligne problematique trouvee: $line" -ForegroundColor Yellow
        Write-Host "  Commentee automatiquement" -ForegroundColor Green
        $newContent += "# $line  # Commente automatiquement - non necessaire avec gcloud auth"
        $modified = $true
    }
    else {
        $newContent += $line
    }
}

if ($modified) {
    Write-Host ""
    Write-Host "Sauvegarde du fichier .env..." -ForegroundColor Yellow
    $newContent | Set-Content ".env" -Encoding UTF8
    Write-Host "  ✅ Fichier .env nettoyé" -ForegroundColor Green
    Write-Host ""
    Write-Host "Modifications effectuées:" -ForegroundColor Cyan
    Write-Host "  • GOOGLE_APPLICATION_CREDENTIALS vide commenté" -ForegroundColor White
    Write-Host "  • Le système utilisera gcloud auth application-default" -ForegroundColor White
} else {
    Write-Host "  ✅ Aucune modification nécessaire" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Test de la configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test rapide
python -c "from dotenv import load_dotenv; import os; load_dotenv(); cred = os.getenv('GOOGLE_APPLICATION_CREDENTIALS'); print('GOOGLE_APPLICATION_CREDENTIALS:', 'NON CONFIGURÉ' if not cred else cred)"

Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Testez la connexion:" -ForegroundColor White
Write-Host "     python test_vertex_connection.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Si le test réussit, redémarrez le serveur:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
