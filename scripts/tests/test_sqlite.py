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
