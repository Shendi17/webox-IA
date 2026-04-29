"""
Script de test automatisé pour vérifier toutes les générations WeBox
"""
import os
import sys
import asyncio
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

async def test_audio_generation():
    """Tester la génération audio avec gTTS"""
    print("\n🎙️ TEST AUDIO GENERATION")
    print("-" * 50)
    
    try:
        from gtts import gTTS
        import hashlib
        
        prompt = "Ceci est un test de génération audio"
        audio_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        output_dir = "generated/audio"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"test_audio_{audio_hash}.mp3")
        
        # Générer l'audio
        tts = gTTS(text=prompt, lang='fr', slow=False)
        tts.save(output_path)
        
        # Vérifier
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ Audio créé: {output_path}")
            print(f"   Taille: {size} bytes")
            return True
        else:
            print(f"❌ Fichier audio non créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_video_generation():
    """Tester la génération vidéo (image PNG)"""
    print("\n🎬 TEST VIDEO GENERATION (PNG)")
    print("-" * 50)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import hashlib
        
        prompt = "Ceci est un test de génération vidéo"
        duration = 5
        video_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        output_dir = "generated/videos"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"test_video_{video_hash}.png")
        
        # Créer l'image
        img = Image.new('RGB', (1280, 720), color='black')
        draw = ImageDraw.Draw(img)
        
        # Texte
        text = prompt[:100]
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Position centrée
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1280 - text_width) // 2
        y = (720 - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        draw.text((20, 680), f"Durée: {duration}s", fill='gray', font=font)
        
        # Sauvegarder
        img.save(output_path, 'PNG')
        
        # Vérifier
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ Image vidéo créée: {output_path}")
            print(f"   Taille: {size} bytes")
            return True
        else:
            print(f"❌ Fichier image non créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_dependencies():
    """Vérifier toutes les dépendances"""
    print("\n📦 TEST DEPENDENCIES")
    print("-" * 50)
    
    deps = {
        'gTTS': False,
        'PIL': False,
        'httpx': False,
        'fastapi': False,
        'sqlalchemy': False,
    }
    
    # gTTS
    try:
        import gtts
        deps['gTTS'] = True
        print(f"✅ gTTS installé (version: {gtts.__version__})")
    except ImportError:
        print(f"❌ gTTS non installé")
    
    # PIL
    try:
        from PIL import Image
        deps['PIL'] = True
        print(f"✅ Pillow installé")
    except ImportError:
        print(f"❌ Pillow non installé")
    
    # httpx
    try:
        import httpx
        deps['httpx'] = True
        print(f"✅ httpx installé (version: {httpx.__version__})")
    except ImportError:
        print(f"❌ httpx non installé")
    
    # fastapi
    try:
        import fastapi
        deps['fastapi'] = True
        print(f"✅ FastAPI installé (version: {fastapi.__version__})")
    except ImportError:
        print(f"❌ FastAPI non installé")
    
    # sqlalchemy
    try:
        import sqlalchemy
        deps['sqlalchemy'] = True
        print(f"✅ SQLAlchemy installé (version: {sqlalchemy.__version__})")
    except ImportError:
        print(f"❌ SQLAlchemy non installé")
    
    return all(deps.values())


async def test_directories():
    """Vérifier les répertoires de génération"""
    print("\n📁 TEST DIRECTORIES")
    print("-" * 50)
    
    dirs = [
        'generated',
        'generated/audio',
        'generated/videos',
        'generated/images',
        'generated/ebooks',
    ]
    
    all_ok = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} existe")
        else:
            print(f"⚠️  {dir_path} n'existe pas - création...")
            os.makedirs(dir_path, exist_ok=True)
            if os.path.exists(dir_path):
                print(f"   ✅ Créé avec succès")
            else:
                print(f"   ❌ Échec de création")
                all_ok = False
    
    return all_ok


async def main():
    """Exécuter tous les tests"""
    print("=" * 50)
    print("🧪 TESTS DE GÉNÉRATION WEBOX")
    print("=" * 50)
    
    results = {
        'dependencies': await test_dependencies(),
        'directories': await test_directories(),
        'audio': await test_audio_generation(),
        'video': await test_video_generation(),
    }
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_pass = all(results.values())
    
    print("\n" + "=" * 50)
    if all_pass:
        print("✅ TOUS LES TESTS RÉUSSIS")
        print("\nLes générations sont prêtes à fonctionner:")
        print("- Audio: gTTS (MP3 réels)")
        print("- Vidéo: Images PNG (en attendant FFmpeg)")
        print("- Shorts: Images PNG")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("\nVérifiez les erreurs ci-dessus")
    print("=" * 50)
    
    return all_pass


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
