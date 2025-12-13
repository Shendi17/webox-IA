# Script pour ouvrir WeBox dans le navigateur

Write-Host "🌐 Ouverture de WeBox Multi-IA dans le navigateur..." -ForegroundColor Cyan
Write-Host ""

# Essayer localhost
Start-Process "http://localhost:8501"

Write-Host "✅ Navigateur ouvert sur http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Si webox.local est configuré, vous pouvez aussi accéder à :" -ForegroundColor Yellow
Write-Host "   → http://webox.local:8501" -ForegroundColor Cyan
Write-Host ""
