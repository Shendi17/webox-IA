"""
Script de test de connexion à l'API Perplexity
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement
load_dotenv()

def test_perplexity_connection():
    """Teste la connexion à l'API Perplexity"""
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: PERPLEXITY_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION PERPLEXITY")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client Perplexity (compatible OpenAI)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Liste des modèles Perplexity disponibles (selon la documentation)
        print("📋 Modèles Perplexity disponibles:\n")
        
        models_by_category = {
            "Sonar (Recherche en ligne) 🔍": [
                ("sonar", "Sonar - Recherche en ligne standard"),
                ("sonar-pro", "Sonar Pro - Recherche avancée"),
                ("sonar-reasoning", "Sonar Reasoning - Raisonnement avec recherche"),
            ],
            "Llama (Sans recherche)": [
                ("llama-3.1-sonar-small-128k-online", "Llama 3.1 Sonar Small - En ligne"),
                ("llama-3.1-sonar-large-128k-online", "Llama 3.1 Sonar Large - En ligne"),
                ("llama-3.1-sonar-huge-128k-online", "Llama 3.1 Sonar Huge - En ligne"),
                ("llama-3.1-8b-instruct", "Llama 3.1 8B Instruct"),
                ("llama-3.1-70b-instruct", "Llama 3.1 70B Instruct"),
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
        
        # Utiliser sonar comme modèle de test
        test_model = "sonar"
        
        print(f"📤 Envoi d'une requête de test à {test_model}...")
        
        response = client.chat.completions.create(
            model=test_model,
            messages=[
                {"role": "user", "content": "Dis bonjour en français en une phrase"}
            ],
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f"\n✅ Réponse reçue: {result}")
        
        # Afficher les informations d'usage
        if hasattr(response, 'usage') and response.usage:
            print(f"\n📊 Tokens utilisés:")
            print(f"  • Prompt: {response.usage.prompt_tokens}")
            print(f"  • Completion: {response.usage.completion_tokens}")
            print(f"  • Total: {response.usage.total_tokens}")
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\n💡 Votre clé API Perplexity fonctionne correctement.")
        print(f"🎯 Modèle recommandé: {test_model}")
        
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
    test_perplexity_connection()
