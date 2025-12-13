"""
Service principal de gestion des appels vocaux
"""
import os
from typing import Dict, Optional
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from datetime import datetime

from app.services.speech_to_text_service import SpeechToTextService
from app.services.text_to_speech_service import TextToSpeechService
from app.services.ai_providers import AIProviderFactory


class VoiceCallService:
    """Service de gestion des appels vocaux"""
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
        
        self.stt_service = SpeechToTextService()
        self.tts_service = TextToSpeechService()
    
    def generate_welcome_twiml(self, assistant_config: Dict) -> str:
        """
        Générer le TwiML pour accueillir l'appelant
        
        Args:
            assistant_config: Configuration de l'assistant vocal
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Message de bienvenue
        welcome_message = assistant_config.get("welcome_message", 
            "Bonjour, je suis votre assistant vocal. Comment puis-je vous aider ?")
        
        response.say(
            welcome_message,
            voice='Polly.Celine',
            language='fr-FR'
        )
        
        # Enregistrer la réponse de l'utilisateur
        response.record(
            max_length=30,
            action='/api/voice/process-recording',
            method='POST',
            transcribe=True,
            transcribe_callback='/api/voice/transcription'
        )
        
        return str(response)
    
    def process_user_input(
        self, 
        transcript: str, 
        assistant_config: Dict,
        conversation_history: list = None
    ) -> Dict:
        """
        Traiter l'entrée utilisateur et générer une réponse IA
        
        Args:
            transcript: Transcription de ce que l'utilisateur a dit
            assistant_config: Configuration de l'assistant
            conversation_history: Historique de la conversation
        
        Returns:
            Dict avec success, response_text, et éventuellement error
        """
        try:
            # Obtenir le modèle IA
            ai_model = assistant_config.get("ai_model", "gpt-4")
            ai_context = assistant_config.get("ai_context", "")
            
            # Construire le prompt
            system_prompt = f"""Tu es un assistant vocal pour {assistant_config.get('client_name', 'une entreprise')}.
            
Contexte: {ai_context}

Personnalité: {assistant_config.get('ai_personality', 'professional')}

Instructions:
- Réponds de manière concise et claire
- Sois naturel et conversationnel
- Aide l'utilisateur avec sa demande
- Si tu ne peux pas aider, propose de transférer à un humain
"""
            
            # Préparer les messages
            messages = [{"role": "system", "content": system_prompt}]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": transcript})
            
            # Obtenir la réponse de l'IA
            ai_provider = AIProviderFactory.get_provider(ai_model)
            ai_response = ai_provider.chat(messages)
            
            if ai_response.get("success"):
                return {
                    "success": True,
                    "response_text": ai_response["content"],
                    "model_used": ai_model
                }
            else:
                return {
                    "success": False,
                    "error": ai_response.get("error", "Erreur IA")
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de traitement: {str(e)}"
            }
    
    def generate_response_twiml(self, response_text: str, continue_call: bool = True) -> str:
        """
        Générer le TwiML pour la réponse de l'assistant
        
        Args:
            response_text: Texte de la réponse à dire
            continue_call: Si True, continue d'écouter l'utilisateur
        
        Returns:
            TwiML XML string
        """
        response = VoiceResponse()
        
        # Dire la réponse
        response.say(
            response_text,
            voice='Polly.Celine',
            language='fr-FR'
        )
        
        if continue_call:
            # Continuer à écouter
            response.record(
                max_length=30,
                action='/api/voice/process-recording',
                method='POST',
                transcribe=True,
                transcribe_callback='/api/voice/transcription'
            )
        else:
            # Terminer l'appel
            response.say(
                "Au revoir et bonne journée !",
                voice='Polly.Celine',
                language='fr-FR'
            )
            response.hangup()
        
        return str(response)
    
    def handle_incoming_call(self, from_number: str, to_number: str, call_sid: str) -> Dict:
        """
        Gérer un appel entrant
        
        Args:
            from_number: Numéro de l'appelant
            to_number: Numéro appelé
            call_sid: ID de l'appel Twilio
        
        Returns:
            Dict avec success, twiml, et éventuellement error
        """
        try:
            # Ici, on devrait chercher l'assistant associé au numéro
            # Pour l'instant, on retourne un TwiML de base
            
            assistant_config = {
                "client_name": "WeBox",
                "welcome_message": "Bonjour, bienvenue chez WeBox. Comment puis-je vous aider ?",
                "ai_model": "gpt-4",
                "ai_context": "Vous êtes un assistant pour une entreprise de développement web.",
                "ai_personality": "professional"
            }
            
            twiml = self.generate_welcome_twiml(assistant_config)
            
            return {
                "success": True,
                "twiml": twiml,
                "call_sid": call_sid
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de gestion d'appel: {str(e)}"
            }
    
    def get_call_details(self, call_sid: str) -> Dict:
        """
        Obtenir les détails d'un appel Twilio
        
        Args:
            call_sid: ID de l'appel
        
        Returns:
            Dict avec les détails de l'appel
        """
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "Client Twilio non configuré"
                }
            
            call = self.client.calls(call_sid).fetch()
            
            return {
                "success": True,
                "call": {
                    "sid": call.sid,
                    "from": call.from_,
                    "to": call.to,
                    "status": call.status,
                    "duration": call.duration,
                    "start_time": call.start_time.isoformat() if call.start_time else None,
                    "end_time": call.end_time.isoformat() if call.end_time else None
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de récupération: {str(e)}"
            }
