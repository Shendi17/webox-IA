"""
Test Authentification et Profil - Phase 2
Date: 25 Janvier 2026
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_authentification_profil():
    """Tester authentification et fonctionnalités profil"""
    
    print("\n" + "="*70)
    print("TEST AUTHENTIFICATION & PROFIL - PHASE 2")
    print("="*70 + "\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "tests": []
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        
        # ========== TEST 1: INSCRIPTION ==========
        print("📝 TEST 1: Inscription utilisateur")
        results["total"] += 1
        try:
            response = await client.post(
                f"{BASE_URL}/register",
                data={
                    "email": f"test_phase2_{os.urandom(4).hex()}@webox.com",
                    "username": f"testuser_{os.urandom(4).hex()}",
                    "password": "TestPassword123!",
                    "name": "Test Phase 2"
                }
            )
            
            if response.status_code in [200, 201]:
                print("   ✅ Inscription réussie")
                results["passed"] += 1
                results["tests"].append({"test": "Inscription", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Inscription", "status": f"⚠️ FAIL ({response.status_code})"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Inscription", "status": f"❌ ERROR"})
        
        print()
        
        # ========== TEST 2: CONNEXION ==========
        print("🔐 TEST 2: Connexion utilisateur")
        results["total"] += 1
        
        # Utiliser compte admin existant
        try:
            response = await client.post(
                f"{BASE_URL}/api/auth/login",
                data={
                    "email": os.getenv("ADMIN_EMAIL", "admin@webox.com"),
                    "password": os.getenv("ADMIN_PASSWORD", "admin123")
                }
            )
            
            if response.status_code == 200:
                print("   ✅ Connexion réussie")
                results["passed"] += 1
                results["tests"].append({"test": "Connexion", "status": "✅ PASS"})
                
                # Récupérer les cookies
                cookies = client.cookies
                print(f"   📋 Cookies: {len(cookies)} cookie(s)")
                
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Connexion", "status": f"⚠️ FAIL ({response.status_code})"})
                return results
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Connexion", "status": f"❌ ERROR"})
            return results
        
        print()
        
        # ========== TEST 3: RÉCUPÉRATION PROFIL ==========
        print("👤 TEST 3: Récupération profil")
        results["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/profile/me")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Profil récupéré")
                print(f"   📧 Email: {data.get('email', 'N/A')}")
                print(f"   👤 Nom: {data.get('name', 'N/A')}")
                print(f"   🔑 Admin: {data.get('is_admin', False)}")
                results["passed"] += 1
                results["tests"].append({"test": "Récupération profil", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Récupération profil", "status": f"⚠️ FAIL"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Récupération profil", "status": f"❌ ERROR"})
        
        print()
        
        # ========== TEST 4: MODIFICATION PROFIL ==========
        print("✏️ TEST 4: Modification profil")
        results["total"] += 1
        try:
            response = await client.put(
                f"{BASE_URL}/api/profile/update",
                json={
                    "name": "Admin WeBox Updated"
                }
            )
            
            if response.status_code == 200:
                print("   ✅ Profil modifié")
                results["passed"] += 1
                results["tests"].append({"test": "Modification profil", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Modification profil", "status": f"⚠️ FAIL"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Modification profil", "status": f"❌ ERROR"})
        
        print()
        
        # ========== TEST 5: GESTION CLÉS API ==========
        print("🔑 TEST 5: Ajout clé API")
        results["total"] += 1
        try:
            response = await client.post(
                f"{BASE_URL}/api/profile/api-keys",
                json={
                    "service": "test_service",
                    "api_key": "test_key_12345"
                }
            )
            
            if response.status_code in [200, 201]:
                print("   ✅ Clé API ajoutée")
                results["passed"] += 1
                results["tests"].append({"test": "Ajout clé API", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Ajout clé API", "status": f"⚠️ FAIL"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Ajout clé API", "status": f"❌ ERROR"})
        
        print()
        
        # ========== TEST 6: PRÉFÉRENCES ==========
        print("⚙️ TEST 6: Modification préférences")
        results["total"] += 1
        try:
            response = await client.put(
                f"{BASE_URL}/api/profile/preferences",
                json={
                    "theme": "dark",
                    "language": "fr"
                }
            )
            
            if response.status_code == 200:
                print("   ✅ Préférences modifiées")
                results["passed"] += 1
                results["tests"].append({"test": "Modification préférences", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Modification préférences", "status": f"⚠️ FAIL"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Modification préférences", "status": f"❌ ERROR"})
        
        print()
        
        # ========== TEST 7: STATISTIQUES ==========
        print("📊 TEST 7: Statistiques utilisateur")
        results["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/api/profile/stats")
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Statistiques récupérées")
                print(f"   📈 Données: {len(data)} entrée(s)")
                results["passed"] += 1
                results["tests"].append({"test": "Statistiques", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Statistiques", "status": f"⚠️ FAIL"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Statistiques", "status": f"❌ ERROR"})
        
        print()
        
        # ========== TEST 8: DÉCONNEXION ==========
        print("🚪 TEST 8: Déconnexion")
        results["total"] += 1
        try:
            response = await client.get(f"{BASE_URL}/logout")
            
            if response.status_code in [200, 302]:
                print("   ✅ Déconnexion réussie")
                results["passed"] += 1
                results["tests"].append({"test": "Déconnexion", "status": "✅ PASS"})
            else:
                print(f"   ⚠️ Statut: {response.status_code}")
                results["failed"] += 1
                results["tests"].append({"test": "Déconnexion", "status": f"⚠️ FAIL"})
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            results["failed"] += 1
            results["tests"].append({"test": "Déconnexion", "status": f"❌ ERROR"})
    
    return results


async def main():
    results = await test_authentification_profil()
    
    # Résumé
    print("\n" + "="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)
    print(f"\n📊 Total: {results['total']}")
    print(f"✅ Réussis: {results['passed']}")
    print(f"❌ Échoués: {results['failed']}")
    print(f"📈 Taux de réussite: {(results['passed']/results['total']*100):.1f}%")
    
    print("\n📋 Détail:")
    for test in results["tests"]:
        print(f"   {test['status']} - {test['test']}")
    
    print("\n" + "="*70)
    print()


if __name__ == "__main__":
    asyncio.run(main())
