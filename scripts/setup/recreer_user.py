"""
Recréer l'utilisateur test avec le bon mot de passe
Date: 24 Janvier 2026
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from passlib.context import CryptContext

# Importer tous les modèles
try:
    from app.models.user_db import UserDB
    from app.models.conversation_db import ConversationDB
    from app.models.prompt_db import PromptDB
    from app.models.product_db import ProductDB, CartItemDB, OrderDB
except ImportError as e:
    print(f"Avertissement import: {e}")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def recreate_user():
    """Recréer l'utilisateur test"""
    
    print("\n" + "="*60)
    print("RECREATION UTILISATEUR TEST")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Supprimer l'ancien utilisateur s'il existe
        existing_user = db.query(UserDB).filter(UserDB.email == "test@webox.com").first()
        
        if existing_user:
            print(f"Suppression ancien utilisateur ID {existing_user.id}...")
            db.delete(existing_user)
            db.commit()
        
        # Créer le nouveau avec le bon hash
        hashed_password = pwd_context.hash("test123456")
        
        test_user = UserDB(
            email="test@webox.com",
            username="testuser",
            name="Test User",
            hashed_password=hashed_password,
            is_active=True,
            is_admin=False,
            is_premium=True,
            role="user"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        # Vérifier le mot de passe
        if pwd_context.verify("test123456", test_user.hashed_password):
            print("OK Utilisateur cree avec succes!")
            print(f"   ID: {test_user.id}")
            print(f"   Email: test@webox.com")
            print(f"   Password: test123456")
            print(f"   Hash valide: OUI")
        else:
            print("ERREUR Hash invalide")
        
    except Exception as e:
        db.rollback()
        print(f"ERREUR: {e}")
    finally:
        db.close()
    
    print("\n" + "="*60)

if __name__ == "__main__":
    recreate_user()
