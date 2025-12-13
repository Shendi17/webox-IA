"""
Script de test des API Marketing
"""
import requests

BASE_URL = "http://localhost:8000"

# Test des endpoints API (sans auth pour voir les erreurs)
endpoints = [
    ("GET", "/api/marketing/funnels"),
    ("GET", "/api/marketing/campaigns"),
    ("GET", "/api/marketing/leads"),
    ("GET", "/api/marketing/pipeline/stats"),
]

print("🧪 TEST DES API MARKETING\n")
print("=" * 60)

for method, endpoint in endpoints:
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        
        status = response.status_code
        
        if status == 200:
            print(f"✅ {method:4} {endpoint:35} - OK (200)")
        elif status == 401:
            print(f"🔒 {method:4} {endpoint:35} - Auth requise (401)")
        elif status == 422:
            print(f"⚠️  {method:4} {endpoint:35} - Validation (422)")
        else:
            print(f"❌ {method:4} {endpoint:35} - Erreur ({status})")
            
    except Exception as e:
        print(f"❌ {method:4} {endpoint:35} - Exception: {str(e)[:30]}")

print("=" * 60)
print("\n✅ Test terminé !")
