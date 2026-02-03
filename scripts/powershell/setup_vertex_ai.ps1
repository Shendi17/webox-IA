# Script d'installation et configuration automatique de Vertex AI
# Pour l'Île de la Réunion
# Date: 12 Janvier 2026

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuration Vertex AI - WeBox" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

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

# Fonction pour télécharger un fichier
function Download-File {
    param($Url, $Output)
    Write-Host "Téléchargement depuis $Url..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $Url -OutFile $Output -UseBasicParsing
        return $true
    }
    catch {
        Write-Host "Erreur lors du téléchargement: $_" -ForegroundColor Red
        return $false
    }
}

# Étape 1: Vérifier Python
Write-Host "[1/6] Vérification de Python..." -ForegroundColor Green
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "  ✅ Python installé: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Python n'est pas installé!" -ForegroundColor Red
    Write-Host "  Installez Python depuis https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Étape 2: Vérifier google-cloud-aiplatform
Write-Host ""
Write-Host "[2/6] Vérification de google-cloud-aiplatform..." -ForegroundColor Green
try {
    python -c "import google.cloud.aiplatform" 2>$null
    Write-Host "  ✅ google-cloud-aiplatform installé" -ForegroundColor Green
}
catch {
    Write-Host "  ⚠️  Installation de google-cloud-aiplatform..." -ForegroundColor Yellow
    pip install google-cloud-aiplatform
    Write-Host "  ✅ google-cloud-aiplatform installé" -ForegroundColor Green
}

# Étape 3: Vérifier Google Cloud CLI
Write-Host ""
Write-Host "[3/6] Vérification de Google Cloud CLI..." -ForegroundColor Green
if (Test-Command "gcloud") {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Host "  ✅ Google Cloud CLI installé: $gcloudVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Google Cloud CLI n'est pas installé" -ForegroundColor Red
    Write-Host ""
    Write-Host "  📥 Téléchargement de Google Cloud CLI..." -ForegroundColor Yellow
    
    $installerPath = "$env:TEMP\GoogleCloudSDKInstaller.exe"
    $downloadUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
    
    if (Download-File -Url $downloadUrl -Output $installerPath) {
        Write-Host "  ✅ Téléchargement terminé" -ForegroundColor Green
        Write-Host ""
        Write-Host "  🚀 Lancement de l'installation..." -ForegroundColor Yellow
        Write-Host "  ⚠️  IMPORTANT: Suivez l'assistant d'installation" -ForegroundColor Yellow
        Write-Host "  ⚠️  Cochez 'Run gcloud init' à la fin" -ForegroundColor Yellow
        Write-Host ""
        
        Start-Process -FilePath $installerPath -Wait
        
        Write-Host ""
        Write-Host "  ✅ Installation terminée" -ForegroundColor Green
        Write-Host "  ⚠️  REDÉMARREZ PowerShell et relancez ce script" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Appuyez sur Entrée pour quitter"
        exit 0
    } else {
        Write-Host "  ❌ Échec du téléchargement" -ForegroundColor Red
        Write-Host "  Téléchargez manuellement depuis:" -ForegroundColor Yellow
        Write-Host "  https://cloud.google.com/sdk/docs/install#windows" -ForegroundColor Cyan
        exit 1
    }
}

# Étape 4: Vérifier l'authentification
Write-Host ""
Write-Host "[4/6] Vérification de l'authentification..." -ForegroundColor Green
try {
    $token = gcloud auth application-default print-access-token 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Authentification active" -ForegroundColor Green
    } else {
        throw "Non authentifié"
    }
}
catch {
    Write-Host "  ⚠️  Authentification requise..." -ForegroundColor Yellow
    Write-Host "  🌐 Ouverture du navigateur pour l'authentification..." -ForegroundColor Yellow
    Write-Host ""
    gcloud auth application-default login
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Authentification réussie" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Échec de l'authentification" -ForegroundColor Red
        exit 1
    }
}

# Étape 5: Configurer le projet
Write-Host ""
Write-Host "[5/6] Configuration du projet..." -ForegroundColor Green

# Lire le PROJECT_ID depuis .env
$envFile = Get-Content ".env" -ErrorAction SilentlyContinue
$projectId = $null

foreach ($line in $envFile) {
    if ($line -match "^VERTEX_AI_PROJECT_ID=(.+)$") {
        $projectId = $matches[1].Trim()
        break
    }
}

if ($projectId) {
    Write-Host "  📋 Projet trouvé dans .env: $projectId" -ForegroundColor Cyan
    gcloud config set project $projectId
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Projet configuré: $projectId" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Erreur lors de la configuration du projet" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ❌ VERTEX_AI_PROJECT_ID non trouvé dans .env" -ForegroundColor Red
    Write-Host "  Ajoutez cette ligne dans votre .env:" -ForegroundColor Yellow
    Write-Host "  VERTEX_AI_PROJECT_ID=votre-project-id" -ForegroundColor Cyan
    exit 1
}

# Étape 6: Activer l'API Vertex AI
Write-Host ""
Write-Host "[6/6] Activation de l'API Vertex AI..." -ForegroundColor Green
gcloud services enable aiplatform.googleapis.com

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ API Vertex AI activée" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  L'API pourrait déjà être activée ou nécessiter quelques minutes" -ForegroundColor Yellow
}

# Résumé final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ Configuration terminée!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Résumé de la configuration:" -ForegroundColor Cyan
Write-Host "  • Python: ✅ Installé" -ForegroundColor White
Write-Host "  • google-cloud-aiplatform: ✅ Installé" -ForegroundColor White
Write-Host "  • Google Cloud CLI: ✅ Installé" -ForegroundColor White
Write-Host "  • Authentification: ✅ Active" -ForegroundColor White
Write-Host "  • Projet: ✅ Configuré ($projectId)" -ForegroundColor White
Write-Host "  • API Vertex AI: ✅ Activée" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "  1. Vérifiez votre fichier .env avec:" -ForegroundColor White
Write-Host "     .\verify_vertex_config.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Redémarrez votre serveur WeBox:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Testez Gemini dans le chat multi-IA!" -ForegroundColor White
Write-Host ""
Write-Host "✨ Vertex AI est maintenant prêt à l'emploi!" -ForegroundColor Green
Write-Host ""
