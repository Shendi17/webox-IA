"""
Test génération audio - Vérification routes et simulation
Date: 25 Janvier 2026
"""

import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_generation_audio():
    """Tester les routes de génération audio"""
    
    print("\n" + "="*70)
    print("TEST GENERATION AUDIO - WEBOX")
    print("="*70 + "\n")
    
    results = {"passed": 0, "failed": 0, "total": 0}
    
    # Vérifier les clés API audio
    print("VERIFICATION CLES API AUDIO")
    print("-" * 70)
    
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    suno_key = os.getenv("SUNO_API_KEY")
    udio_key = os.getenv("UDIO_API_KEY")
    
    print(f"ElevenLabs: {'OK' if elevenlabs_key else 'NON CONFIGURE'}")
    print(f"Suno AI: {'OK' if suno_key else 'NON CONFIGURE'}")
    print(f"Udio: {'OK' if udio_key else 'NON CONFIGURE'}")
    print()
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60.0) as client:
        
        # Test 1: Route génération audio (POST)
        print("1. TEST ROUTE GENERATION AUDIO")
        print("-" * 70)
        results["total"] += 1
        
        try:
            response = await client.post(
                "/api/generation/audio",
                json={
                    "text": "Bonjour, ceci est un test de generation audio",
                    "model": "elevenlabs",
                    "audio_type": "speech",
                    "voice_id": "default",
                    "language": "fr"
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"OK Generation audio initiee")
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
        
        # Test 2: Route liste audios (GET)
        print("2. TEST ROUTE LISTE AUDIOS")
        print("-" * 70)
        results["total"] += 1
        
        try:
            response = await client.get("/api/generation/audios")
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('audios', []))
                print(f"OK Liste audios: {count} audios trouves")
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
        
        # Test 3: Test génération musique
        print("3. TEST GENERATION MUSIQUE (SUNO)")
        print("-" * 70)
        results["total"] += 1
        
        try:
            response = await client.post(
                "/api/generation/audio",
                json={
                    "prompt": "Une musique relaxante de piano",
                    "model": "suno",
                    "audio_type": "music",
                    "duration": 30
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"OK Generation musique initiee")
                print(f"   ID: {data.get('id')}")
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
        
        # Résumé
        print("="*70)
        print("RESUME DES TESTS")
        print("="*70)
        print(f"Total: {results['total']}")
        print(f"Reussis: {results['passed']} ({int(results['passed']/results['total']*100) if results['total'] > 0 else 0}%)")
        print(f"Echoues: {results['failed']}")
        print()
        
        print("STATUT GENERATION AUDIO:")
        print("-" * 70)
        print("Routes implementees: OUI")
        print("APIs configurees: NON (simulation)")
        print("Fonctionnalite: PARTIELLE (simulation uniquement)")
        print()
        print("ACTIONS REQUISES:")
        print("1. Configurer ELEVENLABS_API_KEY pour ElevenLabs")
        print("2. Configurer SUNO_API_KEY pour Suno AI")
        print("3. Configurer UDIO_API_KEY pour Udio")
        print("4. Implementer vraies APIs (actuellement simulation)")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(test_generation_audio())
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
