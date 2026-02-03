# Script de vérification de la configuration Vertex AI
# Pour l'Île de la Réunion
# Date: 12 Janvier 2026

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Vérification Configuration Vertex AI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Fonction pour vérifier si une commande existe
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# 1. Vérifier Python
Write-Host "[1/7] Python..." -ForegroundColor Cyan
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "  ✅ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Python non installé" -ForegroundColor Red
    $allGood = $false
}

# 2. Vérifier google-cloud-aiplatform
Write-Host "[2/7] google-cloud-aiplatform..." -ForegroundColor Cyan
try {
    python -c "import google.cloud.aiplatform; print('Version:', google.cloud.aiplatform.__version__)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Installé" -ForegroundColor Green
    } else {
        throw "Non installé"
    }
}
catch {
    Write-Host "  ❌ Non installé" -ForegroundColor Red
    Write-Host "     Installez avec: pip install google-cloud-aiplatform" -ForegroundColor Yellow
    $allGood = $false
}

# 3. Vérifier Google Cloud CLI
Write-Host "[3/7] Google Cloud CLI..." -ForegroundColor Cyan
if (Test-Command "gcloud") {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Host "  ✅ $gcloudVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Non installé" -ForegroundColor Red
    Write-Host "     Téléchargez depuis: https://cloud.google.com/sdk/docs/install#windows" -ForegroundColor Yellow
    $allGood = $false
}

# 4. Vérifier l'authentification
Write-Host "[4/7] Authentification Google Cloud..." -ForegroundColor Cyan
if (Test-Command "gcloud") {
    try {
        $token = gcloud auth application-default print-access-token 2>&1
        if ($LASTEXITCODE -eq 0 -and $token -match "^ya29\.") {
            Write-Host "  ✅ Authentifié" -ForegroundColor Green
        } else {
            throw "Non authentifié"
        }
    }
    catch {
        Write-Host "  ❌ Non authentifié" -ForegroundColor Red
        Write-Host "     Authentifiez-vous avec: gcloud auth application-default login" -ForegroundColor Yellow
        $allGood = $false
    }
} else {
    Write-Host "  ⏭️  Ignoré (gcloud non installé)" -ForegroundColor Yellow
}

# 5. Vérifier le fichier .env
Write-Host "[5/7] Fichier .env..." -ForegroundColor Cyan
if (Test-Path ".env") {
    Write-Host "  ✅ Fichier .env trouvé" -ForegroundColor Green
    
    # Charger les variables avec Python
    $envVars = python -c "from dotenv import load_dotenv; import os; load_dotenv(); import json; print(json.dumps({'project_id': os.getenv('VERTEX_AI_PROJECT_ID', ''), 'location': os.getenv('VERTEX_AI_LOCATION', ''), 'google_api_key': os.getenv('GOOGLE_API_KEY', '')}))" 2>$null | ConvertFrom-Json
    
    Write-Host ""
    Write-Host "  Variables d'environnement:" -ForegroundColor White
    
    # Vérifier VERTEX_AI_PROJECT_ID
    if ($envVars.project_id) {
        Write-Host "    • VERTEX_AI_PROJECT_ID: $($envVars.project_id)" -ForegroundColor Green
    } else {
        Write-Host "    • VERTEX_AI_PROJECT_ID: ❌ NON CONFIGURÉ" -ForegroundColor Red
        Write-Host "      Ajoutez: VERTEX_AI_PROJECT_ID=webox-482718" -ForegroundColor Yellow
        $allGood = $false
    }
    
    # Vérifier VERTEX_AI_LOCATION
    if ($envVars.location) {
        if ($envVars.location -eq "europe-west1") {
            Write-Host "    • VERTEX_AI_LOCATION: $($envVars.location) ✅" -ForegroundColor Green
        } else {
            Write-Host "    • VERTEX_AI_LOCATION: $($envVars.location) ⚠️" -ForegroundColor Yellow
            Write-Host "      Recommandé pour la Réunion: europe-west1" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    • VERTEX_AI_LOCATION: ❌ NON CONFIGURÉ" -ForegroundColor Red
        Write-Host "      Ajoutez: VERTEX_AI_LOCATION=europe-west1" -ForegroundColor Yellow
        $allGood = $false
    }
    
    # Vérifier GOOGLE_API_KEY (ne doit PAS être configuré)
    if ($envVars.google_api_key) {
        Write-Host "    • GOOGLE_API_KEY: ⚠️ CONFIGURÉ (à supprimer pour Vertex AI)" -ForegroundColor Yellow
        Write-Host "      Supprimez ou commentez cette ligne dans .env" -ForegroundColor Yellow
    } else {
        Write-Host "    • GOOGLE_API_KEY: ✅ Non configuré (correct)" -ForegroundColor Green
    }
    
} else {
    Write-Host "  ❌ Fichier .env non trouvé" -ForegroundColor Red
    Write-Host "     Créez un fichier .env avec:" -ForegroundColor Yellow
    Write-Host "     VERTEX_AI_PROJECT_ID=webox-482718" -ForegroundColor Yellow
    Write-Host "     VERTEX_AI_LOCATION=europe-west1" -ForegroundColor Yellow
    $allGood = $false
}

# 6. Vérifier le projet configuré
Write-Host ""
Write-Host "[6/7] Projet Google Cloud configuré..." -ForegroundColor Cyan
if (Test-Command "gcloud") {
    try {
        $currentProject = gcloud config get-value project 2>$null
        if ($currentProject) {
            Write-Host "  ✅ Projet actif: $currentProject" -ForegroundColor Green
        } else {
            throw "Pas de projet"
        }
    }
    catch {
        Write-Host "  ❌ Aucun projet configuré" -ForegroundColor Red
        Write-Host "     Configurez avec: gcloud config set project webox-482718" -ForegroundColor Yellow
        $allGood = $false
    }
} else {
    Write-Host "  ⏭️  Ignoré (gcloud non installé)" -ForegroundColor Yellow
}

# 7. Vérifier l'API Vertex AI
Write-Host "[7/7] API Vertex AI..." -ForegroundColor Cyan
if (Test-Command "gcloud") {
    try {
        $apiEnabled = gcloud services list --enabled --filter="name:aiplatform.googleapis.com" --format="value(name)" 2>$null
        if ($apiEnabled -match "aiplatform") {
            Write-Host "  ✅ API activée" -ForegroundColor Green
        } else {
            Write-Host "  ❌ API non activée" -ForegroundColor Red
            Write-Host "     Activez avec: gcloud services enable aiplatform.googleapis.com" -ForegroundColor Yellow
            $allGood = $false
        }
    }
    catch {
        Write-Host "  ⚠️  Impossible de vérifier (vérifiez manuellement)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⏭️  Ignoré (gcloud non installé)" -ForegroundColor Yellow
}

# Résumé final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✅ Configuration complète!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Vertex AI est prêt à l'emploi!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Prochaines étapes:" -ForegroundColor Cyan
    Write-Host "  1. Redémarrez votre serveur WeBox" -ForegroundColor White
    Write-Host "  2. Testez Gemini dans le chat multi-IA" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  ⚠️  Configuration incomplète" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Corrigez les problèmes ci-dessus, puis:" -ForegroundColor Yellow
    Write-Host "  • Relancez ce script pour vérifier" -ForegroundColor White
    Write-Host "  • Ou exécutez: .\setup_vertex_ai.ps1" -ForegroundColor White
    Write-Host ""
}

Write-Host "Pour plus d'aide, consultez:" -ForegroundColor Cyan
Write-Host "  • VERTEX_AI_CONFIGURATION_REUNION.md" -ForegroundColor White
Write-Host ""
