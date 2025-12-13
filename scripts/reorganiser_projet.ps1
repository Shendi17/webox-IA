# Script de réorganisation du projet WeBox
# Date : 1er Décembre 2025

Write-Host "🧹 REORGANISATION DU PROJET WEBOX" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Créer la structure docs/
Write-Host "📁 Création de la structure docs/..." -ForegroundColor Yellow

$docsStructure = @(
    "docs/bilans",
    "docs/features",
    "docs/guides",
    "docs/archive"
)

foreach ($dir in $docsStructure) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Créé: $dir" -ForegroundColor Green
    }
}

Write-Host ""

# Déplacer les fichiers BILAN_*
Write-Host "📄 Déplacement des bilans..." -ForegroundColor Yellow

$bilans = Get-ChildItem -Path "." -Filter "BILAN_*.md" -File
foreach ($file in $bilans) {
    Move-Item -Path $file.FullName -Destination "docs/bilans/" -Force
    Write-Host "✅ Déplacé: $($file.Name)" -ForegroundColor Green
}

# Déplacer les fichiers STUDIO_*
Write-Host ""
Write-Host "📄 Déplacement des docs Studio Créatif..." -ForegroundColor Yellow

$studio = Get-ChildItem -Path "." -Filter "STUDIO_*.md" -File
foreach ($file in $studio) {
    Move-Item -Path $file.FullName -Destination "docs/features/" -Force
    Write-Host "✅ Déplacé: $($file.Name)" -ForegroundColor Green
}

# Déplacer les fichiers de fonctionnalités
Write-Host ""
Write-Host "📄 Déplacement des docs fonctionnalités..." -ForegroundColor Yellow

$features = @(
    "PODCAST_CREATOR_TERMINE.md",
    "SERIES_IA_TERMINE.md",
    "DOCUMENTS_IA_TERMINE.md",
    "PHASE2_3_PROGRESSION.md",
    "ENRICHISSEMENT_*.md",
    "SESSION_*.md"
)

foreach ($pattern in $features) {
    $files = Get-ChildItem -Path "." -Filter $pattern -File
    foreach ($file in $files) {
        if (Test-Path $file.FullName) {
            Move-Item -Path $file.FullName -Destination "docs/features/" -Force
            Write-Host "✅ Déplacé: $($file.Name)" -ForegroundColor Green
        }
    }
}

# Supprimer les fichiers vides
Write-Host ""
Write-Host "🗑️ Suppression des fichiers vides..." -ForegroundColor Yellow

$emptyFiles = @(
    "FIX_PREHEADER_COLUMN.md",
    "FIX_TABLES_MANQUANTES.md",
    "GUIDE_TEST_MARKETING.md",
    "MIGRATION_FINALE_COMPLETE.md",
    "PLAN_NETTOYAGE_PROJET.md",
    "SOLUTION_FINALE_MARKETING.md",
    "diagnostic-wsl.txt"
)

foreach ($file in $emptyFiles) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
        Write-Host "✅ Supprimé: $file" -ForegroundColor Green
    }
}

# Supprimer les fichiers de test
Write-Host ""
Write-Host "🗑️ Suppression des fichiers de test..." -ForegroundColor Yellow

$testFiles = Get-ChildItem -Path "templates/dashboard" -Filter "test_*.html" -File
foreach ($file in $testFiles) {
    Remove-Item -Path $file.FullName -Force
    Write-Host "✅ Supprimé: $($file.Name)" -ForegroundColor Green
}

# Supprimer les anciennes versions
Write-Host ""
Write-Host "🗑️ Suppression des anciennes versions..." -ForegroundColor Yellow

$oldFiles = @(
    "templates/dashboard/index_old.html",
    "templates/dashboard/project_editor_v2.html"
)

foreach ($file in $oldFiles) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
        Write-Host "✅ Supprimé: $file" -ForegroundColor Green
    }
}

# Déplacer les autres docs dans archive
Write-Host ""
Write-Host "📄 Archivage des autres docs..." -ForegroundColor Yellow

$otherDocs = Get-ChildItem -Path "." -Filter "*.md" -File | Where-Object {
    $_.Name -notmatch "^(README|QUICK_START|INDEX_DOCUMENTATION|LICENSE)" -and
    !(Test-Path "docs/bilans/$($_.Name)") -and
    !(Test-Path "docs/features/$($_.Name)")
}

foreach ($file in $otherDocs) {
    Move-Item -Path $file.FullName -Destination "docs/archive/" -Force
    Write-Host "✅ Archivé: $($file.Name)" -ForegroundColor Green
}

# Remplacer l'ancien index par le nouveau
Write-Host ""
Write-Host "🔄 Mise à jour de la page d'accueil..." -ForegroundColor Yellow

if (Test-Path "templates/dashboard/index_updated.html") {
    # Sauvegarder l'ancien
    if (Test-Path "templates/dashboard/index.html") {
        Copy-Item -Path "templates/dashboard/index.html" -Destination "templates/dashboard/index_backup.html" -Force
        Write-Host "✅ Sauvegarde: index_backup.html" -ForegroundColor Green
    }
    
    # Remplacer
    Copy-Item -Path "templates/dashboard/index_updated.html" -Destination "templates/dashboard/index.html" -Force
    Write-Host "✅ Page d'accueil mise à jour !" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ REORGANISATION TERMINEE !" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Résumé:" -ForegroundColor Cyan
Write-Host "  - Structure docs/ créée" -ForegroundColor White
Write-Host "  - Fichiers MD réorganisés" -ForegroundColor White
Write-Host "  - Fichiers vides supprimés" -ForegroundColor White
Write-Host "  - Fichiers de test supprimés" -ForegroundColor White
Write-Host "  - Page d'accueil mise à jour" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Projet nettoyé et organisé !" -ForegroundColor Green
