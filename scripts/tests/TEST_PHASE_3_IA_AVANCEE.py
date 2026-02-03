"""
Test Phase 3 - IA Avancée (eBooks, Vidéos Shorts, Publicités)
Date: 25 Janvier 2026
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_phase_3_ia_avancee():
    """Tester Phase 3 - Génération IA Avancée"""
    
    print("\n" + "="*70)
    print("TEST PHASE 3 - IA AVANCÉE")
    print("="*70 + "\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "categories": {}
    }
    
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=False) as client:
        
        # ========== CONNEXION ==========
        print("🔐 CONNEXION")
        print("-" * 70)
        
        try:
            response = await client.post(
                f"{BASE_URL}/login",
                data={
                    "email": os.getenv("ADMIN_EMAIL", "admin@webox.com"),
                    "password": os.getenv("ADMIN_PASSWORD", "admin123")
                }
            )
            
            if response.status_code in [200, 302]:
                print("   ✅ Connexion réussie\n")
            else:
                print(f"   ❌ Échec connexion: {response.status_code}")
                return results
                
        except Exception as e:
            print(f"   ❌ Erreur connexion: {e}")
            return results
        
        # ========== CATÉGORIE 1: GÉNÉRATION EBOOKS ==========
        print("📚 CATÉGORIE 1: GÉNÉRATION EBOOKS")
        print("-" * 70)
        
        category = "eBooks"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test 1: Route existe
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.post(
                f"{BASE_URL}/api/generation/ebook",
                json={
                    "topic": "Intelligence Artificielle",
                    "num_chapters": 5,
                    "style": "informatif",
                    "language": "fr"
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"   ✅ POST /api/generation/ebook: {response.status_code}")
                print(f"      📖 Sujet: Intelligence Artificielle")
                print(f"      📄 Chapitres: 5")
                if data.get("file_path"):
                    print(f"      💾 Fichier: {data.get('file_path')}")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "Génération eBook", "status": "✅"})
            else:
                print(f"   ⚠️ POST /api/generation/ebook: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "Génération eBook", "status": f"⚠️ {response.status_code}"})
        except Exception as e:
            print(f"   ❌ POST /api/generation/ebook: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "Génération eBook", "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 2: VIDÉOS SHORTS ==========
        print("🎬 CATÉGORIE 2: VIDÉOS SHORTS")
        print("-" * 70)
        
        category = "Vidéos Shorts"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test 1: Route existe
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.post(
                f"{BASE_URL}/api/generation/video-short",
                json={
                    "topic": "Marketing Digital",
                    "duration": 30,
                    "style": "éducatif",
                    "language": "fr"
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"   ✅ POST /api/generation/video-short: {response.status_code}")
                print(f"      🎥 Sujet: Marketing Digital")
                print(f"      ⏱️ Durée: 30s")
                if data.get("video_url"):
                    print(f"      🔗 URL: {data.get('video_url')}")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "Génération vidéo short", "status": "✅"})
            else:
                print(f"   ⚠️ POST /api/generation/video-short: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "Génération vidéo short", "status": f"⚠️ {response.status_code}"})
        except Exception as e:
            print(f"   ❌ POST /api/generation/video-short: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "Génération vidéo short", "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 3: PUBLICITÉS VIDÉO ==========
        print("📺 CATÉGORIE 3: PUBLICITÉS VIDÉO")
        print("-" * 70)
        
        category = "Publicités"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test 1: Route existe
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.post(
                f"{BASE_URL}/api/generation/video-ad",
                json={
                    "product_name": "Produit Test",
                    "product_description": "Description du produit",
                    "ad_type": "showcase",
                    "duration": 15,
                    "cta": "Acheter maintenant"
                }
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"   ✅ POST /api/generation/video-ad: {response.status_code}")
                print(f"      📦 Produit: Produit Test")
                print(f"      ⏱️ Durée: 15s")
                print(f"      🎯 CTA: Acheter maintenant")
                if data.get("video_url"):
                    print(f"      🔗 URL: {data.get('video_url')}")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "Génération publicité", "status": "✅"})
            else:
                print(f"   ⚠️ POST /api/generation/video-ad: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "Génération publicité", "status": f"⚠️ {response.status_code}"})
        except Exception as e:
            print(f"   ❌ POST /api/generation/video-ad: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "Génération publicité", "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 4: VÉRIFICATION FICHIERS ==========
        print("💾 CATÉGORIE 4: VÉRIFICATION FICHIERS GÉNÉRÉS")
        print("-" * 70)
        
        category = "Fichiers"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        import os as os_module
        
        # Vérifier dossiers de génération
        folders = [
            ("generated/ebooks", "Dossier eBooks"),
            ("generated/videos", "Dossier vidéos"),
            ("generated/images", "Dossier images")
        ]
        
        for folder, name in folders:
            results["total"] += 1
            results["categories"][category]["total"] += 1
            full_path = os_module.path.join(os.getcwd(), folder)
            if os_module.path.exists(full_path):
                files = os_module.listdir(full_path)
                print(f"   ✅ {name}: {len(files)} fichier(s)")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": name, "status": "✅"})
            else:
                print(f"   ⚠️ {name}: Dossier manquant")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": name, "status": "⚠️"})
        
        print()
    
    return results


async def main():
    results = await test_phase_3_ia_avancee()
    
    # Résumé global
    print("="*70)
    print("RÉSUMÉ GLOBAL - PHASE 3 IA AVANCÉE")
    print("="*70)
    print(f"\n📊 Total tests: {results['total']}")
    print(f"✅ Réussis: {results['passed']}")
    print(f"❌ Échoués: {results['failed']}")
    
    if results['total'] > 0:
        print(f"📈 Taux de réussite: {(results['passed']/results['total']*100):.1f}%")
    
    # Résumé par catégorie
    print("\n📋 Par catégorie:")
    for category, data in results["categories"].items():
        if data["total"] > 0:
            taux = (data["passed"]/data["total"]*100)
            print(f"\n   {category}: {data['passed']}/{data['total']} ({taux:.0f}%)")
            for test in data["tests"]:
                print(f"      {test['status']} {test['test']}")
    
    print("\n" + "="*70)
    print()


if __name__ == "__main__":
    asyncio.run(main())
