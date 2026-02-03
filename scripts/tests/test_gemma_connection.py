"""
Script de test de connexion aux modèles Gemma via Google AI
Vérifie que la clé API fonctionne et teste les modèles Gemma
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Charger les variables d'environnement
load_dotenv()

def test_gemma_connection():
    """Teste la connexion aux modèles Gemma via Google AI"""
    
    # Essayer GEMINI_API_KEY puis GOOGLE_API_KEY
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: GEMINI_API_KEY ou GOOGLE_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION GEMMA (GOOGLE AI)")
    print("="*60 + "\n")
    
    try:
        # Configurer l'API Google
        genai.configure(api_key=api_key)
        
        # Lister tous les modèles disponibles
        print("📋 Récupération de la liste des modèles Google AI...")
        all_models = genai.list_models()
        
        # Filtrer les modèles Gemma
        gemma_models = []
        gemini_models = []
        
        for model in all_models:
            model_name = model.name.replace('models/', '')
            if 'gemma' in model_name.lower():
                gemma_models.append(model_name)
            elif 'gemini' in model_name.lower():
                gemini_models.append(model_name)
        
        print(f"\n✅ {len(gemma_models)} modèles Gemma trouvés:")
        if gemma_models:
            for model_name in sorted(gemma_models):
                print(f"  • {model_name}")
        else:
            print("  ⚠️ Aucun modèle Gemma trouvé dans Google AI")
        
        print(f"\n✅ {len(gemini_models)} modèles Gemini disponibles:")
        for model_name in sorted(gemini_models)[:5]:
            print(f"  • {model_name}")
        if len(gemini_models) > 5:
            print(f"  ... et {len(gemini_models) - 5} autres")
        
        # Test d'appel API avec un modèle Gemma si disponible
        print("\n" + "="*60)
        print("TEST D'APPEL API")
        print("="*60 + "\n")
        
        # Essayer avec gemma-2-9b-it si disponible, sinon gemini
        test_models = [
            'gemma-2-9b-it',
            'gemma-2-27b-it',
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash'
        ]
        
        test_model = None
        for model_name in test_models:
            if model_name in gemma_models or model_name in gemini_models:
                test_model = model_name
                break
        
        if not test_model and gemini_models:
            test_model = gemini_models[0]
        
        if not test_model:
            print("❌ Aucun modèle disponible pour le test")
            return False
        
        print(f"📤 Envoi d'une requête de test à {test_model}...")
        
        model = genai.GenerativeModel(test_model)
        response = model.generate_content("Dis bonjour en français en une phrase")
        
        result = response.text
        print(f"\n✅ Réponse reçue: {result}")
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\n💡 Votre clé API Google fonctionne correctement.")
        
        if gemma_models:
            print(f"🎯 Modèles Gemma disponibles: {len(gemma_models)}")
            print(f"   Recommandé: {gemma_models[0] if gemma_models else 'N/A'}")
        else:
            print("⚠️ Les modèles Gemma ne sont pas disponibles via Google AI API")
            print("💡 Les modèles Gemma sont disponibles via:")
            print("   - Groq (llama-3.1-8b-instant, etc.)")
            print("   - Ollama (local)")
            print("   - Hugging Face")
        
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
    test_gemma_connection()
