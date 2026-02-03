"""Vérifier la clé API OpenAI chargée par l'application"""
from modules.core.config import config

print("="*60)
print("VÉRIFICATION DE LA CLÉ API OPENAI")
print("="*60)

if config.OPENAI_API_KEY:
    print(f"✅ Clé API trouvée: {config.OPENAI_API_KEY[:20]}...")
    print(f"   Longueur: {len(config.OPENAI_API_KEY)} caractères")
else:
    print("❌ Clé API OpenAI VIDE ou non configurée")

print("\n" + "="*60)
