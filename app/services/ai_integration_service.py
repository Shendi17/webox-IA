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
        # Clés API - Chat & Text (12 providers)
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.cohere_key = os.getenv("COHERE_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        self.xai_key = os.getenv("XAI_API_KEY")
        self.together_key = os.getenv("TOGETHER_API_KEY")
        self.replicate_key = os.getenv("REPLICATE_API_KEY")
        self.huggingface_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # Vertex AI (Google Cloud)
        self.vertex_project_id = os.getenv("VERTEX_AI_PROJECT_ID")
        self.vertex_location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
        self.google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # Clés API - Images
        self.stability_key = os.getenv("STABILITY_API_KEY")
        
        # Clés API - Audio
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        
        # Clés API - Vidéo
        self.runway_key = os.getenv("RUNWAY_API_KEY")
    
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
        model: str = "claude-3-5-sonnet-latest",
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
    
    async def chat_mistral(
        self,
        messages: list,
        model: str = "mistral-large-latest",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Mistral AI"""
        if not self.mistral_key:
            return {"success": False, "error": "Clé Mistral non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.mistral_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    input_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                    output_tokens = data.get("usage", {}).get("completion_tokens", 0)
                    cost = (input_tokens / 1000 * 0.002) + (output_tokens / 1000 * 0.006)
                    
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
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
    
    async def chat_groq(
        self,
        messages: list,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Groq (ultra-rapide)"""
        if not self.groq_key:
            return {"success": False, "error": "Clé Groq non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    input_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                    output_tokens = data.get("usage", {}).get("completion_tokens", 0)
                    cost = 0.0  # Groq est gratuit actuellement
                    
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
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
    
    async def chat_cohere(
        self,
        message: str,
        model: str = "command-r-plus-08-2024",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Cohere"""
        if not self.cohere_key:
            return {"success": False, "error": "Clé Cohere non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.cohere.ai/v1/chat",
                    headers={
                        "Authorization": f"Bearer {self.cohere_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "message": message,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    return {
                        "success": True,
                        "message": data["text"],
                        "cost": 0.0,  # Coût variable selon le plan
                        "model": model
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def chat_perplexity(
        self,
        messages: list,
        model: str = "llama-3.1-sonar-small-128k-online",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Perplexity (avec recherche web)"""
        if not self.perplexity_key:
            return {"success": False, "error": "Clé Perplexity non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.perplexity_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
                        "cost": 0.0,
                        "model": model,
                        "citations": data.get("citations", [])
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def chat_deepseek(
        self,
        messages: list,
        model: str = "deepseek-chat",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec DeepSeek"""
        if not self.deepseek_key:
            return {"success": False, "error": "Clé DeepSeek non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.deepseek_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    input_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                    output_tokens = data.get("usage", {}).get("completion_tokens", 0)
                    cost = (input_tokens / 1000 * 0.00014) + (output_tokens / 1000 * 0.00028)
                    
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
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
    
    async def chat_xai(
        self,
        messages: list,
        model: str = "grok-3",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec xAI Grok"""
        if not self.xai_key:
            return {"success": False, "error": "Clé xAI non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.xai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
                        "cost": 0.0,
                        "model": model
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}


    async def chat_vertex_ai(
        self,
        messages: list,
        model: str = "gemini-2.0-flash-exp",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Google Vertex AI (Gemini)"""
        if not self.vertex_project_id or not self.google_credentials:
            return {"success": False, "error": "Vertex AI non configuré"}
        
        try:
            # Import dynamique pour éviter erreur si SDK non installé
            import vertexai
            from vertexai.preview.generative_models import GenerativeModel
            
            vertexai.init(project=self.vertex_project_id, location=self.vertex_location)
            
            model_instance = GenerativeModel(model)
            
            # Convertir messages au format Vertex AI
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            response = model_instance.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": 1024}
            )
            
            return {
                "success": True,
                "message": response.text,
                "cost": 0.0,  # Coût variable selon usage
                "model": model
            }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def chat_together(
        self,
        messages: list,
        model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Together AI"""
        if not self.together_key:
            return {"success": False, "error": "Clé Together non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.together_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    input_tokens = data.get("usage", {}).get("prompt_tokens", 0)
                    output_tokens = data.get("usage", {}).get("completion_tokens", 0)
                    
                    return {
                        "success": True,
                        "message": data["choices"][0]["message"]["content"],
                        "cost": 0.0,  # Coût variable
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
    
    async def chat_replicate(
        self,
        messages: list,
        model: str = "meta/meta-llama-3.1-405b-instruct",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Replicate"""
        if not self.replicate_key:
            return {"success": False, "error": "Clé Replicate non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Convertir messages en prompt
                prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                
                response = await client.post(
                    "https://api.replicate.com/v1/predictions",
                    headers={
                        "Authorization": f"Bearer {self.replicate_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": model,
                        "input": {
                            "prompt": prompt,
                            "temperature": temperature
                        }
                    }
                )
                
                if response.status_code == 201:
                    data = response.json()
                    prediction_url = data.get("urls", {}).get("get")
                    
                    # Attendre la complétion
                    for _ in range(30):
                        await asyncio.sleep(2)
                        status_response = await client.get(
                            prediction_url,
                            headers={"Authorization": f"Bearer {self.replicate_key}"}
                        )
                        status_data = status_response.json()
                        
                        if status_data["status"] == "succeeded":
                            return {
                                "success": True,
                                "message": "".join(status_data.get("output", [])),
                                "cost": 0.0,
                                "model": model
                            }
                        elif status_data["status"] == "failed":
                            return {"success": False, "error": "Prédiction échouée"}
                    
                    return {"success": False, "error": "Timeout"}
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def chat_huggingface(
        self,
        messages: list,
        model: str = "meta-llama/Meta-Llama-3-70B-Instruct",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Chat avec Hugging Face Inference API"""
        if not self.huggingface_key:
            return {"success": False, "error": "Clé Hugging Face non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # Convertir messages en prompt
                prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers={
                        "Authorization": f"Bearer {self.huggingface_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "temperature": temperature,
                            "max_new_tokens": 1024
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Format de réponse variable selon modèle
                    if isinstance(data, list) and len(data) > 0:
                        message = data[0].get("generated_text", "")
                    else:
                        message = str(data)
                    
                    return {
                        "success": True,
                        "message": message,
                        "cost": 0.0,  # Gratuit pour la plupart
                        "model": model
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}


# Instance globale du service
ai_service = AIIntegrationService()
