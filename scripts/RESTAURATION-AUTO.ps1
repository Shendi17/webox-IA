# Restauration automatique du fichier hosts
# Ce script restaure la derniere sauvegarde automatiquement

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "      RESTAURATION AUTOMATIQUE DU FICHIER HOSTS                " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Verifier les droits admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Relancement avec les droits administrateur..." -ForegroundColor Yellow
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File `"$scriptPath`""
    exit
}

Write-Host "OK - Droits administrateur confirmes" -ForegroundColor Green
Write-Host ""

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsDir = "$env:SystemRoot\System32\drivers\etc"

try {
    # Rechercher les sauvegardes
    Write-Host "Recherche de sauvegardes..." -ForegroundColor Cyan
    $backups = Get-ChildItem -Path $hostsDir -Filter "hosts.backup-*" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    
    if ($backups -and $backups.Count -gt 0) {
        # Utiliser la sauvegarde la plus recente
        $latestBackup = $backups[0]
        
        Write-Host "OK - Sauvegarde trouvee : $($latestBackup.Name)" -ForegroundColor Green
        Write-Host "     Date : $($latestBackup.LastWriteTime)" -ForegroundColor Gray
        Write-Host ""
        
        # Afficher le contenu de la sauvegarde
        Write-Host "Contenu de la sauvegarde :" -ForegroundColor Cyan
        $backupContent = Get-Content $latestBackup.FullName -Raw
        $backupLines = $backupContent -split "`r?`n" | Where-Object { $_ -match "^\s*[^#]" -and $_.Trim() -ne "" }
        
        if ($backupLines) {
            foreach ($line in $backupLines) {
                Write-Host "  $line" -ForegroundColor White
            }
        } else {
            Write-Host "  (fichier vide)" -ForegroundColor Gray
        }
        Write-Host ""
        
        # Faire une sauvegarde du fichier actuel
        $currentBackup = "$hostsPath.avant-restauration-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Write-Host "Sauvegarde du fichier actuel..." -ForegroundColor Cyan
        Copy-Item -Path $hostsPath -Destination $currentBackup -Force
        Write-Host "OK - Sauvegarde creee : $currentBackup" -ForegroundColor Green
        Write-Host ""
        
        # Restaurer
        Write-Host "Restauration en cours..." -ForegroundColor Cyan
        Copy-Item -Path $latestBackup.FullName -Destination $hostsPath -Force
        Write-Host "OK - Fichier hosts restaure" -ForegroundColor Green
        Write-Host ""
        
        # Ajouter webox.local si pas present
        $restoredContent = Get-Content $hostsPath -Raw
        
        if ($restoredContent -notmatch "webox\.local") {
            Write-Host "Ajout de webox.local..." -ForegroundColor Cyan
            
            if (-not $restoredContent.EndsWith("`n")) {
                $restoredContent += "`n"
            }
            $restoredContent += "127.0.0.1    webox.local`n"
            
            Set-Content -Path $hostsPath -Value $restoredContent -NoNewline -Force
            Write-Host "OK - webox.local ajoute" -ForegroundColor Green
        } else {
            Write-Host "OK - webox.local deja present" -ForegroundColor Green
        }
        Write-Host ""
        
        # Afficher le resultat final
        Write-Host "Contenu final du fichier hosts :" -ForegroundColor Cyan
        $finalContent = Get-Content $hostsPath -Raw
        $finalLines = $finalContent -split "`r?`n" | Where-Object { $_ -match "^\s*[^#]" -and $_.Trim() -ne "" }
        
        foreach ($line in $finalLines) {
            if ($line -match "webox\.local") {
                Write-Host "  $line" -ForegroundColor Green
            } else {
                Write-Host "  $line" -ForegroundColor White
            }
        }
        Write-Host ""
        
        # Vider le cache DNS
        Write-Host "Vidage du cache DNS..." -ForegroundColor Cyan
        ipconfig /flushdns | Out-Null
        Write-Host "OK - Cache DNS vide" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host "           RESTAURATION REUSSIE !                               " -ForegroundColor Green
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Vos projets sont maintenant accessibles !" -ForegroundColor Green
        Write-Host "webox.local a ete ajoute sans toucher aux autres projets." -ForegroundColor Green
        Write-Host ""
        
    } else {
        # Pas de sauvegarde - creer un fichier hosts avec webox.local uniquement
        Write-Host "ATTENTION - Aucune sauvegarde trouvee" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Je vais creer un fichier hosts de base avec webox.local" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "IMPORTANT: Vous devrez ajouter vos autres projets manuellement !" -ForegroundColor Red
        Write-Host ""
        
        # Sauvegarder le fichier actuel
        $currentBackup = "$hostsPath.avant-restauration-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item -Path $hostsPath -Destination $currentBackup -Force -ErrorAction SilentlyContinue
        
        # Creer un fichier hosts de base
        $defaultHosts = @"
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost

# Projets locaux
127.0.0.1    webox.local
"@
        
        Set-Content -Path $hostsPath -Value $defaultHosts -Force
        Write-Host "OK - Fichier hosts cree avec webox.local" -ForegroundColor Green
        Write-Host ""
        Write-Host "ATTENTION: Ajoutez vos autres projets manuellement !" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Voulez-vous ouvrir le fichier hosts pour ajouter vos projets ? (O/N)" -ForegroundColor Cyan
        $response = Read-Host
        
        if ($response -eq "O" -or $response -eq "o") {
            notepad $hostsPath
        }
    }
    
} catch {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "                    ERREUR                                      " -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Erreur : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
