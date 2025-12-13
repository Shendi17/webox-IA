# Script de configuration PostgreSQL pour WeBox
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           CONFIGURATION POSTGRESQL - WEBOX                   ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Étape 1 : Trouver PostgreSQL
Write-Host "🔍 Recherche de PostgreSQL..." -ForegroundColor Cyan
Write-Host ""

$postgresPath = $null
$possiblePaths = @(
    "C:\Program Files\PostgreSQL\16\bin",
    "C:\Program Files\PostgreSQL\15\bin",
    "C:\Program Files\PostgreSQL\14\bin",
    "C:\Program Files (x86)\PostgreSQL\16\bin",
    "C:\Program Files (x86)\PostgreSQL\15\bin"
)

foreach ($path in $possiblePaths) {
    if (Test-Path "$path\psql.exe") {
        $postgresPath = $path
        Write-Host "✅ PostgreSQL trouvé : $path" -ForegroundColor Green
        break
    }
}

if (-not $postgresPath) {
    Write-Host "❌ PostgreSQL non trouvé dans les emplacements standards" -ForegroundColor Red
    Write-Host ""
    Write-Host "Vérifiez que PostgreSQL est bien installé." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host ""

# Étape 2 : Ajouter au PATH temporairement
Write-Host "⚙️  Ajout de PostgreSQL au PATH..." -ForegroundColor Cyan
$env:Path += ";$postgresPath"
Write-Host "✅ PATH mis à jour pour cette session" -ForegroundColor Green
Write-Host ""

# Étape 3 : Vérifier la version
Write-Host "📊 Version de PostgreSQL :" -ForegroundColor Cyan
& "$postgresPath\psql.exe" --version
Write-Host ""

# Étape 4 : Demander le mot de passe postgres
Write-Host "🔐 Configuration de la base de données" -ForegroundColor Cyan
Write-Host ""
Write-Host "Vous allez créer la base de données WeBox." -ForegroundColor White
Write-Host "Vous aurez besoin du mot de passe que vous avez défini lors de l'installation." -ForegroundColor White
Write-Host ""

$postgresPassword = Read-Host "Entrez le mot de passe de l'utilisateur 'postgres'" -AsSecureString
$postgresPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($postgresPassword)
)

Write-Host ""
Write-Host "🔑 Mot de passe pour le nouvel utilisateur 'webox_user'" -ForegroundColor Cyan
$weboxPassword = Read-Host "Choisissez un mot de passe pour 'webox_user'" -AsSecureString
$weboxPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($weboxPassword)
)

Write-Host ""
Write-Host "📝 Création de la base de données..." -ForegroundColor Cyan
Write-Host ""

# Créer un fichier SQL temporaire
$sqlFile = "$env:TEMP\webox_setup.sql"
$sqlCommands = @"
-- Créer la base de données
CREATE DATABASE webox_db;

-- Créer l'utilisateur
CREATE USER webox_user WITH PASSWORD '$weboxPasswordPlain';

-- Accorder tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE webox_db TO webox_user;

-- Afficher un message de confirmation
\echo 'Base de données webox_db créée avec succès!'
\echo 'Utilisateur webox_user créé avec succès!'
"@

Set-Content -Path $sqlFile -Value $sqlCommands -Encoding UTF8

# Exécuter les commandes SQL
$env:PGPASSWORD = $postgresPasswordPlain
try {
    & "$postgresPath\psql.exe" -U postgres -f $sqlFile
    
    Write-Host ""
    Write-Host "✅ Configuration terminée avec succès !" -ForegroundColor Green
    Write-Host ""
    
    # Tester la connexion
    Write-Host "🧪 Test de connexion..." -ForegroundColor Cyan
    $env:PGPASSWORD = $weboxPasswordPlain
    $testResult = & "$postgresPath\psql.exe" -U webox_user -d webox_db -c "SELECT version();" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Connexion réussie à la base de données !" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Erreur de connexion : $testResult" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Erreur lors de la configuration : $_" -ForegroundColor Red
}
finally {
    # Nettoyer
    Remove-Item $sqlFile -ErrorAction SilentlyContinue
    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 Configuration du fichier .env" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ajoutez cette ligne dans votre fichier .env :" -ForegroundColor White
Write-Host ""
Write-Host "DATABASE_URL=postgresql://webox_user:$weboxPasswordPlain@localhost:5432/webox_db" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Conseil : Copiez cette ligne et ajoutez-la dans votre fichier .env" -ForegroundColor Cyan
Write-Host ""

# Proposer d'ouvrir le fichier .env
$openEnv = Read-Host "Voulez-vous ouvrir le fichier .env maintenant ? (O/N)"
if ($openEnv -eq "O" -or $openEnv -eq "o") {
    if (Test-Path ".env") {
        notepad .env
    } else {
        Write-Host "⚠️  Fichier .env non trouvé. Création..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env" -ErrorAction SilentlyContinue
        notepad .env
    }
}

Write-Host ""
Write-Host "🎉 Configuration PostgreSQL terminée !" -ForegroundColor Green
Write-Host ""
Write-Host "Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Installer les dépendances Python" -ForegroundColor White
Write-Host "  2. Configurer SQLAlchemy et Alembic" -ForegroundColor White
Write-Host "  3. Créer les modèles de données" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
