"""
Ajouter automatiquement les clés générées dans .env
Date: 24 Janvier 2026
"""

import os

print("\n" + "="*60)
print("AJOUT AUTOMATIQUE DES CLES DANS .ENV")
print("="*60 + "\n")

# Lire les clés générées
with open("cles_generees.txt", "r") as f:
    cles = f.read()

# Lire le fichier .env actuel
with open(".env", "r") as f:
    env_content = f.read()

# Vérifier si les clés existent déjà
if "JWT_SECRET_KEY=" in env_content and "SECRET_KEY=" in env_content:
    print("Les cles JWT_SECRET_KEY et SECRET_KEY existent deja dans .env")
    print("Aucune modification necessaire.\n")
else:
    # Ajouter les clés à la fin du fichier
    with open(".env", "a") as f:
        f.write("\n# Cles de securite (generees automatiquement)\n")
        f.write(cles)
    
    print("OK Cles ajoutees avec succes dans .env!")
    print("- JWT_SECRET_KEY")
    print("- SECRET_KEY\n")

print("="*60 + "\n")
