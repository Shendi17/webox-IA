"""
Créer un utilisateur de test dans PostgreSQL
Date : 30 Octobre 2025
"""

from app.database import SessionLocal
from app.models.user_db import UserDB
from passlib.context import CryptContext

# Configuration du hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    """Créer un utilisateur de test"""
    db = SessionLocal()
    
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(UserDB).filter(UserDB.email == "test@webox.local").first()
        
        if existing_user:
            print("⚠️  L'utilisateur test existe déjà")
            print(f"   Email: {existing_user.email}")
            print(f"   Username: {existing_user.username}")
            print(f"   ID: {existing_user.id}")
            return
        
        # Créer le nouvel utilisateur
        hashed_password = pwd_context.hash("test123")
        
        new_user = UserDB(
            email="test@webox.local",
            username="testuser",
            hashed_password=hashed_password,
            name="Utilisateur Test",
            is_active=True,
            is_admin=True,
            is_premium=True,
            role="admin"
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ Utilisateur de test créé avec succès !")
        print("")
        print("📝 Informations de connexion :")
        print(f"   Email    : test@webox.local")
        print(f"   Password : test123")
        print(f"   Username : testuser")
        print(f"   ID       : {new_user.id}")
        print(f"   Role     : {new_user.role}")
        print("")
        print("🎯 Tu peux maintenant te connecter avec ces identifiants !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Création d'un utilisateur de test...")
    print("")
    create_test_user()
