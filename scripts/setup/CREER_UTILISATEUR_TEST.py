"""
Script pour créer un utilisateur test
Date: 24 Janvier 2026
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from passlib.context import CryptContext

# Importer tous les modèles pour éviter les erreurs de relations
try:
    from app.models.user_db import UserDB
    from app.models.conversation_db import ConversationDB
    from app.models.prompt_db import PromptDB
    from app.models.product_db import ProductDB, CartItemDB, OrderDB
except ImportError as e:
    print(f"⚠️ Avertissement import: {e}")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    """Créer un utilisateur test"""
    
    print("\n" + "="*60)
    print("👤 CRÉATION UTILISATEUR TEST")
    print("="*60 + "\n")
    
    db = SessionLocal()
    
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(UserDB).filter(UserDB.email == "test@webox.com").first()
        
        if existing_user:
            print("⚠️ L'utilisateur test@webox.com existe déjà")
            print(f"   ID: {existing_user.id}")
            print(f"   Username: {existing_user.username}")
            print(f"   Email: {existing_user.email}")
            print(f"   Créé le: {existing_user.created_at}")
            return
        
        # Créer l'utilisateur
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
        
        print("✅ Utilisateur test créé avec succès!")
        print(f"   ID: {test_user.id}")
        print(f"   Email: test@webox.com")
        print(f"   Username: testuser")
        print(f"   Password: test123456")
        print(f"   Premium: Oui")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n" + "="*60)


if __name__ == "__main__":
    create_test_user()
