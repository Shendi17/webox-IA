# Script pour ajouter DATABASE_URL dans .env
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           CONFIGURATION DATABASE_URL - WEBOX                 ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Vérifier si .env existe
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Fichier .env non trouvé. Création depuis .env.example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Fichier .env créé" -ForegroundColor Green
    } else {
        Write-Host "❌ Fichier .env.example non trouvé" -ForegroundColor Red
        pause
        exit
    }
}

Write-Host ""
Write-Host "🔐 Configuration de DATABASE_URL" -ForegroundColor Cyan
Write-Host ""

# Demander le mot de passe webox_user
$weboxPassword = Read-Host "Entrez le mot de passe de 'webox_user' (celui que vous avez choisi)"

# Créer la ligne DATABASE_URL
$databaseUrl = "DATABASE_URL=postgresql://webox_user:$weboxPassword@localhost:5432/webox_db"

Write-Host ""
Write-Host "📝 Ajout de DATABASE_URL dans .env..." -ForegroundColor Cyan

# Lire le contenu actuel de .env
$envContent = Get-Content ".env" -Raw

# Vérifier si DATABASE_URL existe déjà
if ($envContent -match "DATABASE_URL=") {
    Write-Host "⚠️  DATABASE_URL existe déjà dans .env" -ForegroundColor Yellow
    $replace = Read-Host "Voulez-vous le remplacer ? (O/N)"
    
    if ($replace -eq "O" -or $replace -eq "o") {
        # Remplacer la ligne existante
        $envContent = $envContent -replace "DATABASE_URL=.*", $databaseUrl
        Set-Content ".env" $envContent -NoNewline
        Write-Host "✅ DATABASE_URL mis à jour" -ForegroundColor Green
    } else {
        Write-Host "❌ Opération annulée" -ForegroundColor Red
    }
} else {
    # Ajouter DATABASE_URL
    Add-Content ".env" "`n# PostgreSQL Database"
    Add-Content ".env" $databaseUrl
    Write-Host "✅ DATABASE_URL ajouté" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Configuration terminée !" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Installer les dépendances Python" -ForegroundColor White
Write-Host "     pip install sqlalchemy alembic psycopg2-binary" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Initialiser Alembic" -ForegroundColor White
Write-Host "     cd app" -ForegroundColor Gray
Write-Host "     alembic init alembic" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Créer les modèles de données" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
