#!/usr/bin/env python3
"""
Script pour tester tous les modèles Gemini disponibles sur Vertex AI
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Liste de tous les modèles Gemini à tester (modèles réels disponibles sur Vertex AI)
GEMINI_MODELS = [
    # Gemini 2.5 (Generally Available)
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-image",
    # Gemini 2.0 (Generally Available)
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite-001",
    # Gemini 3 (Preview)
    "gemini-3-pro",
    "gemini-3-flash",
    "gemini-3-pro-image",
]

def test_model(model_name):
    """Teste un modèle Gemini spécifique"""
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv('VERTEX_AI_PROJECT_ID')
        location = os.getenv('VERTEX_AI_LOCATION')
        
        vertexai.init(project=project_id, location=location)
        
        model = GenerativeModel(model_name)
        response = model.generate_content(
            "Dis simplement 'Bonjour' en français",
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 50
            }
        )
        
        return True, response.text.strip()
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("TEST DE TOUS LES MODÈLES GEMINI VERTEX AI")
    print("=" * 70)
    print()
    
    project_id = os.getenv('VERTEX_AI_PROJECT_ID')
    location = os.getenv('VERTEX_AI_LOCATION')
    
    print(f"Projet: {project_id}")
    print(f"Région: {location}")
    print()
    print("-" * 70)
    print()
    
    results = []
    
    for i, model_name in enumerate(GEMINI_MODELS, 1):
        print(f"[{i}/{len(GEMINI_MODELS)}] Test de {model_name}...", end=" ")
        
        success, result = test_model(model_name)
        
        if success:
            print(f"✅ SUCCÈS")
            print(f"    Réponse: {result}")
            results.append((model_name, "✅ Disponible", result))
        else:
            print(f"❌ ÉCHEC")
            error_msg = result[:100] + "..." if len(result) > 100 else result
            print(f"    Erreur: {error_msg}")
            results.append((model_name, "❌ Non disponible", error_msg))
        
        print()
    
    print("=" * 70)
    print("RÉSUMÉ DES TESTS")
    print("=" * 70)
    print()
    
    available_count = sum(1 for _, status, _ in results if "✅" in status)
    total_count = len(results)
    
    print(f"Modèles disponibles: {available_count}/{total_count}")
    print()
    
    print("MODÈLES DISPONIBLES:")
    for model, status, _ in results:
        if "✅" in status:
            print(f"  ✅ {model}")
    
    print()
    print("MODÈLES NON DISPONIBLES:")
    for model, status, error in results:
        if "❌" in status:
            print(f"  ❌ {model}")
            if "404" in error or "not found" in error.lower():
                print(f"     → Modèle non trouvé dans la région {location}")
            elif "403" in error or "permission" in error.lower():
                print(f"     → Problème de permissions")
            else:
                print(f"     → {error[:80]}")
    
    print()
    print("=" * 70)
    
    if available_count > 0:
        print("✅ Au moins un modèle Gemini fonctionne!")
        print()
        print("RECOMMANDATIONS:")
        print("  - Utilisez les modèles disponibles dans le chat multi-IA")
        print("  - gemini-2.5-flash est recommandé (rapide et performant)")
        print("  - gemini-2.5-pro pour les tâches complexes")
    else:
        print("❌ Aucun modèle Gemini n'est disponible")
        print()
        print("SOLUTIONS:")
        print("  1. Vérifiez que la facturation est activée")
        print("  2. Essayez une autre région (us-central1)")
        print("  3. Utilisez Groq comme alternative gratuite")

if __name__ == "__main__":
    main()
