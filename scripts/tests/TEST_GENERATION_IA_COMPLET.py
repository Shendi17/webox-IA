"""
Test complet de génération IA - Toutes les APIs
Date: 25 Janvier 2026
"""

import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_generation_ia():
    """Tester toutes les APIs de génération IA"""
    
    print("\n" + "="*70)
    print("TEST COMPLET GENERATION IA - WEBOX")
    print("="*70 + "\n")
    
    results = {"passed": 0, "failed": 0, "total": 0}
    
    # Vérifier les clés API
    print("VERIFICATION DES CLES API")
    print("-" * 70)
    
    apis = {
        "OpenAI (GPT-4, DALL-E)": os.getenv("OPENAI_API_KEY"),
        "Anthropic (Claude)": os.getenv("ANTHROPIC_API_KEY"),
        "Vertex AI (Gemini)": os.getenv("VERTEX_AI_PROJECT_ID"),
        "Mistral": os.getenv("MISTRAL_API_KEY"),
        "Groq": os.getenv("GROQ_API_KEY"),
        "Cohere": os.getenv("COHERE_API_KEY"),
    }
    
    for name, key in apis.items():
        if key:
            print(f"OK {name}: {key[:15]}...")
        else:
            print(f"ERREUR {name}: Non configure")
    
    print()
    
    # Créer un client HTTP avec cookies
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60.0, follow_redirects=True) as client:
        
        # 1. Connexion
        print("1. CONNEXION UTILISATEUR")
        print("-" * 70)
        results["total"] += 1
        
        try:
            login_response = await client.post(
                "/login",
                data={
                    "email": "test@webox.com",
                    "password": "test123456",
                    "remember_me": False
                }
            )
            
            if login_response.status_code == 200:
                print("OK Connexion reussie")
                results["passed"] += 1
            else:
                print(f"ERREUR Connexion: {login_response.status_code}")
                results["failed"] += 1
                print("Impossible de continuer sans connexion")
                return
        except Exception as e:
            print(f"ERREUR: {e}")
            results["failed"] += 1
            return
        
        print()
        
        # 2. Test Chat GPT-4
        print("2. TEST CHAT GPT-4")
        print("-" * 70)
        results["total"] += 1
        
        if os.getenv("OPENAI_API_KEY"):
            try:
                chat_response = await client.post(
                    "/api/chat/message",
                    json={
                        "message": "Bonjour, peux-tu me dire bonjour en retour ?",
                        "model": "gpt-4",
                        "conversation_id": None
                    }
                )
                
                if chat_response.status_code == 200:
                    data = chat_response.json()
                    print(f"OK Chat GPT-4 fonctionne")
                    print(f"   Reponse: {data.get('response', '')[:100]}...")
                    results["passed"] += 1
                else:
                    print(f"ERREUR Status: {chat_response.status_code}")
                    print(f"   {chat_response.text[:200]}")
                    results["failed"] += 1
            except Exception as e:
                print(f"ERREUR: {e}")
                results["failed"] += 1
        else:
            print("SKIP OpenAI non configure")
            results["total"] -= 1
        
        print()
        
        # 3. Test Chat Claude
        print("3. TEST CHAT CLAUDE (ANTHROPIC)")
        print("-" * 70)
        results["total"] += 1
        
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                chat_response = await client.post(
                    "/api/chat/message",
                    json={
                        "message": "Bonjour Claude, comment vas-tu ?",
                        "model": "claude-3-sonnet",
                        "conversation_id": None
                    }
                )
                
                if chat_response.status_code == 200:
                    data = chat_response.json()
                    print(f"OK Chat Claude fonctionne")
                    print(f"   Reponse: {data.get('response', '')[:100]}...")
                    results["passed"] += 1
                else:
                    print(f"ERREUR Status: {chat_response.status_code}")
                    print(f"   {chat_response.text[:200]}")
                    results["failed"] += 1
            except Exception as e:
                print(f"ERREUR: {e}")
                results["failed"] += 1
        else:
            print("SKIP Anthropic non configure")
            results["total"] -= 1
        
        print()
        
        # 4. Test Chat Gemini (Vertex AI)
        print("4. TEST CHAT GEMINI (VERTEX AI)")
        print("-" * 70)
        results["total"] += 1
        
        if os.getenv("VERTEX_AI_PROJECT_ID"):
            try:
                chat_response = await client.post(
                    "/api/chat/message",
                    json={
                        "message": "Bonjour Gemini, presente-toi brievement",
                        "model": "gemini-pro",
                        "conversation_id": None
                    }
                )
                
                if chat_response.status_code == 200:
                    data = chat_response.json()
                    print(f"OK Chat Gemini fonctionne")
                    print(f"   Reponse: {data.get('response', '')[:100]}...")
                    results["passed"] += 1
                else:
                    print(f"ERREUR Status: {chat_response.status_code}")
                    print(f"   {chat_response.text[:200]}")
                    results["failed"] += 1
            except Exception as e:
                print(f"ERREUR: {e}")
                results["failed"] += 1
        else:
            print("SKIP Vertex AI non configure")
            results["total"] -= 1
        
        print()
        
        # 5. Test Génération Image DALL-E 3
        print("5. TEST GENERATION IMAGE DALL-E 3")
        print("-" * 70)
        results["total"] += 1
        
        if os.getenv("OPENAI_API_KEY"):
            try:
                image_response = await client.post(
                    "/api/generation/image",
                    json={
                        "prompt": "Un chat mignon qui code sur un ordinateur, style cartoon",
                        "model": "dall-e-3",
                        "size": "1024x1024",
                        "quality": "standard",
                        "style": "vivid"
                    }
                )
                
                if image_response.status_code == 200:
                    data = image_response.json()
                    print(f"OK Generation image DALL-E 3 reussie")
                    print(f"   URL: {data.get('url', '')[:60]}...")
                    print(f"   ID: {data.get('id')}")
                    results["passed"] += 1
                else:
                    print(f"ERREUR Status: {image_response.status_code}")
                    print(f"   {image_response.text[:200]}")
                    results["failed"] += 1
            except Exception as e:
                print(f"ERREUR: {e}")
                results["failed"] += 1
        else:
            print("SKIP OpenAI non configure")
            results["total"] -= 1
        
        print()
        
        # 6. Test Liste des images générées
        print("6. TEST LISTE IMAGES GENEREES")
        print("-" * 70)
        results["total"] += 1
        
        try:
            list_response = await client.get("/api/generation/images")
            
            if list_response.status_code == 200:
                data = list_response.json()
                count = len(data.get('images', []))
                print(f"OK Liste images: {count} images trouvees")
                results["passed"] += 1
            else:
                print(f"ERREUR Status: {list_response.status_code}")
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
        
        if results['passed'] == results['total']:
            print("OK TOUS LES TESTS SONT PASSES!")
        elif results['passed'] >= results['total'] * 0.7:
            print("OK Majorite des tests passes")
        else:
            print("ATTENTION Plusieurs tests ont echoue")
        
        print()


if __name__ == "__main__":
    try:
        asyncio.run(test_generation_ia())
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
