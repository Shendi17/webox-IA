# Configuration SQLite pour WeBox
# Date : 1er Novembre 2025

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     CONFIGURATION SQLITE - WEBOX                               " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "SQLite est une base de données légère qui :" -ForegroundColor Yellow
Write-Host "  ✅ Fonctionne sans serveur" -ForegroundColor Green
Write-Host "  ✅ Pas de problème d'encodage" -ForegroundColor Green
Write-Host "  ✅ Parfait pour le développement" -ForegroundColor Green
Write-Host "  ✅ Migration facile vers PostgreSQL plus tard" -ForegroundColor Green
Write-Host ""

Write-Host "Étape 1 : Mise à jour de database.py..." -ForegroundColor Cyan

$databasePy = @"
"""
Configuration de la base de données SQLite
Date : 1er Novembre 2025
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de connexion à la base de données SQLite
DATABASE_URL = "sqlite:///./webox.db"

# Créer le moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Nécessaire pour SQLite
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

Write-Host "Étape 2 : Test de connexion..." -ForegroundColor Cyan

$testScript = @"
from app.database import engine, Base
from sqlalchemy import text

try:
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    # Tester la connexion
    with engine.connect() as conn:
        result = conn.execute(text("SELECT sqlite_version();"))
        version = result.fetchone()[0]
        print(f"✅ Connexion SQLite réussie !")
        print(f"SQLite version : {version}")
        print(f"Fichier de base de données : webox.db")
except Exception as e:
    print(f"❌ Erreur : {e}")
    import traceback
    traceback.print_exc()
"@

$testScript | Out-File -FilePath "C:\Users\Anthony\CascadeProjects\webox\test_sqlite.py" -Encoding UTF8 -Force

python C:\Users\Anthony\CascadeProjects\webox\test_sqlite.py

Write-Host ""
Write-Host "================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ CONFIGURATION SQLITE TERMINÉE !" -ForegroundColor Green
Write-Host ""
Write-Host "Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Créer les tables : python create_tables.py" -ForegroundColor White
Write-Host "  2. Créer l'utilisateur admin : python create_test_user.py" -ForegroundColor White
Write-Host "  3. Lancer le backend : python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor White
Write-Host "  4. Tester la connexion : http://webox.local:8000/login" -ForegroundColor White
Write-Host ""
Write-Host "Base de données : webox.db (fichier local)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note : Vous pourrez migrer vers PostgreSQL plus tard quand" -ForegroundColor Gray
Write-Host "       le problème d'encodage sera résolu." -ForegroundColor Gray
Write-Host ""

Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
