# Script pour ajouter UNIQUEMENT webox.local SANS toucher aux autres projets
# Version SAFE qui preserve toutes les entrees existantes

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "    AJOUT DE WEBOX.LOCAL (PRESERVE VOS AUTRES PROJETS)         " -ForegroundColor Cyan
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

Write-Host "OK - Droits administrateur confirmes" -ForegroundColor Green
Write-Host ""

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$backupPath = "$env:SystemRoot\System32\drivers\etc\hosts.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

try {
    # ETAPE 1 : Faire une sauvegarde du fichier hosts actuel
    Write-Host "ETAPE 1 : Sauvegarde du fichier hosts actuel..." -ForegroundColor Cyan
    Copy-Item -Path $hostsPath -Destination $backupPath -Force
    Write-Host "OK - Sauvegarde creee : $backupPath" -ForegroundColor Green
    Write-Host ""
    
    # ETAPE 2 : Lire le contenu actuel
    Write-Host "ETAPE 2 : Lecture du fichier hosts..." -ForegroundColor Cyan
    $hostsContent = Get-Content $hostsPath -Raw -ErrorAction SilentlyContinue
    
    if ([string]::IsNullOrEmpty($hostsContent)) {
        $hostsContent = ""
        Write-Host "ATTENTION - Fichier hosts vide!" -ForegroundColor Yellow
    } else {
        Write-Host "OK - Fichier hosts lu" -ForegroundColor Green
    }
    
    # Afficher les entrees actuelles
    $lines = $hostsContent -split "`r?`n" | Where-Object { $_ -match "^\s*[^#]" -and $_.Trim() -ne "" }
    if ($lines) {
        Write-Host ""
        Write-Host "Entrees actuelles dans le fichier hosts :" -ForegroundColor Cyan
        foreach ($line in $lines) {
            Write-Host "  $line" -ForegroundColor White
        }
    }
    Write-Host ""
    
    # ETAPE 3 : Verifier si webox.local existe deja
    Write-Host "ETAPE 3 : Verification de webox.local..." -ForegroundColor Cyan
    
    if ($hostsContent -match "^\s*127\.0\.0\.1\s+webox\.local\s*$" -or $hostsContent -match "webox\.local") {
        Write-Host "ATTENTION - webox.local existe deja dans le fichier hosts" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Voulez-vous quand meme mettre a jour l'entree ? (O/N)" -ForegroundColor Yellow
        $response = Read-Host
        
        if ($response -ne "O" -and $response -ne "o") {
            Write-Host ""
            Write-Host "Operation annulee - aucune modification apportee" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Appuyez sur une touche pour fermer..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit
        }
        
        # Supprimer UNIQUEMENT les lignes webox.local
        Write-Host "Suppression de l'ancienne entree webox.local..." -ForegroundColor Yellow
        $lines = $hostsContent -split "`r?`n"
        $newLines = $lines | Where-Object { $_ -notmatch "webox\.local" }
        $hostsContent = $newLines -join "`n"
    } else {
        Write-Host "OK - webox.local n'existe pas encore" -ForegroundColor Green
    }
    Write-Host ""
    
    # ETAPE 4 : Ajouter webox.local
    Write-Host "ETAPE 4 : Ajout de webox.local..." -ForegroundColor Cyan
    
    # S'assurer qu'il y a une nouvelle ligne a la fin
    if (-not [string]::IsNullOrEmpty($hostsContent) -and -not $hostsContent.EndsWith("`n")) {
        $hostsContent += "`n"
    }
    
    # Ajouter l'entree webox.local
    $hostsContent += "127.0.0.1    webox.local`n"
    
    # ETAPE 5 : Ecrire le nouveau contenu
    Write-Host "ETAPE 5 : Ecriture du fichier hosts..." -ForegroundColor Cyan
    Set-Content -Path $hostsPath -Value $hostsContent -NoNewline -Force
    Write-Host "OK - Fichier hosts mis a jour" -ForegroundColor Green
    Write-Host ""
    
    # ETAPE 6 : Afficher le nouveau contenu
    Write-Host "Nouvelles entrees dans le fichier hosts :" -ForegroundColor Cyan
    $newContent = Get-Content $hostsPath -Raw
    $newLines = $newContent -split "`r?`n" | Where-Object { $_ -match "^\s*[^#]" -and $_.Trim() -ne "" }
    foreach ($line in $newLines) {
        if ($line -match "webox\.local") {
            Write-Host "  $line" -ForegroundColor Green -NoNewline
            Write-Host " <- NOUVEAU" -ForegroundColor Yellow
        } else {
            Write-Host "  $line" -ForegroundColor White
        }
    }
    Write-Host ""
    
    # ETAPE 7 : Vider le cache DNS
    Write-Host "ETAPE 6 : Vidage du cache DNS..." -ForegroundColor Cyan
    ipconfig /flushdns | Out-Null
    Write-Host "OK - Cache DNS vide" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "              CONFIGURATION REUSSIE !                           " -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "webox.local a ete ajoute SANS modifier vos autres projets" -ForegroundColor Green
    Write-Host ""
    Write-Host "Sauvegarde disponible : $backupPath" -ForegroundColor Cyan
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "                    ERREUR                                      " -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Erreur : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "La sauvegarde est disponible ici :" -ForegroundColor Yellow
    Write-Host "$backupPath" -ForegroundColor White
    Write-Host ""
    Write-Host "Pour restaurer, executez :" -ForegroundColor Yellow
    Write-Host "Copy-Item '$backupPath' '$hostsPath' -Force" -ForegroundColor White
    Write-Host ""
}

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
