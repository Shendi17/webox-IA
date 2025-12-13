import os
import time
import uuid
from typing import Dict, List, Optional
import google.generativeai as genai
from openai import OpenAI

class AIAgentService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Configuration Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configuration OpenAI
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Contexte système par défaut
        self.system_context = """Tu es un assistant IA intelligent et serviable intégré dans WeBox, 
une plateforme de création de contenu IA. Tu aides les utilisateurs avec :
- La création de podcasts
- La génération d'avatars
- Des conseils sur l'utilisation de l'IA
- Des réponses rapides et précises

Tu es disponible 24/7 et tu réponds toujours de manière professionnelle, claire et utile.
Sois concis mais complet dans tes réponses."""
    
    def generate_session_id(self) -> str:
        """Génère un ID de session unique"""
        return f"session_{uuid.uuid4().hex[:16]}"
    
    async def chat(self, message: str, conversation_history: List[Dict], model: str = "gemini-2.0-flash") -> Dict:
        """
        Envoie un message à l'IA et retourne la réponse
        
        Args:
            message: Message de l'utilisateur
            conversation_history: Historique de la conversation
            model: Modèle à utiliser
        
        Returns:
            Dict avec la réponse et les métadonnées
        """
        start_time = time.time()
        
        try:
            if model.startswith("gemini"):
                return await self._chat_gemini(message, conversation_history)
            elif model.startswith("gpt"):
                return await self._chat_openai(message, conversation_history, model)
            else:
                return {
                    "success": False,
                    "error": f"Modèle non supporté : {model}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération : {str(e)}"
            }
    
    async def _chat_gemini(self, message: str, history: List[Dict]) -> Dict:
        """Chat avec Gemini"""
        try:
            # Construire l'historique pour Gemini
            gemini_history = []
            for msg in history[-10:]:  # Garder les 10 derniers messages
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })
            
            # Créer le chat
            chat = self.gemini_model.start_chat(history=gemini_history)
            
            # Envoyer le message
            start_time = time.time()
            response = chat.send_message(message)
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": True,
                "content": response.text,
                "model": "gemini-2.0-flash",
                "response_time": response_time,
                "tokens": len(response.text.split())  # Approximation
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur Gemini : {str(e)}"
            }
    
    async def _chat_openai(self, message: str, history: List[Dict], model: str) -> Dict:
        """Chat avec OpenAI"""
        try:
            # Construire les messages pour OpenAI
            messages = [{"role": "system", "content": self.system_context}]
            
            # Ajouter l'historique
            for msg in history[-10:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Ajouter le nouveau message
            messages.append({"role": "user", "content": message})
            
            # Envoyer à OpenAI
            start_time = time.time()
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": model,
                "response_time": response_time,
                "tokens": response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur OpenAI : {str(e)}"
            }
    
    def generate_title(self, first_message: str) -> str:
        """Génère un titre pour la conversation basé sur le premier message"""
        # Prendre les 50 premiers caractères
        title = first_message[:50]
        if len(first_message) > 50:
            title += "..."
        return title
    
    def get_available_models(self) -> List[Dict]:
        """Retourne la liste des modèles disponibles"""
        models = []
        
        if self.gemini_api_key:
            models.append({
                "id": "gemini-2.0-flash",
                "name": "Gemini 2.0 Flash",
                "provider": "Google",
                "speed": "ultra-fast",
                "cost": "free",
                "icon": "⚡"
            })
        
        if self.openai_api_key:
            models.extend([
                {
                    "id": "gpt-4o",
                    "name": "GPT-4o",
                    "provider": "OpenAI",
                    "speed": "fast",
                    "cost": "low",
                    "icon": "🤖"
                },
                {
                    "id": "gpt-4o-mini",
                    "name": "GPT-4o Mini",
                    "provider": "OpenAI",
                    "speed": "very-fast",
                    "cost": "very-low",
                    "icon": "⚡"
                }
            ])
        
        return models
    
    def get_quick_actions(self) -> List[Dict]:
        """Retourne les actions rapides suggérées"""
        return [
            {
                "id": "create_podcast",
                "icon": "🎙️",
                "title": "Créer un podcast",
                "prompt": "Je veux créer un podcast sur..."
            },
            {
                "id": "create_avatar",
                "icon": "👤",
                "title": "Créer un avatar",
                "prompt": "Je veux créer un avatar..."
            },
            {
                "id": "help",
                "icon": "❓",
                "title": "Aide",
                "prompt": "Comment utiliser WeBox ?"
            },
            {
                "id": "ideas",
                "icon": "💡",
                "title": "Idées de contenu",
                "prompt": "Donne-moi des idées de contenu à créer"
            }
        ]
