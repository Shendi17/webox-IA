"""
Test final complet - Version simplifiée
Date: 24 Janvier 2026
"""

import httpx
import asyncio

BASE_URL = "http://localhost:8000"

async def test_final():
    """Test final complet"""
    
    print("\n" + "="*70)
    print("TEST FINAL COMPLET - WEBOX")
    print("="*70 + "\n")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0, follow_redirects=False) as client:
        
        # Test 1: Health check
        print("1. HEALTH CHECK")
        print("-" * 70)
        results["total"] += 1
        try:
            response = await client.get("/health")
            if response.status_code == 200:
                data = response.json()
                print(f"OK Serveur: {data.get('app')} v{data.get('version')}")
                results["passed"] += 1
            else:
                print(f"ERREUR Status: {response.status_code}")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        print()
        
        # Test 2: Page marketplace
        print("2. PAGE MARKETPLACE")
        print("-" * 70)
        results["total"] += 1
        try:
            response = await client.get("/marketplace")
            if response.status_code == 200:
                print("OK Page marketplace accessible")
                results["passed"] += 1
            else:
                print(f"ERREUR Status: {response.status_code}")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        print()
        
        # Test 3: Page login
        print("3. PAGE LOGIN")
        print("-" * 70)
        results["total"] += 1
        try:
            response = await client.get("/login")
            if response.status_code == 200:
                print("OK Page login accessible")
                results["passed"] += 1
            else:
                print(f"ERREUR Status: {response.status_code}")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        print()
        
        # Test 4: Configuration Stripe
        print("4. CONFIGURATION STRIPE")
        print("-" * 70)
        results["total"] += 1
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        stripe_secret = os.getenv("STRIPE_SECRET_KEY")
        stripe_public = os.getenv("STRIPE_PUBLIC_KEY")
        
        if stripe_secret and stripe_public:
            mode_secret = "LIVE" if stripe_secret.startswith("sk_live_") else "TEST"
            mode_public = "LIVE" if stripe_public.startswith("pk_live_") else "TEST"
            print(f"OK Stripe Secret: Mode {mode_secret}")
            print(f"OK Stripe Public: Mode {mode_public}")
            results["passed"] += 1
        else:
            print("ERREUR Stripe incomplet")
            results["failed"] += 1
        print()
        
        # Test 5: Configuration OpenAI
        print("5. CONFIGURATION OPENAI")
        print("-" * 70)
        results["total"] += 1
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if openai_key:
            print(f"OK OpenAI: {openai_key[:15]}...")
            results["passed"] += 1
        else:
            print("ERREUR OpenAI non configure")
            results["failed"] += 1
        print()
        
        # Test 6: Configuration Vertex AI
        print("6. CONFIGURATION VERTEX AI")
        print("-" * 70)
        results["total"] += 1
        vertex_project = os.getenv("VERTEX_AI_PROJECT_ID")
        vertex_location = os.getenv("VERTEX_AI_LOCATION")
        
        if vertex_project and vertex_location:
            print(f"OK Vertex AI: {vertex_project} ({vertex_location})")
            results["passed"] += 1
        else:
            print("ERREUR Vertex AI non configure")
            results["failed"] += 1
        print()
        
        # Test 7: Base de données - Produits
        print("7. BASE DE DONNEES - PRODUITS")
        print("-" * 70)
        results["total"] += 1
        try:
            import sys
            sys.path.append(".")
            from app.database import SessionLocal
            from app.models.product_db import ProductDB
            
            db = SessionLocal()
            product_count = db.query(ProductDB).count()
            db.close()
            
            if product_count > 0:
                print(f"OK {product_count} produits en base")
                results["passed"] += 1
            else:
                print("ERREUR Aucun produit")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        print()
        
        # Test 8: Base de données - Utilisateur test
        print("8. BASE DE DONNEES - UTILISATEUR TEST")
        print("-" * 70)
        results["total"] += 1
        try:
            from app.models.user_db import UserDB
            
            db = SessionLocal()
            test_user = db.query(UserDB).filter(UserDB.email == "test@webox.com").first()
            db.close()
            
            if test_user:
                print(f"OK Utilisateur test existe (ID: {test_user.id})")
                results["passed"] += 1
            else:
                print("ERREUR Utilisateur test inexistant")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        print()
        
        # Résumé
        print("="*70)
        print("RESUME DES TESTS")
        print("="*70)
        print(f"Total: {results['total']}")
        print(f"Reussis: {results['passed']} ({int(results['passed']/results['total']*100)}%)")
        print(f"Echoues: {results['failed']}")
        print()
        
        if results['passed'] == results['total']:
            print("OK TOUS LES TESTS SONT PASSES!")
        elif results['passed'] >= results['total'] * 0.7:
            print("OK Configuration fonctionnelle (quelques tests echoues)")
        else:
            print("ATTENTION Plusieurs tests ont echoue")
        
        print()
        
        # Recommandations
        print("PROCHAINES ETAPES:")
        print("-" * 70)
        print("1. Tester manuellement la connexion sur http://localhost:8000/login")
        print("2. Tester l'ajout au panier sur la marketplace")
        print("3. Tester un paiement Stripe en mode TEST")
        print("4. Tester la generation IA (chat, images)")
        print()
        print("DOCUMENTATION:")
        print("- RAPPORT_FINAL_SESSION.md - Rapport complet")
        print("- GUIDE_CONFIGURATION_CLES_API.md - Configuration APIs")
        print("- DEMARRAGE_RAPIDE.md - Guide demarrage")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(test_final())
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
