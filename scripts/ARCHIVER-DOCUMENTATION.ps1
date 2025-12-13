# Script d'archivage de la documentation obsolète
# Phase 2 : Archivage des fichiers MD
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║        ARCHIVAGE DOCUMENTATION OBSOLÈTE - PHASE 2           ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Créer le dossier d'archives
$archiveFolder = "docs\archives\migration_fastapi"
if (-not (Test-Path $archiveFolder)) {
    New-Item -ItemType Directory -Force -Path $archiveFolder | Out-Null
    Write-Host "✅ Dossier créé : $archiveFolder" -ForegroundColor Green
} else {
    Write-Host "✅ Dossier existe déjà : $archiveFolder" -ForegroundColor Green
}

Write-Host ""
Write-Host "📁 Fichiers à archiver :" -ForegroundColor Cyan
Write-Host ""

# Liste des fichiers à archiver
$filesToArchive = @(
    "BOUTONS_FONCTIONNELS.md",
    "CLARIFICATION_LIENS.md",
    "COMPLETION_FINALE.md",
    "CONFIGURATION_WEBOX_LOCAL.md",
    "CONFIRMATION_LIENS.md",
    "DEBUG_BOUTONS.md",
    "DIAGNOSTIC_COMPLET.md",
    "DIAGNOSTIC_UI.md",
    "ENRICHISSEMENT_COMPLET.md",
    "ETAPES_FINALES.md",
    "FIX_CHAT_ERROR.md",
    "FIX_CONSOLE_ERRORS.md",
    "FONCTIONNALITES_COMPLETES.md",
    "GUIDE_CONNEXION.md",
    "GUIDE_COULEURS_SIDEBAR.md",
    "INTERFACE_COMPLETE.md",
    "LIENS_COMPLETS.md",
    "MIGRATION_COMPLETE.md",
    "PLAN_ENRICHISSEMENT.md",
    "SOLUTION_FINALE.md",
    "SOLUTION_LIENS.md",
    "STRUCTURE_PROJET.md",
    "STRUCTURE_PROJET_PROPRE.md",
    "SYSTEME_UI_COMPLET.md",
    "TEST_CONNEXION.md",
    "TEST_DIRECT.md",
    "TEST_LIENS_DASHBOARD.md",
    "TOUS_BOUTONS_FONCTIONNELS.md",
    "TOUTES_FONCTIONNALITES_COMPLETES.md",
    "TOUTES_FONCTIONS_ENRICHIES.md"
)

Write-Host "  Total : $($filesToArchive.Count) fichiers" -ForegroundColor White
Write-Host ""

$confirmation = Read-Host "Voulez-vous archiver ces fichiers ? (O/N)"

if ($confirmation -ne "O" -and $confirmation -ne "o") {
    Write-Host ""
    Write-Host "❌ Opération annulée" -ForegroundColor Red
    Write-Host ""
    pause
    exit
}

Write-Host ""
Write-Host "📦 Archivage en cours..." -ForegroundColor Cyan
Write-Host ""

$filesMoved = 0
$filesNotFound = 0

foreach ($file in $filesToArchive) {
    if (Test-Path $file) {
        try {
            Move-Item $file $archiveFolder -Force -ErrorAction Stop
            Write-Host "  ✅ Archivé : $file" -ForegroundColor Green
            $filesMoved++
        }
        catch {
            Write-Host "  ❌ Erreur : $file - $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "  ⚠️  Non trouvé : $file" -ForegroundColor Yellow
        $filesNotFound++
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Archivage terminé !" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Résumé :" -ForegroundColor White
Write-Host "  - Fichiers archivés : $filesMoved" -ForegroundColor Green
Write-Host "  - Fichiers non trouvés : $filesNotFound" -ForegroundColor Yellow
Write-Host ""
Write-Host "📁 Emplacement : $archiveFolder" -ForegroundColor Cyan
Write-Host ""

if ($filesMoved -gt 0) {
    Write-Host "💡 Les fichiers ont été déplacés vers le dossier archives." -ForegroundColor Cyan
    Write-Host "   Vous pouvez les consulter à tout moment si nécessaire." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "📝 Prochaine étape : Phase 3 - Suppression des modules Streamlit" -ForegroundColor Yellow
Write-Host "   Consultez FICHIERS_OBSOLETES_STREAMLIT.md pour plus d'infos" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
