"""
Vérifier et corriger la configuration .env
Date: 24 Janvier 2026
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("VERIFICATION CONFIGURATION COMPLETE")
print("="*70 + "\n")

# Vérifier Google Vertex AI
print("1. GOOGLE VERTEX AI")
print("-" * 70)
vertex_project = os.getenv("VERTEX_AI_PROJECT_ID")
vertex_location = os.getenv("VERTEX_AI_LOCATION")
google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if vertex_project:
    print(f"OK VERTEX_AI_PROJECT_ID: {vertex_project}")
else:
    print("ERREUR VERTEX_AI_PROJECT_ID manquant")

if vertex_location:
    print(f"OK VERTEX_AI_LOCATION: {vertex_location}")
else:
    print("ERREUR VERTEX_AI_LOCATION manquant")

if google_creds:
    print(f"OK GOOGLE_APPLICATION_CREDENTIALS: {google_creds}")
else:
    print("ATTENTION GOOGLE_APPLICATION_CREDENTIALS manquant")

print()

# Vérifier Stripe
print("2. STRIPE")
print("-" * 70)
stripe_public = os.getenv("STRIPE_PUBLIC_KEY") or os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe_secret = os.getenv("STRIPE_SECRET_KEY")

if stripe_public:
    mode = "LIVE" if stripe_public.startswith("pk_live_") else "TEST" if stripe_public.startswith("pk_test_") else "INVALIDE"
    print(f"OK STRIPE_PUBLIC_KEY: {stripe_public[:15]}... (Mode: {mode})")
else:
    print("ERREUR STRIPE_PUBLIC_KEY manquant")

if stripe_secret:
    mode = "LIVE" if stripe_secret.startswith("sk_live_") else "TEST" if stripe_secret.startswith("sk_test_") else "INVALIDE"
    print(f"OK STRIPE_SECRET_KEY: {stripe_secret[:15]}... (Mode: {mode})")
else:
    print("ERREUR STRIPE_SECRET_KEY manquant")

print()

# Vérifier clés de sécurité
print("3. SECURITE")
print("-" * 70)
jwt_secret = os.getenv("JWT_SECRET_KEY")
secret_key = os.getenv("SECRET_KEY")

if jwt_secret:
    print(f"OK JWT_SECRET_KEY: {jwt_secret[:10]}...")
else:
    print("ERREUR JWT_SECRET_KEY manquant")

if secret_key:
    print(f"OK SECRET_KEY: {secret_key[:10]}...")
else:
    print("ERREUR SECRET_KEY manquant")

print()

# Résumé
print("="*70)
print("RESUME")
print("="*70)

issues = []
if not vertex_project:
    issues.append("VERTEX_AI_PROJECT_ID manquant")
if not stripe_public:
    issues.append("STRIPE_PUBLIC_KEY manquant (ou STRIPE_PUBLISHABLE_KEY)")
if not jwt_secret:
    issues.append("JWT_SECRET_KEY manquant")
if not secret_key:
    issues.append("SECRET_KEY manquant")

if issues:
    print("ATTENTION Problemes detectes:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("OK Configuration complete!")

print()

# Recommandations
print("RECOMMANDATIONS:")
print("-" * 70)

if not stripe_public and stripe_secret:
    if stripe_secret.startswith("sk_live_"):
        print("Ajouter dans .env:")
        print("STRIPE_PUBLISHABLE_KEY=pk_live_...")
    else:
        print("Ajouter dans .env:")
        print("STRIPE_PUBLISHABLE_KEY=pk_test_...")

if vertex_project and not google_creds:
    print("Pour Vertex AI, ajouter:")
    print("GOOGLE_APPLICATION_CREDENTIALS=/chemin/vers/credentials.json")

print()
