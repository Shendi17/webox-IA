"""
Script de test de connexion à l'API OpenAI
Vérifie que la clé API fonctionne et liste les modèles disponibles
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement
load_dotenv()

def test_openai_connection():
    """Teste la connexion à l'API OpenAI"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ ERREUR: OPENAI_API_KEY n'est pas définie dans le fichier .env")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:20]}...")
    print("\n" + "="*60)
    print("TEST DE CONNEXION OPENAI")
    print("="*60 + "\n")
    
    try:
        # Initialiser le client OpenAI
        client = OpenAI(api_key=api_key)
        
        # Test 1: Lister les modèles disponibles
        print("📋 Récupération de la liste des modèles...")
        models = client.models.list()
        
        # Filtrer les modèles GPT
        gpt_models = [m for m in models.data if 'gpt' in m.id.lower()]
        
        print(f"\n✅ {len(gpt_models)} modèles GPT disponibles:\n")
        for model in sorted(gpt_models, key=lambda x: x.id):
            print(f"  • {model.id}")
        
        # Test 2: Faire un appel simple à l'API
        print("\n" + "="*60)
        print("TEST D'APPEL API")
        print("="*60 + "\n")
        
        print("📤 Envoi d'une requête de test à gpt-4o...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Dis bonjour en français"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"\n✅ Réponse reçue: {result}")
        
        # Afficher les informations d'usage
        print(f"\n📊 Tokens utilisés:")
        print(f"  • Prompt: {response.usage.prompt_tokens}")
        print(f"  • Completion: {response.usage.completion_tokens}")
        print(f"  • Total: {response.usage.total_tokens}")
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*60)
        print("\n💡 Votre clé API OpenAI fonctionne correctement.")
        print("💰 Solde visible: $10.00 (selon votre capture)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR lors du test:")
        print(f"   {str(e)}")
        print("\n💡 Vérifiez:")
        print("   1. Que votre clé API est correcte")
        print("   2. Que vous avez un solde disponible")
        print("   3. Que votre compte n'a pas de restrictions")
        return False

if __name__ == "__main__":
    test_openai_connection()
