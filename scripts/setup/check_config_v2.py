"""
Vérification configuration complète avec Vertex AI et Stripe
Date: 24 Janvier 2026
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*80)
print("VERIFICATION CONFIGURATION WEBOX")
print("="*80 + "\n")

configured = 0
total = 0

# Paiements
print("PAIEMENTS")
print("-" * 80)

stripe_secret = os.getenv("STRIPE_SECRET_KEY")
stripe_public = os.getenv("STRIPE_PUBLIC_KEY") or os.getenv("STRIPE_PUBLISHABLE_KEY")
paypal_id = os.getenv("PAYPAL_CLIENT_ID")
paypal_secret = os.getenv("PAYPAL_CLIENT_SECRET")

if stripe_secret:
    mode = "LIVE" if stripe_secret.startswith("sk_live_") else "TEST"
    print(f"OK STRIPE_SECRET_KEY: {stripe_secret[:15]}... (Mode: {mode})")
    configured += 1
else:
    print("ERREUR STRIPE_SECRET_KEY manquant")
total += 1

if stripe_public:
    mode = "LIVE" if stripe_public.startswith("pk_live_") else "TEST"
    print(f"OK STRIPE_PUBLIC_KEY: {stripe_public[:15]}... (Mode: {mode})")
    configured += 1
else:
    print("ERREUR STRIPE_PUBLIC_KEY manquant")
total += 1

if paypal_id:
    print(f"OK PAYPAL_CLIENT_ID: {paypal_id[:10]}...")
    configured += 1
else:
    print("ERREUR PAYPAL_CLIENT_ID manquant")
total += 1

if paypal_secret:
    print(f"OK PAYPAL_CLIENT_SECRET: ****")
    configured += 1
else:
    print("ERREUR PAYPAL_CLIENT_SECRET manquant")
total += 1

print()

# IA - Chat
print("IA - CHAT")
print("-" * 80)

openai = os.getenv("OPENAI_API_KEY")
anthropic = os.getenv("ANTHROPIC_API_KEY")
vertex_project = os.getenv("VERTEX_AI_PROJECT_ID")
vertex_location = os.getenv("VERTEX_AI_LOCATION")
mistral = os.getenv("MISTRAL_API_KEY")
groq = os.getenv("GROQ_API_KEY")
cohere = os.getenv("COHERE_API_KEY")

if openai:
    print(f"OK OPENAI_API_KEY: {openai[:15]}...")
    configured += 1
else:
    print("ERREUR OPENAI_API_KEY manquant")
total += 1

if anthropic:
    print(f"OK ANTHROPIC_API_KEY: {anthropic[:15]}...")
    configured += 1
else:
    print("ERREUR ANTHROPIC_API_KEY manquant")
total += 1

if vertex_project and vertex_location:
    print(f"OK GOOGLE_VERTEX_AI: {vertex_project} ({vertex_location})")
    configured += 1
else:
    print("ERREUR GOOGLE_VERTEX_AI manquant")
total += 1

if mistral:
    print(f"OK MISTRAL_API_KEY: {mistral[:15]}...")
    configured += 1
else:
    print("ERREUR MISTRAL_API_KEY manquant")
total += 1

if groq:
    print(f"OK GROQ_API_KEY: {groq[:15]}...")
    configured += 1
else:
    print("ERREUR GROQ_API_KEY manquant")
total += 1

if cohere:
    print(f"OK COHERE_API_KEY: {cohere[:15]}...")
    configured += 1
else:
    print("ERREUR COHERE_API_KEY manquant")
total += 1

print()

# Sécurité
print("SECURITE")
print("-" * 80)

jwt = os.getenv("JWT_SECRET_KEY")
secret = os.getenv("SECRET_KEY")

if jwt:
    print(f"OK JWT_SECRET_KEY: {jwt[:10]}...")
    configured += 1
else:
    print("ERREUR JWT_SECRET_KEY manquant")
total += 1

if secret:
    print(f"OK SECRET_KEY: {secret[:10]}...")
    configured += 1
else:
    print("ERREUR SECRET_KEY manquant")
total += 1

print()

# Résumé
print("="*80)
print(f"RESUME: {configured}/{total} cles configurees ({int(configured/total*100)}%)")
print("="*80)

if configured == total:
    print("\nOK Configuration complete!")
elif configured >= total * 0.7:
    print("\nOK Configuration suffisante pour demarrer!")
else:
    print("\nATTENTION Configuration incomplete")

print()
