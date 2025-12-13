# Script pour configurer webox.local - À EXÉCUTER EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║         🔧 CONFIGURATION DE WEBOX.LOCAL                     ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Vérifier les droits administrateur
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ ERREUR : Ce script doit être exécuté en tant qu'administrateur" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pour exécuter en tant qu'administrateur :" -ForegroundColor Yellow
    Write-Host "  1. Clic droit sur PowerShell" -ForegroundColor White
    Write-Host "  2. Sélectionnez 'Exécuter en tant qu'administrateur'" -ForegroundColor White
    Write-Host "  3. Naviguez vers : cd c:\Users\Anthony\CascadeProjects\webox" -ForegroundColor White
    Write-Host "  4. Exécutez : .\fix-webox-local.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "Appuyez sur une touche pour fermer..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "✅ Droits administrateur confirmés" -ForegroundColor Green
Write-Host ""

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$hostsEntry = "127.0.0.1    webox.local"

Write-Host "📝 Vérification du fichier hosts..." -ForegroundColor Cyan
Write-Host "   Chemin : $hostsPath" -ForegroundColor Gray
Write-Host ""

# Lire le contenu actuel
try {
    $hostsContent = Get-Content $hostsPath -Raw -ErrorAction Stop
    
    # Vérifier si l'entrée existe déjà
    if ($hostsContent -match "webox\.local") {
        Write-Host "⚠️  Une entrée webox.local existe déjà" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Voulez-vous la remplacer ? (O/N)" -ForegroundColor Yellow
        $response = Read-Host
        
        if ($response -eq "O" -or $response -eq "o") {
            # Supprimer les anciennes entrées webox.local
            $hostsContent = $hostsContent -replace ".*webox\.local.*\r?\n?", ""
            Set-Content -Path $hostsPath -Value $hostsContent -NoNewline
            Write-Host "✅ Ancienne entrée supprimée" -ForegroundColor Green
        } else {
            Write-Host "❌ Opération annulée" -ForegroundColor Red
            Write-Host ""
            Write-Host "Appuyez sur une touche pour fermer..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 0
        }
    }
    
    # Ajouter la nouvelle entrée
    Write-Host "➕ Ajout de l'entrée webox.local..." -ForegroundColor Cyan
    
    # S'assurer qu'il y a une nouvelle ligne à la fin
    if (-not $hostsContent.EndsWith("`n")) {
        $hostsContent += "`n"
    }
    
    # Ajouter l'entrée
    $hostsContent += "$hostsEntry`n"
    
    # Sauvegarder
    Set-Content -Path $hostsPath -Value $hostsContent -NoNewline
    
    Write-Host "✅ Entrée ajoutée avec succès !" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Contenu ajouté :" -ForegroundColor Cyan
    Write-Host "   $hostsEntry" -ForegroundColor White
    Write-Host ""
    
    # Vider le cache DNS
    Write-Host "🔄 Vidage du cache DNS..." -ForegroundColor Cyan
    ipconfig /flushdns | Out-Null
    Write-Host "✅ Cache DNS vidé" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                              ║" -ForegroundColor Green
    Write-Host "║              ✅ CONFIGURATION TERMINÉE !                     ║" -ForegroundColor Green
    Write-Host "║                                                              ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Vous pouvez maintenant accéder à l'application via :" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   → http://webox.local:8501" -ForegroundColor Cyan
    Write-Host "   → http://localhost:8501" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  NOTE : N'oubliez pas le port :8501" -ForegroundColor Yellow
    Write-Host ""
    
    # Ouvrir dans le navigateur
    Write-Host "Voulez-vous ouvrir webox.local dans le navigateur ? (O/N)" -ForegroundColor Yellow
    $openBrowser = Read-Host
    
    if ($openBrowser -eq "O" -or $openBrowser -eq "o") {
        Start-Process "http://webox.local:8501"
        Write-Host "✅ Navigateur ouvert" -ForegroundColor Green
    }
    
} catch {
    Write-Host "❌ ERREUR : Impossible de modifier le fichier hosts" -ForegroundColor Red
    Write-Host "   Détails : $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
