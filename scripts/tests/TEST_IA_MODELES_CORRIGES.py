"""
Test génération IA avec modèles corrigés (non dépréciés)
Date: 25 Janvier 2026
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("TEST GENERATION IA - MODELES CORRIGES")
print("="*70 + "\n")

results = {"passed": 0, "failed": 0, "total": 0}

# Test 1: OpenAI GPT-4
print("1. TEST OPENAI GPT-4")
print("-" * 70)
results["total"] += 1

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    try:
        import openai
        openai.api_key = openai_key
        
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}],
            max_tokens=50
        )
        print(f"OK GPT-4: {response.choices[0].message.content}")
        results["passed"] += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        results["failed"] += 1
else:
    print("SKIP OpenAI non configure")
    results["total"] -= 1

print()

# Test 2: Anthropic Claude (modèle corrigé)
print("2. TEST ANTHROPIC CLAUDE-3.5-SONNET")
print("-" * 70)
results["total"] += 1

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_key:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        
        # Utiliser claude-3-5-sonnet-20241022 au lieu du modèle déprécié
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}]
        )
        print(f"OK Claude 3.5: {message.content[0].text}")
        results["passed"] += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        results["failed"] += 1
else:
    print("SKIP Anthropic non configure")
    results["total"] -= 1

print()

# Test 3: Vertex AI Gemini (modèle corrigé)
print("3. TEST VERTEX AI GEMINI-1.5-PRO")
print("-" * 70)
results["total"] += 1

vertex_project = os.getenv("VERTEX_AI_PROJECT_ID")
vertex_location = os.getenv("VERTEX_AI_LOCATION")

if vertex_project and vertex_location:
    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel
        
        vertexai.init(project=vertex_project, location=vertex_location)
        
        # Utiliser gemini-1.5-pro au lieu de gemini-pro
        model = GenerativeModel("gemini-1.5-pro")
        response = model.generate_content("Dis bonjour en une phrase")
        print(f"OK Gemini 1.5 Pro: {response.text}")
        results["passed"] += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        results["failed"] += 1
else:
    print("SKIP Vertex AI non configure")
    results["total"] -= 1

print()

# Test 4: Mistral (nouvelle API)
print("4. TEST MISTRAL AI")
print("-" * 70)
results["total"] += 1

mistral_key = os.getenv("MISTRAL_API_KEY")
if mistral_key:
    try:
        from mistralai import Mistral
        
        client = Mistral(api_key=mistral_key)
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}]
        )
        print(f"OK Mistral: {response.choices[0].message.content}")
        results["passed"] += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        results["failed"] += 1
else:
    print("SKIP Mistral non configure")
    results["total"] -= 1

print()

# Test 5: Groq (modèle corrigé)
print("5. TEST GROQ LLAMA-3.3")
print("-" * 70)
results["total"] += 1

groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    try:
        from groq import Groq
        
        client = Groq(api_key=groq_key)
        
        # Utiliser llama-3.3-70b-versatile au lieu de mixtral déprécié
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}],
            max_tokens=50
        )
        print(f"OK Groq Llama 3.3: {response.choices[0].message.content}")
        results["passed"] += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        results["failed"] += 1
else:
    print("SKIP Groq non configure")
    results["total"] -= 1

print()

# Test 6: OpenAI DALL-E 3 (génération image)
print("6. TEST OPENAI DALL-E 3 (IMAGE)")
print("-" * 70)
results["total"] += 1

if openai_key:
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt="Un chat mignon qui code sur un ordinateur, style cartoon",
            size="1024x1024",
            quality="standard",
            n=1
        )
        print(f"OK DALL-E 3: Image generee")
        print(f"   URL: {response.data[0].url[:60]}...")
        results["passed"] += 1
    except Exception as e:
        print(f"ERREUR: {e}")
        results["failed"] += 1
else:
    print("SKIP OpenAI non configure")
    results["total"] -= 1

print()

# Résumé
print("="*70)
print("RESUME DES TESTS")
print("="*70)
print(f"Total: {results['total']}")
print(f"Reussis: {results['passed']} ({int(results['passed']/results['total']*100) if results['total'] > 0 else 0}%)")
print(f"Echoues: {results['failed']}")
print()

if results['passed'] == results['total']:
    print("OK TOUS LES TESTS SONT PASSES!")
    print("\nModeles corriges:")
    print("- Claude: claude-3-5-sonnet-20241022")
    print("- Gemini: gemini-1.5-pro")
    print("- Groq: llama-3.3-70b-versatile")
    print("- Mistral: mistral-small-latest (nouvelle API)")
elif results['passed'] >= results['total'] * 0.7:
    print("OK Majorite des tests passes")
else:
    print("ATTENTION Plusieurs tests ont echoue")

print()
