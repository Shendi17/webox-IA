"""
Test des routes Email Campaigns après migration
Date: 3 Février 2026
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_email_campaigns():
    """Test complet des routes email campaigns"""
    print("=" * 60)
    print("TEST DES ROUTES EMAIL CAMPAIGNS")
    print("=" * 60)
    
    # 1. Login pour obtenir un token
    print("\n1️⃣ Connexion...")
    login_data = {
        "username": "admin@webox.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Connexion réussie - Token obtenu")
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Créer une campagne email
    print("\n2️⃣ Création d'une campagne email...")
    campaign_data = {
        "name": "Test Campaign Migration",
        "subject": "Test après migration des doublons",
        "preview_text": "Ceci est un test",
        "content_html": "<h1>Test Email</h1><p>Contenu de test après migration</p>",
        "recipients": ["test@example.com", "test2@example.com"],
        "scheduled_time": None
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/email-campaigns/create",
            json=campaign_data,
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            campaign_id = result.get("campaign_id")
            print(f"✅ Campagne créée avec succès")
            print(f"   ID: {campaign_id}")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Erreur création: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur création: {str(e)}")
        return
    
    # 3. Lister les campagnes
    print("\n3️⃣ Liste des campagnes...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/email-campaigns/list",
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            campaigns = result.get("campaigns", [])
            print(f"✅ Liste récupérée: {len(campaigns)} campagne(s)")
            for camp in campaigns[:3]:
                print(f"   - {camp.get('name')} (ID: {camp.get('id')})")
        else:
            print(f"❌ Erreur liste: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur liste: {str(e)}")
    
    # 4. Envoyer la campagne
    print("\n4️⃣ Envoi de la campagne...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/email-campaigns/{campaign_id}/send",
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Envoi lancé")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Erreur envoi: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur envoi: {str(e)}")
    
    # 5. Supprimer la campagne
    print("\n5️⃣ Suppression de la campagne de test...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/email-campaigns/{campaign_id}",
            headers=headers
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Campagne supprimée")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"❌ Erreur suppression: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur suppression: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️  Assurez-vous que le serveur est démarré sur http://localhost:8000\n")
    test_email_campaigns()
