# Script pour basculer vers gcloud auth et supprimer le service account
# Cela resout le probleme de permissions IAM

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Basculement vers gcloud auth" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Probleme identifie:" -ForegroundColor Yellow
Write-Host "  Le compte de service n'a pas les permissions IAM necessaires" -ForegroundColor White
Write-Host "  Permission manquante: aiplatform.endpoints.predict" -ForegroundColor Red
Write-Host ""
Write-Host "Solution:" -ForegroundColor Green
Write-Host "  Utiliser gcloud auth application-default (votre compte personnel)" -ForegroundColor White
Write-Host "  au lieu du service account" -ForegroundColor White
Write-Host ""

# Vérifier que gcloud est installé
$gcloudPath = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin"
if (-not (Test-Path "$gcloudPath\gcloud.cmd")) {
    Write-Host "Erreur: gcloud CLI non trouve" -ForegroundColor Red
    exit 1
}

$env:Path = "$gcloudPath;$env:Path"

Write-Host "[1/3] Modification du fichier .env..." -ForegroundColor Green
Write-Host ""

if (-not (Test-Path ".env")) {
    Write-Host "Erreur: Fichier .env non trouve" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content ".env"
$newContent = @()
$modified = $false

foreach ($line in $envContent) {
    # Commenter la ligne GOOGLE_APPLICATION_CREDENTIALS
    if ($line -match "^GOOGLE_APPLICATION_CREDENTIALS=") {
        Write-Host "  Commentaire de: $line" -ForegroundColor Yellow
        $newContent += "# $line  # Desactive - utilisation de gcloud auth"
        $modified = $true
    } else {
        $newContent += $line
    }
}

if ($modified) {
    $newContent | Set-Content ".env" -Encoding UTF8
    Write-Host "  Fichier .env mis a jour" -ForegroundColor Green
} else {
    Write-Host "  Aucune modification necessaire dans .env" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/3] Verification de l'authentification gcloud..." -ForegroundColor Green
Write-Host ""

# Vérifier si déjà authentifié
$authList = & "$gcloudPath\gcloud.cmd" auth list --format="value(account)" 2>$null
if ($authList -match "@") {
    Write-Host "  Compte authentifie: $authList" -ForegroundColor Green
    
    # Vérifier les credentials application-default
    $credPath = "$env:APPDATA\gcloud\application_default_credentials.json"
    if (Test-Path $credPath) {
        Write-Host "  Credentials application-default: OK" -ForegroundColor Green
    } else {
        Write-Host "  Creation des credentials application-default..." -ForegroundColor Yellow
        Write-Host "  Une page web va s'ouvrir pour l'authentification..." -ForegroundColor Cyan
        Write-Host ""
        & "$gcloudPath\gcloud.cmd" auth application-default login
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Authentification reussie!" -ForegroundColor Green
        } else {
            Write-Host "  Erreur d'authentification" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "  Aucun compte authentifie" -ForegroundColor Yellow
    Write-Host "  Lancement de l'authentification..." -ForegroundColor Cyan
    Write-Host "  Une page web va s'ouvrir..." -ForegroundColor Cyan
    Write-Host ""
    & "$gcloudPath\gcloud.cmd" auth application-default login
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Authentification reussie!" -ForegroundColor Green
    } else {
        Write-Host "  Erreur d'authentification" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "[3/3] Configuration du projet..." -ForegroundColor Green
Write-Host ""

$projectId = "webox-482718"
& "$gcloudPath\gcloud.cmd" config set project $projectId 2>&1 | Out-Null
Write-Host "  Projet configure: $projectId" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Test de connexion" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Verification des variables d'environnement..." -ForegroundColor Yellow
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('PROJECT_ID:', os.getenv('VERTEX_AI_PROJECT_ID')); print('LOCATION:', os.getenv('VERTEX_AI_LOCATION')); cred = os.getenv('GOOGLE_APPLICATION_CREDENTIALS'); print('CREDENTIALS:', 'gcloud auth' if not cred else cred)"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuration terminee!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Prochaines etapes:" -ForegroundColor Cyan
Write-Host "  1. Testez la connexion Vertex AI:" -ForegroundColor White
Write-Host "     python test_vertex_connection.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Si le test reussit, redemarrez le serveur:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: Votre compte personnel (master@tonyalpha80.com)" -ForegroundColor Cyan
Write-Host "      a automatiquement les permissions necessaires." -ForegroundColor Cyan
Write-Host ""
