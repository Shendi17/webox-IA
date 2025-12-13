# Script de création de sauvegarde complète
# Avant migration FastAPI
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           CRÉATION SAUVEGARDE COMPLÈTE - WEBOX              ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Générer le nom de la sauvegarde avec timestamp
$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupName = "webox_backup_$date.zip"
$projectPath = "C:\Users\Anthony\CascadeProjects\webox"
$backupPath = "C:\Users\Anthony\CascadeProjects\$backupName"

Write-Host "📦 Informations de sauvegarde :" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Source : $projectPath" -ForegroundColor White
Write-Host "  Destination : $backupPath" -ForegroundColor White
Write-Host "  Date : $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor White
Write-Host ""

# Calculer la taille du projet
Write-Host "📊 Calcul de la taille du projet..." -ForegroundColor Cyan
$totalSize = 0
Get-ChildItem -Path $projectPath -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    $totalSize += $_.Length
}
$sizeMB = [math]::Round($totalSize / 1MB, 2)
Write-Host "  Taille totale : $sizeMB MB" -ForegroundColor White
Write-Host ""

$confirmation = Read-Host "Voulez-vous créer la sauvegarde ? (O/N)"

if ($confirmation -ne "O" -and $confirmation -ne "o") {
    Write-Host ""
    Write-Host "❌ Opération annulée" -ForegroundColor Red
    Write-Host ""
    pause
    exit
}

Write-Host ""
Write-Host "🔄 Création de la sauvegarde en cours..." -ForegroundColor Cyan
Write-Host "   Cela peut prendre quelques minutes..." -ForegroundColor Yellow
Write-Host ""

try {
    # Créer l'archive ZIP
    Compress-Archive -Path "$projectPath\*" -DestinationPath $backupPath -Force -ErrorAction Stop
    
    Write-Host "✅ Sauvegarde créée avec succès !" -ForegroundColor Green
    Write-Host ""
    
    # Vérifier la taille de l'archive
    $archiveSize = (Get-Item $backupPath).Length
    $archiveSizeMB = [math]::Round($archiveSize / 1MB, 2)
    
    Write-Host "📊 Détails de la sauvegarde :" -ForegroundColor Cyan
    Write-Host "  Fichier : $backupName" -ForegroundColor White
    Write-Host "  Taille : $archiveSizeMB MB" -ForegroundColor White
    Write-Host "  Emplacement : C:\Users\Anthony\CascadeProjects\" -ForegroundColor White
    Write-Host ""
    
    Write-Host "💡 Conseils :" -ForegroundColor Yellow
    Write-Host "  - Conservez cette sauvegarde jusqu'à la fin de la migration" -ForegroundColor Gray
    Write-Host "  - Vous pouvez la copier sur un disque externe pour plus de sécurité" -ForegroundColor Gray
    Write-Host "  - Pour restaurer : Extraire le ZIP dans le dossier du projet" -ForegroundColor Gray
    Write-Host ""
    
    # Proposer d'ouvrir l'emplacement
    $openFolder = Read-Host "Voulez-vous ouvrir l'emplacement de la sauvegarde ? (O/N)"
    if ($openFolder -eq "O" -or $openFolder -eq "o") {
        explorer "C:\Users\Anthony\CascadeProjects\"
    }
}
catch {
    Write-Host "❌ Erreur lors de la création de la sauvegarde !" -ForegroundColor Red
    Write-Host "   $_" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
