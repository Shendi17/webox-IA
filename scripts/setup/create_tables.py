"""
Script pour créer les tables PostgreSQL
Date : 30 Octobre 2025
"""

from app.database import Base, engine
from app.models.user_db import UserDB
from app.models.conversation_db import ConversationDB, MessageDB
from app.models.prompt_db import PromptDB

print("🔧 Création des tables PostgreSQL...")
print("")

try:
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables créées avec succès !")
    print("")
    print("Tables créées :")
    print("  - users")
    print("  - conversations")
    print("  - messages")
    print("  - prompts")
    print("")
    print("🎉 Base de données prête à l'emploi !")
    
except Exception as e:
    print(f"❌ Erreur lors de la création des tables : {e}")
    print("")
    print("Vérifiez votre fichier .env et DATABASE_URL")
