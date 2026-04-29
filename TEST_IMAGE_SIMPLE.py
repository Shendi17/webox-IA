"""
Test simple pour diagnostiquer l'erreur de génération d'images
"""

import os
from dotenv import load_dotenv

# IMPORTANT: Charger .env AVANT d'importer les services
load_dotenv()

import asyncio
from app.services.image_generation_service import ImageGenerationService

async def test_imagen():
    """Test Vertex AI Imagen"""
    print("\n🧪 TEST IMAGEN")
    service = ImageGenerationService()
    
    print(f"Vertex Project ID: {service.vertex_project_id}")
    print(f"Google Credentials: {service.google_credentials}")
    
    result = await service.generate_imagen(
        prompt="Professional logo for WeBox brand, modern minimalist design",
        model="imagen-4.0-ultra-generate-001"
    )
    
    print(f"\nRésultat: {result}")
    return result

async def test_dalle():
    """Test DALL-E"""
    print("\n🧪 TEST DALL-E")
    service = ImageGenerationService()
    
    print(f"OpenAI Key: {service.openai_key[:20] if service.openai_key else 'Non configuré'}...")
    
    result = await service.generate_dalle(
        prompt="Professional logo for WeBox brand, modern minimalist design",
        model="dall-e-3",
        size="1024x1024",
        quality="standard"
    )
    
    print(f"\nRésultat: {result}")
    return result

async def main():
    print("="*60)
    print("🔍 DIAGNOSTIC GÉNÉRATION D'IMAGES")
    print("="*60)
    
    # Test 1: Imagen
    try:
        result_imagen = await test_imagen()
        if result_imagen['success']:
            print("✅ Imagen fonctionne")
        else:
            print(f"❌ Imagen échoue: {result_imagen['error']}")
    except Exception as e:
        print(f"❌ Exception Imagen: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: DALL-E
    try:
        result_dalle = await test_dalle()
        if result_dalle['success']:
            print("✅ DALL-E fonctionne")
        else:
            print(f"❌ DALL-E échoue: {result_dalle['error']}")
    except Exception as e:
        print(f"❌ Exception DALL-E: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
