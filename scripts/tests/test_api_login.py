import requests
import json

# Test de la route de connexion
url = "http://localhost:8000/login"

# Données du formulaire
data = {
    "email": "admin@webox.com",
    "password": "admin123",
    "remember_me": "false"
}

print("🧪 Test de connexion API...")
print(f"URL: {url}")
print(f"Données: {data}")
print("-" * 50)

try:
    # Envoyer la requête POST
    response = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"\n📊 Statut HTTP: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    # Afficher la réponse
    if response.status_code == 200:
        print("\n✅ Réponse JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
        # Vérifier le cookie
        if 'set-cookie' in response.headers:
            print(f"\n🍪 Cookie défini: {response.headers['set-cookie']}")
        else:
            print("\n⚠️ Aucun cookie défini")
    else:
        print(f"\n❌ Erreur {response.status_code}")
        print("Réponse:", response.text)
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERREUR: Impossible de se connecter au serveur")
    print("Vérifie que le serveur est démarré sur http://localhost:8000")
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    print(f"Type: {type(e)}")
