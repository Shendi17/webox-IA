"""
Service d'intégration des APIs IA externes
Gère les appels aux différentes APIs de génération (images, vidéos, audio)
"""
import os
import httpx
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime


class AIIntegrationService:
    """Service centralisé pour toutes les intégrations IA"""
    
    def __init__(self):
        # Clés API
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.stability_key = os.getenv("STABILITY_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.runway_key = os.getenv("RUNWAY_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY")
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
    
    # ============================================
    # GÉNÉRATION D'IMAGES
    # ============================================
    
    async def generate_image_dalle(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "vivid"
    ) -> Dict[str, Any]:
        """Générer une image avec DALL-E"""
        if not self.openai_key:
            return {"success": False, "error": "Clé OpenAI non configurée"}
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                style=style if model == "dall-e-3" else None,
                n=1
            )
            
            # Calculer coût
            if model == "dall-e-3":
                cost = 0.080 if quality == "hd" and size == "1024x1024" else 0.040
            else:
                cost = 0.020
            
            return {
                "success": True,
                "image_url": response.data[0].url,
                "cost": cost,
                "model": model
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def generate_image_stable_diffusion(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        steps: int = 30
    ) -> Dict[str, Any]:
        """Générer une image avec Stable Diffusion"""
        if not self.stability_key:
            return {"success": False, "error": "Clé Stability AI non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers={
                        "Authorization": f"Bearer {self.stability_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "text_prompts": [
                            {"text": prompt, "weight": 1},
                            {"text": negative_prompt or "", "weight": -1}
                        ],
                        "cfg_scale": 7,
                        "height": height,
                        "width": width,
                        "steps": steps,
                        "samples": 1
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # Sauvegarder l'image
                    import base64
                    image_data = base64.b64decode(data["artifacts"][0]["base64"])
                    
                    output_dir = "generated/images"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    filename = f"sd_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                    
                    return {
                        "success": True,
                        "image_path": filepath,
                        "cost": 0.02,
                        "model": "stable-diffusion-xl"
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ============================================
    # GÉNÉRATION AUDIO & VOIX
    # ============================================
    
    async def generate_voice_elevenlabs(
        self,
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
        model_id: str = "eleven_multilingual_v2"
    ) -> Dict[str, Any]:
        """Générer une voix avec ElevenLabs"""
        if not self.elevenlabs_key:
            return {"success": False, "error": "Clé ElevenLabs non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": self.elevenlabs_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "text": text,
                        "model_id": model_id,
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.75
                        }
                    }
                )
                
                if response.status_code == 200:
                    output_dir = "generated/audio"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    filename = f"voice_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.mp3"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    
                    # Coût approximatif: $0.30 per 1000 characters
                    cost = (len(text) / 1000) * 0.30
                    
                    return {
                        "success": True,
                        "audio_path": filepath,
                        "cost": cost,
                        "model": "elevenlabs"
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def generate_music_suno(
        self,
        prompt: str,
        duration: int = 30
    ) -> Dict[str, Any]:
        """Générer de la musique avec Suno AI (simulation)"""
        # Note: Suno n'a pas d'API publique officielle actuellement
        return {
            "success": False,
            "error": "Suno AI n'a pas d'API publique. Utiliser l'interface web.",
            "web_url": "https://suno.ai"
        }
    
    async def generate_music_udio(
        self,
        prompt: str,
        duration: int = 30
    ) -> Dict[str, Any]:
        """Générer de la musique avec Udio (simulation)"""
        # Note: Udio n'a pas d'API publique officielle actuellement
        return {
            "success": False,
            "error": "Udio n'a pas d'API publique. Utiliser l'interface web.",
            "web_url": "https://udio.com"
        }
    
    # ============================================
    # GÉNÉRATION VIDÉO
    # ============================================
    
    async def generate_video_runway(
        self,
        prompt: str,
        duration: int = 5,
        model: str = "gen3"
    ) -> Dict[str, Any]:
        """Générer une vidéo avec Runway ML"""
        if not self.runway_key:
            return {"success": False, "error": "Clé Runway non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Lancer la génération
                response = await client.post(
                    "https://api.runwayml.com/v1/generate",
                    headers={
                        "Authorization": f"Bearer {self.runway_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "prompt": prompt,
                        "duration": duration
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    task_id = data.get("id")
                    
                    # Attendre la génération (polling)
                    for _ in range(30):  # Max 30 tentatives
                        await asyncio.sleep(5)
                        
                        status_response = await client.get(
                            f"https://api.runwayml.com/v1/tasks/{task_id}",
                            headers={"Authorization": f"Bearer {self.runway_key}"}
                        )
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            
                            if status_data.get("status") == "completed":
                                video_url = status_data.get("output", {}).get("url")
                                
                                # Coût approximatif: $0.05 per second
                                cost = duration * 0.05
                                
                                return {
                                    "success": True,
                                    "video_url": video_url,
                                    "cost": cost,
                                    "model": model
                                }
                            elif status_data.get("status") == "failed":
                                return {"success": False, "error": "Génération échouée"}
                    
                    return {"success": False, "error": "Timeout: génération trop longue"}
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def generate_video_pika(
        self,
        prompt: str,
        duration: int = 3
    ) -> Dict[str, Any]:
        """Générer une vidéo avec Pika Labs (simulation)"""
        # Note: Pika n'a pas d'API publique officielle actuellement
        return {
            "success": False,
            "error": "Pika Labs n'a pas d'API publique. Utiliser Discord Bot.",
            "discord_url": "https://discord.gg/pika"
        }
    
    async def generate_video_luma(
        self,
        prompt: str,
        duration: int = 5
    ) -> Dict[str, Any]:
        """Générer une vidéo avec Luma AI (simulation)"""
        # Note: Luma n'a pas d'API publique officielle actuellement
        return {
            "success": False,
            "error": "Luma AI n'a pas d'API publique. Utiliser l'interface web.",
            "web_url": "https://lumalabs.ai"
        }
    
    # ============================================
    # CHAT IA
    # ============================================
    
    async def chat_openai(
        self,
        messages: list,
        model: str = "gpt-4",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec OpenAI GPT"""
        if not self.openai_key:
            return {"success": False, "error": "Clé OpenAI non configurée"}
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            
            # Calculer coût approximatif
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            if "gpt-4" in model:
                cost = (input_tokens / 1000 * 0.03) + (output_tokens / 1000 * 0.06)
            else:  # gpt-3.5
                cost = (input_tokens / 1000 * 0.0015) + (output_tokens / 1000 * 0.002)
            
            return {
                "success": True,
                "message": response.choices[0].message.content,
                "cost": cost,
                "model": model,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def chat_anthropic(
        self,
        messages: list,
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 1024
    ) -> Dict[str, Any]:
        """Chat avec Anthropic Claude"""
        if not self.anthropic_key:
            return {"success": False, "error": "Clé Anthropic non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "max_tokens": max_tokens,
                        "messages": messages
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Coût approximatif pour Claude 3 Sonnet
                    input_tokens = data.get("usage", {}).get("input_tokens", 0)
                    output_tokens = data.get("usage", {}).get("output_tokens", 0)
                    cost = (input_tokens / 1000 * 0.003) + (output_tokens / 1000 * 0.015)
                    
                    return {
                        "success": True,
                        "message": data["content"][0]["text"],
                        "cost": cost,
                        "model": model,
                        "tokens": {
                            "input": input_tokens,
                            "output": output_tokens,
                            "total": input_tokens + output_tokens
                        }
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def chat_google(
        self,
        prompt: str,
        model: str = "gemini-pro"
    ) -> Dict[str, Any]:
        """Chat avec Google Gemini"""
        if not self.google_key:
            return {"success": False, "error": "Clé Google non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={self.google_key}",
                    json={
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    message = data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    return {
                        "success": True,
                        "message": message,
                        "cost": 0.0,  # Gratuit jusqu'à certaines limites
                        "model": model
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}


# Instance globale du service
ai_service = AIIntegrationService()
