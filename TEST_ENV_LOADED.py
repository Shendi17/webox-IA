"""
Test pour vérifier que les variables d'environnement sont chargées
"""

import os
from dotenv import load_dotenv

# Charger explicitement
load_dotenv()

print("="*60)
print("🔍 VÉRIFICATION VARIABLES D'ENVIRONNEMENT")
print("="*60)

# Liste des clés à vérifier
keys_to_check = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "VERTEX_AI_PROJECT_ID",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "MISTRAL_API_KEY",
    "GROQ_API_KEY",
    "REPLICATE_API_KEY",
    "HUGGINGFACE_API_KEY",
    "STABILITY_API_KEY"
]

configured = []
missing = []

for key in keys_to_check:
    value = os.getenv(key)
    if value:
        # Masquer la clé pour la sécurité
        if len(value) > 20:
            display = f"{value[:10]}...{value[-10:]}"
        else:
            display = f"{value[:5]}..."
        print(f"✅ {key:35} = {display}")
        configured.append(key)
    else:
        print(f"❌ {key:35} = Non configuré")
        missing.append(key)

print("\n" + "="*60)
print(f"📊 RÉSUMÉ")
print("="*60)
print(f"✅ Configurées: {len(configured)}/{len(keys_to_check)}")
print(f"❌ Manquantes:  {len(missing)}/{len(keys_to_check)}")

if configured:
    print(f"\n🎯 APIs disponibles pour génération:")
    if "OPENAI_API_KEY" in configured:
        print("   - OpenAI DALL-E (images)")
    if "VERTEX_AI_PROJECT_ID" in configured and "GOOGLE_APPLICATION_CREDENTIALS" in configured:
        print("   - Vertex AI Imagen (images)")
        print("   - Vertex AI Veo (vidéos)")
    if "REPLICATE_API_KEY" in configured:
        print("   - Replicate Flux/SDXL (images)")
    if "HUGGINGFACE_API_KEY" in configured:
        print("   - Hugging Face SDXL (images - GRATUIT)")
    if "STABILITY_API_KEY" in configured:
        print("   - Stability AI SD 3.5 (images)")

print("\n" + "="*60)
