import hashlib
import json
from datetime import datetime

# Hash correct pour admin123
password_hash = hashlib.sha256("admin123".encode()).hexdigest()
print(f"Hash pour 'admin123': {password_hash}")

# Créer le fichier users.json avec le bon hash
users = {
    "admin@webox.com": {
        "name": "Administrateur",
        "password": password_hash,
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "role": "admin"
    }
}

with open("data/users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, ensure_ascii=False, indent=2)

print("\n✅ Fichier users.json mis à jour !")
print("\nCompte admin:")
print("Email: admin@webox.com")
print("Mot de passe: admin123")
