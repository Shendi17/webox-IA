"""
Script pour corriger DATABASE_URL avec encodage URL
Date : 30 Octobre 2025
"""

import urllib.parse
import os

print("🔧 Correction de DATABASE_URL...")
print("")

# Demander le mot de passe
password = input("Entrez le mot de passe de 'webox_user': ")

# Encoder le mot de passe pour URL
encoded_password = urllib.parse.quote_plus(password)

# Créer la nouvelle DATABASE_URL
database_url = f"postgresql://webox_user:{encoded_password}@localhost:5432/webox_db"

print("")
print("✅ Mot de passe encodé !")
print("")
print("📝 Nouvelle DATABASE_URL :")
print(database_url)
print("")

# Mettre à jour le .env
env_path = ".env"
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remplacer ou ajouter DATABASE_URL
    found = False
    for i, line in enumerate(lines):
        if line.startswith("DATABASE_URL="):
            lines[i] = f"DATABASE_URL={database_url}\n"
            found = True
            break
    
    if not found:
        lines.append(f"\n# PostgreSQL Database\n")
        lines.append(f"DATABASE_URL={database_url}\n")
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Fichier .env mis à jour")
else:
    print("❌ Fichier .env non trouvé")

print("")
print("🎯 Prochaine étape : Créer les tables")
print("   python create_tables.py")
print("")
