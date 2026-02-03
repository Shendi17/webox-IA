"""
Script de test de connexion à l'API Cohere
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
import cohere

# Charger les variables d'environnement
load_dotenv()

def test_cohere_connection():
    """Teste la connexion à l'API Cohere"""
    
    api_key = os.getenv('COHERE_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: COHERE_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION COHERE")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client Cohere
        client = cohere.Client(api_key=api_key)
        
        # Liste des modèles Cohere disponibles (selon la documentation)
        print("📋 Modèles Cohere disponibles:\n")
        
        models_by_category = {
            "Command R+ (Dernière génération) 🌟": [
                ("command-r-plus", "Command R+ - Le plus puissant"),
                ("command-r-plus-08-2024", "Command R+ (Août 2024)"),
            ],
            "Command R": [
                ("command-r", "Command R - Équilibré"),
                ("command-r-08-2024", "Command R (Août 2024)"),
            ],
            "Command": [
                ("command", "Command - Standard"),
                ("command-light", "Command Light - Rapide"),
            ],
            "Embed (Embeddings)": [
                ("embed-english-v3.0", "Embed English v3"),
                ("embed-multilingual-v3.0", "Embed Multilingual v3"),
                ("embed-english-light-v3.0", "Embed English Light v3"),
                ("embed-multilingual-light-v3.0", "Embed Multilingual Light v3"),
            ]
        }
        
        for category, model_list in models_by_category.items():
            print(f"\n{category}")
            for model_id, description in model_list:
                print(f"  • {model_id}")
                print(f"    → {description}")
        
        # Test d'appel API
        print("\n" + "="*60)
        print("TEST D'APPEL API")
        print("="*60 + "\n")
        
        print("📤 Envoi d'une requête de test à command-light...")
        
        response = client.chat(
            model="command-light",
            message="Dis bonjour en français en une phrase"
        )
        
        result = response.text
        print(f"\n✅ Réponse reçue: {result}")
        
        # Afficher les informations d'usage si disponibles
        if hasattr(response, 'meta') and response.meta:
            if hasattr(response.meta, 'tokens'):
                print(f"\n📊 Tokens utilisés:")
                if hasattr(response.meta.tokens, 'input_tokens'):
                    print(f"  • Input: {response.meta.tokens.input_tokens}")
                if hasattr(response.meta.tokens, 'output_tokens'):
                    print(f"  • Output: {response.meta.tokens.output_tokens}")
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\n💡 Votre clé API Cohere fonctionne correctement.")
        print("🎯 Modèle recommandé: command-r-plus")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR lors du test:")
        print(f"   {str(e)}")
        print("\n💡 Vérifiez:")
        print("   1. Que votre clé API est correcte")
        print("   2. Que vous avez un compte actif")
        print("   3. Que votre compte n'a pas de restrictions")
        return False

if __name__ == "__main__":
    test_cohere_connection()
