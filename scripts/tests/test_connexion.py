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
