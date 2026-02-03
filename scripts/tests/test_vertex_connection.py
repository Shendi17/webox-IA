"""
Script de test de connexion Vertex AI
Pour diagnostiquer l'erreur "File was not found"
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

print("=" * 50)
print("Test de connexion Vertex AI")
print("=" * 50)
print()

# Vérifier les variables d'environnement
project_id = os.getenv('VERTEX_AI_PROJECT_ID')
location = os.getenv('VERTEX_AI_LOCATION', 'us-central1')

print(f"1. Variables d'environnement:")
print(f"   VERTEX_AI_PROJECT_ID: {project_id}")
print(f"   VERTEX_AI_LOCATION: {location}")
print()

# Vérifier les credentials
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if cred_path:
    print(f"2. GOOGLE_APPLICATION_CREDENTIALS: {cred_path}")
    if os.path.exists(cred_path):
        print(f"   ✅ Fichier trouvé")
    else:
        print(f"   ❌ Fichier non trouvé")
else:
    print(f"2. GOOGLE_APPLICATION_CREDENTIALS: Non configuré")
    print(f"   ℹ️  Utilisation de gcloud auth application-default")

# Vérifier les credentials application-default
appdata = os.getenv('APPDATA')
default_cred_path = os.path.join(appdata, 'gcloud', 'application_default_credentials.json')
print(f"3. Credentials application-default:")
print(f"   Chemin: {default_cred_path}")
if os.path.exists(default_cred_path):
    print(f"   ✅ Fichier trouvé")
else:
    print(f"   ❌ Fichier non trouvé")
print()

# Test d'import
print("4. Test d'import des modules:")
try:
    import vertexai
    print("   ✅ vertexai importé")
except ImportError as e:
    print(f"   ❌ Erreur d'import vertexai: {e}")
    exit(1)

try:
    from vertexai.generative_models import GenerativeModel
    print("   ✅ GenerativeModel importé")
except ImportError as e:
    print(f"   ❌ Erreur d'import GenerativeModel: {e}")
    exit(1)

print()

# Test d'initialisation
print("5. Test d'initialisation Vertex AI:")
try:
    vertexai.init(project=project_id, location=location)
    print(f"   ✅ Vertex AI initialisé")
    print(f"   Projet: {project_id}")
    print(f"   Région: {location}")
except Exception as e:
    print(f"   ❌ Erreur d'initialisation: {e}")
    print(f"   Type d'erreur: {type(e).__name__}")
    exit(1)

print()

# Test de création du modèle
print("6. Test de création du modèle:")
try:
    model = GenerativeModel("gemini-1.5-flash")
    print(f"   ✅ Modèle gemini-1.5-flash créé")
except Exception as e:
    print(f"   ❌ Erreur de création du modèle: {e}")
    print(f"   Type d'erreur: {type(e).__name__}")
    exit(1)

print()

# Test de génération
print("7. Test de génération de contenu:")
try:
    response = model.generate_content(
        "Dis simplement 'Bonjour' en français",
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 100
        }
    )
    print(f"   ✅ Génération réussie!")
    print(f"   Réponse: {response.text}")
except Exception as e:
    print(f"   ❌ Erreur de génération: {e}")
    print(f"   Type d'erreur: {type(e).__name__}")
    import traceback
    print(f"\n   Traceback complet:")
    traceback.print_exc()
    exit(1)

print()
print("=" * 50)
print("✅ Tous les tests sont passés avec succès!")
print("=" * 50)
print()
print("Vertex AI fonctionne correctement.")
print("Si le chat WeBox affiche toujours une erreur,")
print("redémarrez le serveur avec: python main.py")
