"""
Créer l'utilisateur admin dans la base de données
Date : 1er Novembre 2025
"""

from app.database import SessionLocal
from app.models.user_db import UserDB
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Créer l'utilisateur admin"""
    db = SessionLocal()
    
    try:
        # Vérifier si l'utilisateur admin existe déjà
        existing_user = db.query(UserDB).filter(UserDB.email == "admin@webox.com").first()
        
        if existing_user:
            print("⚠️  L'utilisateur admin existe déjà")
            print(f"   Email: {existing_user.email}")
            print(f"   Username: {existing_user.username}")
            print(f"   ID: {existing_user.id}")
            return
        
        # Créer le nouvel utilisateur admin
        password = "admin123"
        hashed_password = generate_password_hash(password)
        
        new_user = UserDB(
            email="admin@webox.com",
            username="admin",
            hashed_password=hashed_password,
            name="Administrateur",
            is_active=True,
            is_admin=True,
            is_premium=True,
            role="admin"
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("✅ Utilisateur admin créé avec succès !")
        print("")
        print("📝 Informations de connexion :")
        print(f"   Email    : admin@webox.com")
        print(f"   Password : admin123")
        print(f"   Username : admin")
        print(f"   ID       : {new_user.id}")
        print(f"   Role     : {new_user.role}")
        print("")
        print("🎯 Tu peux maintenant te connecter avec ces identifiants !")
        print("")
        print("🌐 URL : http://webox.local:8000/login")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur : {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Création de l'utilisateur admin...")
    print("")
    create_admin_user()
