"""Gestionnaires pour les différents fournisseurs d'IA"""
import asyncio
from typing import List, Dict, Optional, AsyncGenerator
from abc import ABC, abstractmethod
import openai
import anthropic
import google.generativeai as genai
from modules.core.config import config


class AIProvider(ABC):
    """Classe de base pour les fournisseurs d'IA"""
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse à partir des messages"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Vérifie si le fournisseur est configuré"""
        pass


class OpenAIProvider(AIProvider):
    """Fournisseur OpenAI (GPT-4, GPT-3.5)"""
    
    def __init__(self):
        if config.OPENAI_API_KEY:
            self.client = openai.AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        return bool(config.OPENAI_API_KEY)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec OpenAI"""
        if not self.is_configured():
            return "❌ OpenAI n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur OpenAI: {str(e)}"


class AnthropicProvider(AIProvider):
    """Fournisseur Anthropic (Claude)"""
    
    def __init__(self):
        if config.ANTHROPIC_API_KEY:
            self.client = anthropic.AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        return bool(config.ANTHROPIC_API_KEY)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "claude-3-sonnet-20240229",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Claude"""
        if not self.is_configured():
            return "❌ Anthropic n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            # Séparer le system message des autres messages
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message if system_message else None,
                messages=user_messages
            )
            return response.content[0].text
        except Exception as e:
            return f"❌ Erreur Anthropic: {str(e)}"


class GoogleProvider(AIProvider):
    """Fournisseur Google (Gemini)"""
    
    def __init__(self):
        if config.GOOGLE_API_KEY:
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.configured = True
        else:
            self.configured = False
    
    def is_configured(self) -> bool:
        return self.configured
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gemini-pro",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Gemini"""
        if not self.is_configured():
            return "❌ Google AI n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            model_instance = genai.GenerativeModel(model)
            
            # Convertir les messages au format Gemini
            prompt = ""
            for msg in messages:
                if msg["role"] == "system":
                    prompt += f"Instructions: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    prompt += f"User: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    prompt += f"Assistant: {msg['content']}\n"
            
            # Exécuter dans un thread pour éviter les problèmes d'async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: model_instance.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                )
            )
            return response.text
        except Exception as e:
            return f"❌ Erreur Google AI: {str(e)}"


class MistralProvider(AIProvider):
    """Fournisseur Mistral AI"""
    
    def __init__(self):
        self.api_key = config.MISTRAL_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "mistral-large-latest",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Mistral AI"""
        if not self.is_configured():
            return "❌ Mistral AI n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.mistral.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erreur Mistral AI: {str(e)}"


class CohereProvider(AIProvider):
    """Fournisseur Cohere"""
    
    def __init__(self):
        self.api_key = config.COHERE_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "command-r-plus",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Cohere"""
        if not self.is_configured():
            return "❌ Cohere n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            # Convertir les messages en format Cohere
            chat_history = []
            message = ""
            for msg in messages:
                if msg["role"] == "user":
                    message = msg["content"]
                elif msg["role"] == "assistant":
                    chat_history.append({"role": "CHATBOT", "message": msg["content"]})
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.cohere.ai/v1/chat",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "message": message,
                        "chat_history": chat_history,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["text"]
        except Exception as e:
            return f"❌ Erreur Cohere: {str(e)}"


class PerplexityProvider(AIProvider):
    """Fournisseur Perplexity AI"""
    
    def __init__(self):
        self.api_key = config.PERPLEXITY_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "pplx-70b-online",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Perplexity AI"""
        if not self.is_configured():
            return "❌ Perplexity AI n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erreur Perplexity AI: {str(e)}"


class DeepSeekProvider(AIProvider):
    """Fournisseur DeepSeek AI"""
    
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec DeepSeek AI"""
        if not self.is_configured():
            return "❌ DeepSeek AI n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erreur DeepSeek AI: {str(e)}"


class GroqProvider(AIProvider):
    """Fournisseur Groq (Ultra rapide)"""
    
    def __init__(self):
        self.api_key = config.GROQ_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "llama-3.1-70b-versatile",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Groq"""
        if not self.is_configured():
            return "❌ Groq n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erreur Groq: {str(e)}"


class TogetherProvider(AIProvider):
    """Fournisseur Together AI"""
    
    def __init__(self):
        self.api_key = config.TOGETHER_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "meta-llama/Llama-3-70b-chat-hf",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Together AI"""
        if not self.is_configured():
            return "❌ Together AI n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erreur Together AI: {str(e)}"


