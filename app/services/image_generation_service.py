"""
Service de génération d'images multi-providers
Supporte: Vertex AI Imagen, OpenAI DALL-E, Replicate, HuggingFace, Stability AI
"""

import os
import httpx
import base64
from typing import Dict, Any, Optional
from datetime import datetime


class ImageGenerationService:
    """Service unifié pour la génération d'images avec plusieurs providers"""
    
    def __init__(self):
        # Clés API
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.stability_key = os.getenv("STABILITY_API_KEY")
        self.replicate_key = os.getenv("REPLICATE_API_KEY")
        self.huggingface_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # Vertex AI
        self.vertex_project_id = os.getenv("VERTEX_AI_PROJECT_ID")
        self.vertex_location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
        self.google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    async def generate_image(
        self,
        prompt: str,
        model: str,
        size: str = "1024x1024",
        quality: str = "standard",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Générer une image avec le provider approprié selon le modèle
        """
        # Router vers le bon provider
        if model.startswith("imagen-"):
            return await self.generate_imagen(prompt, model, size, quality)
        elif model.startswith("dall-e"):
            return await self.generate_dalle(prompt, model, size, quality)
        elif model.startswith("black-forest-labs/") or model.startswith("stability-ai/"):
            return await self.generate_replicate(prompt, model, size)
        elif model.startswith("stabilityai/"):
            return await self.generate_huggingface(prompt, model, size)
        elif model.startswith("stable-diffusion"):
            return await self.generate_stability_ai(prompt, model, size)
        else:
            return {"success": False, "error": f"Modèle non supporté: {model}"}
    
    async def generate_imagen(
        self,
        prompt: str,
        model: str = "imagen-4.0-generate-001",
        size: str = "1024x1024",
        quality: str = "standard"
    ) -> Dict[str, Any]:
        """Générer une image avec Vertex AI Imagen"""
        if not self.vertex_project_id or not self.google_credentials:
            return {"success": False, "error": "Vertex AI non configuré"}
        
        try:
            import vertexai
            from vertexai.preview.vision_models import ImageGenerationModel
            
            # Configurer les credentials avant d'initialiser
            if self.google_credentials and os.path.exists(self.google_credentials):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_credentials
            
            vertexai.init(project=self.vertex_project_id, location=self.vertex_location)
            
            # Charger le modèle
            image_model = ImageGenerationModel.from_pretrained(model)
            
            # Générer l'image
            images = image_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="1:1" if size == "1024x1024" else "16:9"
            )
            
            # Sauvegarder l'image
            output_dir = "generated/images"
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"imagen_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(output_dir, filename)
            
            images[0].save(filepath)
            
            return {
                "success": True,
                "image_url": filepath,
                "cost": 0.02,  # Coût variable selon modèle
                "model": model
            }
            
        except Exception as e:
            return {"success": False, "error": f"Erreur Vertex AI Imagen: {str(e)}"}
    
    async def generate_dalle(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard"
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
                n=1
            )
            
            # Calculer coût
            if model == "dall-e-3":
                cost = 0.080 if quality == "hd" else 0.040
            else:
                cost = 0.020
            
            return {
                "success": True,
                "image_url": response.data[0].url,
                "cost": cost,
                "model": model
            }
            
        except Exception as e:
            return {"success": False, "error": f"Erreur DALL-E: {str(e)}"}
    
    async def generate_replicate(
        self,
        prompt: str,
        model: str,
        size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """Générer une image avec Replicate (Flux, SDXL, etc.)"""
        if not self.replicate_key:
            return {"success": False, "error": "Clé Replicate non configurée"}
        
        try:
            import asyncio
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Créer la prédiction
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
                            "width": int(size.split("x")[0]),
                            "height": int(size.split("x")[1])
                        }
                    }
                )
                
                if response.status_code != 201:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                
                data = response.json()
                prediction_url = data.get("urls", {}).get("get")
                
                # Attendre la complétion
                for _ in range(60):
                    await asyncio.sleep(2)
                    status_response = await client.get(
                        prediction_url,
                        headers={"Authorization": f"Bearer {self.replicate_key}"}
                    )
                    status_data = status_response.json()
                    
                    if status_data["status"] == "succeeded":
                        image_url = status_data["output"][0] if isinstance(status_data["output"], list) else status_data["output"]
                        
                        return {
                            "success": True,
                            "image_url": image_url,
                            "cost": 0.01,
                            "model": model
                        }
                    elif status_data["status"] == "failed":
                        return {"success": False, "error": "Génération échouée"}
                
                return {"success": False, "error": "Timeout"}
                
        except Exception as e:
            return {"success": False, "error": f"Erreur Replicate: {str(e)}"}
    
    async def generate_huggingface(
        self,
        prompt: str,
        model: str,
        size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """Générer une image avec Hugging Face Inference API"""
        if not self.huggingface_key:
            return {"success": False, "error": "Clé Hugging Face non configurée"}
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers={
                        "Authorization": f"Bearer {self.huggingface_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "width": int(size.split("x")[0]),
                            "height": int(size.split("x")[1])
                        }
                    }
                )
                
                if response.status_code == 200:
                    # Sauvegarder l'image
                    output_dir = "generated/images"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    filename = f"hf_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    
                    return {
                        "success": True,
                        "image_url": filepath,
                        "cost": 0.0,  # Gratuit
                        "model": model
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": f"Erreur Hugging Face: {str(e)}"}
    
    async def generate_stability_ai(
        self,
        prompt: str,
        model: str,
        size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """Générer une image avec Stability AI"""
        if not self.stability_key:
            return {"success": False, "error": "Clé Stability AI non configurée"}
        
        try:
            # Mapper le modèle vers l'endpoint Stability AI
            model_map = {
                "stable-diffusion-3.5-large": "stable-diffusion-v3-5-large",
                "stable-diffusion-3.5-medium": "stable-diffusion-v3-5-medium",
                "stable-diffusion-xl-1024-v1-0": "stable-diffusion-xl-1024-v1-0"
            }
            
            api_model = model_map.get(model, "stable-diffusion-xl-1024-v1-0")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://api.stability.ai/v1/generation/{api_model}/text-to-image",
                    headers={
                        "Authorization": f"Bearer {self.stability_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "text_prompts": [{"text": prompt, "weight": 1}],
                        "cfg_scale": 7,
                        "height": int(size.split("x")[1]),
                        "width": int(size.split("x")[0]),
                        "steps": 30,
                        "samples": 1
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    image_data = base64.b64decode(data["artifacts"][0]["base64"])
                    
                    output_dir = "generated/images"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    filename = f"sd_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                    
                    return {
                        "success": True,
                        "image_url": filepath,
                        "cost": 0.02,
                        "model": model
                    }
                else:
                    return {"success": False, "error": f"Erreur API: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": f"Erreur Stability AI: {str(e)}"}


# Instance globale
image_service = ImageGenerationService()
