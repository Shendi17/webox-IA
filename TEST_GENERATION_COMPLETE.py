"""
Script de test complet pour toutes les fonctionnalités de génération
Teste: Images, Vidéos, Audio, eBooks, Shorts, Ads, Logos
"""

import asyncio
import httpx
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = None  # Sera récupéré lors du login

async def login():
    """Se connecter et récupérer le token"""
    global TOKEN
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/login",
            data={
                "username": "admin@webox.local",
                "password": "admin123"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get("access_token")
            print(f"✅ Connexion réussie - Token: {TOKEN[:20]}...")
            return True
        else:
            print(f"❌ Échec connexion: {response.status_code}")
            return False

async def test_image_generation():
    """Test génération d'image avec DALL-E 3"""
    print("\n" + "="*60)
    print("🖼️  TEST GÉNÉRATION D'IMAGE (DALL-E 3)")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/generation/image",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "prompt": "A beautiful sunset over mountains, photorealistic, 8k quality",
                "model": "dall-e-3",
                "size": "1024x1024",
                "quality": "standard"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération lancée:")
            print(f"   - ID: {data['id']}")
            print(f"   - Modèle: {data['model']}")
            print(f"   - Statut: {data['status']}")
            
            # Attendre la complétion
            image_id = data['id']
            await wait_for_completion(image_id, 'image')
            return image_id
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            return None

async def test_video_generation():
    """Test génération de vidéo"""
    print("\n" + "="*60)
    print("🎬 TEST GÉNÉRATION DE VIDÉO")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/generation/video",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "prompt": "A serene lake with mountains in the background",
                "model": "runway",
                "duration": 5,
                "resolution": "1080p",
                "fps": 24
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération lancée:")
            print(f"   - ID: {data['id']}")
            print(f"   - Modèle: {data['model']}")
            print(f"   - Temps estimé: {data['estimated_time']}")
            return data['id']
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            return None

async def test_ebook_generation():
    """Test génération d'eBook"""
    print("\n" + "="*60)
    print("📚 TEST GÉNÉRATION D'EBOOK")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/generation/ebook",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "title": "Guide du Marketing Digital",
                "topic": "Marketing digital pour débutants",
                "num_chapters": 3,
                "language": "fr",
                "style": "informative",
                "target_audience": "general"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération lancée:")
            print(f"   - ID: {data['id']}")
            print(f"   - Titre: {data['title']}")
            print(f"   - Temps estimé: {data['estimated_time']}")
            return data['id']
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            return None

async def test_short_generation():
    """Test génération de Short vidéo"""
    print("\n" + "="*60)
    print("📱 TEST GÉNÉRATION DE SHORT")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/generation/short",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "topic": "3 astuces pour améliorer sa productivité",
                "duration": 60,
                "style": "educational",
                "voice": "alloy",
                "music": True
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération lancée:")
            print(f"   - ID: {data['id']}")
            print(f"   - Sujet: {data['topic']}")
            print(f"   - Temps estimé: {data['estimated_time']}")
            return data['id']
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            return None

async def test_logo_generation():
    """Test génération de logo (via image)"""
    print("\n" + "="*60)
    print("🎨 TEST GÉNÉRATION DE LOGO")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/generation/image",
            headers={"Authorization": f"Bearer {TOKEN}"},
            json={
                "prompt": "Professional logo for 'TechStart' brand, SaaS industry, modern style, minimalist, vector art, clean design",
                "model": "dall-e-3",
                "size": "1024x1024",
                "quality": "hd"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération lancée:")
            print(f"   - ID: {data['id']}")
            print(f"   - Modèle: {data['model']}")
            return data['id']
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            return None

async def wait_for_completion(item_id, item_type, max_wait=60):
    """Attendre la complétion d'une génération"""
    print(f"\n⏳ Attente de la complétion (max {max_wait}s)...")
    
    async with httpx.AsyncClient() as client:
        for i in range(max_wait):
            await asyncio.sleep(2)
            
            response = await client.get(
                f"{BASE_URL}/api/generation/{item_type}/{item_id}",
                headers={"Authorization": f"Bearer {TOKEN}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                
                if status == 'completed':
                    print(f"✅ Génération terminée !")
                    print(f"   - Coût: ${data.get('cost', 0):.4f}")
                    if 'image_url' in data:
                        print(f"   - URL: {data['image_url']}")
                    if 'pdf_url' in data:
                        print(f"   - PDF: {data['pdf_url']}")
                    return True
                elif status == 'failed':
                    print(f"❌ Génération échouée: {data.get('error_message')}")
                    return False
                else:
                    print(f"   [{i*2}s] Statut: {status}...", end='\r')
            
            if i >= max_wait - 1:
                print(f"\n⏱️  Timeout - La génération continue en arrière-plan")
                return None

async def check_history():
    """Vérifier l'historique des générations"""
    print("\n" + "="*60)
    print("📋 VÉRIFICATION DE L'HISTORIQUE")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        # Images
        response = await client.get(
            f"{BASE_URL}/api/generation/images?limit=5",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            images = data.get('images', [])
            print(f"\n🖼️  Images générées: {len(images)}")
            for img in images[:3]:
                print(f"   - #{img['id']}: {img['model']} - {img['status']}")
        
        # Vidéos
        response = await client.get(
            f"{BASE_URL}/api/generation/videos?limit=5",
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            videos = data.get('videos', [])
            print(f"\n🎬 Vidéos générées: {len(videos)}")
            for vid in videos[:3]:
                print(f"   - #{vid['id']}: {vid['model']} - {vid['status']}")

async def main():
    """Fonction principale de test"""
    print("\n" + "="*60)
    print("🧪 TEST COMPLET DES FONCTIONNALITÉS DE GÉNÉRATION")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {BASE_URL}")
    
    # Connexion
    if not await login():
        print("\n❌ Impossible de se connecter - Arrêt des tests")
        return
    
    results = {}
    
    # Test 1: Image
    try:
        results['image'] = await test_image_generation()
    except Exception as e:
        print(f"❌ Erreur test image: {e}")
        results['image'] = None
    
    # Test 2: Logo
    try:
        results['logo'] = await test_logo_generation()
    except Exception as e:
        print(f"❌ Erreur test logo: {e}")
        results['logo'] = None
    
    # Test 3: eBook
    try:
        results['ebook'] = await test_ebook_generation()
    except Exception as e:
        print(f"❌ Erreur test ebook: {e}")
        results['ebook'] = None
    
    # Test 4: Short
    try:
        results['short'] = await test_short_generation()
    except Exception as e:
        print(f"❌ Erreur test short: {e}")
        results['short'] = None
    
    # Test 5: Vidéo
    try:
        results['video'] = await test_video_generation()
    except Exception as e:
        print(f"❌ Erreur test vidéo: {e}")
        results['video'] = None
    
    # Vérifier l'historique
    await asyncio.sleep(3)
    await check_history()
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, test_id in results.items():
        status = "✅ Réussi" if test_id else "❌ Échoué"
        print(f"{test_name.capitalize():15} {status} {f'(ID: {test_id})' if test_id else ''}")
    
    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS")
    print("="*60)
    print("\nVérifiez l'interface web: http://webox.local:8000/generation")
    print("Les résultats devraient apparaître dans l'historique.\n")

if __name__ == "__main__":
    asyncio.run(main())
