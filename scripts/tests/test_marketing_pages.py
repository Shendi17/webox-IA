"""
Script de test des pages Marketing
"""
import requests

BASE_URL = "http://localhost:8000"

pages = [
    "/marketing-dashboard",
    "/crm",
    "/email-marketing",
    "/funnels"
]

print("🧪 TEST DES PAGES MARKETING\n")
print("=" * 50)

for page in pages:
    url = f"{BASE_URL}{page}"
    try:
        response = requests.get(url, allow_redirects=False)
        
        if response.status_code == 200:
            print(f"✅ {page:25} - OK (200)")
        elif response.status_code == 302:
            print(f"⚠️  {page:25} - Redirect (302) - Auth requise")
        else:
            print(f"❌ {page:25} - Erreur ({response.status_code})")
    except Exception as e:
        print(f"❌ {page:25} - Exception: {str(e)}")

print("=" * 50)
print("\n✅ Test terminé !")
