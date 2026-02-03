"""
Script de test de connexion à l'API Groq
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Charger les variables d'environnement
load_dotenv()

def test_groq_connection():
    """Teste la connexion à l'API Groq"""
    
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: GROQ_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION GROQ")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client Groq
        client = Groq(api_key=api_key)
        
        # Lister les modèles disponibles
        print("📋 Récupération de la liste des modèles...")
        models = client.models.list()
        
        print(f"\n✅ {len(models.data)} modèles Groq disponibles:\n")
        
        # Organiser les modèles par catégorie
        models_by_category = {
            "Llama (Meta) 🦙": [],
            "Mixtral (Mistral)": [],
            "Gemma (Google)": [],
            "DeepSeek": [],
            "Qwen": [],
            "Autres": []
        }
        
        for model in models.data:
            model_id = model.id
            if "llama" in model_id.lower():
                models_by_category["Llama (Meta) 🦙"].append(model_id)
            elif "mixtral" in model_id.lower():
                models_by_category["Mixtral (Mistral)"].append(model_id)
            elif "gemma" in model_id.lower():
                models_by_category["Gemma (Google)"].append(model_id)
            elif "deepseek" in model_id.lower():
                models_by_category["DeepSeek"].append(model_id)
            elif "qwen" in model_id.lower():
                models_by_category["Qwen"].append(model_id)
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
        
        # Utiliser llama-3.3-70b-versatile ou le premier modèle disponible
        test_model = "llama-3.3-70b-versatile"
        if models.data:
            # Chercher llama-3.3
            llama_models = [m for m in models.data if "llama-3.3" in m.id.lower()]
            if llama_models:
                test_model = llama_models[0].id
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
        print("\n💡 Votre clé API Groq fonctionne correctement.")
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
    test_groq_connection()
