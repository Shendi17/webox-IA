"""
Script de test pour vérifier les modèles Gemma disponibles via Vertex AI
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_vertex_gemma():
    """Teste les modèles Gemma sur Vertex AI"""
    
    project_id = os.getenv('VERTEX_AI_PROJECT_ID')
    location = os.getenv('VERTEX_AI_LOCATION', 'us-central1')
    credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not project_id:
        print("❌ ERREUR: VERTEX_AI_PROJECT_ID n'est pas défini dans le fichier .env")
        return False
    
    print(f"✅ VERTEX_AI_PROJECT_ID: {project_id}")
    print(f"✅ VERTEX_AI_LOCATION: {location}")
    print(f"✅ GOOGLE_APPLICATION_CREDENTIALS: {'Défini' if credentials else 'Non défini'}")
    
    print("\n" + "="*60)
    print("TEST DES MODÈLES GEMMA SUR VERTEX AI")
    print("="*60 + "\n")
    
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        # Initialiser Vertex AI
        print("📋 Initialisation de Vertex AI...")
        vertexai.init(project=project_id, location=location)
        print("✅ Vertex AI initialisé avec succès\n")
        
        # Liste des modèles Gemma à tester
        gemma_models = [
            ("gemma-2-9b-it", "Gemma 2 9B Instruct"),
            ("gemma-2-27b-it", "Gemma 2 27B Instruct"),
            ("codegemma-7b-it", "CodeGemma 7B Instruct"),
            ("gemma-3", "Gemma 3"),
            ("gemma-2", "Gemma 2"),
        ]
        
        available_models = []
        
        for model_id, model_name in gemma_models:
            try:
                print(f"📤 Test de {model_name} ({model_id})...")
                
                model = GenerativeModel(model_id)
                response = model.generate_content(
                    "Dis bonjour en français en une phrase",
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 100
                    }
                )
                
                result = response.text
                print(f"✅ {model_name}: {result[:50]}...\n")
                available_models.append((model_id, model_name))
                
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "not found" in error_msg.lower():
                    print(f"❌ {model_name}: Modèle non trouvé sur Vertex AI\n")
                elif "403" in error_msg or "permission" in error_msg.lower():
                    print(f"⚠️ {model_name}: Pas de permission (activez l'API)\n")
                else:
                    print(f"❌ {model_name}: {error_msg[:100]}\n")
        
        print("="*60)
        if available_models:
            print(f"✅ {len(available_models)} modèles Gemma disponibles sur Vertex AI:")
            for model_id, model_name in available_models:
                print(f"  • {model_id} - {model_name}")
        else:
            print("⚠️ Aucun modèle Gemma disponible sur Vertex AI")
            print("\n💡 Vérifiez:")
            print("   1. Que l'API Vertex AI est activée")
            print("   2. Que votre projet a accès aux modèles Gemma")
            print("   3. Que vous êtes dans la bonne région")
        print("="*60)
        
        return available_models
        
    except ImportError:
        print("❌ ERREUR: Module 'vertexai' non installé")
        print("💡 Installez avec: pip install google-cloud-aiplatform")
        return []
    except Exception as e:
        print(f"❌ ERREUR lors du test:")
        print(f"   {str(e)}")
        return []

if __name__ == "__main__":
    available = test_vertex_gemma()
    
    if available:
        print("\n" + "="*60)
        print("CONCLUSION")
        print("="*60)
        print(f"\n✅ {len(available)} modèles Gemma disponibles via Vertex AI")
        print("\n💡 Ces modèles peuvent être réactivés dans l'interface WeBox")
        print("   en les mappant vers le provider 'Google' (Vertex AI)")
    else:
        print("\n" + "="*60)
        print("CONCLUSION")
        print("="*60)
        print("\n⚠️ Les modèles Gemma ne sont pas accessibles actuellement")
        print("\n💡 Vérifiez la configuration Vertex AI et les permissions")
