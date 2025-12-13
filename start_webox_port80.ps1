# Script de démarrage WeBox sur le port 80 (nécessite admin)
# Permet d'accéder à http://webox.local sans spécifier le port

# Vérifier les droits administrateur
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Ce script nécessite les droits administrateur" -ForegroundColor Red
    Write-Host "   Clic droit sur PowerShell > Exécuter en tant qu'administrateur" -ForegroundColor Yellow
    Write-Host "   Puis relancez ce script" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "🚀 Démarrage de WeBox Multi-IA sur le port 80..." -ForegroundColor Cyan

# Vérifier si le port 80 est disponible
$port80InUse = Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue

if ($port80InUse) {
    Write-Host "⚠️  Le port 80 est déjà utilisé" -ForegroundColor Yellow
    Write-Host "   Processus : $($port80InUse.OwningProcess)" -ForegroundColor Yellow
    
    $response = Read-Host "Voulez-vous arrêter le processus qui utilise le port 80 ? (O/N)"
    if ($response -eq "O" -or $response -eq "o") {
        Stop-Process -Id $port80InUse.OwningProcess -Force
        Write-Host "✅ Processus arrêté" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "❌ Impossible de démarrer sur le port 80" -ForegroundColor Red
        Write-Host "   Utilisez plutôt : .\start_webox_local.ps1 (port 8000)" -ForegroundColor Yellow
        pause
        exit
    }
}

# Arrêter les anciens processus uvicorn
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "🌐 Lancement du serveur sur http://webox.local" -ForegroundColor Yellow
Write-Host "" -ForegroundColor Yellow
Write-Host "📱 Accédez à l'application via :" -ForegroundColor Cyan
Write-Host "   - http://webox.local" -ForegroundColor Green
Write-Host "   - http://localhost" -ForegroundColor Green
Write-Host "" -ForegroundColor Yellow

# Démarrer le serveur sur le port 80
python -m uvicorn main:app --reload --host 0.0.0.0 --port 80

Write-Host "`n💡 Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Cyan
