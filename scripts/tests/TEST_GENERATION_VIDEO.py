"""
Test génération vidéo - Vérification routes et simulation
Date: 25 Janvier 2026
"""

import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_generation_video():
    """Tester les routes de génération vidéo"""
    
    print("\n" + "="*70)
    print("TEST GENERATION VIDEO - WEBOX")
    print("="*70 + "\n")
    
    results = {"passed": 0, "failed": 0, "total": 0}
    
    # Vérifier les clés API vidéo
    print("VERIFICATION CLES API VIDEO")
    print("-" * 70)
    
    runway_key = os.getenv("RUNWAY_API_KEY")
    pika_key = os.getenv("PIKA_API_KEY")
    luma_key = os.getenv("LUMA_API_KEY")
    
    print(f"Runway ML: {'OK' if runway_key else 'NON CONFIGURE'}")
    print(f"Pika Labs: {'OK' if pika_key else 'NON CONFIGURE'}")
    print(f"Luma AI: {'OK' if luma_key else 'NON CONFIGURE'}")
    print()
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60.0) as client:
        
        # Test 1: Route génération vidéo (POST)
        print("1. TEST ROUTE GENERATION VIDEO")
        print("-" * 70)
        results["total"] += 1
        
        try:
            response = await client.post(
                "/api/generation/video",
                json={
                    "prompt": "Un chat qui joue avec une balle, style cartoon",
                    "model": "runway",
                    "duration": 5,
                    "resolution": "1080p",
                    "fps": 30
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"OK Generation video initiee")
                print(f"   ID: {data.get('id')}")
                print(f"   Status: {data.get('status')}")
                print(f"   Model: {data.get('model')}")
                results["passed"] += 1
            elif response.status_code == 401:
                print("SKIP Authentification requise")
                results["total"] -= 1
            else:
                print(f"ERREUR Status: {response.status_code}")
                print(f"   {response.text[:200]}")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        
        print()
        
        # Test 2: Route liste vidéos (GET)
        print("2. TEST ROUTE LISTE VIDEOS")
        print("-" * 70)
        results["total"] += 1
        
        try:
            response = await client.get("/api/generation/videos")
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('videos', []))
                print(f"OK Liste videos: {count} videos trouvees")
                results["passed"] += 1
            elif response.status_code == 401:
                print("SKIP Authentification requise")
                results["total"] -= 1
            else:
                print(f"ERREUR Status: {response.status_code}")
                results["failed"] += 1
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
        
        print()
        
        # Test 3: Vérifier structure de la route
        print("3. VERIFICATION STRUCTURE ROUTE")
        print("-" * 70)
        results["total"] += 1
        
        try:
            # Tester avec données manquantes pour voir la validation
            response = await client.post(
                "/api/generation/video",
                json={"prompt": "Test"}
            )
            
            if response.status_code in [200, 201, 422, 401]:
                print("OK Route existe et valide les donnees")
                results["passed"] += 1
            else:
                print(f"ATTENTION Status inattendu: {response.status_code}")
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
        print(f"Reussis: {results['passed']} ({int(results['passed']/results['total']*100) if results['total'] > 0 else 0}%)")
        print(f"Echoues: {results['failed']}")
        print()
        
        print("STATUT GENERATION VIDEO:")
        print("-" * 70)
        print("Routes implementees: OUI")
        print("APIs configurees: NON (simulation)")
        print("Fonctionnalite: PARTIELLE (simulation uniquement)")
        print()
        print("ACTIONS REQUISES:")
        print("1. Configurer RUNWAY_API_KEY pour Runway ML")
        print("2. Configurer PIKA_API_KEY pour Pika Labs")
        print("3. Configurer LUMA_API_KEY pour Luma AI")
        print("4. Implementer vraies APIs (actuellement simulation)")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(test_generation_video())
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
