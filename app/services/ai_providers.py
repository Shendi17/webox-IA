"""
Service pour gérer les différents fournisseurs d'IA
"""
import os
from typing import List, Dict, Optional


class AIProvider:
    """Classe de base pour les fournisseurs d'IA"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    async def chat(self, messages: List[Dict], model: str, **kwargs) -> str:
        """Envoyer un message et recevoir une réponse"""
        raise NotImplementedError


class OpenAIProvider(AIProvider):
    """Fournisseur OpenAI (GPT-4, GPT-3.5)"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv("OPENAI_API_KEY"))
    
    async def chat(self, messages: List[Dict], model: str = "gpt-4-turbo-preview", **kwargs) -> str:
        """Appeler l'API OpenAI"""
        if not self.api_key:
            return "⚠️ Clé API OpenAI non configurée. Ajoutez OPENAI_API_KEY dans .env"
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2000)
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "⚠️ Package OpenAI non installé. Installez avec : pip install openai"
        except Exception as e:
            return f"❌ Erreur OpenAI : {str(e)}"


class ClaudeProvider(AIProvider):
    """Fournisseur Anthropic (Claude 3)"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv("ANTHROPIC_API_KEY"))
    
    async def chat(self, messages: List[Dict], model: str = "claude-3-opus-20240229", **kwargs) -> str:
        """Appeler l'API Claude"""
        if not self.api_key:
            return "⚠️ Clé API Anthropic non configurée. Ajoutez ANTHROPIC_API_KEY dans .env"
        
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=self.api_key)
            
            # Extraire le message système
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            response = client.messages.create(
                model=model,
                max_tokens=kwargs.get('max_tokens', 2000),
                system=system_message,
                messages=user_messages
            )
            
            return response.content[0].text
            
        except ImportError:
            return "⚠️ Package Anthropic non installé. Installez avec : pip install anthropic"
        except Exception as e:
            return f"❌ Erreur Claude : {str(e)}"


class GeminiProvider(AIProvider):
    """Fournisseur Google (Gemini Pro)"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv("GOOGLE_API_KEY"))
    
    async def chat(self, messages: List[Dict], model: str = "gemini-pro", **kwargs) -> str:
        """Appeler l'API Gemini"""
        if not self.api_key:
            return "⚠️ Clé API Google non configurée. Ajoutez GOOGLE_API_KEY dans .env"
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            model_instance = genai.GenerativeModel(model)
            
            # Convertir les messages en format Gemini
            prompt = "\n\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            response = model_instance.generate_content(prompt)
            return response.text
            
        except ImportError:
            return "⚠️ Package Google Generative AI non installé. Installez avec : pip install google-generativeai"
        except Exception as e:
            return f"❌ Erreur Gemini : {str(e)}"


class MistralProvider(AIProvider):
    """Fournisseur Mistral AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv("MISTRAL_API_KEY"))
    
    async def chat(self, messages: List[Dict], model: str = "mistral-large-latest", **kwargs) -> str:
        """Appeler l'API Mistral"""
        if not self.api_key:
            return "⚠️ Clé API Mistral non configurée. Ajoutez MISTRAL_API_KEY dans .env"
        
        try:
            from mistralai.client import MistralClient
            client = MistralClient(api_key=self.api_key)
            
            response = client.chat(
                model=model,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "⚠️ Package Mistral AI non installé. Installez avec : pip install mistralai"
        except Exception as e:
            return f"❌ Erreur Mistral : {str(e)}"


class AIProviderFactory:
    """Factory pour créer les fournisseurs d'IA"""
    
    # Mapping des modèles vers les fournisseurs
    MODEL_PROVIDERS = {
        # OpenAI - Derniers modèles
        "gpt-4o": ("openai", "gpt-4o"),  # GPT-4 Omni - Le plus récent et puissant
        "gpt-4-turbo": ("openai", "gpt-4-turbo-preview"),
        "gpt-4": ("openai", "gpt-4"),
        "gpt-3.5-turbo": ("openai", "gpt-3.5-turbo"),
        
        # Anthropic Claude - Derniers modèles
        "claude-3.5-sonnet": ("claude", "claude-3-5-sonnet-20241022"),  # Claude 3.5 Sonnet - Le plus récent
        "claude-3-opus": ("claude", "claude-3-opus-20240229"),
        "claude-3-sonnet": ("claude", "claude-3-sonnet-20240229"),
        "claude-3-haiku": ("claude", "claude-3-haiku-20240307"),
        
        # Google Gemini
        "gemini-pro": ("gemini", "gemini-pro"),
        
        # Mistral AI
        "mistral-large": ("mistral", "mistral-large-latest"),
        "mistral-medium": ("mistral", "mistral-medium-latest"),
    }
    
    @classmethod
    def get_provider(cls, model: str) -> tuple[AIProvider, str]:
        """Récupérer le fournisseur approprié pour un modèle"""
        if model not in cls.MODEL_PROVIDERS:
            # Par défaut, utiliser OpenAI GPT-4 Turbo
            model = "gpt-4-turbo"
        
        provider_name, actual_model = cls.MODEL_PROVIDERS[model]
        
        providers = {
            "openai": OpenAIProvider(),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "mistral": MistralProvider()
        }
        
        return providers[provider_name], actual_model
    
    @classmethod
    async def chat(cls, messages: List[Dict], model: str = "gpt-4-turbo", **kwargs) -> str:
        """Envoyer un message à l'IA appropriée"""
        provider, actual_model = cls.get_provider(model)
        return await provider.chat(messages, actual_model, **kwargs)


# Export pour faciliter l'utilisation
async def call_ai(messages: List[Dict], model: str = "gpt-4-turbo", **kwargs) -> str:
    """
    Fonction helper pour appeler une IA
    
    Args:
        messages: Liste des messages au format [{"role": "user/assistant/system", "content": "..."}]
        model: Nom du modèle (gpt-4-turbo, claude-3-opus, etc.)
        **kwargs: Arguments supplémentaires (temperature, max_tokens, etc.)
    
    Returns:
        Réponse de l'IA
    """
    return await AIProviderFactory.chat(messages, model, **kwargs)
