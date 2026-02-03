# Script pour corriger le fichier .env et activer correctement GOOGLE_APPLICATION_CREDENTIALS

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Correction du fichier .env" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".env")) {
    Write-Host "Erreur: Fichier .env non trouve" -ForegroundColor Red
    exit 1
}

Write-Host "Lecture du fichier .env..." -ForegroundColor Yellow
$envContent = Get-Content ".env"
$newContent = @()

foreach ($line in $envContent) {
    # Ignorer les lignes commentees avec le texte problematique
    if ($line -match "^#.*Commente automatiquement") {
        Write-Host "  Suppression de la ligne commentee incorrecte" -ForegroundColor Yellow
        continue
    }
    # Ignorer les lignes GOOGLE_APPLICATION_CREDENTIALS commentees
    elseif ($line -match "^#\s*GOOGLE_APPLICATION_CREDENTIALS=") {
        Write-Host "  Suppression de: $line" -ForegroundColor Yellow
        continue
    }
    # Garder les autres lignes
    else {
        $newContent += $line
    }
}

# Ajouter la ligne GOOGLE_APPLICATION_CREDENTIALS correcte si elle n'existe pas
$hasCredentials = $false
foreach ($line in $newContent) {
    if ($line -match "^GOOGLE_APPLICATION_CREDENTIALS=C:\\") {
        $hasCredentials = $true
        break
    }
}

if (-not $hasCredentials) {
    Write-Host "  Ajout de GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Green
    $newContent += "GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json"
}

# Sauvegarder
$newContent | Set-Content ".env" -Encoding UTF8

Write-Host "  Fichier .env nettoye et corrige" -ForegroundColor Green
Write-Host ""

# Verification
Write-Host "Verification de la configuration:" -ForegroundColor Cyan
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('PROJECT_ID:', os.getenv('VERTEX_AI_PROJECT_ID')); print('LOCATION:', os.getenv('VERTEX_AI_LOCATION')); cred = os.getenv('GOOGLE_APPLICATION_CREDENTIALS'); print('CREDENTIALS:', cred); print('Fichier existe:', os.path.exists(cred) if cred else 'N/A')"

Write-Host ""
Write-Host "Configuration terminee!" -ForegroundColor Green
