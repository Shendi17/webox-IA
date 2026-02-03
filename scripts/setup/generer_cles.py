"""
Générer les clés secrètes manquantes
Date: 24 Janvier 2026
"""

import secrets

print("\n" + "="*60)
print("GENERATION CLES SECRETES")
print("="*60 + "\n")

jwt_secret = secrets.token_urlsafe(32)
secret_key = secrets.token_urlsafe(32)

print("Cles generees avec succes!")
print("\nAjoutez ces lignes dans votre fichier .env:\n")
print(f"JWT_SECRET_KEY={jwt_secret}")
print(f"SECRET_KEY={secret_key}")
print("\n" + "="*60 + "\n")

# Écrire dans un fichier temporaire
with open("cles_generees.txt", "w") as f:
    f.write(f"JWT_SECRET_KEY={jwt_secret}\n")
    f.write(f"SECRET_KEY={secret_key}\n")

print("Les cles ont aussi ete sauvegardees dans: cles_generees.txt")
print("Vous pouvez copier-coller ces lignes dans .env\n")
