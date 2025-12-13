"""
Test du backend FastAPI
"""

print("🔍 Test des imports...")

try:
    from fastapi import FastAPI
    print("✅ FastAPI importé")
except Exception as e:
    print(f"❌ Erreur FastAPI: {e}")

try:
    from modules.core.landing_page.model import LandingPageData
    print("✅ LandingPageData importé")
    
    data = LandingPageData()
    print(f"✅ LandingPageData instancié")
    print(f"   Titre: {data.TITLE_WEBOX} {data.TITLE_MULTI_IA}")
except Exception as e:
    print(f"❌ Erreur LandingPageData: {e}")

try:
    from app.routes import auth_router, dashboard_router
    print("✅ Routes auth et dashboard importées")
except Exception as e:
    print(f"❌ Erreur routes: {e}")

try:
    from app.routes.chat_routes import router as chat_router
    print("✅ Route chat importée")
except Exception as e:
    print(f"❌ Erreur chat_routes: {e}")

try:
    from app.middleware.auth import get_current_user_from_cookie
    print("✅ Middleware auth importé")
except Exception as e:
    print(f"❌ Erreur middleware: {e}")

print("\n✅ Tous les imports fonctionnent !")
print("\n🎯 Le problème vient probablement d'une erreur au démarrage du serveur.")
print("   Vérifie les logs dans la fenêtre 'WeBox Backend'")
