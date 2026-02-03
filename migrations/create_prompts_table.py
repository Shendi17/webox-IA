"""
Migration pour créer toutes les tables nécessaires
Date : 3 Février 2026
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.models.user_db import UserDB
from app.models.conversation_db import ConversationDB, MessageDB
from app.models.prompt_db import PromptDB

print("🔧 Création des tables de la base de données...")
print("")

try:
    # Créer toutes les tables dans le bon ordre (users en premier pour les foreign keys)
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables créées avec succès !")
    print("")
    print("Tables créées :")
    print("  - users")
    print("  - conversations")
    print("  - messages")
    print("  - prompts")
    print("")
    print("🎉 Migration terminée avec succès !")
    
except Exception as e:
    print(f"❌ Erreur lors de la création des tables : {e}")
    print("")
    import traceback
    traceback.print_exc()
