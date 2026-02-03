"""
Script de test de connexion à l'API Anthropic (Claude)
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Charger les variables d'environnement
load_dotenv()

def test_anthropic_connection():
    """Teste la connexion à l'API Anthropic"""
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: ANTHROPIC_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION ANTHROPIC (CLAUDE)")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client Anthropic
        client = Anthropic(api_key=api_key)
        
        print("📋 Modèles Claude disponibles:\n")
        
        models_by_version = {
            "Claude 3.5 (Dernière génération) 🌟": [
                ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet (Oct 2024) - Le plus puissant"),
                ("claude-3-5-sonnet-20240620", "Claude 3.5 Sonnet (Jun 2024)"),
                ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku (Oct 2024) - Rapide"),
            ],
            "Claude 3": [
                ("claude-3-opus-20240229", "Claude 3 Opus - Ultra puissant"),
                ("claude-3-sonnet-20240229", "Claude 3 Sonnet - Équilibré"),
                ("claude-3-haiku-20240307", "Claude 3 Haiku - Rapide"),
            ],
            "Claude 2": [
                ("claude-2.1", "Claude 2.1"),
                ("claude-2.0", "Claude 2.0"),
            ],
            "Claude Instant": [
                ("claude-instant-1.2", "Claude Instant 1.2 - Économique"),
            ]
        }
        
        for version, models in models_by_version.items():
            print(f"\n{version}")
            for model_id, description in models:
                print(f"  • {model_id}")
                print(f"    → {description}")
        
        # Test d'appel API avec claude-3-5-sonnet-20240620
        print("\n" + "="*60)
        print("TEST D'APPEL API")
        print("="*60 + "\n")
        
        print("📤 Envoi d'une requête de test à claude-3-5-sonnet-20240620...")
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Dis bonjour en français en une phrase"}
            ]
        )
        
        result = message.content[0].text
        print(f"\n✅ Réponse reçue: {result}")
        
        # Afficher les informations d'usage
        print(f"\n📊 Tokens utilisés:")
        print(f"  • Input: {message.usage.input_tokens}")
        print(f"  • Output: {message.usage.output_tokens}")
        print(f"  • Total: {message.usage.input_tokens + message.usage.output_tokens}")
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\n💡 Votre clé API Anthropic fonctionne correctement.")
        print("🎯 Modèle recommandé: claude-3-5-sonnet-20240620")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR lors du test:")
        print(f"   {str(e)}")
        print("\n💡 Vérifiez:")
        print("   1. Que votre clé API est correcte")
        print("   2. Que vous avez activé la facturation sur Anthropic")
        print("   3. Que votre compte n'a pas de restrictions")
        return False

if __name__ == "__main__":
    test_anthropic_connection()
