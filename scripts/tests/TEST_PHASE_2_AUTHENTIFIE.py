"""
Test Phase 2 avec Authentification Complète
Date: 25 Janvier 2026
Objectif: Tester toutes les routes protégées avec authentification
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_phase_2_authentifie():
    """Tester Phase 2 avec authentification"""
    
    print("\n" + "="*70)
    print("TEST PHASE 2 AVEC AUTHENTIFICATION COMPLÈTE")
    print("="*70 + "\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "categories": {}
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as client:
        
        # ========== ÉTAPE 1: CONNEXION ==========
        print("🔐 ÉTAPE 1: CONNEXION")
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
                print("   ✅ Connexion réussie")
                print(f"   📋 Cookies: {len(client.cookies)} cookie(s)")
            else:
                print(f"   ❌ Échec connexion: {response.status_code}")
                print("   ⚠️ Impossible de continuer les tests")
                return results
                
        except Exception as e:
            print(f"   ❌ Erreur connexion: {e}")
            return results
        
        print()
        
        # ========== CATÉGORIE 1: PAGES PROTÉGÉES ==========
        print("📄 CATÉGORIE 1: PAGES PROTÉGÉES")
        print("-" * 70)
        
        category = "Pages Protégées"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        pages_protegees = [
            ("/blog", "Blog"),
            ("/orders", "Commandes"),
            ("/notifications", "Notifications"),
            ("/settings", "Paramètres"),
            ("/support", "Support"),
            ("/activities", "Activités"),
            ("/admin", "Admin"),
        ]
        
        for url, name in pages_protegees:
            results["total"] += 1
            results["categories"][category]["total"] += 1
            try:
                response = await client.get(f"{BASE_URL}{url}")
                if response.status_code == 200:
                    print(f"   ✅ {name}: Accessible")
                    results["passed"] += 1
                    results["categories"][category]["passed"] += 1
                    results["categories"][category]["tests"].append({"test": name, "status": "✅"})
                elif response.status_code == 302:
                    print(f"   ⚠️ {name}: Redirection")
                    results["passed"] += 1
                    results["categories"][category]["passed"] += 1
                    results["categories"][category]["tests"].append({"test": name, "status": "⚠️ Redirect"})
                else:
                    print(f"   ❌ {name}: {response.status_code}")
                    results["failed"] += 1
                    results["categories"][category]["tests"].append({"test": name, "status": f"❌ {response.status_code}"})
            except Exception as e:
                print(f"   ❌ {name}: {e}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": name, "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 2: API PROFIL ==========
        print("👤 CATÉGORIE 2: API PROFIL")
        print("-" * 70)
        
        category = "API Profil"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test 1: Récupération profil
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/profile/me")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ GET /api/profile/me")
                print(f"      📧 Email: {data.get('email', 'N/A')}")
                print(f"      👤 Nom: {data.get('name', 'N/A')}")
                print(f"      🔑 Admin: {data.get('is_admin', False)}")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "GET profil", "status": "✅"})
            else:
                print(f"   ❌ GET /api/profile/me: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "GET profil", "status": f"❌"})
        except Exception as e:
            print(f"   ❌ GET /api/profile/me: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "GET profil", "status": "❌"})
        
        # Test 2: Modification profil
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.put(
                f"{BASE_URL}/api/profile/update",
                json={"name": "Admin WeBox Test"}
            )
            if response.status_code == 200:
                print(f"   ✅ PUT /api/profile/update")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "PUT profil", "status": "✅"})
            else:
                print(f"   ❌ PUT /api/profile/update: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "PUT profil", "status": f"❌"})
        except Exception as e:
            print(f"   ❌ PUT /api/profile/update: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "PUT profil", "status": "❌"})
        
        # Test 3: Préférences
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.put(
                f"{BASE_URL}/api/profile/preferences",
                json={"theme": "dark", "language": "fr"}
            )
            if response.status_code == 200:
                print(f"   ✅ PUT /api/profile/preferences")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "PUT préférences", "status": "✅"})
            else:
                print(f"   ❌ PUT /api/profile/preferences: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "PUT préférences", "status": f"❌"})
        except Exception as e:
            print(f"   ❌ PUT /api/profile/preferences: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "PUT préférences", "status": "❌"})
        
        # Test 4: Statistiques
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/profile/stats")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ GET /api/profile/stats")
                print(f"      📊 Données: {len(data)} entrée(s)")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "GET stats", "status": "✅"})
            else:
                print(f"   ❌ GET /api/profile/stats: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "GET stats", "status": f"❌"})
        except Exception as e:
            print(f"   ❌ GET /api/profile/stats: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "GET stats", "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 3: API ADMIN ==========
        print("👑 CATÉGORIE 3: API ADMIN")
        print("-" * 70)
        
        category = "API Admin"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test 1: Analytics
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/admin/analytics")
            if response.status_code == 200:
                print(f"   ✅ GET /api/admin/analytics")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "GET analytics", "status": "✅"})
            else:
                print(f"   ⚠️ GET /api/admin/analytics: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "GET analytics", "status": f"⚠️"})
        except Exception as e:
            print(f"   ❌ GET /api/admin/analytics: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "GET analytics", "status": "❌"})
        
        # Test 2: Clés API globales
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/admin/api-keys/global")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ GET /api/admin/api-keys/global")
                print(f"      🔑 Clés configurées: {len(data)} clé(s)")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "GET clés API", "status": "✅"})
            else:
                print(f"   ⚠️ GET /api/admin/api-keys/global: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "GET clés API", "status": f"⚠️"})
        except Exception as e:
            print(f"   ❌ GET /api/admin/api-keys/global: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "GET clés API", "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 4: API COMMANDES ==========
        print("📦 CATÉGORIE 4: API COMMANDES")
        print("-" * 70)
        
        category = "API Commandes"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test liste commandes
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/orders/list")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ GET /api/orders/list")
                print(f"      📦 Commandes: {len(data) if isinstance(data, list) else 'N/A'}")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "GET liste commandes", "status": "✅"})
            else:
                print(f"   ⚠️ GET /api/orders/list: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "GET liste commandes", "status": f"⚠️"})
        except Exception as e:
            print(f"   ❌ GET /api/orders/list: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "GET liste commandes", "status": "❌"})
        
        print()
        
        # ========== CATÉGORIE 5: API BLOG ==========
        print("📝 CATÉGORIE 5: API BLOG (CRUD COMPLET)")
        print("-" * 70)
        
        category = "API Blog"
        results["categories"][category] = {"total": 0, "passed": 0, "tests": []}
        
        # Test 1: Liste articles
        results["total"] += 1
        results["categories"][category]["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/blog/articles")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ GET /api/blog/articles: {len(data)} article(s)")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "GET articles", "status": "✅"})
            else:
                print(f"   ❌ GET /api/blog/articles: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "GET articles", "status": f"❌"})
        except Exception as e:
            print(f"   ❌ GET /api/blog/articles: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "GET articles", "status": "❌"})
        
        # Test 2: Créer article
        results["total"] += 1
        results["categories"][category]["total"] += 1
        article_id = None
        try:
            response = await client.post(
                f"{BASE_URL}/api/blog/articles",
                json={
                    "title": "Article Test Phase 2",
                    "content": "Contenu de test pour Phase 2",
                    "status": "draft"
                }
            )
            if response.status_code in [200, 201]:
                data = response.json()
                article_id = data.get("id")
                print(f"   ✅ POST /api/blog/articles: Article créé (ID: {article_id})")
                results["passed"] += 1
                results["categories"][category]["passed"] += 1
                results["categories"][category]["tests"].append({"test": "POST article", "status": "✅"})
            else:
                print(f"   ❌ POST /api/blog/articles: {response.status_code}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "POST article", "status": f"❌"})
        except Exception as e:
            print(f"   ❌ POST /api/blog/articles: {e}")
            results["failed"] += 1
            results["categories"][category]["tests"].append({"test": "POST article", "status": "❌"})
        
        # Test 3: Modifier article (si créé)
        if article_id:
            results["total"] += 1
            results["categories"][category]["total"] += 1
            try:
                response = await client.put(
                    f"{BASE_URL}/api/blog/articles/{article_id}",
                    json={
                        "title": "Article Test Phase 2 - Modifié",
                        "status": "published"
                    }
                )
                if response.status_code == 200:
                    print(f"   ✅ PUT /api/blog/articles/{article_id}: Modifié")
                    results["passed"] += 1
                    results["categories"][category]["passed"] += 1
                    results["categories"][category]["tests"].append({"test": "PUT article", "status": "✅"})
                else:
                    print(f"   ❌ PUT /api/blog/articles/{article_id}: {response.status_code}")
                    results["failed"] += 1
                    results["categories"][category]["tests"].append({"test": "PUT article", "status": f"❌"})
            except Exception as e:
                print(f"   ❌ PUT /api/blog/articles/{article_id}: {e}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "PUT article", "status": "❌"})
            
            # Test 4: Supprimer article
            results["total"] += 1
            results["categories"][category]["total"] += 1
            try:
                response = await client.delete(f"{BASE_URL}/api/blog/articles/{article_id}")
                if response.status_code in [200, 204]:
                    print(f"   ✅ DELETE /api/blog/articles/{article_id}: Supprimé")
                    results["passed"] += 1
                    results["categories"][category]["passed"] += 1
                    results["categories"][category]["tests"].append({"test": "DELETE article", "status": "✅"})
                else:
                    print(f"   ❌ DELETE /api/blog/articles/{article_id}: {response.status_code}")
                    results["failed"] += 1
                    results["categories"][category]["tests"].append({"test": "DELETE article", "status": f"❌"})
            except Exception as e:
                print(f"   ❌ DELETE /api/blog/articles/{article_id}: {e}")
                results["failed"] += 1
                results["categories"][category]["tests"].append({"test": "DELETE article", "status": "❌"})
        
        print()
    
    return results


async def main():
    results = await test_phase_2_authentifie()
    
    # Résumé global
    print("="*70)
    print("RÉSUMÉ GLOBAL - PHASE 2 AUTHENTIFIÉE")
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
