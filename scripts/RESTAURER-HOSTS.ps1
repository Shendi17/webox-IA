# Script pour restaurer le fichier hosts a partir d'une sauvegarde

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "         RESTAURATION DU FICHIER HOSTS                          " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Verifier les droits admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ATTENTION: Droits administrateur requis" -ForegroundColor Yellow
    Write-Host "Relancement avec les droits administrateur..." -ForegroundColor Cyan
    
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$scriptPath`""
    exit
}

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsDir = "$env:SystemRoot\System32\drivers\etc"

Write-Host "Recherche des sauvegardes disponibles..." -ForegroundColor Cyan
Write-Host ""

# Lister les sauvegardes
$backups = Get-ChildItem -Path $hostsDir -Filter "hosts.backup-*" | Sort-Object LastWriteTime -Descending

if ($backups.Count -eq 0) {
    Write-Host "Aucune sauvegarde trouvee!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vous pouvez restaurer manuellement en recreant le fichier hosts" -ForegroundColor Yellow
    Write-Host "avec vos entrees de projets." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "Sauvegardes disponibles :" -ForegroundColor Green
Write-Host ""

for ($i = 0; $i -lt $backups.Count; $i++) {
    $backup = $backups[$i]
    Write-Host "[$($i + 1)] $($backup.Name)" -ForegroundColor White
    Write-Host "    Date : $($backup.LastWriteTime)" -ForegroundColor Gray
    
    # Afficher un apercu du contenu
    $content = Get-Content $backup.FullName -Raw
    $lines = $content -split "`r?`n" | Where-Object { $_ -match "^\s*[^#]" -and $_.Trim() -ne "" }
    if ($lines) {
        Write-Host "    Entrees :" -ForegroundColor Gray
        foreach ($line in $lines | Select-Object -First 5) {
            Write-Host "      $line" -ForegroundColor DarkGray
        }
        if ($lines.Count -gt 5) {
            Write-Host "      ... et $($lines.Count - 5) autres entrees" -ForegroundColor DarkGray
        }
    }
    Write-Host ""
}

Write-Host "Quelle sauvegarde voulez-vous restaurer ? (1-$($backups.Count))" -ForegroundColor Cyan
$choice = Read-Host

try {
    $index = [int]$choice - 1
    
    if ($index -lt 0 -or $index -ge $backups.Count) {
        Write-Host ""
        Write-Host "Choix invalide!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Appuyez sur une touche pour fermer..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit
    }
    
    $selectedBackup = $backups[$index]
    
    Write-Host ""
    Write-Host "Restauration de : $($selectedBackup.Name)" -ForegroundColor Yellow
    Write-Host ""
    
    # Faire une sauvegarde du fichier actuel avant de restaurer
    $currentBackup = "$hostsPath.avant-restauration-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -Path $hostsPath -Destination $currentBackup -Force
    Write-Host "Sauvegarde du fichier actuel : $currentBackup" -ForegroundColor Cyan
    
    # Restaurer
    Copy-Item -Path $selectedBackup.FullName -Destination $hostsPath -Force
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "              RESTAURATION REUSSIE !                            " -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    
    # Afficher le contenu restaure
    Write-Host "Contenu restaure :" -ForegroundColor Cyan
    $restoredContent = Get-Content $hostsPath -Raw
    $restoredLines = $restoredContent -split "`r?`n" | Where-Object { $_ -match "^\s*[^#]" -and $_.Trim() -ne "" }
    foreach ($line in $restoredLines) {
        Write-Host "  $line" -ForegroundColor White
    }
    Write-Host ""
    
    # Vider le cache DNS
    Write-Host "Vidage du cache DNS..." -ForegroundColor Cyan
    ipconfig /flushdns | Out-Null
    Write-Host "OK - Cache DNS vide" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "ERREUR : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