class ReplicateProvider(AIProvider):
    """Fournisseur Replicate"""
    
    def __init__(self):
        self.api_key = config.REPLICATE_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "meta/llama-2-70b-chat",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Replicate"""
        if not self.is_configured():
            return "❌ Replicate n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            # Convertir les messages en prompt
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.replicate.com/v1/predictions",
                    headers={
                        "Authorization": f"Token {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": model,
                        "input": {
                            "prompt": prompt,
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        }
                    }
                ) as response:
                    data = await response.json()
                    return data.get("output", "Réponse en cours de génération...")
        except Exception as e:
            return f"❌ Erreur Replicate: {str(e)}"


class HuggingFaceProvider(AIProvider):
    """Fournisseur Hugging Face Inference API"""
    
    def __init__(self):
        self.api_key = config.HUGGINGFACE_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "meta-llama/Meta-Llama-3-70B-Instruct",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec Hugging Face"""
        if not self.is_configured():
            return "❌ Hugging Face n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            # Convertir les messages en prompt
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "temperature": temperature,
                            "max_new_tokens": max_tokens
                        }
                    }
                ) as response:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 0:
                        return data[0].get("generated_text", "")
                    return str(data)
        except Exception as e:
            return f"❌ Erreur Hugging Face: {str(e)}"


class xAIProvider(AIProvider):
    """Fournisseur xAI (Grok)"""
    
    def __init__(self):
        self.api_key = config.XAI_API_KEY
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "grok-beta",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Génère une réponse avec xAI Grok"""
        if not self.is_configured():
            return "❌ xAI (Grok) n'est pas configuré. Veuillez ajouter votre clé API dans le fichier .env"
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                ) as response:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erreur xAI (Grok): {str(e)}"


class MultiAIManager:
    """Gestionnaire pour interroger plusieurs IA en parallèle"""
    
    def __init__(self):
        self.providers = {
            "OpenAI": OpenAIProvider(),
            "Anthropic": AnthropicProvider(),
            "Google": GoogleProvider(),
            "Mistral": MistralProvider(),
            "Cohere": CohereProvider(),
            "Perplexity": PerplexityProvider(),
            "DeepSeek": DeepSeekProvider(),
            "Groq": GroqProvider(),
            "Together": TogetherProvider(),
            "Replicate": ReplicateProvider(),
            "HuggingFace": HuggingFaceProvider(),
            "xAI": xAIProvider()
        }
    
    def get_available_providers(self) -> List[str]:
        """Retourne la liste des fournisseurs configurés"""
        return [
            name for name, provider in self.providers.items() 
            if provider.is_configured()
        ]
    
    def get_all_providers(self) -> List[str]:
        """Retourne la liste de tous les fournisseurs (configurés ou non)"""
        return list(self.providers.keys())
    
    def get_provider_status(self, provider_name: str) -> bool:
        """Vérifie si un fournisseur est configuré"""
        if provider_name in self.providers:
            return self.providers[provider_name].is_configured()
        return False
    
    async def generate_multi_response(
        self,
        messages: List[Dict[str, str]],
        selected_providers: List[str],
        models: Dict[str, str],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, str]:
        """Génère des réponses de plusieurs IA en parallèle"""
        tasks = []
        provider_names = []
        
        for provider_name in selected_providers:
            if provider_name in self.providers:
                provider = self.providers[provider_name]
                model = models.get(provider_name, "")
                
                if model:
                    tasks.append(
                        provider.generate_response(
                            messages, 
                            model, 
                            temperature, 
                            max_tokens
                        )
                    )
                    provider_names.append(provider_name)
        
        if not tasks:
            return {}
        
        # Exécuter toutes les requêtes en parallèle
        responses = await asyncio.gather(*tasks)
        
        # Créer un dictionnaire des réponses
        return {
            provider_names[i]: responses[i] 
            for i in range(len(responses))
        }
    
    async def cross_verify(
        self,
        question: str,
        answer: str,
        verifier_provider: str,
        verifier_model: str
    ) -> str:
        """Vérifie une réponse avec une autre IA"""
        verification_messages = [
            {
                "role": "system",
                "content": "Tu es un expert en vérification de faits. Analyse la réponse suivante et identifie les points corrects, les erreurs potentielles et les améliorations possibles."
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\nRéponse à vérifier:\n{answer}\n\nFournis une analyse critique et constructive."
            }
        ]
        
        if verifier_provider in self.providers:
            provider = self.providers[verifier_provider]
            return await provider.generate_response(
                verification_messages,
                verifier_model,
                temperature=0.3
            )
        
        return "Fournisseur de vérification non disponible"


# Instance globale
ai_manager = MultiAIManager()
