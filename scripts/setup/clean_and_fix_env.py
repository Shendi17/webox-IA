#!/usr/bin/env python3
"""
Script pour nettoyer et corriger le fichier .env
Supprime les lignes dupliquées et configure correctement GOOGLE_APPLICATION_CREDENTIALS
"""

import os

env_path = '.env'

if not os.path.exists(env_path):
    print("❌ Fichier .env non trouvé")
    exit(1)

print("📝 Lecture du fichier .env...")
with open(env_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
seen_vars = set()
credentials_added = False

print("🔧 Nettoyage et correction...")

for line in lines:
    stripped = line.strip()
    
    # Ignorer les lignes vides
    if not stripped:
        new_lines.append(line)
        continue
    
    # Ignorer les commentaires qui contiennent "Commente automatiquement"
    if stripped.startswith('#') and 'Commente automatiquement' in stripped:
        print(f"  ❌ Suppression: {stripped[:50]}...")
        continue
    
    # Traiter GOOGLE_APPLICATION_CREDENTIALS
    if 'GOOGLE_APPLICATION_CREDENTIALS' in stripped:
        if stripped.startswith('#'):
            # Ignorer les lignes commentées
            print(f"  ⏭️  Ignoré (commentaire): {stripped[:50]}...")
            continue
        elif not credentials_added:
            # Ajouter la bonne ligne
            correct_line = "GOOGLE_APPLICATION_CREDENTIALS=C:\\Users\\Anthony\\CascadeProjects\\webox\\webox-482718-f86837e5ce03.json\n"
            new_lines.append(correct_line)
            credentials_added = True
            print(f"  ✅ Ajouté: GOOGLE_APPLICATION_CREDENTIALS")
        else:
            # Déjà ajouté, ignorer les doublons
            print(f"  ⏭️  Doublon ignoré: {stripped[:50]}...")
        continue
    
    # Extraire le nom de la variable
    if '=' in stripped and not stripped.startswith('#'):
        var_name = stripped.split('=')[0].strip()
        if var_name in seen_vars:
            print(f"  ⏭️  Doublon ignoré: {var_name}")
            continue
        seen_vars.add(var_name)
    
    # Garder la ligne
    new_lines.append(line)

# Si GOOGLE_APPLICATION_CREDENTIALS n'a pas été ajouté, l'ajouter maintenant
if not credentials_added:
    print("  ➕ Ajout de GOOGLE_APPLICATION_CREDENTIALS")
    new_lines.append("GOOGLE_APPLICATION_CREDENTIALS=C:\\Users\\Anthony\\CascadeProjects\\webox\\webox-482718-f86837e5ce03.json\n")

print("\n💾 Sauvegarde du fichier .env...")
with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Fichier .env nettoyé et corrigé!\n")

# Vérification
print("🔍 Vérification de la configuration:")
from dotenv import load_dotenv
load_dotenv()

project_id = os.getenv('VERTEX_AI_PROJECT_ID')
location = os.getenv('VERTEX_AI_LOCATION')
credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

print(f"  PROJECT_ID: {project_id}")
print(f"  LOCATION: {location}")
print(f"  CREDENTIALS: {credentials}")

if credentials and os.path.exists(credentials):
    print(f"  ✅ Fichier credentials existe")
else:
    print(f"  ❌ Fichier credentials introuvable: {credentials}")

print("\n✨ Configuration prête pour Vertex AI!")
