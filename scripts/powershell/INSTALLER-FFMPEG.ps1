# Script d'installation automatique de FFmpeg pour Windows
# Ce script télécharge FFmpeg et le configure dans le PATH système

$ErrorActionPreference = "Stop"

Write-Host "=== Installation automatique de FFmpeg ===" -ForegroundColor Cyan

# Définir les chemins
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$downloadPath = "$env:TEMP\ffmpeg.zip"
$extractPath = "C:\ffmpeg"
$ffmpegBinPath = "$extractPath\bin"

try {
    # Vérifier si FFmpeg est déjà installé
    Write-Host "`nVérification de l'installation existante..." -ForegroundColor Yellow
    $existingFfmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($existingFfmpeg) {
        Write-Host "FFmpeg est déjà installé: $($existingFfmpeg.Source)" -ForegroundColor Green
        ffmpeg -version
        exit 0
    }

    # Télécharger FFmpeg
    Write-Host "`nTéléchargement de FFmpeg..." -ForegroundColor Yellow
    Write-Host "URL: $ffmpegUrl"
    Invoke-WebRequest -Uri $ffmpegUrl -OutFile $downloadPath -UseBasicParsing
    Write-Host "Téléchargement terminé!" -ForegroundColor Green

    # Créer le dossier d'extraction si nécessaire
    if (Test-Path $extractPath) {
        Write-Host "`nSuppression de l'ancienne installation..." -ForegroundColor Yellow
        Remove-Item -Path $extractPath -Recurse -Force
    }
    New-Item -ItemType Directory -Path $extractPath -Force | Out-Null

    # Extraire l'archive
    Write-Host "`nExtraction de l'archive..." -ForegroundColor Yellow
    Expand-Archive -Path $downloadPath -DestinationPath $extractPath -Force
    
    # Déplacer les fichiers du sous-dossier vers le dossier principal
    $subFolder = Get-ChildItem -Path $extractPath -Directory | Select-Object -First 1
    if ($subFolder) {
        Get-ChildItem -Path $subFolder.FullName -Recurse | Move-Item -Destination $extractPath -Force
        Remove-Item -Path $subFolder.FullName -Recurse -Force
    }

    Write-Host "Extraction terminée!" -ForegroundColor Green

    # Nettoyer le fichier téléchargé
    Remove-Item -Path $downloadPath -Force

    # Ajouter au PATH système
    Write-Host "`nConfiguration du PATH système..." -ForegroundColor Yellow
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    
    if ($currentPath -notlike "*$ffmpegBinPath*") {
        $newPath = "$currentPath;$ffmpegBinPath"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Host "FFmpeg ajouté au PATH système!" -ForegroundColor Green
    } else {
        Write-Host "FFmpeg est déjà dans le PATH système." -ForegroundColor Green
    }

    # Mettre à jour le PATH de la session actuelle
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")

    # Vérifier l'installation
    Write-Host "`nVérification de l'installation..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    
    # Tester avec le chemin complet
    $ffmpegExe = Join-Path $ffmpegBinPath "ffmpeg.exe"
    if (Test-Path $ffmpegExe) {
        Write-Host "`n=== Installation réussie! ===" -ForegroundColor Green
        Write-Host "FFmpeg installé dans: $extractPath" -ForegroundColor Cyan
        Write-Host "Exécutable: $ffmpegExe" -ForegroundColor Cyan
        
        # Afficher la version
        & $ffmpegExe -version | Select-Object -First 1
        
        Write-Host "`nREMARQUE IMPORTANTE:" -ForegroundColor Yellow
        Write-Host "Vous devez REDÉMARRER PowerShell pour que la commande 'ffmpeg' soit disponible globalement." -ForegroundColor Yellow
        Write-Host "Ou utilisez le chemin complet: $ffmpegExe" -ForegroundColor Cyan
    } else {
        throw "Le fichier ffmpeg.exe n'a pas été trouvé après l'installation."
    }

} catch {
    Write-Host "`n=== ERREUR lors de l'installation ===" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
