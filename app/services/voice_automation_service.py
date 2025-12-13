"""
Service Voice Automation - Piloter WeBox par commande vocale
"""
import os
import re
from typing import Dict, Optional, List
from app.services.speech_to_text_service import SpeechToTextService
from app.services.text_to_speech_service import TextToSpeechService
from app.services.ai_providers import AIProviderFactory


class VoiceAutomationService:
    """Service pour piloter WeBox par commande vocale"""
    
    def __init__(self):
        self.stt_service = SpeechToTextService()
        self.tts_service = TextToSpeechService()
        self.ai_model = "gpt-4"
    
    def process_voice_command(self, audio_bytes: bytes, user_context: Dict = None) -> Dict:
        """
        Traiter une commande vocale complète
        
        Args:
            audio_bytes: Audio de la commande
            user_context: Contexte utilisateur (projets, etc.)
        
        Returns:
            Dict avec success, action, response, audio_response
        """
        try:
            # 1. Transcrire l'audio
            transcription = self.stt_service.transcribe_audio_bytes(audio_bytes, "fr")
            
            if not transcription.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de transcription",
                    "details": transcription.get("error")
                }
            
            command_text = transcription["transcript"]
            
            # 2. Analyser la commande
            command_analysis = self.analyze_command(command_text, user_context)
            
            if not command_analysis.get("success"):
                return {
                    "success": False,
                    "error": "Commande non comprise",
                    "transcript": command_text
                }
            
            # 3. Générer la réponse vocale
            response_text = command_analysis["response"]
            audio_response = self.tts_service.generate_speech(
                response_text,
                provider="openai",
                voice_id="nova"
            )
            
            return {
                "success": True,
                "transcript": command_text,
                "action": command_analysis["action"],
                "parameters": command_analysis.get("parameters", {}),
                "response": response_text,
                "audio_response": audio_response.get("audio_content") if audio_response.get("success") else None
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de traitement: {str(e)}"
            }
    
    def analyze_command(self, command_text: str, user_context: Dict = None) -> Dict:
        """
        Analyser une commande textuelle et déterminer l'action
        
        Args:
            command_text: Texte de la commande
            user_context: Contexte utilisateur
        
        Returns:
            Dict avec success, action, parameters, response
        """
        try:
            # Utiliser l'IA pour comprendre la commande
            system_prompt = """Tu es l'assistant vocal de WeBox, une plateforme de création web et marketing.

Tu dois analyser les commandes vocales et les transformer en actions structurées.

Types d'actions possibles:
1. NAVIGATION: Naviguer dans l'interface
   - "ouvre mes projets", "va sur le dashboard", "affiche les statistiques"
   
2. CREATE_PROJECT: Créer un projet web
   - "crée un site e-commerce", "nouveau site portfolio", "génère un blog"
   
3. GENERATE_CONTENT: Générer du contenu
   - "génère 5 articles sur le marketing", "crée 10 posts Instagram", "écris un email"
   
4. DEPLOY: Déployer un projet
   - "déploie en production", "publie le site", "mets en ligne"
   
5. AI_CHAT: Discuter avec l'IA
   - "aide-moi à", "explique-moi", "comment faire"

Réponds UNIQUEMENT en JSON avec ce format:
{
    "action": "TYPE_ACTION",
    "parameters": {
        "key": "value"
    },
    "response": "Confirmation en français naturel"
}

Exemples:
- "crée un site e-commerce" → {"action": "CREATE_PROJECT", "parameters": {"type": "e-commerce", "template": "shop"}, "response": "Je crée un site e-commerce pour vous."}
- "génère 5 articles sur le SEO" → {"action": "GENERATE_CONTENT", "parameters": {"type": "articles", "count": 5, "topic": "SEO"}, "response": "Je génère 5 articles sur le SEO."}
"""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command_text}
            ]
            
            ai_provider = AIProviderFactory.get_provider(self.ai_model)
            ai_response = ai_provider.chat(messages)
            
            if not ai_response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur IA"
                }
            
            # Parser la réponse JSON
            import json
            try:
                # Extraire le JSON de la réponse
                content = ai_response["content"]
                
                # Chercher le JSON dans la réponse
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = json.loads(content)
                
                return {
                    "success": True,
                    "action": result.get("action"),
                    "parameters": result.get("parameters", {}),
                    "response": result.get("response", "Commande comprise.")
                }
            
            except json.JSONDecodeError:
                # Si le parsing JSON échoue, utiliser des patterns simples
                return self._fallback_command_parsing(command_text)
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur d'analyse: {str(e)}"
            }
    
    def _fallback_command_parsing(self, command_text: str) -> Dict:
        """
        Parser de secours avec des patterns simples
        
        Args:
            command_text: Texte de la commande
        
        Returns:
            Dict avec action et parameters
        """
        command_lower = command_text.lower()
        
        # Navigation
        if any(word in command_lower for word in ["ouvre", "va sur", "affiche", "montre"]):
            if "projet" in command_lower:
                return {
                    "success": True,
                    "action": "NAVIGATION",
                    "parameters": {"page": "projects"},
                    "response": "J'ouvre vos projets."
                }
            elif "dashboard" in command_lower:
                return {
                    "success": True,
                    "action": "NAVIGATION",
                    "parameters": {"page": "dashboard"},
                    "response": "J'ouvre le dashboard."
                }
        
        # Création de projet
        if any(word in command_lower for word in ["crée", "créer", "nouveau", "génère"]):
            if "site" in command_lower or "projet" in command_lower:
                project_type = "static"
                if "e-commerce" in command_lower or "boutique" in command_lower:
                    project_type = "e-commerce"
                elif "blog" in command_lower:
                    project_type = "blog"
                elif "portfolio" in command_lower:
                    project_type = "portfolio"
                
                return {
                    "success": True,
                    "action": "CREATE_PROJECT",
                    "parameters": {"type": project_type},
                    "response": f"Je crée un projet {project_type} pour vous."
                }
            
            # Génération de contenu
            if "article" in command_lower or "post" in command_lower or "email" in command_lower:
                # Extraire le nombre
                count_match = re.search(r'(\d+)', command_text)
                count = int(count_match.group(1)) if count_match else 1
                
                content_type = "articles"
                if "post" in command_lower:
                    content_type = "posts"
                elif "email" in command_lower:
                    content_type = "emails"
                
                # Extraire le sujet
                topic_match = re.search(r'sur (.+)', command_lower)
                topic = topic_match.group(1) if topic_match else "général"
                
                return {
                    "success": True,
                    "action": "GENERATE_CONTENT",
                    "parameters": {
                        "type": content_type,
                        "count": count,
                        "topic": topic
                    },
                    "response": f"Je génère {count} {content_type} sur {topic}."
                }
        
        # Déploiement
        if any(word in command_lower for word in ["déploie", "publie", "mets en ligne"]):
            return {
                "success": True,
                "action": "DEPLOY",
                "parameters": {"environment": "production"},
                "response": "Je déploie en production."
            }
        
        # Par défaut: AI Chat
        return {
            "success": True,
            "action": "AI_CHAT",
            "parameters": {"message": command_text},
            "response": "Je peux vous aider avec ça."
        }
    
    def execute_action(self, action: str, parameters: Dict, user_id: int = None) -> Dict:
        """
        Exécuter une action déterminée par la commande vocale
        
        Args:
            action: Type d'action
            parameters: Paramètres de l'action
            user_id: ID de l'utilisateur
        
        Returns:
            Dict avec success, result, message
        """
        try:
            if action == "NAVIGATION":
                return {
                    "success": True,
                    "result": {
                        "redirect": f"/{parameters.get('page', 'dashboard')}"
                    },
                    "message": "Navigation effectuée"
                }
            
            elif action == "CREATE_PROJECT":
                # Ici, on appellerait le service de création de projet
                return {
                    "success": True,
                    "result": {
                        "project_id": None,  # À implémenter
                        "type": parameters.get("type")
                    },
                    "message": f"Projet {parameters.get('type')} créé"
                }
            
            elif action == "GENERATE_CONTENT":
                # Ici, on appellerait le service de génération de contenu
                return {
                    "success": True,
                    "result": {
                        "content_type": parameters.get("type"),
                        "count": parameters.get("count"),
                        "topic": parameters.get("topic")
                    },
                    "message": f"{parameters.get('count')} {parameters.get('type')} générés"
                }
            
            elif action == "DEPLOY":
                # Ici, on appellerait le service de déploiement
                return {
                    "success": True,
                    "result": {
                        "environment": parameters.get("environment")
                    },
                    "message": "Déploiement lancé"
                }
            
            elif action == "AI_CHAT":
                return {
                    "success": True,
                    "result": {
                        "message": parameters.get("message")
                    },
                    "message": "Message envoyé au chat IA"
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Action non supportée: {action}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur d'exécution: {str(e)}"
            }
