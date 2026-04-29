"""
Script de diagnostic pour vérifier le rôle utilisateur
"""

from app.database import SessionLocal
from app.models.user_db import UserDB

db = SessionLocal()

print("=" * 60)
print("🔍 DIAGNOSTIC - Utilisateurs et Rôles")
print("=" * 60)

users = db.query(UserDB).all()

if not users:
    print("\n❌ Aucun utilisateur trouvé dans la base de données")
else:
    print(f"\n📊 {len(users)} utilisateur(s) trouvé(s):\n")
    
    for user in users:
        print(f"👤 {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Nom: {user.name}")
        print(f"   Rôle: {user.role or 'None'}")
        print(f"   Est admin: {'✅ OUI' if user.role == 'admin' else '❌ NON'}")
        print()

db.close()

print("=" * 60)
print("💡 INSTRUCTIONS:")
print("=" * 60)
print()
print("Si votre rôle n'est PAS 'admin':")
print("  python set_admin.py votre@email.com")
print()
print("Ensuite:")
print("  1. Déconnectez-vous: http://webox.local:8000/logout")
print("  2. Reconnectez-vous: http://webox.local:8000/login")
print("  3. Ouvrez la console (F12)")
print("  4. Allez sur: http://webox.local:8000/generation")
print("  5. Vérifiez les logs dans la console")
print()
print("=" * 60)
