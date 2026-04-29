"""
Script de test pour les nouvelles APIs IA ajoutées
Date: 10 Février 2026
"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

async def test_api(name: str, url: str, headers: dict, payload: dict):
    """Tester une API IA"""
    print(f"\n{BLUE}🧪 Test {name}...{RESET}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                print(f"{GREEN}✅ {name}: OK{RESET}")
                data = response.json()
                
                # Afficher un extrait de la réponse
                if "choices" in data:
                    message = data["choices"][0]["message"]["content"][:100]
                    print(f"   Réponse: {message}...")
                elif "text" in data:
                    print(f"   Réponse: {data['text'][:100]}...")
                elif "content" in data:
                    print(f"   Réponse: {data['content'][0]['text'][:100]}...")
                
                return True
            else:
                print(f"{RED}❌ {name}: Erreur {response.status_code}{RESET}")
                print(f"   {response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"{RED}❌ {name}: Exception - {str(e)[:100]}{RESET}")
        return False

async def main():
    """Tester toutes les nouvelles APIs"""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST DES NOUVELLES APIS IA{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = {}
    
    # 1. OpenAI (GPT-4)
    if os.getenv("OPENAI_API_KEY"):
        results["OpenAI"] = await test_api(
            "OpenAI GPT-4",
            "https://api.openai.com/v1/chat/completions",
            {
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": "Dis bonjour en français"}],
                "max_tokens": 50
            }
        )
    else:
        print(f"{YELLOW}⚠️  OpenAI: Clé non configurée{RESET}")
        results["OpenAI"] = None
    
    # 2. Anthropic (Claude)
    if os.getenv("ANTHROPIC_API_KEY"):
        results["Anthropic"] = await test_api(
            "Anthropic Claude",
            "https://api.anthropic.com/v1/messages",
            {
                "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            {
                "model": "claude-3-5-sonnet-latest",
                "max_tokens": 50,
                "messages": [{"role": "user", "content": "Dis bonjour en français"}]
            }
        )
    else:
        print(f"{YELLOW}⚠️  Anthropic: Clé non configurée{RESET}")
        results["Anthropic"] = None
    
    # 3. Mistral
    if os.getenv("MISTRAL_API_KEY"):
        results["Mistral"] = await test_api(
            "Mistral AI",
            "https://api.mistral.ai/v1/chat/completions",
            {
                "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "mistral-large-latest",
                "messages": [{"role": "user", "content": "Dis bonjour en français"}],
                "max_tokens": 50
            }
        )
    else:
        print(f"{YELLOW}⚠️  Mistral: Clé non configurée{RESET}")
        results["Mistral"] = None
    
    # 4. Groq
    if os.getenv("GROQ_API_KEY"):
        results["Groq"] = await test_api(
            "Groq (ultra-rapide)",
            "https://api.groq.com/openai/v1/chat/completions",
            {
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": "Dis bonjour en français"}],
                "max_tokens": 50
            }
        )
    else:
        print(f"{YELLOW}⚠️  Groq: Clé non configurée{RESET}")
        results["Groq"] = None
    
    # 5. Cohere
    if os.getenv("COHERE_API_KEY"):
        results["Cohere"] = await test_api(
            "Cohere",
            "https://api.cohere.ai/v1/chat",
            {
                "Authorization": f"Bearer {os.getenv('COHERE_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "command-r-plus-08-2024",
                "message": "Dis bonjour en français"
            }
        )
    else:
        print(f"{YELLOW}⚠️  Cohere: Clé non configurée{RESET}")
        results["Cohere"] = None
    
    # 6. Perplexity
    if os.getenv("PERPLEXITY_API_KEY"):
        results["Perplexity"] = await test_api(
            "Perplexity (avec recherche web)",
            "https://api.perplexity.ai/chat/completions",
            {
                "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [{"role": "user", "content": "Dis bonjour en français"}]
            }
        )
    else:
        print(f"{YELLOW}⚠️  Perplexity: Clé non configurée{RESET}")
        results["Perplexity"] = None
    
    # 7. DeepSeek
    if os.getenv("DEEPSEEK_API_KEY"):
        results["DeepSeek"] = await test_api(
            "DeepSeek",
            "https://api.deepseek.com/v1/chat/completions",
            {
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Dis bonjour en français"}],
                "max_tokens": 50
            }
        )
    else:
        print(f"{YELLOW}⚠️  DeepSeek: Clé non configurée{RESET}")
        results["DeepSeek"] = None
    
    # 8. xAI (Grok)
    if os.getenv("XAI_API_KEY"):
        results["xAI"] = await test_api(
            "xAI Grok",
            "https://api.x.ai/v1/chat/completions",
            {
                "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            {
                "model": "grok-3",
                "messages": [{"role": "user", "content": "Dis bonjour en français"}],
                "max_tokens": 50
            }
        )
    else:
        print(f"{YELLOW}⚠️  xAI: Clé non configurée{RESET}")
        results["xAI"] = None
    
    # Résumé
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}RÉSUMÉ DES TESTS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    total = len(results)
    success = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    print(f"Total APIs testées: {total}")
    print(f"{GREEN}✅ Succès: {success}{RESET}")
    print(f"{RED}❌ Échecs: {failed}{RESET}")
    print(f"{YELLOW}⚠️  Non configurées: {skipped}{RESET}")
    
    print(f"\n{BLUE}Détails par API:{RESET}")
    for name, result in results.items():
        if result is True:
            print(f"  {GREEN}✅ {name}: Fonctionnel{RESET}")
        elif result is False:
            print(f"  {RED}❌ {name}: Erreur{RESET}")
        else:
            print(f"  {YELLOW}⚠️  {name}: Non configuré{RESET}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    
    if success > 0:
        print(f"\n{GREEN}🎉 {success} API(s) fonctionnelle(s) !{RESET}")
    
    if failed > 0:
        print(f"\n{RED}⚠️  {failed} API(s) en erreur. Vérifiez les clés API.{RESET}")
    
    if skipped > 0:
        print(f"\n{YELLOW}💡 {skipped} API(s) non configurée(s). Ajoutez les clés dans .env{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
