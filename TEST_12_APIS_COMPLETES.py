"""
Script de test complet pour les 12 APIs IA intégrées
Teste chaque API avec un message simple et affiche les résultats
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_integration_service import ai_service

# Couleurs pour le terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


async def test_api(name: str, method, *args, **kwargs):
    """Teste une API et retourne le résultat"""
    print(f"\n🧪 Test {name}...")
    try:
        result = await method(*args, **kwargs)
        if result.get("success"):
            message = result.get("message", "")[:80]
            print(f"{GREEN}✅ {name}: OK{RESET}")
            print(f"   Réponse: {message}...")
            return True
        else:
            error = result.get("error", "Erreur inconnue")
            print(f"{RED}❌ {name}: {error}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}❌ {name}: Exception - {str(e)}{RESET}")
        return False


async def main():
    """Teste toutes les APIs"""
    load_dotenv()
    
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST COMPLET DES 12 APIS IA{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = {}
    test_message = [{"role": "user", "content": "Dis bonjour en français"}]
    
    # 1. OpenAI
    results['OpenAI'] = await test_api(
        "OpenAI GPT-4",
        ai_service.chat_openai,
        test_message
    )
    
    # 2. Anthropic
    results['Anthropic'] = await test_api(
        "Anthropic Claude",
        ai_service.chat_anthropic,
        test_message
    )
    
    # 3. Vertex AI (Google)
    results['Vertex AI'] = await test_api(
        "Google Vertex AI (Gemini)",
        ai_service.chat_vertex_ai,
        test_message
    )
    
    # 4. Mistral
    results['Mistral'] = await test_api(
        "Mistral AI",
        ai_service.chat_mistral,
        test_message
    )
    
    # 5. Groq
    results['Groq'] = await test_api(
        "Groq (ultra-rapide)",
        ai_service.chat_groq,
        test_message
    )
    
    # 6. Cohere
    results['Cohere'] = await test_api(
        "Cohere",
        ai_service.chat_cohere,
        "Dis bonjour en français"
    )
    
    # 7. Perplexity
    results['Perplexity'] = await test_api(
        "Perplexity (recherche web)",
        ai_service.chat_perplexity,
        test_message
    )
    
    # 8. DeepSeek
    results['DeepSeek'] = await test_api(
        "DeepSeek",
        ai_service.chat_deepseek,
        test_message
    )
    
    # 9. xAI (Grok)
    results['xAI'] = await test_api(
        "xAI Grok",
        ai_service.chat_xai,
        test_message
    )
    
    # 10. Together AI
    results['Together AI'] = await test_api(
        "Together AI",
        ai_service.chat_together,
        test_message
    )
    
    # 11. Replicate
    print(f"\n{YELLOW}⚠️  Replicate: Test désactivé (trop lent - 60s+){RESET}")
    results['Replicate'] = None
    
    # 12. Hugging Face
    results['Hugging Face'] = await test_api(
        "Hugging Face",
        ai_service.chat_huggingface,
        test_message
    )
    
    # Résumé
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}RÉSUMÉ DES TESTS - 12 APIS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    success_count = sum(1 for r in results.values() if r is True)
    failed_count = sum(1 for r in results.values() if r is False)
    skipped_count = sum(1 for r in results.values() if r is None)
    
    print(f"Total APIs: {len(results)}")
    print(f"{GREEN}✅ Succès: {success_count}{RESET}")
    print(f"{RED}❌ Échecs: {failed_count}{RESET}")
    print(f"{YELLOW}⚠️  Ignorées: {skipped_count}{RESET}\n")
    
    print("Détails par API:")
    for name, result in results.items():
        if result is True:
            print(f"  {GREEN}✅ {name}: Fonctionnel{RESET}")
        elif result is False:
            print(f"  {RED}❌ {name}: Erreur{RESET}")
        else:
            print(f"  {YELLOW}⚠️  {name}: Test ignoré{RESET}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    
    if success_count >= 8:
        print(f"\n{GREEN}🎉 {success_count} API(s) fonctionnelle(s) ! Excellent !{RESET}\n")
    elif success_count >= 5:
        print(f"\n{YELLOW}⚠️  {success_count} API(s) fonctionnelle(s). Vérifiez les clés API manquantes.{RESET}\n")
    else:
        print(f"\n{RED}❌ Seulement {success_count} API(s) fonctionnelle(s). Vérifiez votre configuration.{RESET}\n")


if __name__ == "__main__":
    asyncio.run(main())
