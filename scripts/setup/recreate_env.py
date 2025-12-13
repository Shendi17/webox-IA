"""
Script pour recréer .env avec le bon encodage
Date : 30 Octobre 2025
"""

import urllib.parse

print("🔧 Recréation du fichier .env avec encodage UTF-8...")
print("")

# Demander le mot de passe
password = input("Entrez le mot de passe de 'webox_user': ")

# Encoder le mot de passe pour URL
encoded_password = urllib.parse.quote_plus(password)

# Créer la DATABASE_URL
database_url = f"postgresql://webox_user:{encoded_password}@localhost:5432/webox_db"

print("")
print("✅ URL créée !")
print("")

# Lire .env.example pour avoir les autres variables
env_content = []

try:
    with open('.env.example', 'r', encoding='utf-8') as f:
        for line in f:
            # Garder toutes les lignes sauf DATABASE_URL
            if not line.strip().startswith('DATABASE_URL'):
                env_content.append(line.rstrip('\n'))
except FileNotFoundError:
    print("⚠️  .env.example non trouvé, création d'un .env minimal")
    env_content = [
        "# WeBox Multi-IA - Configuration",
        "",
        "# Application",
        "SECRET_KEY=your-secret-key-here-change-in-production",
        "ALGORITHM=HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES=30",
        "",
    ]

# Ajouter DATABASE_URL
env_content.append("")
env_content.append("# PostgreSQL Database")
env_content.append(f"DATABASE_URL={database_url}")

# Écrire le nouveau .env avec encodage UTF-8
with open('.env', 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(env_content))
    f.write('\n')

print("✅ Fichier .env recréé avec succès !")
print("")
print("📝 DATABASE_URL configuré :")
print(f"   {database_url}")
print("")
print("🎯 Prochaine étape : Créer les tables")
print("   python create_tables.py")
print("")
