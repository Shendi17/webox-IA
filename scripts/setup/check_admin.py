"""
Script pour vérifier et mettre à jour le statut admin
"""
from app.database import SessionLocal
from app.models.user_db import UserDB

db = SessionLocal()

# Récupérer l'utilisateur
user = db.query(UserDB).filter(UserDB.email == "admin@webox.com").first()

if user:
    print(f"✅ Utilisateur trouvé: {user.email}")
    print(f"   Nom: {user.name}")
    print(f"   Username: {user.username}")
    print(f"   Is Admin: {user.is_admin}")
    print(f"   Role: {user.role}")
    
    if not user.is_admin:
        print("\n⚠️ L'utilisateur n'est PAS admin. Mise à jour...")
        user.is_admin = True
        user.role = "admin"
        db.commit()
        print("✅ Utilisateur mis à jour en admin !")
    else:
        print("\n✅ L'utilisateur est déjà admin")
else:
    print("❌ Utilisateur non trouvé")

db.close()
