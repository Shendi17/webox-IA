"""
Test de connexion à la base de données
Date : 31 Octobre 2025
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Test de connexion à PostgreSQL...")
print("")

try:
    from app.database import SessionLocal, engine
    from app.models.user_db import UserDB
    
    print("✅ Imports réussis")
    print("")
    
    # Tester la connexion
    print("🔌 Test de connexion à la base de données...")
    db = SessionLocal()
    
    # Compter les utilisateurs
    user_count = db.query(UserDB).count()
    print(f"✅ Connexion réussie ! {user_count} utilisateur(s) dans la base")
    print("")
    
    # Afficher les utilisateurs
    users = db.query(UserDB).all()
    print("📋 Liste des utilisateurs :")
    for user in users:
        print(f"   - {user.email} ({user.name}) - Role: {user.role}")
    
    db.close()
    print("")
    print("✅ Test terminé avec succès !")
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    print("")
    import traceback
    traceback.print_exc()
