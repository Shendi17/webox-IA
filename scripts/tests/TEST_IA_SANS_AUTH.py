"""
Test génération IA sans authentification (routes publiques)
Date: 25 Janvier 2026
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("TEST GENERATION IA - VERIFICATION CONFIGURATION")
print("="*70 + "\n")

# Test 1: Vérifier OpenAI
print("1. TEST OPENAI (GPT-4, DALL-E)")
print("-" * 70)

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    print(f"OK OpenAI configure: {openai_key[:15]}...")
    
    # Test rapide avec l'API OpenAI
    try:
        import openai
        openai.api_key = openai_key
        
        # Test chat completion
        print("\n   Test chat GPT-4...")
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}],
            max_tokens=50
        )
        print(f"   OK Reponse: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"   ERREUR: {e}")
else:
    print("ERREUR OpenAI non configure")

print()

# Test 2: Vérifier Anthropic
print("2. TEST ANTHROPIC (CLAUDE)")
print("-" * 70)

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
if anthropic_key:
    print(f"OK Anthropic configure: {anthropic_key[:15]}...")
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        
        print("\n   Test chat Claude...")
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=50,
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}]
        )
        print(f"   OK Reponse: {message.content[0].text}")
        
    except Exception as e:
        print(f"   ERREUR: {e}")
else:
    print("ERREUR Anthropic non configure")

print()

# Test 3: Vérifier Vertex AI
print("3. TEST VERTEX AI (GEMINI)")
print("-" * 70)

vertex_project = os.getenv("VERTEX_AI_PROJECT_ID")
vertex_location = os.getenv("VERTEX_AI_LOCATION")
google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if vertex_project and vertex_location:
    print(f"OK Vertex AI configure")
    print(f"   Project: {vertex_project}")
    print(f"   Location: {vertex_location}")
    
    if google_creds:
        print(f"   Credentials: {google_creds}")
        
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            print("\n   Test chat Gemini...")
            vertexai.init(project=vertex_project, location=vertex_location)
            model = GenerativeModel("gemini-pro")
            response = model.generate_content("Dis bonjour en une phrase")
            print(f"   OK Reponse: {response.text}")
            
        except Exception as e:
            print(f"   ERREUR: {e}")
    else:
        print("   ATTENTION Credentials manquantes")
else:
    print("ERREUR Vertex AI non configure")

print()

# Test 4: Vérifier Mistral
print("4. TEST MISTRAL")
print("-" * 70)

mistral_key = os.getenv("MISTRAL_API_KEY")
if mistral_key:
    print(f"OK Mistral configure: {mistral_key[:15]}...")
    
    try:
        from mistralai.client import MistralClient
        
        print("\n   Test chat Mistral...")
        client = MistralClient(api_key=mistral_key)
        response = client.chat(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}]
        )
        print(f"   OK Reponse: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"   ERREUR: {e}")
else:
    print("ERREUR Mistral non configure")

print()

# Test 5: Vérifier Groq
print("5. TEST GROQ")
print("-" * 70)

groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    print(f"OK Groq configure: {groq_key[:15]}...")
    
    try:
        from groq import Groq
        
        print("\n   Test chat Groq...")
        client = Groq(api_key=groq_key)
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Dis bonjour en une phrase"}],
            max_tokens=50
        )
        print(f"   OK Reponse: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"   ERREUR: {e}")
else:
    print("ERREUR Groq non configure")

print()

# Résumé
print("="*70)
print("RESUME")
print("="*70)

apis_ok = 0
apis_total = 5

if openai_key: apis_ok += 1
if anthropic_key: apis_ok += 1
if vertex_project and vertex_location: apis_ok += 1
if mistral_key: apis_ok += 1
if groq_key: apis_ok += 1

print(f"APIs configurees: {apis_ok}/{apis_total} ({int(apis_ok/apis_total*100)}%)")
print()

if apis_ok == apis_total:
    print("OK Toutes les APIs IA sont configurees!")
elif apis_ok >= 3:
    print("OK Configuration suffisante pour continuer")
else:
    print("ATTENTION Configuration incomplete")

print()
