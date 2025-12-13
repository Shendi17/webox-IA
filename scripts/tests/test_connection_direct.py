"""
Test de connexion PostgreSQL direct sans fichiers de config
Date : 31 Octobre 2025
"""

import os
import sys

# Forcer l'encodage UTF-8 pour tout
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Désactiver les fichiers de configuration PostgreSQL
os.environ['PGPASSFILE'] = ''
os.environ['PGSERVICEFILE'] = ''

print("🔍 Test de connexion PostgreSQL direct...")
print("")

try:
    import psycopg2
    
    # Connexion directe avec paramètres explicites
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="webox_db",
        user="webox_user",
        password="admin123",
        client_encoding='utf8'
    )
    
    print("✅ Connexion réussie !")
    print("")
    
    # Tester une requête
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📊 PostgreSQL version : {version[0]}")
    print("")
    
    # Vérifier les tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"✅ {len(tables)} table(s) trouvée(s) :")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("⚠️  Aucune table trouvée - Les tables doivent être créées")
    
    cursor.close()
    conn.close()
    
    print("")
    print("✅ Test terminé avec succès !")
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    print("")
    import traceback
    traceback.print_exc()
