"""
Script de test pour les fonctionnalités de génération IA
Date: 24 Janvier 2026
"""

import httpx
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_ia_generation():
    """Tester toutes les fonctionnalités de génération IA"""
    
    print("\n" + "="*80)
    print("🤖 TEST GÉNÉRATION IA - COMPLET")
    print("="*80 + "\n")
    
    # Vérifier les clés API
    print("🔍 Vérification des clés API configurées...")
    print("-" * 80)
    
    apis = {
        "OpenAI (GPT-4, DALL-E)": os.getenv("OPENAI_API_KEY"),
        "Anthropic (Claude)": os.getenv("ANTHROPIC_API_KEY"),
        "Google (Gemini)": os.getenv("GOOGLE_API_KEY"),
        "Mistral": os.getenv("MISTRAL_API_KEY"),
        "Groq": os.getenv("GROQ_API_KEY"),
        "Stability AI": os.getenv("STABILITY_API_KEY"),
        "ElevenLabs": os.getenv("ELEVENLABS_API_KEY"),
    }
    
    configured_apis = []
    for name, key in apis.items():
        if key:
            masked = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "****"
            print(f"✅ {name}: {masked}")
            configured_apis.append(name)
        else:
            print(f"❌ {name}: NON CONFIGURÉ")
    
    print(f"\n📊 {len(configured_apis)}/{len(apis)} APIs configurées\n")
    
    if not apis["OpenAI (GPT-4, DALL-E)"]:
        print("⚠️ OpenAI non configuré - Les tests principaux seront limités")
        print("\nPour configurer OpenAI:")
        print("1. Aller sur https://platform.openai.com")
        print("2. Créer un compte et ajouter un moyen de paiement")
        print("3. Créer une clé API")
        print("4. Ajouter dans .env: OPENAI_API_KEY=sk-proj-...\n")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60.0) as client:
        
        # 1. Connexion
        print("="*80)
        print("1️⃣ CONNEXION UTILISATEUR")
        print("="*80 + "\n")
        
        login_response = await client.post("/api/auth/login", json={
            "email": "test@webox.com",
            "password": "test123456"
        })
        
        if login_response.status_code != 200:
            print("❌ Échec de la connexion")
            print(f"   Status: {login_response.status_code}")
            return
        
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Connexion réussie\n")
        
        # 2. Test Chat IA (Texte)
        print("="*80)
        print("2️⃣ TEST CHAT IA (GÉNÉRATION TEXTE)")
        print("="*80 + "\n")
        
        if apis["OpenAI (GPT-4, DALL-E)"]:
            print("🤖 Test avec GPT-4...")
            chat_response = await client.post("/api/chat/send",
                headers=headers,
                json={
                    "message": "Dis bonjour en une phrase courte",
                    "ai_model": "gpt-4"
                }
            )
            
            if chat_response.status_code in [200, 201]:
                chat_data = chat_response.json()
                print(f"✅ GPT-4 répond:")
                print(f"   {chat_data.get('response', 'Pas de réponse')[:100]}...\n")
            else:
                print(f"❌ Erreur GPT-4: {chat_response.status_code}")
                print(f"   {chat_response.text[:200]}\n")
        
        if apis["Anthropic (Claude)"]:
            print("🤖 Test avec Claude...")
            chat_response = await client.post("/api/chat/send",
                headers=headers,
                json={
                    "message": "Dis bonjour en une phrase courte",
                    "ai_model": "claude-3-sonnet"
                }
            )
            
            if chat_response.status_code in [200, 201]:
                print("✅ Claude répond\n")
            else:
                print(f"❌ Erreur Claude: {chat_response.status_code}\n")
        
        # 3. Test Génération Image
        print("="*80)
        print("3️⃣ TEST GÉNÉRATION IMAGE")
        print("="*80 + "\n")
        
        if apis["OpenAI (GPT-4, DALL-E)"]:
            print("🎨 Test DALL-E 3...")
            print("   Prompt: 'Un chat mignon dans un style cartoon'")
            print("   ⏳ Génération en cours (peut prendre 10-30s)...\n")
            
            image_response = await client.post("/api/generation/image",
                headers=headers,
                json={
                    "prompt": "Un chat mignon dans un style cartoon",
                    "model": "dall-e-3",
                    "size": "1024x1024",
                    "quality": "standard"
                }
            )
            
            if image_response.status_code in [200, 201]:
                image_data = image_response.json()
                print(f"✅ Image générée!")
                print(f"   ID: {image_data.get('id')}")
                print(f"   Statut: {image_data.get('status')}")
                print(f"   Modèle: {image_data.get('model')}")
                
                # Attendre un peu et vérifier le statut
                image_id = image_data.get('id')
                if image_id:
                    await asyncio.sleep(5)
                    status_response = await client.get(f"/api/generation/image/{image_id}", headers=headers)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        print(f"   Statut final: {status_data.get('status')}")
                        if status_data.get('image_url'):
                            print(f"   URL: {status_data.get('image_url')[:50]}...")
                print()
            else:
                print(f"❌ Erreur DALL-E: {image_response.status_code}")
                print(f"   {image_response.text[:200]}\n")
        
        # 4. Test Génération Vidéo
        print("="*80)
        print("4️⃣ TEST GÉNÉRATION VIDÉO")
        print("="*80 + "\n")
        
        print("🎬 Test génération vidéo...")
        print("   Prompt: 'Une belle animation de nature'")
        print("   ⚠️ Note: APIs vidéo en simulation pour l'instant\n")
        
        video_response = await client.post("/api/generation/video",
            headers=headers,
            json={
                "prompt": "Une belle animation de nature",
                "model": "runway",
                "duration": 5
            }
        )
        
        if video_response.status_code in [200, 201]:
            video_data = video_response.json()
            print(f"✅ Vidéo en génération")
            print(f"   ID: {video_data.get('id')}")
            print(f"   Statut: {video_data.get('status')}")
            print(f"   Temps estimé: {video_data.get('estimated_time')}\n")
        else:
            print(f"❌ Erreur: {video_response.status_code}\n")
        
        # 5. Test Génération Audio
        print("="*80)
        print("5️⃣ TEST GÉNÉRATION AUDIO")
        print("="*80 + "\n")
        
        print("🎵 Test génération audio...")
        print("   Texte: 'Bonjour, ceci est un test de synthèse vocale'")
        print("   ⚠️ Note: APIs audio en simulation pour l'instant\n")
        
        audio_response = await client.post("/api/generation/audio",
            headers=headers,
            json={
                "prompt": "Bonjour, ceci est un test de synthèse vocale",
                "model": "elevenlabs",
                "audio_type": "speech",
                "language": "fr"
            }
        )
        
        if audio_response.status_code in [200, 201]:
            audio_data = audio_response.json()
            print(f"✅ Audio en génération")
            print(f"   ID: {audio_data.get('id')}")
            print(f"   Statut: {audio_data.get('status')}\n")
        else:
            print(f"❌ Erreur: {audio_response.status_code}\n")
        
        # 6. Récupérer l'historique
        print("="*80)
        print("6️⃣ HISTORIQUE DES GÉNÉRATIONS")
        print("="*80 + "\n")
        
        # Images
        images_response = await client.get("/api/generation/images?limit=5", headers=headers)
        if images_response.status_code == 200:
            images_data = images_response.json()
            print(f"📷 Images générées: {images_data.get('total', 0)}")
            for img in images_data.get('images', [])[:3]:
                print(f"   - {img.get('prompt', 'N/A')[:50]}... ({img.get('status')})")
        
        # Vidéos
        videos_response = await client.get("/api/generation/videos?limit=5", headers=headers)
        if videos_response.status_code == 200:
            videos_data = videos_response.json()
            print(f"🎬 Vidéos générées: {videos_data.get('total', 0)}")
        
        # Audios
        audios_response = await client.get("/api/generation/audios?limit=5", headers=headers)
        if audios_response.status_code == 200:
            audios_data = audios_response.json()
            print(f"🎵 Audios générés: {audios_data.get('total', 0)}")
        
        print()
        
        # Récapitulatif
        print("="*80)
        print("📊 RÉCAPITULATIF DES TESTS")
        print("="*80)
        print(f"✅ Connexion: OK")
        print(f"{'✅' if apis['OpenAI (GPT-4, DALL-E)'] else '❌'} Chat GPT-4: {'Testé' if apis['OpenAI (GPT-4, DALL-E)'] else 'Non configuré'}")
        print(f"{'✅' if apis['Anthropic (Claude)'] else '❌'} Chat Claude: {'Testé' if apis['Anthropic (Claude)'] else 'Non configuré'}")
        print(f"{'✅' if apis['OpenAI (GPT-4, DALL-E)'] else '⚠️'} Génération Image: {'Testé' if apis['OpenAI (GPT-4, DALL-E)'] else 'Simulation'}")
        print(f"⚠️ Génération Vidéo: Simulation (API à implémenter)")
        print(f"⚠️ Génération Audio: Simulation (API à implémenter)")
        
        print("\n" + "="*80)
        print("🎯 PROCHAINES ÉTAPES")
        print("="*80)
        print("1. Configurer les APIs manquantes (voir ci-dessus)")
        print("2. Implémenter les vraies APIs vidéo (Runway, Pika, Luma)")
        print("3. Implémenter les vraies APIs audio (ElevenLabs, Suno)")
        print("4. Tester avec différents prompts")
        print("5. Vérifier la sauvegarde en base de données")
        print("\n📚 Documentation: GUIDE_CONFIGURATION_CLES_API.md\n")


if __name__ == "__main__":
    print("\n⚠️ Assurez-vous que:")
    print("  1. Le serveur est lancé (python main.py)")
    print("  2. Au moins OpenAI est configuré dans .env")
    print("  3. Un utilisateur test existe (test@webox.com)")
    print("  4. Les tables de génération existent en DB\n")
    
    try:
        asyncio.run(test_ia_generation())
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
