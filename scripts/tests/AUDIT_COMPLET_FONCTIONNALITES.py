"""
AUDIT COMPLET DES FONCTIONNALITÉS WEBOX
Script de test automatisé pour vérifier toutes les fonctionnalités du projet
Date: 24 Janvier 2026
"""

import httpx
import asyncio
import json
from typing import Dict, List, Tuple
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "test@webox.com",
    "password": "test123456"
}

class WeBoxAudit:
    def __init__(self):
        self.results = {
            "authentification": {},
            "profil": {},
            "generation_ia": {},
            "marketplace": {},
            "paiement": {},
            "admin": {},
            "blog": {},
            "autres": {}
        }
        self.token = None
        self.client = None
        
    async def setup(self):
        """Initialiser le client HTTP"""
        self.client = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)
        
    async def cleanup(self):
        """Nettoyer les ressources"""
        if self.client:
            await self.client.aclose()
    
    def log_test(self, category: str, test_name: str, status: str, details: str = ""):
        """Enregistrer le résultat d'un test"""
        self.results[category][test_name] = {
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        status_icon = "✅" if status == "OK" else "❌" if status == "ERREUR" else "⚠️"
        print(f"{status_icon} [{category}] {test_name}: {status} {details}")
    
    # ==========================================
    # TESTS AUTHENTIFICATION
    # ==========================================
    
    async def test_auth_register(self):
        """Test: Inscription d'un nouvel utilisateur"""
        try:
            response = await self.client.post("/api/auth/register", json={
                "email": f"test_{datetime.now().timestamp()}@webox.com",
                "username": f"testuser_{int(datetime.now().timestamp())}",
                "password": "Test123456!"
            })
            
            if response.status_code in [200, 201]:
                self.log_test("authentification", "Inscription", "OK", "Utilisateur créé")
            else:
                self.log_test("authentification", "Inscription", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("authentification", "Inscription", "ERREUR", str(e))
    
    async def test_auth_login(self):
        """Test: Connexion utilisateur"""
        try:
            response = await self.client.post("/api/auth/login", json=TEST_USER)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.token = data["access_token"]
                    self.log_test("authentification", "Connexion", "OK", "Token obtenu")
                else:
                    self.log_test("authentification", "Connexion", "PARTIEL", "Pas de token")
            else:
                self.log_test("authentification", "Connexion", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("authentification", "Connexion", "ERREUR", str(e))
    
    async def test_auth_logout(self):
        """Test: Déconnexion utilisateur"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/auth/logout", headers=headers)
            
            if response.status_code in [200, 204]:
                self.log_test("authentification", "Déconnexion", "OK")
            else:
                self.log_test("authentification", "Déconnexion", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("authentification", "Déconnexion", "ERREUR", str(e))
    
    # ==========================================
    # TESTS PROFIL UTILISATEUR
    # ==========================================
    
    async def test_profile_get(self):
        """Test: Récupération du profil"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.get("/api/profile/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "user" in data:
                    self.log_test("profil", "Récupération profil", "OK", f"Email: {data['user'].get('email')}")
                else:
                    self.log_test("profil", "Récupération profil", "PARTIEL", "Structure incorrecte")
            else:
                self.log_test("profil", "Récupération profil", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("profil", "Récupération profil", "ERREUR", str(e))
    
    async def test_profile_update(self):
        """Test: Modification du profil"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.put("/api/profile/update", 
                headers=headers,
                json={"name": "Test User Updated"}
            )
            
            if response.status_code == 200:
                self.log_test("profil", "Modification profil", "OK")
            else:
                self.log_test("profil", "Modification profil", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("profil", "Modification profil", "ERREUR", str(e))
    
    async def test_profile_api_keys(self):
        """Test: Gestion des clés API"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.put("/api/profile/api-keys",
                headers=headers,
                json={"openai_key": "sk-test123"}
            )
            
            if response.status_code == 200:
                self.log_test("profil", "Clés API", "OK")
            else:
                self.log_test("profil", "Clés API", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("profil", "Clés API", "ERREUR", str(e))
    
    # ==========================================
    # TESTS GÉNÉRATION IA
    # ==========================================
    
    async def test_generation_image(self):
        """Test: Génération d'image"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/generation/image",
                headers=headers,
                json={
                    "prompt": "Un chat mignon",
                    "model": "dall-e-3",
                    "size": "1024x1024"
                }
            )
            
            if response.status_code in [200, 201]:
                self.log_test("generation_ia", "Génération image", "OK")
            else:
                self.log_test("generation_ia", "Génération image", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("generation_ia", "Génération image", "ERREUR", str(e))
    
    async def test_generation_video(self):
        """Test: Génération de vidéo"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/generation/video",
                headers=headers,
                json={
                    "prompt": "Une belle animation",
                    "model": "runway",
                    "duration": 5
                }
            )
            
            if response.status_code in [200, 201]:
                self.log_test("generation_ia", "Génération vidéo", "OK")
            else:
                self.log_test("generation_ia", "Génération vidéo", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("generation_ia", "Génération vidéo", "ERREUR", str(e))
    
    async def test_generation_audio(self):
        """Test: Génération audio"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/generation/audio",
                headers=headers,
                json={
                    "prompt": "Bonjour, ceci est un test",
                    "model": "elevenlabs",
                    "audio_type": "speech"
                }
            )
            
            if response.status_code in [200, 201]:
                self.log_test("generation_ia", "Génération audio", "OK")
            else:
                self.log_test("generation_ia", "Génération audio", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("generation_ia", "Génération audio", "ERREUR", str(e))
    
    async def test_generation_text(self):
        """Test: Chat IA (génération texte)"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/chat/send",
                headers=headers,
                json={
                    "message": "Bonjour, comment vas-tu?",
                    "ai_model": "gpt-4"
                }
            )
            
            if response.status_code in [200, 201]:
                self.log_test("generation_ia", "Chat IA (texte)", "OK")
            else:
                self.log_test("generation_ia", "Chat IA (texte)", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("generation_ia", "Chat IA (texte)", "ERREUR", str(e))
    
    # ==========================================
    # TESTS MARKETPLACE & PANIER
    # ==========================================
    
    async def test_marketplace_list(self):
        """Test: Affichage marketplace"""
        try:
            response = await self.client.get("/marketplace")
            
            if response.status_code == 200:
                self.log_test("marketplace", "Affichage marketplace", "OK")
            else:
                self.log_test("marketplace", "Affichage marketplace", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("marketplace", "Affichage marketplace", "ERREUR", str(e))
    
    async def test_product_detail(self):
        """Test: Détail produit"""
        try:
            response = await self.client.get("/product/test-product-1")
            
            if response.status_code == 200:
                self.log_test("marketplace", "Détail produit", "OK")
            else:
                self.log_test("marketplace", "Détail produit", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("marketplace", "Détail produit", "ERREUR", str(e))
    
    async def test_cart_view(self):
        """Test: Affichage panier"""
        try:
            response = await self.client.get("/cart")
            
            if response.status_code == 200:
                self.log_test("marketplace", "Affichage panier", "OK")
            else:
                self.log_test("marketplace", "Affichage panier", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("marketplace", "Affichage panier", "ERREUR", str(e))
    
    async def test_cart_add(self):
        """Test: Ajout au panier"""
        try:
            # Note: Cette route n'existe peut-être pas encore
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/cart/add",
                headers=headers,
                json={"product_id": "test-product-1", "quantity": 1}
            )
            
            if response.status_code in [200, 201, 404]:
                status = "OK" if response.status_code in [200, 201] else "NON_IMPLÉMENTÉ"
                self.log_test("marketplace", "Ajout panier", status)
            else:
                self.log_test("marketplace", "Ajout panier", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("marketplace", "Ajout panier", "NON_IMPLÉMENTÉ", str(e))
    
    # ==========================================
    # TESTS PAIEMENT & CHECKOUT
    # ==========================================
    
    async def test_checkout_page(self):
        """Test: Page checkout"""
        try:
            response = await self.client.get("/checkout")
            
            if response.status_code == 200:
                self.log_test("paiement", "Page checkout", "OK")
            else:
                self.log_test("paiement", "Page checkout", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("paiement", "Page checkout", "ERREUR", str(e))
    
    async def test_payment_stripe(self):
        """Test: Création intention paiement Stripe"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/payment/stripe/create-intent",
                headers=headers,
                json={"amount": 49.99, "currency": "eur"}
            )
            
            if response.status_code in [200, 201]:
                self.log_test("paiement", "Stripe - Intention paiement", "OK")
            elif response.status_code == 400:
                self.log_test("paiement", "Stripe - Intention paiement", "NON_CONFIGURÉ", "Clé API manquante")
            else:
                self.log_test("paiement", "Stripe - Intention paiement", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("paiement", "Stripe - Intention paiement", "ERREUR", str(e))
    
    async def test_payment_paypal(self):
        """Test: Création commande PayPal"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/payment/paypal/create-order",
                headers=headers,
                json={"amount": 49.99, "currency": "EUR"}
            )
            
            if response.status_code in [200, 201]:
                self.log_test("paiement", "PayPal - Création commande", "OK")
            elif response.status_code == 400:
                self.log_test("paiement", "PayPal - Création commande", "NON_CONFIGURÉ", "Clé API manquante")
            else:
                self.log_test("paiement", "PayPal - Création commande", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("paiement", "PayPal - Création commande", "ERREUR", str(e))
    
    # ==========================================
    # TESTS ADMIN
    # ==========================================
    
    async def test_admin_dashboard(self):
        """Test: Dashboard admin"""
        try:
            response = await self.client.get("/admin/dashboard")
            
            if response.status_code == 200:
                self.log_test("admin", "Dashboard admin", "OK")
            elif response.status_code == 403:
                self.log_test("admin", "Dashboard admin", "ACCÈS_REFUSÉ", "Droits admin requis")
            else:
                self.log_test("admin", "Dashboard admin", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("admin", "Dashboard admin", "ERREUR", str(e))
    
    async def test_admin_analytics(self):
        """Test: Analytics admin"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.get("/api/admin/analytics", headers=headers)
            
            if response.status_code == 200:
                self.log_test("admin", "Analytics", "OK")
            elif response.status_code in [401, 403]:
                self.log_test("admin", "Analytics", "ACCÈS_REFUSÉ", "Droits admin requis")
            else:
                self.log_test("admin", "Analytics", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("admin", "Analytics", "ERREUR", str(e))
    
    # ==========================================
    # TESTS BLOG & CONTENU
    # ==========================================
    
    async def test_blog_list(self):
        """Test: Liste des articles"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.get("/api/blog/articles", headers=headers)
            
            if response.status_code == 200:
                self.log_test("blog", "Liste articles", "OK")
            else:
                self.log_test("blog", "Liste articles", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("blog", "Liste articles", "ERREUR", str(e))
    
    async def test_blog_create(self):
        """Test: Création article"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            response = await self.client.post("/api/blog/articles",
                headers=headers,
                json={
                    "title": "Article de test",
                    "content": "Contenu de test",
                    "status": "draft"
                }
            )
            
            if response.status_code in [200, 201]:
                self.log_test("blog", "Création article", "OK")
            else:
                self.log_test("blog", "Création article", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("blog", "Création article", "ERREUR", str(e))
    
    # ==========================================
    # TESTS AUTRES FONCTIONNALITÉS
    # ==========================================
    
    async def test_notifications(self):
        """Test: Notifications"""
        try:
            response = await self.client.get("/notifications")
            
            if response.status_code == 200:
                self.log_test("autres", "Page notifications", "OK")
            else:
                self.log_test("autres", "Page notifications", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("autres", "Page notifications", "ERREUR", str(e))
    
    async def test_settings(self):
        """Test: Paramètres"""
        try:
            response = await self.client.get("/settings")
            
            if response.status_code == 200:
                self.log_test("autres", "Page paramètres", "OK")
            else:
                self.log_test("autres", "Page paramètres", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("autres", "Page paramètres", "ERREUR", str(e))
    
    async def test_support(self):
        """Test: Support"""
        try:
            response = await self.client.get("/support")
            
            if response.status_code == 200:
                self.log_test("autres", "Page support", "OK")
            else:
                self.log_test("autres", "Page support", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("autres", "Page support", "ERREUR", str(e))
    
    async def test_dashboard(self):
        """Test: Dashboard principal"""
        try:
            response = await self.client.get("/dashboard")
            
            if response.status_code == 200:
                self.log_test("autres", "Dashboard principal", "OK")
            else:
                self.log_test("autres", "Dashboard principal", "ERREUR", f"Status {response.status_code}")
        except Exception as e:
            self.log_test("autres", "Dashboard principal", "ERREUR", str(e))
    
    # ==========================================
    # EXÉCUTION DES TESTS
    # ==========================================
    
    async def run_all_tests(self):
        """Exécuter tous les tests"""
        print("\n" + "="*80)
        print("🚀 AUDIT COMPLET DES FONCTIONNALITÉS WEBOX")
        print("="*80 + "\n")
        
        await self.setup()
        
        # Tests Authentification
        print("\n📋 TESTS AUTHENTIFICATION")
        print("-" * 80)
        await self.test_auth_register()
        await self.test_auth_login()
        
        # Tests Profil (nécessite authentification)
        print("\n👤 TESTS PROFIL UTILISATEUR")
        print("-" * 80)
        await self.test_profile_get()
        await self.test_profile_update()
        await self.test_profile_api_keys()
        
        # Tests Génération IA
        print("\n🤖 TESTS GÉNÉRATION IA")
        print("-" * 80)
        await self.test_generation_text()
        await self.test_generation_image()
        await self.test_generation_video()
        await self.test_generation_audio()
        
        # Tests Marketplace
        print("\n🛒 TESTS MARKETPLACE & PANIER")
        print("-" * 80)
        await self.test_marketplace_list()
        await self.test_product_detail()
        await self.test_cart_view()
        await self.test_cart_add()
        
        # Tests Paiement
        print("\n💳 TESTS PAIEMENT & CHECKOUT")
        print("-" * 80)
        await self.test_checkout_page()
        await self.test_payment_stripe()
        await self.test_payment_paypal()
        
        # Tests Admin
        print("\n👨‍💼 TESTS ADMINISTRATION")
        print("-" * 80)
        await self.test_admin_dashboard()
        await self.test_admin_analytics()
        
        # Tests Blog
        print("\n📝 TESTS BLOG & CONTENU")
        print("-" * 80)
        await self.test_blog_list()
        await self.test_blog_create()
        
        # Tests Autres
        print("\n⚙️ TESTS AUTRES FONCTIONNALITÉS")
        print("-" * 80)
        await self.test_dashboard()
        await self.test_notifications()
        await self.test_settings()
        await self.test_support()
        
        # Déconnexion
        await self.test_auth_logout()
        
        await self.cleanup()
        
        # Afficher le résumé
        self.print_summary()
    
    def print_summary(self):
        """Afficher le résumé des tests"""
        print("\n" + "="*80)
        print("📊 RÉSUMÉ DE L'AUDIT")
        print("="*80 + "\n")
        
        total_tests = 0
        tests_ok = 0
        tests_erreur = 0
        tests_non_impl = 0
        tests_autres = 0
        
        for category, tests in self.results.items():
            if not tests:
                continue
                
            print(f"\n{category.upper().replace('_', ' ')}")
            print("-" * 80)
            
            for test_name, result in tests.items():
                status = result["status"]
                total_tests += 1
                
                if status == "OK":
                    tests_ok += 1
                    icon = "✅"
                elif status == "ERREUR":
                    tests_erreur += 1
                    icon = "❌"
                elif status in ["NON_IMPLÉMENTÉ", "NON_CONFIGURÉ"]:
                    tests_non_impl += 1
                    icon = "⚠️"
                else:
                    tests_autres += 1
                    icon = "ℹ️"
                
                print(f"{icon} {test_name}: {status}")
                if result["details"]:
                    print(f"   → {result['details']}")
        
        # Statistiques globales
        print("\n" + "="*80)
        print("📈 STATISTIQUES GLOBALES")
        print("="*80)
        print(f"Total de tests: {total_tests}")
        print(f"✅ Tests réussis: {tests_ok} ({tests_ok/total_tests*100:.1f}%)")
        print(f"❌ Tests en erreur: {tests_erreur} ({tests_erreur/total_tests*100:.1f}%)")
        print(f"⚠️ Non implémentés/configurés: {tests_non_impl} ({tests_non_impl/total_tests*100:.1f}%)")
        print(f"ℹ️ Autres: {tests_autres}")
        
        # Sauvegarder les résultats
        self.save_results()
    
    def save_results(self):
        """Sauvegarder les résultats dans un fichier JSON"""
        filename = f"audit_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Résultats sauvegardés dans: {filename}")


async def main():
    """Point d'entrée principal"""
    audit = WeBoxAudit()
    await audit.run_all_tests()


if __name__ == "__main__":
    print("\n🔍 Démarrage de l'audit complet des fonctionnalités WeBox...")
    print("⚠️ Assurez-vous que le serveur est lancé sur http://localhost:8000\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Audit interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur lors de l'audit: {str(e)}")
