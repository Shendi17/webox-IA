# Script pour configurer webox.local dans le fichier hosts
# À exécuter en tant qu'administrateur

Write-Host "🔧 Configuration de webox.local..." -ForegroundColor Cyan
Write-Host ""

$hostsFile = "C:\Windows\System32\drivers\etc\hosts"
$entry = "127.0.0.1    webox.local"

# Vérifier si l'entrée existe déjà
$content = Get-Content $hostsFile -ErrorAction SilentlyContinue
if ($content -match "webox.local") {
    Write-Host "✅ webox.local est déjà configuré dans le fichier hosts" -ForegroundColor Green
} else {
    try {
        # Ajouter l'entrée
        Add-Content -Path $hostsFile -Value "`n$entry"
        Write-Host "✅ webox.local ajouté au fichier hosts" -ForegroundColor Green
        Write-Host ""
        Write-Host "Vous pouvez maintenant accéder à l'application via :" -ForegroundColor Yellow
        Write-Host "  → http://webox.local:8501" -ForegroundColor Cyan
    } catch {
        Write-Host "❌ Erreur : Ce script doit être exécuté en tant qu'administrateur" -ForegroundColor Red
        Write-Host ""
        Write-Host "Pour exécuter en tant qu'admin :" -ForegroundColor Yellow
        Write-Host "  1. Clic droit sur PowerShell" -ForegroundColor White
        Write-Host "  2. 'Exécuter en tant qu'administrateur'" -ForegroundColor White
        Write-Host "  3. Exécutez : .\configure-hosts.ps1" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
