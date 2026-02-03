"""
Script de test de connexion à l'API Mistral
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
from mistralai import Mistral

# Charger les variables d'environnement
load_dotenv()

def test_mistral_connection():
    """Teste la connexion à l'API Mistral"""
    
    api_key = os.getenv('MISTRAL_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: MISTRAL_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION MISTRAL")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client Mistral
        client = Mistral(api_key=api_key)
        
        # Lister les modèles disponibles
        print("📋 Récupération de la liste des modèles...")
        models = client.models.list()
        
        print(f"\n✅ {len(models.data)} modèles Mistral disponibles:\n")
        
        # Organiser les modèles par catégorie
        models_by_category = {
            "Mistral Large (Puissant)": [],
            "Mistral Medium": [],
            "Mistral Small (Rapide)": [],
            "Mistral Nemo": [],
            "Codestral (Code)": [],
            "Pixtral (Vision)": [],
            "Autres": []
        }
        
        for model in models.data:
            model_id = model.id
            if "large" in model_id.lower():
                models_by_category["Mistral Large (Puissant)"].append(model_id)
            elif "medium" in model_id.lower():
                models_by_category["Mistral Medium"].append(model_id)
            elif "small" in model_id.lower():
                models_by_category["Mistral Small (Rapide)"].append(model_id)
            elif "nemo" in model_id.lower():
                models_by_category["Mistral Nemo"].append(model_id)
            elif "codestral" in model_id.lower():
                models_by_category["Codestral (Code)"].append(model_id)
            elif "pixtral" in model_id.lower():
                models_by_category["Pixtral (Vision)"].append(model_id)
            else:
                models_by_category["Autres"].append(model_id)
        
        for category, model_list in models_by_category.items():
            if model_list:
                print(f"\n{category}")
                for model_id in sorted(model_list):
                    print(f"  • {model_id}")
        
        # Test d'appel API avec le premier modèle disponible
        print("\n" + "="*60)
        print("TEST D'APPEL API")
        print("="*60 + "\n")
        
        # Utiliser mistral-large-latest ou le premier modèle disponible
        test_model = "mistral-large-latest"
        if models.data:
            # Chercher mistral-large-latest
            large_models = [m for m in models.data if "large" in m.id.lower() and "latest" in m.id.lower()]
            if large_models:
                test_model = large_models[0].id
            else:
                test_model = models.data[0].id
        
        print(f"📤 Envoi d'une requête de test à {test_model}...")
        
        response = client.chat.complete(
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
        print("\n💡 Votre clé API Mistral fonctionne correctement.")
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
    test_mistral_connection()
