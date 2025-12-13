# Script de suppression des fichiers Streamlit obsolètes
# Phase 1 : Suppression sans risque
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║     SUPPRESSION FICHIERS STREAMLIT OBSOLÈTES - PHASE 1      ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  ATTENTION : Cette opération va supprimer des fichiers !" -ForegroundColor Yellow
Write-Host ""
Write-Host "Fichiers qui seront supprimés :" -ForegroundColor White
Write-Host "  - pages\generation_video.py (page placeholder)" -ForegroundColor Gray
Write-Host "  - test_dashboard.py (tests Streamlit)" -ForegroundColor Gray
Write-Host "  - test_links.py (tests Streamlit)" -ForegroundColor Gray
Write-Host "  - test_login.py (tests Streamlit)" -ForegroundColor Gray
Write-Host "  - scripts\DEMARRER-WEBOX.bat (script Streamlit)" -ForegroundColor Gray
Write-Host "  - scripts\LANCER-WEBOX.bat (script Streamlit)" -ForegroundColor Gray
Write-Host "  - scripts\lancer-webox.ps1 (script Streamlit)" -ForegroundColor Gray
Write-Host "  - scripts\start.ps1 (script Streamlit)" -ForegroundColor Gray
Write-Host "  - restart_app.ps1 (script Streamlit)" -ForegroundColor Gray
Write-Host ""

$confirmation = Read-Host "Voulez-vous continuer ? (O/N)"

if ($confirmation -ne "O" -and $confirmation -ne "o") {
    Write-Host ""
    Write-Host "❌ Opération annulée" -ForegroundColor Red
    Write-Host ""
    pause
    exit
}

Write-Host ""
Write-Host "🗑️  Suppression en cours..." -ForegroundColor Cyan
Write-Host ""

$filesDeleted = 0
$filesNotFound = 0

# Fonction pour supprimer un fichier
function Remove-FileIfExists {
    param($filePath)
    
    if (Test-Path $filePath) {
        try {
            Remove-Item $filePath -Force -ErrorAction Stop
            Write-Host "  ✅ Supprimé : $filePath" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Host "  ❌ Erreur : $filePath - $_" -ForegroundColor Red
            return $false
        }
    }
    else {
        Write-Host "  ⚠️  Non trouvé : $filePath" -ForegroundColor Yellow
        return $null
    }
}

# Supprimer les fichiers
Write-Host "📄 Suppression des pages Streamlit..." -ForegroundColor Cyan
$result = Remove-FileIfExists "pages\generation_video.py"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

Write-Host ""
Write-Host "🧪 Suppression des tests Streamlit..." -ForegroundColor Cyan
$result = Remove-FileIfExists "test_dashboard.py"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

$result = Remove-FileIfExists "test_links.py"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

$result = Remove-FileIfExists "test_login.py"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

Write-Host ""
Write-Host "📜 Suppression des scripts Streamlit..." -ForegroundColor Cyan
$result = Remove-FileIfExists "scripts\DEMARRER-WEBOX.bat"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

$result = Remove-FileIfExists "scripts\LANCER-WEBOX.bat"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

$result = Remove-FileIfExists "scripts\lancer-webox.ps1"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

$result = Remove-FileIfExists "scripts\start.ps1"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

$result = Remove-FileIfExists "restart_app.ps1"
if ($result -eq $true) { $filesDeleted++ } elseif ($null -eq $result) { $filesNotFound++ }

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Suppression terminée !" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Résumé :" -ForegroundColor White
Write-Host "  - Fichiers supprimés : $filesDeleted" -ForegroundColor Green
Write-Host "  - Fichiers non trouvés : $filesNotFound" -ForegroundColor Yellow
Write-Host ""

if ($filesDeleted -gt 0) {
    Write-Host "💡 Les fichiers obsolètes ont été supprimés avec succès." -ForegroundColor Cyan
    Write-Host "   L'application FastAPI continue de fonctionner normalement." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "📝 Note : Pour supprimer plus de fichiers, consultez :" -ForegroundColor Yellow
Write-Host "   FICHIERS_OBSOLETES_STREAMLIT.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
