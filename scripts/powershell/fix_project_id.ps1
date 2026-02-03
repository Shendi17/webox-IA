# Script pour corriger le VERTEX_AI_PROJECT_ID dans .env
# Le problème : utilisation d'un OAuth Client ID au lieu du Project ID

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Correction du Project ID" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Diagnostic du probleme:" -ForegroundColor Yellow
Write-Host "  L'erreur montre que le systeme utilise:" -ForegroundColor White
Write-Host "  26997462856-5ftvpki9ghpg59s8rae6aqmr1pjqkeqt.apps.googleusercontent.com" -ForegroundColor Red
Write-Host ""
Write-Host "  Ceci est un OAuth Client ID, PAS un Project ID!" -ForegroundColor Red
Write-Host ""

# Obtenir le vrai Project ID depuis gcloud
Write-Host "Recherche du vrai Project ID..." -ForegroundColor Yellow

$gcloudPath = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin"
if (Test-Path "$gcloudPath\gcloud.cmd") {
    $env:Path = "$gcloudPath;$env:Path"
    
    Write-Host "  Tentative 1: Via gcloud config..." -ForegroundColor Cyan
    $projectId = & "$gcloudPath\gcloud.cmd" config get-value project 2>$null
    
    if ($projectId -and $projectId -ne "(unset)") {
        Write-Host "  Project ID trouve: $projectId" -ForegroundColor Green
    } else {
        Write-Host "  Tentative 2: Liste des projets..." -ForegroundColor Cyan
        $projects = & "$gcloudPath\gcloud.cmd" projects list --format="value(projectId)" 2>$null
        if ($projects) {
            Write-Host "  Projets disponibles:" -ForegroundColor Green
            $projectArray = $projects -split "`n" | Where-Object { $_ -ne "" }
            for ($i = 0; $i -lt $projectArray.Count; $i++) {
                Write-Host "    [$i] $($projectArray[$i])" -ForegroundColor White
            }
            
            if ($projectArray.Count -eq 1) {
                $projectId = $projectArray[0]
                Write-Host "  Utilisation du seul projet disponible: $projectId" -ForegroundColor Green
            } else {
                Write-Host ""
                $choice = Read-Host "  Entrez le numero du projet a utiliser"
                if ($choice -match '^\d+$' -and [int]$choice -lt $projectArray.Count) {
                    $projectId = $projectArray[[int]$choice]
                    Write-Host "  Projet selectionne: $projectId" -ForegroundColor Green
                } else {
                    Write-Host "  Choix invalide" -ForegroundColor Red
                    exit 1
                }
            }
        } else {
            Write-Host "  Aucun projet trouve" -ForegroundColor Red
            Write-Host ""
            Write-Host "  Veuillez creer un projet sur:" -ForegroundColor Yellow
            Write-Host "  https://console.cloud.google.com/projectcreate" -ForegroundColor Cyan
            exit 1
        }
    }
} else {
    Write-Host "  gcloud CLI non trouve" -ForegroundColor Red
    Write-Host "  Utilisation du Project ID par defaut: webox-482718" -ForegroundColor Yellow
    $projectId = "webox-482718"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Mise a jour du fichier .env" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".env")) {
    Write-Host "Fichier .env non trouve" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content ".env"
$newContent = @()
$updated = $false

foreach ($line in $envContent) {
    if ($line -match "^VERTEX_AI_PROJECT_ID=") {
        Write-Host "  Ancienne ligne: $line" -ForegroundColor Yellow
        $newLine = "VERTEX_AI_PROJECT_ID=$projectId"
        Write-Host "  Nouvelle ligne: $newLine" -ForegroundColor Green
        $newContent += $newLine
        $updated = $true
    } else {
        $newContent += $line
    }
}

if ($updated) {
    $newContent | Set-Content ".env" -Encoding UTF8
    Write-Host ""
    Write-Host "Fichier .env mis a jour avec succes!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "VERTEX_AI_PROJECT_ID non trouve dans .env" -ForegroundColor Red
    Write-Host "Ajout de la ligne..." -ForegroundColor Yellow
    Add-Content ".env" "`nVERTEX_AI_PROJECT_ID=$projectId" -Encoding UTF8
    Write-Host "Ligne ajoutee avec succes!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuration du projet dans gcloud" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "$gcloudPath\gcloud.cmd") {
    & "$gcloudPath\gcloud.cmd" config set project $projectId 2>&1 | Out-Null
    Write-Host "Projet configure dans gcloud: $projectId" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('VERTEX_AI_PROJECT_ID:', os.getenv('VERTEX_AI_PROJECT_ID'))"

Write-Host ""
Write-Host "Prochaines etapes:" -ForegroundColor Cyan
Write-Host "  1. Testez la connexion:" -ForegroundColor White
Write-Host "     python test_vertex_connection.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Si le test reussit, redemarrez le serveur:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
