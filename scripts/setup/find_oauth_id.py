#!/usr/bin/env python3
"""
Script pour trouver d'où provient l'ID OAuth client problématique
26997462856-5ftvpki9ghpg59s8rae6aqmr1pjqkeqt.apps.googleusercontent.com
"""

import os
import json

oauth_id = "26997462856-5ftvpki9ghpg59s8rae6aqmr1pjqkeqt.apps.googleusercontent.com"
project_number = "26997462856"

print("=" * 60)
print("RECHERCHE DE L'ID OAUTH CLIENT")
print("=" * 60)
print()
print(f"ID recherché: {oauth_id}")
print(f"Project Number: {project_number}")
print()

# 1. Vérifier le fichier service account
print("[1/4] Vérification du fichier service account...")
service_account_file = r"C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json"
if os.path.exists(service_account_file):
    with open(service_account_file, 'r') as f:
        sa_content = json.load(f)
    print(f"  Fichier: {service_account_file}")
    print(f"  Type: {sa_content.get('type')}")
    print(f"  Project ID: {sa_content.get('project_id')}")
    print(f"  Client ID: {sa_content.get('client_id')}")
    print(f"  Client Email: {sa_content.get('client_email')}")
    
    if oauth_id in json.dumps(sa_content):
        print(f"  ❌ TROUVÉ dans le service account!")
    else:
        print(f"  ✅ Non trouvé dans le service account")
else:
    print(f"  ❌ Fichier non trouvé")

print()

# 2. Vérifier le fichier gcloud application-default credentials
print("[2/4] Vérification gcloud application-default credentials...")
gcloud_cred_file = os.path.join(os.getenv('APPDATA'), 'gcloud', 'application_default_credentials.json')
if os.path.exists(gcloud_cred_file):
    with open(gcloud_cred_file, 'r') as f:
        gcloud_content = json.load(f)
    print(f"  Fichier: {gcloud_cred_file}")
    print(f"  Type: {gcloud_content.get('type')}")
    print(f"  Client ID: {gcloud_content.get('client_id')}")
    print(f"  Client Secret: {'***' if gcloud_content.get('client_secret') else 'Non défini'}")
    print(f"  Quota Project ID: {gcloud_content.get('quota_project_id')}")
    
    if oauth_id in json.dumps(gcloud_content):
        print(f"  ❌ TROUVÉ dans gcloud credentials!")
        print(f"  >>> C'EST LA SOURCE DU PROBLÈME <<<")
    elif project_number in json.dumps(gcloud_content):
        print(f"  ⚠️  Project number {project_number} trouvé")
    else:
        print(f"  ✅ Non trouvé dans gcloud credentials")
else:
    print(f"  ❌ Fichier non trouvé")

print()

# 3. Vérifier les variables d'environnement
print("[3/4] Vérification des variables d'environnement...")
from dotenv import load_dotenv
load_dotenv()

google_app_cred = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
vertex_project_id = os.getenv('VERTEX_AI_PROJECT_ID')
vertex_location = os.getenv('VERTEX_AI_LOCATION')

print(f"  GOOGLE_APPLICATION_CREDENTIALS: {google_app_cred}")
print(f"  VERTEX_AI_PROJECT_ID: {vertex_project_id}")
print(f"  VERTEX_AI_LOCATION: {vertex_location}")

if google_app_cred and os.path.exists(google_app_cred):
    with open(google_app_cred, 'r') as f:
        env_cred_content = json.load(f)
    print(f"  Fichier credentials pointe vers: {env_cred_content.get('project_id')}")
    
    if oauth_id in json.dumps(env_cred_content):
        print(f"  ❌ TROUVÉ dans le fichier credentials de .env!")
    else:
        print(f"  ✅ Non trouvé dans le fichier credentials de .env")

print()

# 4. Test de connexion Vertex AI
print("[4/4] Test de connexion Vertex AI...")
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    
    print(f"  Initialisation avec:")
    print(f"    Project: {vertex_project_id}")
    print(f"    Location: {vertex_location}")
    
    vertexai.init(project=vertex_project_id, location=vertex_location)
    print(f"  ✅ Initialisation réussie")
    
    model = GenerativeModel('gemini-1.0-pro')
    print(f"  ✅ Modèle créé")
    
    print(f"  Test de génération...")
    response = model.generate_content('Dis bonjour')
    print(f"  ✅ SUCCÈS! Réponse: {response.text}")
    
except Exception as e:
    error_msg = str(e)
    print(f"  ❌ ERREUR: {error_msg}")
    
    if oauth_id in error_msg:
        print(f"  >>> L'ID OAUTH APPARAÎT DANS L'ERREUR <<<")
        print(f"  >>> Le problème vient des credentials utilisés par Vertex AI <<<")
    
    if project_number in error_msg:
        print(f"  >>> Le project number {project_number} apparaît dans l'erreur <<<")

print()
print("=" * 60)
print("CONCLUSION")
print("=" * 60)
print()
print("L'ID OAuth client provient probablement de:")
print("  1. gcloud application-default credentials")
print("  2. Créé lors de 'gcloud auth application-default login'")
print()
print("SOLUTION:")
print("  1. Supprimer les credentials gcloud:")
print(f"     del {gcloud_cred_file}")
print("  2. Utiliser UNIQUEMENT le service account:")
print("     GOOGLE_APPLICATION_CREDENTIALS dans .env")
print("  3. OU re-authentifier avec gcloud pour le bon projet")
print()
