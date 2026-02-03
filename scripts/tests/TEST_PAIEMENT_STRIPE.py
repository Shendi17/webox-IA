"""
Script de test pour les paiements Stripe
Date: 24 Janvier 2026
"""

import httpx
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_stripe_payment():
    """Tester le flux complet de paiement Stripe"""
    
    print("\n" + "="*60)
    print("💳 TEST PAIEMENT STRIPE")
    print("="*60 + "\n")
    
    # Vérifier que Stripe est configuré
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_key:
        print("❌ STRIPE_SECRET_KEY non configuré dans .env")
        print("\nPour configurer Stripe:")
        print("1. Créer un compte sur https://stripe.com")
        print("2. Récupérer les clés de test")
        print("3. Ajouter dans .env:")
        print("   STRIPE_SECRET_KEY=sk_test_...")
        print("   STRIPE_PUBLISHABLE_KEY=pk_test_...")
        return
    
    print(f"✅ Clé Stripe configurée: {stripe_key[:12]}...\n")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        
        # 1. Connexion
        print("1️⃣ Connexion utilisateur...")
        login_response = await client.post("/api/auth/login", json={
            "email": "test@webox.com",
            "password": "test123456"
        })
        
        if login_response.status_code != 200:
            print("❌ Échec de la connexion")
            print(f"   Status: {login_response.status_code}")
            print("\nCréez d'abord un utilisateur test:")
            print("POST /api/auth/register")
            print('{"email": "test@webox.com", "username": "testuser", "password": "test123456"}')
            return
        
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Connexion réussie\n")
        
        # 2. Créer une intention de paiement
        print("2️⃣ Création d'une intention de paiement Stripe...")
        amount = 49.99
        
        intent_response = await client.post("/api/payment/stripe/create-intent",
            headers=headers,
            json={
                "amount": amount,
                "currency": "eur",
                "metadata": {
                    "product": "Test Product",
                    "order_id": "TEST-001"
                }
            }
        )
        
        if intent_response.status_code == 200:
            intent_data = intent_response.json()
            print(f"✅ Intention de paiement créée")
            print(f"   Client Secret: {intent_data.get('client_secret', 'N/A')[:20]}...")
            print(f"   Montant: {amount}€")
            print(f"   Statut: {intent_data.get('status', 'N/A')}\n")
            
            payment_intent_id = intent_data.get('id')
            
        elif intent_response.status_code == 400:
            error_data = intent_response.json()
            print(f"❌ Erreur Stripe: {error_data.get('detail', 'Erreur inconnue')}")
            print("\nVérifiez:")
            print("- Que la clé Stripe est valide")
            print("- Que le compte Stripe est actif")
            print("- Que vous êtes en mode test\n")
            return
        else:
            print(f"❌ Erreur: {intent_response.status_code}")
            print(f"   {intent_response.text}\n")
            return
        
        # 3. Simuler une confirmation de paiement (en test)
        print("3️⃣ Simulation de confirmation de paiement...")
        print("   (En production, ceci serait fait par Stripe.js côté client)\n")
        
        # Note: En mode test, on peut utiliser des cartes de test Stripe
        print("📝 Cartes de test Stripe:")
        print("   - Succès: 4242 4242 4242 4242")
        print("   - Échec: 4000 0000 0000 0002")
        print("   - 3D Secure: 4000 0027 6000 3184")
        print("   - Date: N'importe quelle date future")
        print("   - CVC: N'importe quel 3 chiffres\n")
        
        # 4. Vérifier le webhook (simulation)
        print("4️⃣ Webhook Stripe...")
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if webhook_secret:
            print(f"✅ Webhook configuré: {webhook_secret[:12]}...")
            print("   URL: /api/payment/stripe/webhook")
            print("   Événements écoutés:")
            print("   - payment_intent.succeeded")
            print("   - payment_intent.payment_failed\n")
        else:
            print("⚠️ STRIPE_WEBHOOK_SECRET non configuré")
            print("   Les webhooks ne fonctionneront pas\n")
        
        # 5. Récapitulatif
        print("="*60)
        print("📊 RÉCAPITULATIF DU TEST")
        print("="*60)
        print(f"✅ Connexion utilisateur: OK")
        print(f"✅ Création intention paiement: OK")
        print(f"✅ Montant: {amount}€")
        print(f"⚠️ Confirmation paiement: À faire manuellement")
        print(f"{'✅' if webhook_secret else '⚠️'} Webhook: {'Configuré' if webhook_secret else 'Non configuré'}")
        print("\n" + "="*60)
        print("🎯 PROCHAINES ÉTAPES")
        print("="*60)
        print("1. Intégrer Stripe.js dans le frontend")
        print("2. Utiliser le client_secret pour confirmer le paiement")
        print("3. Configurer le webhook Stripe")
        print("4. Tester avec les cartes de test")
        print("5. Vérifier les paiements dans le dashboard Stripe")
        print("\n📚 Documentation: https://stripe.com/docs/payments/accept-a-payment")
        print("🔗 Dashboard: https://dashboard.stripe.com/test/payments\n")


