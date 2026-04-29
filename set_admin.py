"""
Script pour définir un utilisateur comme administrateur
Usage: python set_admin.py <email>
"""

import sys
from app.database import SessionLocal
from app.models.user_db import UserDB

def set_admin(email: str):
    """Définir un utilisateur comme admin"""
    db = SessionLocal()
    
    try:
        user = db.query(UserDB).filter(UserDB.email == email).first()
        
        if not user:
            print(f"❌ Utilisateur avec email '{email}' non trouvé")
            print("\nUtilisateurs disponibles:")
            users = db.query(UserDB).all()
            for u in users:
                print(f"  - {u.email} (ID: {u.id}, Role: {u.role})")
            return
        
        print(f"📧 Utilisateur trouvé: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Rôle actuel: {user.role}")
        
        user.role = "admin"
        db.commit()
        
        print(f"\n✅ Utilisateur {user.email} est maintenant ADMIN")
        print(f"   Nouveau rôle: {user.role}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python set_admin.py <email>")
        print("\nExemple: python set_admin.py votre@email.com")
        
        # Afficher les utilisateurs disponibles
        db = SessionLocal()
        users = db.query(UserDB).all()
        if users:
            print("\nUtilisateurs disponibles:")
            for u in users:
                print(f"  - {u.email} (ID: {u.id}, Role: {u.role})")
        db.close()
    else:
        email = sys.argv[1]
        set_admin(email)
