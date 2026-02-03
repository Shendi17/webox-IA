# Script pour vider le cache et redémarrer le serveur
# Date: 14 Décembre 2024

Write-Host "🧹 Nettoyage du cache..." -ForegroundColor Cyan

# Arrêter le serveur si en cours d'exécution
Write-Host "Arrêt du serveur..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*webox*" } | Stop-Process -Force

# Attendre un peu
Start-Sleep -Seconds 2

# Vider le cache Python
Write-Host "Nettoyage des fichiers __pycache__..." -ForegroundColor Yellow
Get-ChildItem -Path "C:\Users\Anthony\CascadeProjects\webox" -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Redémarrer le serveur
Write-Host "`n✅ Cache nettoyé!" -ForegroundColor Green
Write-Host "`n🚀 Redémarrage du serveur..." -ForegroundColor Cyan
Write-Host "Utilisez: python main.py" -ForegroundColor Yellow
Write-Host "`nPuis dans le navigateur:" -ForegroundColor White
Write-Host "  1. Ouvrez les DevTools (F12)" -ForegroundColor White
Write-Host "  2. Faites un clic droit sur le bouton Actualiser" -ForegroundColor White
Write-Host "  3. Sélectionnez 'Vider le cache et actualiser'" -ForegroundColor White
