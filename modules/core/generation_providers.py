"""Providers pour la génération de médias (images, audio, vidéo)"""
import asyncio
from typing import Optional, Dict, List
from abc import ABC, abstractmethod
import openai
from modules.core.config import config


class ImageProvider(ABC):
    """Classe de base pour les générateurs d'images"""
    
    @abstractmethod
    async def generate_image(self, prompt: str, **kwargs) -> bytes:
        """Génère une image à partir d'un prompt"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Vérifie si le provider est configuré"""
        pass


class DALLEProvider(ImageProvider):
    """Provider pour DALL-E 3 (OpenAI)"""
    
    def __init__(self):
        if config.OPENAI_API_KEY:
            self.client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        return bool(config.OPENAI_API_KEY)
    
    async def generate_image(
        self, 
        prompt: str, 
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "vivid"
    ) -> bytes:
        """Génère une image avec DALL-E 3"""
        if not self.is_configured():
            raise Exception("DALL-E 3 n'est pas configuré. Ajoutez votre clé OpenAI.")
        
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1
            )
            
            # Télécharger l'image
            image_url = response.data[0].url
            
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    return await resp.read()
        
        except Exception as e:
            raise Exception(f"Erreur DALL-E 3: {str(e)}")


class StableDiffusionProvider(ImageProvider):
    """Provider pour Stable Diffusion (Stability AI)"""
    
    def __init__(self):
        self.api_key = config.STABILITY_API_KEY if hasattr(config, 'STABILITY_API_KEY') else None
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_image(
        self, 
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30
    ) -> bytes:
        """Génère une image avec Stable Diffusion"""
        if not self.is_configured():
            raise Exception("Stable Diffusion n'est pas configuré. Ajoutez votre clé Stability AI.")
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "text_prompts": [
                            {"text": prompt, "weight": 1},
                            {"text": negative_prompt, "weight": -1} if negative_prompt else {}
                        ],
                        "cfg_scale": 7,
                        "height": height,
                        "width": width,
                        "steps": steps,
                        "samples": 1
                    }
                ) as response:
                    data = await response.json()
                    
                    if "artifacts" in data and len(data["artifacts"]) > 0:
                        import base64
                        return base64.b64decode(data["artifacts"][0]["base64"])
                    else:
                        raise Exception("Aucune image générée")
        
        except Exception as e:
            raise Exception(f"Erreur Stable Diffusion: {str(e)}")


class AudioProvider(ABC):
    """Classe de base pour les générateurs audio"""
    
    @abstractmethod
    async def text_to_speech(self, text: str, **kwargs) -> bytes:
        """Convertit du texte en audio"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Vérifie si le provider est configuré"""
        pass


class ElevenLabsProvider(AudioProvider):
    """Provider pour ElevenLabs (synthèse vocale)"""
    
    def __init__(self):
        self.api_key = config.ELEVENLABS_API_KEY if hasattr(config, 'ELEVENLABS_API_KEY') else None
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def text_to_speech(
        self,
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
        model_id: str = "eleven_monolingual_v1"
    ) -> bytes:
        """Convertit du texte en audio avec ElevenLabs"""
        if not self.is_configured():
            raise Exception("ElevenLabs n'est pas configuré. Ajoutez votre clé API.")
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "text": text,
                        "model_id": model_id,
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.5
                        }
                    }
                ) as response:
                    return await response.read()
        
        except Exception as e:
            raise Exception(f"Erreur ElevenLabs: {str(e)}")
    
    async def get_voices(self) -> List[Dict]:
        """Récupère la liste des voix disponibles"""
        if not self.is_configured():
            return []
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.elevenlabs.io/v1/voices",
                    headers={"xi-api-key": self.api_key}
                ) as response:
                    data = await response.json()
                    return data.get("voices", [])
        except:
            return []


class WhisperProvider(AudioProvider):
    """Provider pour Whisper (OpenAI - transcription)"""
    
    def __init__(self):
        if config.OPENAI_API_KEY:
            self.client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        return bool(config.OPENAI_API_KEY)
    
    async def text_to_speech(self, text: str, voice: str = "alloy") -> bytes:
        """Convertit du texte en audio avec OpenAI TTS"""
        if not self.is_configured():
            raise Exception("Whisper/OpenAI n'est pas configuré.")
        
        try:
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            return response.content
        
        except Exception as e:
            raise Exception(f"Erreur OpenAI TTS: {str(e)}")
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        """Transcrit un fichier audio en texte"""
        if not self.is_configured():
            raise Exception("Whisper n'est pas configuré.")
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Erreur Whisper: {str(e)}")


class VideoProvider(ABC):
    """Classe de base pour les générateurs vidéo"""
    
    @abstractmethod
    async def generate_video(self, prompt: str, **kwargs) -> bytes:
        """Génère une vidéo à partir d'un prompt"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Vérifie si le provider est configuré"""
        pass


class RunwayProvider(VideoProvider):
    """Provider pour Runway (génération vidéo) - Placeholder"""
    
    def __init__(self):
        self.api_key = config.RUNWAY_API_KEY if hasattr(config, 'RUNWAY_API_KEY') else None
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_video(self, prompt: str, **kwargs) -> bytes:
        """Génère une vidéo avec Runway - Bientôt disponible"""
        raise Exception("Runway - Bientôt disponible")


class MediaGenerationManager:
    """Gestionnaire pour la génération de médias"""
    
    def __init__(self):
        self.image_providers = {
            "DALL-E 3": DALLEProvider(),
            "Stable Diffusion": StableDiffusionProvider()
        }
        
        self.audio_providers = {
            "ElevenLabs": ElevenLabsProvider(),
            "OpenAI TTS": WhisperProvider()
        }
        
        self.video_providers = {
            "Runway": RunwayProvider()
        }
    
    def get_available_image_providers(self) -> List[str]:
        """Retourne les providers d'images configurés"""
        return [name for name, provider in self.image_providers.items() if provider.is_configured()]
    
    def get_available_audio_providers(self) -> List[str]:
        """Retourne les providers audio configurés"""
        return [name for name, provider in self.audio_providers.items() if provider.is_configured()]
    
    def get_available_video_providers(self) -> List[str]:
        """Retourne les providers vidéo configurés"""
        return [name for name, provider in self.video_providers.items() if provider.is_configured()]
    
    async def generate_image(self, provider_name: str, prompt: str, **kwargs) -> bytes:
        """Génère une image avec le provider spécifié"""
        if provider_name not in self.image_providers:
            raise Exception(f"Provider {provider_name} non trouvé")
        
        provider = self.image_providers[provider_name]
        return await provider.generate_image(prompt, **kwargs)
    
    async def generate_audio(self, provider_name: str, text: str, **kwargs) -> bytes:
        """Génère de l'audio avec le provider spécifié"""
        if provider_name not in self.audio_providers:
            raise Exception(f"Provider {provider_name} non trouvé")
        
        provider = self.audio_providers[provider_name]
        return await provider.text_to_speech(text, **kwargs)
    
    async def generate_video(self, provider_name: str, prompt: str, **kwargs) -> bytes:
        """Génère une vidéo avec le provider spécifié"""
        if provider_name not in self.video_providers:
            raise Exception(f"Provider {provider_name} non trouvé")
        
        provider = self.video_providers[provider_name]
        return await provider.generate_video(prompt, **kwargs)


# Instance globale
generation_manager = MediaGenerationManager()
