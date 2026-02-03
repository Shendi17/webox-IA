"""
Script pour supprimer l'utilisateur test
Date: 25 Janvier 2026
"""

import sys
sys.path.append(".")

from app.database import SessionLocal
from app.models.user_db import UserDB

def supprimer_utilisateur_test():
    """Supprimer l'utilisateur test@webox.com"""
    
    print("\n" + "="*70)
    print("SUPPRESSION UTILISATEUR TEST")
    print("="*70 + "\n")
    
    db = SessionLocal()
    
    try:
        # Chercher l'utilisateur test
        user = db.query(UserDB).filter(UserDB.email == "test@webox.com").first()
        
        if user:
            print(f"Utilisateur trouvé:")
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Nom: {user.name}")
            print(f"  Username: {user.username}")
            print()
            
            # Supprimer
            db.delete(user)
            db.commit()
            
            print("✅ Utilisateur test supprimé avec succès!")
            print()
            
        else:
            print("ℹ️ Aucun utilisateur test@webox.com trouvé")
            print()
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        
    finally:
        db.close()
    
    print("="*70)
    print()


if __name__ == "__main__":
    supprimer_utilisateur_test()
