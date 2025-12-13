# Configuration PostgreSQL natif Windows pour WeBox
# Date : 1er Novembre 2025
# DOIT ÊTRE EXÉCUTÉ EN TANT QU'ADMINISTRATEUR

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     CONFIGURATION POSTGRESQL NATIF - WEBOX                     " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Cette solution utilise PostgreSQL Windows natif" -ForegroundColor Yellow
Write-Host "au lieu de Docker (qui ne fonctionne pas sur Boot Camp)" -ForegroundColor Yellow
Write-Host ""

# Demander le mot de passe postgres
$postgresPassword = Read-Host "Entrez le mot de passe de l'utilisateur 'postgres'" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($postgresPassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "Étape 1 : Configuration de l'encodage système..." -ForegroundColor Cyan

# Définir les variables d'environnement pour forcer UTF-8
[Environment]::SetEnvironmentVariable("PGCLIENTENCODING", "UTF8", "User")
[Environment]::SetEnvironmentVariable("LANG", "en_US.UTF-8", "User")

$env:PGCLIENTENCODING = "UTF8"
$env:LANG = "en_US.UTF-8"
$env:PGPASSWORD = $plainPassword

Write-Host "✅ Variables d'environnement configurées" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 2 : Recréation de la base de données..." -ForegroundColor Cyan

# Supprimer l'ancienne base
psql -U postgres -c "DROP DATABASE IF EXISTS webox_db;" 2>$null
psql -U postgres -c "DROP USER IF EXISTS webox_user;" 2>$null

Write-Host "✅ Nettoyage effectué" -ForegroundColor Green

# Créer le nouvel utilisateur
Write-Host "Création de l'utilisateur webox_user..." -ForegroundColor Yellow
psql -U postgres -c "CREATE USER webox_user WITH PASSWORD 'admin123';"

# Créer la base avec encodage UTF-8 explicite
Write-Host "Création de la base webox_db..." -ForegroundColor Yellow
psql -U postgres -c "CREATE DATABASE webox_db WITH OWNER webox_user ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"

# Donner tous les privilèges
Write-Host "Attribution des privilèges..." -ForegroundColor Yellow
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE webox_db TO webox_user;"
psql -U postgres -d webox_db -c "GRANT ALL ON SCHEMA public TO webox_user;"
psql -U postgres -d webox_db -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO webox_user;"

Write-Host "✅ Base de données créée" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 3 : Configuration de database.py..." -ForegroundColor Cyan

# Mettre à jour database.py
$databasePy = @"
"""
Configuration de la base de données PostgreSQL
Date : 1er Novembre 2025
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de connexion à la base de données
DATABASE_URL = "postgresql://webox_user:admin123@localhost:5432/webox_db"

# Créer le moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "options": "-c client_encoding=utf8"
    },
    echo=False
)

# Créer une session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"@

$databasePy | Out-File -FilePath "C:\Users\Anthony\CascadeProjects\webox\app\database.py" -Encoding UTF8 -Force

Write-Host "✅ database.py mis à jour" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 4 : Test de connexion..." -ForegroundColor Cyan

# Tester la connexion
$testScript = @"
import os
os.environ['PGCLIENTENCODING'] = 'UTF8'

from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connexion réussie !")
        print(f"PostgreSQL version : {version}")
except Exception as e:
    print(f"❌ Erreur : {e}")
"@

$testScript | Out-File -FilePath "C:\Users\Anthony\CascadeProjects\webox\test_connexion.py" -Encoding UTF8 -Force

python C:\Users\Anthony\CascadeProjects\webox\test_connexion.py

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ CONFIGURATION TERMINÉE !" -ForegroundColor Green
Write-Host ""
Write-Host "Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Créer les tables : python create_tables.py" -ForegroundColor White
Write-Host "  2. Créer l'utilisateur admin : python create_test_user.py" -ForegroundColor White
Write-Host "  3. Lancer le backend : python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor White
Write-Host "  4. Tester la connexion : http://webox.local:8000/login" -ForegroundColor White
Write-Host ""
Write-Host "Informations de connexion :" -ForegroundColor Yellow
Write-Host "  Database : webox_db" -ForegroundColor White
Write-Host "  User     : webox_user" -ForegroundColor White
Write-Host "  Password : admin123" -ForegroundColor White
Write-Host "  Host     : localhost" -ForegroundColor White
Write-Host "  Port     : 5432" -ForegroundColor White
Write-Host ""

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
