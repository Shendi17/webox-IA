# Script de diagnostic et correction automatique Vertex AI
# Pour résoudre l'erreur "File was not found"
# Date: 12 Janvier 2026

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Diagnostic et Correction Vertex AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Étape 1: Vérifier si PowerShell a été redémarré
Write-Host "[1/8] Vérification de l'environnement..." -ForegroundColor Green
Write-Host "  ⚠️  Avez-vous redémarré PowerShell après l'installation de gcloud CLI?" -ForegroundColor Yellow
Write-Host "  Si NON, fermez cette fenêtre et ouvrez un nouveau PowerShell!" -ForegroundColor Yellow
Write-Host ""
Start-Sleep -Seconds 2

# Étape 2: Chercher gcloud dans les emplacements courants
Write-Host "[2/8] Recherche de Google Cloud CLI..." -ForegroundColor Green

$possiblePaths = @(
    "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin",
    "$env:ProgramFiles\Google\Cloud SDK\google-cloud-sdk\bin",
    "$env:ProgramFiles(x86)\Google\Cloud SDK\google-cloud-sdk\bin",
    "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
)

$gcloudPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path "$path\gcloud.cmd") {
        $gcloudPath = $path
        Write-Host "  ✅ Trouvé: $path" -ForegroundColor Green
        break
    }
}

if (-not $gcloudPath) {
    Write-Host "  ❌ Google Cloud CLI introuvable" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Solutions:" -ForegroundColor Yellow
    Write-Host "  1. Redémarrez PowerShell (IMPORTANT!)" -ForegroundColor White
    Write-Host "  2. Si le problème persiste, réinstallez depuis:" -ForegroundColor White
    Write-Host "     https://cloud.google.com/sdk/docs/install#windows" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Étape 3: Ajouter gcloud au PATH temporairement
Write-Host "[3/8] Configuration du PATH..." -ForegroundColor Green
$env:Path = "$gcloudPath;$env:Path"
Write-Host "  ✅ PATH configuré pour cette session" -ForegroundColor Green

# Étape 4: Vérifier la version de gcloud
Write-Host "[4/8] Vérification de gcloud..." -ForegroundColor Green
try {
    $gcloudVersion = & "$gcloudPath\gcloud.cmd" --version 2>&1 | Select-Object -First 1
    Write-Host "  ✅ $gcloudVersion" -ForegroundColor Green
}
catch {
    Write-Host "  ❌ Erreur lors de l'exécution de gcloud" -ForegroundColor Red
    exit 1
}

# Étape 5: Vérifier l'authentification
Write-Host "[5/8] Vérification de l'authentification..." -ForegroundColor Green
try {
    $authList = & "$gcloudPath\gcloud.cmd" auth list --format="value(account)" 2>&1
    if ($authList -match "@") {
        Write-Host "  ✅ Compte authentifié: $authList" -ForegroundColor Green
        
        # Vérifier les credentials application-default
        $credPath = "$env:APPDATA\gcloud\application_default_credentials.json"
        if (Test-Path $credPath) {
            Write-Host "  ✅ Credentials application-default trouvés" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Credentials application-default manquants" -ForegroundColor Yellow
            Write-Host "  🔄 Création des credentials..." -ForegroundColor Yellow
            & "$gcloudPath\gcloud.cmd" auth application-default login
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Credentials créés avec succès" -ForegroundColor Green
            } else {
                Write-Host "  ❌ Échec de la création des credentials" -ForegroundColor Red
                exit 1
            }
        }
    } else {
        Write-Host "  ❌ Aucun compte authentifié" -ForegroundColor Red
        Write-Host "  🔄 Lancement de l'authentification..." -ForegroundColor Yellow
        & "$gcloudPath\gcloud.cmd" auth application-default login
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ Authentification réussie" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Échec de l'authentification" -ForegroundColor Red
            exit 1
        }
    }
}
catch {
    Write-Host "  ❌ Erreur: $_" -ForegroundColor Red
    exit 1
}

# Étape 6: Configurer le projet
Write-Host "[6/8] Configuration du projet..." -ForegroundColor Green
$projectId = "webox-482718"
& "$gcloudPath\gcloud.cmd" config set project $projectId 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Projet configuré: $projectId" -ForegroundColor Green
} else {
    Write-Host "  ❌ Erreur lors de la configuration du projet" -ForegroundColor Red
    exit 1
}

# Étape 7: Activer l'API Vertex AI
Write-Host "[7/8] Activation de l'API Vertex AI..." -ForegroundColor Green
& "$gcloudPath\gcloud.cmd" services enable aiplatform.googleapis.com 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ API Vertex AI activée" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  L'API pourrait déjà être activée" -ForegroundColor Yellow
}

# Étape 8: Vérifier le fichier .env
Write-Host "[8/8] Vérification du fichier .env..." -ForegroundColor Green
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    # Vérifier VERTEX_AI_PROJECT_ID
    if ($envContent -match "VERTEX_AI_PROJECT_ID=webox-482718") {
        Write-Host "  ✅ VERTEX_AI_PROJECT_ID correct" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  VERTEX_AI_PROJECT_ID à corriger" -ForegroundColor Yellow
        Write-Host "     Doit être: VERTEX_AI_PROJECT_ID=webox-482718" -ForegroundColor Yellow
    }
    
    # Vérifier VERTEX_AI_LOCATION
    if ($envContent -match "VERTEX_AI_LOCATION=europe-west1") {
        Write-Host "  ✅ VERTEX_AI_LOCATION correct" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  VERTEX_AI_LOCATION à corriger" -ForegroundColor Yellow
        Write-Host "     Doit être: VERTEX_AI_LOCATION=europe-west1" -ForegroundColor Yellow
        Write-Host "     (sans '(Iowa)' ou autre texte)" -ForegroundColor Yellow
    }
    
    # Vérifier que GOOGLE_API_KEY n'est pas configuré
    if ($envContent -match "GOOGLE_API_KEY=\S+") {
        Write-Host "  ⚠️  GOOGLE_API_KEY est configuré (à supprimer)" -ForegroundColor Yellow
        Write-Host "     Commentez ou supprimez cette ligne pour Vertex AI" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ GOOGLE_API_KEY non configuré (correct)" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ Fichier .env non trouvé" -ForegroundColor Red
}

# Test de connexion Vertex AI
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Test de connexion Vertex AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tentative de connexion à Vertex AI..." -ForegroundColor Yellow

$testScript = @"
from dotenv import load_dotenv
import os
load_dotenv()

project_id = os.getenv('VERTEX_AI_PROJECT_ID')
location = os.getenv('VERTEX_AI_LOCATION', 'us-central1')

print(f'Projet: {project_id}')
print(f'Région: {location}')

try:
    import vertexai
    vertexai.init(project=project_id, location=location)
    print('✅ Connexion Vertex AI réussie!')
except Exception as e:
    print(f'❌ Erreur: {e}')
"@

python -c $testScript

# Résumé final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ Configuration terminée!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Vérifiez que votre .env contient:" -ForegroundColor White
Write-Host "     VERTEX_AI_PROJECT_ID=webox-482718" -ForegroundColor Yellow
Write-Host "     VERTEX_AI_LOCATION=europe-west1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Redémarrez votre serveur WeBox:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Testez Gemini dans le chat multi-IA!" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANT: Si gcloud n'est toujours pas reconnu," -ForegroundColor Yellow
Write-Host "    fermez PowerShell et ouvrez une NOUVELLE fenêtre!" -ForegroundColor Yellow
Write-Host ""
