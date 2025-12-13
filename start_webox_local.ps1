# Script de démarrage WeBox sur webox.local

Write-Host "🚀 Démarrage de WeBox Multi-IA sur webox.local..." -ForegroundColor Cyan

# Vérifier si le fichier hosts contient webox.local
$hostsFile = "C:\Windows\System32\drivers\etc\hosts"
$hostsContent = Get-Content $hostsFile -Raw

if ($hostsContent -notmatch "webox.local") {
    Write-Host "⚠️  Ajout de webox.local au fichier hosts..." -ForegroundColor Yellow
    Write-Host "   Nécessite les droits administrateur" -ForegroundColor Yellow
    
    # Demander les droits admin
    if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur" -ForegroundColor Red
        Write-Host "   Clic droit sur PowerShell > Exécuter en tant qu'administrateur" -ForegroundColor Yellow
        pause
        exit
    }
    
    Add-Content -Path $hostsFile -Value "`n127.0.0.1    webox.local"
    Write-Host "✅ webox.local ajouté au fichier hosts" -ForegroundColor Green
} else {
    Write-Host "✅ webox.local déjà configuré dans le fichier hosts" -ForegroundColor Green
}

# Arrêter les anciens processus
Write-Host "🧹 Nettoyage des anciens processus..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Démarrer FastAPI sur le port 80
Write-Host "🌐 Lancement du serveur sur http://webox.local:8000" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Yellow
Write-Host "📱 Accédez à l'application via :" -ForegroundColor Cyan
Write-Host "   - http://webox.local:8000" -ForegroundColor Green
Write-Host "   - http://localhost:8000" -ForegroundColor Green
Write-Host "" -ForegroundColor Yellow

# Démarrer le serveur
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

Write-Host "`n💡 Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Cyan
