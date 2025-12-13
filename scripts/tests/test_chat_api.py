"""
Test de l'API Chat
"""

import requests

# URL de base
BASE_URL = "http://webox.local:8000"

# Se connecter d'abord
login_data = {
    "email": "admin@webox.com",
    "password": "admin123"
}

session = requests.Session()
response = session.post(f"{BASE_URL}/login", data=login_data)
print(f"Login status: {response.status_code}")
print(f"Cookies: {session.cookies}")

# Tester l'envoi d'un message
chat_data = {
    "message": "Bonjour, test",
    "selected_providers": ["GPT-4"],
    "selected_models": {"GPT-4": "gpt-4"},
    "temperature": 0.7,
    "max_tokens": 1000
}

response = session.post(f"{BASE_URL}/api/chat/send", json=chat_data)
print(f"\nChat API status: {response.status_code}")
print(f"Response: {response.text}")
