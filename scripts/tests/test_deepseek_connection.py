"""
Script de test de connexion à l'API DeepSeek
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement
load_dotenv()

def test_deepseek_connection():
    """Teste la connexion à l'API DeepSeek"""
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: DEEPSEEK_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION DEEPSEEK")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client DeepSeek (compatible OpenAI)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        # Lister les modèles disponibles
        print("📋 Récupération de la liste des modèles...")
        models = client.models.list()
        
        print(f"\n✅ {len(models.data)} modèles DeepSeek disponibles:\n")
        
        # Organiser les modèles par catégorie
        models_by_category = {
            "DeepSeek Chat": [],
            "DeepSeek Coder": [],
            "DeepSeek Reasoner": [],
            "Autres": []
        }
        
        for model in models.data:
            model_id = model.id
            if "chat" in model_id.lower():
                models_by_category["DeepSeek Chat"].append(model_id)
            elif "coder" in model_id.lower():
                models_by_category["DeepSeek Coder"].append(model_id)
            elif "reasoner" in model_id.lower() or "r1" in model_id.lower():
                models_by_category["DeepSeek Reasoner"].append(model_id)
            else:
                models_by_category["Autres"].append(model_id)
        
        for category, model_list in models_by_category.items():
            if model_list:
                print(f"\n{category}")
                for model_id in sorted(model_list):
                    print(f"  • {model_id}")
        
        # Test d'appel API
        print("\n" + "="*60)
        print("TEST D'APPEL API")
        print("="*60 + "\n")
        
        # Utiliser le premier modèle disponible ou deepseek-chat
        test_model = "deepseek-chat"
        if models.data:
            # Chercher deepseek-chat
            chat_models = [m for m in models.data if "chat" in m.id.lower()]
            if chat_models:
                test_model = chat_models[0].id
            else:
                test_model = models.data[0].id
        
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
        print("\n💡 Votre clé API DeepSeek fonctionne correctement.")
        print(f"🎯 Modèle recommandé: {test_model}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR lors du test:")
        print(f"   {str(e)}")
        print("\n💡 Vérifiez:")
        print("   1. Que votre clé API est correcte")
        print("   2. Que vous avez des crédits disponibles")
        print("   3. Que votre compte n'a pas de restrictions")
        return False

if __name__ == "__main__":
    test_deepseek_connection()
