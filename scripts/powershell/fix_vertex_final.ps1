# Script final pour corriger Vertex AI
# Probleme identifie: Les modeles Gemini ne sont pas disponibles dans europe-west1
# Solution: Utiliser us-central1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CORRECTION FINALE VERTEX AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "PROBLEME IDENTIFIE:" -ForegroundColor Yellow
Write-Host "  Les modeles Gemini ne sont PAS disponibles dans europe-west1" -ForegroundColor Red
Write-Host "  Erreur: 'Publisher Model was not found or your project does not have access to it'" -ForegroundColor Red
Write-Host ""

Write-Host "SOLUTION:" -ForegroundColor Green
Write-Host "  1. Changer la region vers us-central1" -ForegroundColor White
Write-Host "  2. Activer GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor White
Write-Host "  3. Utiliser gemini-1.0-pro (disponible dans us-central1)" -ForegroundColor White
Write-Host ""

# Modifier le fichier .env
Write-Host "[1/3] Modification du fichier .env..." -ForegroundColor Green
Write-Host ""

if (-not (Test-Path ".env")) {
    Write-Host "Erreur: Fichier .env non trouve" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content ".env"
$newContent = @()
$locationUpdated = $false
$credentialsUpdated = $false

foreach ($line in $envContent) {
    # Changer VERTEX_AI_LOCATION
    if ($line -match "^VERTEX_AI_LOCATION=") {
        Write-Host "  Ancienne ligne: $line" -ForegroundColor Yellow
        $newLine = "VERTEX_AI_LOCATION=us-central1"
        Write-Host "  Nouvelle ligne: $newLine" -ForegroundColor Green
        $newContent += $newLine
        $locationUpdated = $true
    }
    # Decommenter GOOGLE_APPLICATION_CREDENTIALS
    elseif ($line -match "^#\s*GOOGLE_APPLICATION_CREDENTIALS=(.+)") {
        $credPath = $matches[1].Trim()
        Write-Host "  Decommentage de: GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Yellow
        $newLine = "GOOGLE_APPLICATION_CREDENTIALS=$credPath"
        Write-Host "  Nouvelle ligne: $newLine" -ForegroundColor Green
        $newContent += $newLine
        $credentialsUpdated = $true
    }
    else {
        $newContent += $line
    }
}

$newContent | Set-Content ".env" -Encoding UTF8

if ($locationUpdated) {
    Write-Host "  VERTEX_AI_LOCATION mis a jour vers us-central1" -ForegroundColor Green
} else {
    Write-Host "  VERTEX_AI_LOCATION deja configure" -ForegroundColor Yellow
}

if ($credentialsUpdated) {
    Write-Host "  GOOGLE_APPLICATION_CREDENTIALS active" -ForegroundColor Green
} else {
    Write-Host "  GOOGLE_APPLICATION_CREDENTIALS deja active" -ForegroundColor Yellow
}

Write-Host ""

# Verifier la configuration
Write-Host "[2/3] Verification de la configuration..." -ForegroundColor Green
Write-Host ""

python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('PROJECT_ID:', os.getenv('VERTEX_AI_PROJECT_ID')); print('LOCATION:', os.getenv('VERTEX_AI_LOCATION')); print('CREDENTIALS:', os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))"

Write-Host ""

# Test de connexion
Write-Host "[3/3] Test de connexion Vertex AI..." -ForegroundColor Green
Write-Host ""

$testScript = @"
import os
from dotenv import load_dotenv
load_dotenv()

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    project_id = os.getenv('VERTEX_AI_PROJECT_ID')
    location = os.getenv('VERTEX_AI_LOCATION')
    
    print(f'Initialisation Vertex AI...')
    print(f'  Projet: {project_id}')
    print(f'  Region: {location}')
    
    vertexai.init(project=project_id, location=location)
    print('  Status: OK')
    print()
    
    print('Creation du modele gemini-1.0-pro...')
    model = GenerativeModel('gemini-1.0-pro')
    print('  Status: OK')
    print()
    
    print('Test de generation...')
    response = model.generate_content('Dis bonjour en francais')
    print(f'  Reponse: {response.text}')
    print()
    print('========================================')
    print('  SUCCES! Vertex AI fonctionne!')
    print('========================================')
    
except Exception as e:
    print(f'ERREUR: {e}')
    print()
    print('Si vous voyez une erreur de facturation:')
    print('  Activez la facturation sur:')
    print('  https://console.cloud.google.com/billing/linkedaccount?project=webox-482718')
    print()
    print('Si vous voyez une erreur de permissions:')
    print('  Verifiez les roles IAM sur:')
    print('  https://console.cloud.google.com/iam-admin/iam?project=webox-482718')
"@

python -c $testScript

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PROCHAINES ETAPES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Si le test a reussi:" -ForegroundColor Green
Write-Host "  1. Redemarrez le serveur WeBox:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Testez Gemini dans le chat multi-IA" -ForegroundColor White
Write-Host ""

Write-Host "Si le test a echoue:" -ForegroundColor Red
Write-Host "  1. Verifiez que la facturation est activee:" -ForegroundColor White
Write-Host "     https://console.cloud.google.com/billing/linkedaccount?project=webox-482718" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Verifiez les roles IAM du service account:" -ForegroundColor White
Write-Host "     https://console.cloud.google.com/iam-admin/iam?project=webox-482718" -ForegroundColor Cyan
Write-Host "     Roles necessaires:" -ForegroundColor White
Write-Host "     - Vertex AI User" -ForegroundColor White
Write-Host "     - ML Developer" -ForegroundColor White
Write-Host ""

Write-Host "Note importante:" -ForegroundColor Cyan
Write-Host "  us-central1 (Iowa, USA) est la region principale pour Vertex AI" -ForegroundColor White
Write-Host "  C'est la ou tous les modeles Gemini sont disponibles" -ForegroundColor White
Write-Host ""
