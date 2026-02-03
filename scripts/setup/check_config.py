"""
Script de vérification de la configuration complète
Date: 24 Janvier 2026
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*80)
print("🔍 VÉRIFICATION CONFIGURATION WEBOX")
print("="*80 + "\n")

# Catégories de clés API
categories = {
    " PAIEMENTS": {
        "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY"),
        "STRIPE_PUBLISHABLE_KEY": os.getenv("STRIPE_PUBLISHABLE_KEY"),
        "STRIPE_WEBHOOK_SECRET": os.getenv("STRIPE_WEBHOOK_SECRET"),
        "PAYPAL_CLIENT_ID": os.getenv("PAYPAL_CLIENT_ID"),
        "PAYPAL_CLIENT_SECRET": os.getenv("PAYPAL_CLIENT_SECRET"),
    },
    " IA - CHAT": {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "VERTEX_AI_PROJECT_ID": os.getenv("VERTEX_AI_PROJECT_ID"),
        "VERTEX_AI_LOCATION": os.getenv("VERTEX_AI_LOCATION"),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "COHERE_API_KEY": os.getenv("COHERE_API_KEY"),
    },
    " IA - IMAGES": {
        "STABILITY_API_KEY": os.getenv("STABILITY_API_KEY"),
        "REPLICATE_API_KEY": os.getenv("REPLICATE_API_KEY"),
    },
    "🎵 IA - AUDIO": {
        "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY"),
        "SUNO_API_KEY": os.getenv("SUNO_API_KEY"),
    },
    "🎬 IA - VIDÉO": {
        "RUNWAY_API_KEY": os.getenv("RUNWAY_API_KEY"),
        "PIKA_API_KEY": os.getenv("PIKA_API_KEY"),
    },
    "🔐 SÉCURITÉ": {
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY"),
    },
    "🗄️ BASE DE DONNÉES": {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
    }
}

total_configured = 0
total_keys = 0

for category, keys in categories.items():
    print(f"\n{category}")
    print("-" * 80)
    
    for key_name, key_value in keys.items():
        total_keys += 1
        if key_value:
            total_configured += 1
            # Masquer la clé
            if len(key_value) > 12:
                masked = f"{key_value[:8]}...{key_value[-4:]}"
            else:
                masked = "****"
            print(f"✅ {key_name}: {masked}")
        else:
            print(f"❌ {key_name}: NON CONFIGURÉ")

print("\n" + "="*80)
print(f"📊 RÉSUMÉ: {total_configured}/{total_keys} clés configurées ({int(total_configured/total_keys*100)}%)")
print("="*80)

# Recommandations
print("\n🎯 RECOMMANDATIONS:")
print("-" * 80)

if not os.getenv("OPENAI_API_KEY"):
    print("⚠️ OpenAI non configuré - Fonctionnalités principales limitées")
    
if not os.getenv("STRIPE_SECRET_KEY"):
    print("⚠️ Stripe non configuré - Paiements désactivés")
    
if not os.getenv("DATABASE_URL"):
    print("⚠️ DATABASE_URL non configuré - Utilisation de SQLite par défaut")

if total_configured >= 5:
    print("✅ Configuration suffisante pour démarrer!")
else:
    print("⚠️ Configuration minimale requise: OpenAI + Stripe")

print()
