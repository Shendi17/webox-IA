# Script pour encoder le mot de passe dans DATABASE_URL
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           ENCODAGE MOT DE PASSE - DATABASE_URL               ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  Problème détecté : Le mot de passe contient des caractères spéciaux" -ForegroundColor Yellow
Write-Host "   qui doivent être encodés dans l'URL PostgreSQL." -ForegroundColor Yellow
Write-Host ""

$password = Read-Host "Entrez le mot de passe de 'webox_user'"

# Encoder le mot de passe pour URL
Add-Type -AssemblyName System.Web
$encodedPassword = [System.Web.HttpUtility]::UrlEncode($password)

Write-Host ""
Write-Host "✅ Mot de passe encodé !" -ForegroundColor Green
Write-Host ""

$databaseUrl = "DATABASE_URL=postgresql://webox_user:$encodedPassword@localhost:5432/webox_db"

Write-Host "📝 Nouvelle ligne DATABASE_URL :" -ForegroundColor Cyan
Write-Host ""
Write-Host $databaseUrl -ForegroundColor Yellow
Write-Host ""

# Mettre à jour le .env
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -match "DATABASE_URL=") {
        $envContent = $envContent -replace "DATABASE_URL=.*", $databaseUrl
        Set-Content ".env" $envContent -NoNewline -Encoding UTF8
        Write-Host "✅ Fichier .env mis à jour" -ForegroundColor Green
    } else {
        Add-Content ".env" "`n# PostgreSQL Database"
        Add-Content ".env" $databaseUrl
        Write-Host "✅ DATABASE_URL ajouté au .env" -ForegroundColor Green
    }
} else {
    Write-Host "❌ Fichier .env non trouvé" -ForegroundColor Red
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "🎯 Prochaine étape : Créer les tables" -ForegroundColor Cyan
Write-Host "   python create_tables.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
