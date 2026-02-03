"""
Script de test pour vérifier les modèles Gemma disponibles via Groq
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def test_gemma_on_groq():
    """Teste les modèles Gemma sur Groq"""
    
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: GROQ_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API Groq trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("RECHERCHE DES MODÈLES GEMMA SUR GROQ")
    print("="*60 + "\n")
    
    try:
        client = Groq(api_key=api_key)
        
        print("📋 Récupération de la liste des modèles...")
        models = client.models.list()
        
        # Filtrer les modèles Gemma
        gemma_models = []
        
        for model in models.data:
            model_id = model.id
            if "gemma" in model_id.lower():
                gemma_models.append(model_id)
        
        print(f"\n✅ {len(gemma_models)} modèles Gemma trouvés sur Groq:\n")
        
        if gemma_models:
            for model_id in sorted(gemma_models):
                print(f"  • {model_id}")
            
            # Test avec le premier modèle Gemma trouvé
            test_model = gemma_models[0]
            print(f"\n📤 Test avec {test_model}...")
            
            response = client.chat.completions.create(
                model=test_model,
                messages=[{"role": "user", "content": "Dis bonjour en français en une phrase"}],
                max_tokens=100
            )
            
            result = response.choices[0].message.content
            print(f"\n✅ Réponse reçue: {result}")
            
            print("\n" + "="*60)
            print("✅ MODÈLES GEMMA DISPONIBLES SUR GROQ!")
            print("="*60)
            
            return gemma_models
        else:
            print("⚠️ Aucun modèle Gemma trouvé sur Groq")
            print("\n💡 Les modèles Gemma ne sont pas disponibles via Groq actuellement.")
            print("   Groq propose principalement des modèles Llama, Mixtral, et Qwen.")
            return []
        
    except Exception as e:
        print(f"\n❌ ERREUR lors du test:")
        print(f"   {str(e)}")
        return []

if __name__ == "__main__":
    gemma_models = test_gemma_on_groq()
    
    if not gemma_models:
        print("\n" + "="*60)
        print("CONCLUSION")
        print("="*60)
        print("\n⚠️ Les modèles Gemma ne sont PAS disponibles via Groq.")
        print("\n💡 Solutions alternatives:")
        print("   1. Utiliser les modèles Llama sur Groq (similaires)")
        print("   2. Utiliser Google AI API avec GOOGLE_API_KEY")
        print("   3. Utiliser Ollama en local")
        print("   4. Retirer les modèles Gemma de l'interface")
