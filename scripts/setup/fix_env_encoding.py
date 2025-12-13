"""
Fixer l'encodage du fichier .env
Date : 31 Octobre 2025
"""

import urllib.parse

# Mot de passe PostgreSQL
password = "VotreMotDePasseSecurise123!"
encoded_password = urllib.parse.quote_plus(password)

# Contenu du .env avec encodage UTF-8
env_content = f"""# Configuration WeBox Multi-IA
# Date : 31 Octobre 2025

# Database PostgreSQL
DATABASE_URL=postgresql://webox_user:{encoded_password}@localhost:5432/webox_db

# JWT Secret Key
SECRET_KEY=your-secret-key-change-this-in-production-webox-2025

# API Keys (à configurer)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GOOGLE_API_KEY=your-google-api-key-here

# Application
DEBUG=True
ENVIRONMENT=development
"""

# Écrire le fichier avec encodage UTF-8
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ Fichier .env recréé avec le bon encodage UTF-8")
print("")
print("📝 Contenu du fichier .env :")
print("=" * 60)
print(env_content)
print("=" * 60)
print("")
print("🔐 Mot de passe encodé :")
print(f"   Original : {password}")
print(f"   Encodé   : {encoded_password}")
