"""
Test de connexion PostgreSQL direct
Date : 30 Octobre 2025
"""

import urllib.parse
from sqlalchemy import create_engine, text

print("🔧 Test de connexion PostgreSQL...")
print("")

# Demander les informations
password = input("Entrez le mot de passe de 'webox_user': ")

# Encoder le mot de passe
encoded_password = urllib.parse.quote_plus(password)

# Créer l'URL
database_url = f"postgresql://webox_user:{encoded_password}@localhost:5432/webox_db"

print("")
print("📡 Tentative de connexion...")

try:
    # Créer le moteur
    engine = create_engine(database_url)
    
    # Tester la connexion
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        
        print("")
        print("✅ Connexion réussie !")
        print("")
        print(f"📊 Version PostgreSQL :")
        print(f"   {version}")
        print("")
        
        # Maintenant créer les tables
        print("🔧 Création des tables...")
        
        from app.database import Base
        from app.models.user_db import UserDB
        from app.models.conversation_db import ConversationDB, MessageDB
        
        Base.metadata.create_all(bind=engine)
        
        print("")
        print("✅ Tables créées avec succès !")
        print("")
        print("Tables créées :")
        print("  - users")
        print("  - conversations")
        print("  - messages")
        print("")
        print("🎉 Base de données prête à l'emploi !")
        
except Exception as e:
    print("")
    print(f"❌ Erreur : {e}")
    print("")
    print("Vérifiez :")
    print("  - Le mot de passe est correct")
    print("  - PostgreSQL est démarré")
    print("  - La base de données webox_db existe")

print("")