async def test_stripe_config():
    """Vérifier la configuration Stripe"""
    
    print("\n" + "="*60)
    print("🔍 VÉRIFICATION CONFIGURATION STRIPE")
    print("="*60 + "\n")
    
    stripe_secret = os.getenv("STRIPE_SECRET_KEY")
    stripe_public = os.getenv("STRIPE_PUBLISHABLE_KEY")
    stripe_webhook = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    print("Configuration Stripe:")
    print("-" * 60)
    
    if stripe_secret:
        is_test = stripe_secret.startswith("sk_test_")
        is_live = stripe_secret.startswith("sk_live_")
        mode = "TEST" if is_test else "LIVE" if is_live else "INVALIDE"
        print(f"✅ Secret Key: {stripe_secret[:12]}... (Mode: {mode})")
    else:
        print("❌ Secret Key: NON CONFIGURÉ")
    
    if stripe_public:
        is_test = stripe_public.startswith("pk_test_")
        is_live = stripe_public.startswith("pk_live_")
        mode = "TEST" if is_test else "LIVE" if is_live else "INVALIDE"
        print(f"✅ Publishable Key: {stripe_public[:12]}... (Mode: {mode})")
    else:
        print("❌ Publishable Key: NON CONFIGURÉ")
    
    if stripe_webhook:
        print(f"✅ Webhook Secret: {stripe_webhook[:12]}...")
    else:
        print("⚠️ Webhook Secret: NON CONFIGURÉ (optionnel)")
    
    print("\n" + "="*60)
    
    if not stripe_secret or not stripe_public:
        print("\n❌ Configuration incomplète")
        print("\n📖 Guide de configuration:")
        print("1. Aller sur https://stripe.com")
        print("2. Créer un compte (gratuit)")
        print("3. Aller dans Développeurs > Clés API")
        print("4. Copier les clés de TEST")
        print("5. Ajouter dans .env:")
        print("   STRIPE_SECRET_KEY=sk_test_...")
        print("   STRIPE_PUBLISHABLE_KEY=pk_test_...")
        print("\n6. Pour le webhook (optionnel):")
        print("   - Aller dans Développeurs > Webhooks")
        print("   - Ajouter un endpoint")
        print("   - URL: https://votre-domaine.com/api/payment/stripe/webhook")
        print("   - Copier la clé de signature")
        print("   - Ajouter dans .env:")
        print("   STRIPE_WEBHOOK_SECRET=whsec_...")
    else:
        print("\n✅ Configuration Stripe OK")
        print("Vous pouvez maintenant tester les paiements")


if __name__ == "__main__":
    print("\n⚠️ Assurez-vous que:")
    print("  1. Le serveur est lancé (python main.py)")
    print("  2. Les clés Stripe sont configurées dans .env")
    print("  3. Un utilisateur test existe (test@webox.com)\n")
    
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Mode vérification uniquement
        asyncio.run(test_stripe_config())
    else:
        # Mode test complet
        try:
            asyncio.run(test_stripe_config())
            print("\n" + "="*60 + "\n")
            asyncio.run(test_stripe_payment())
        except KeyboardInterrupt:
            print("\n\n⚠️ Test interrompu par l'utilisateur")
        except Exception as e:
            print(f"\n\n❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
