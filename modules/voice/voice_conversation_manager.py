"""Gestionnaire de conversations vocales avec IA"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from modules.voice.voice_telephony import twilio_manager
from modules.voice.voice_stt import google_stt_manager
from modules.voice.voice_tts import google_tts_manager
from modules.core.ai_providers import ai_manager
import asyncio


class VoiceConversationManager:
    """Gestionnaire de conversations vocales automatisées"""
    
    def __init__(self):
        """Initialise le gestionnaire"""
        self.conversations = {}
        self.call_flows = {}
        self.load_call_flows()
    
    def load_call_flows(self):
        """Charge les flux d'appels prédéfinis"""
        self.call_flows = {
            "accueil": {
                "name": "Accueil Standard",
                "description": "Message d'accueil et orientation",
                "steps": [
                    {
                        "id": "welcome",
                        "type": "say",
                        "message": "Bonjour et bienvenue. Je suis votre assistant vocal IA. Comment puis-je vous aider aujourd'hui ?",
                        "next": "listen"
                    },
                    {
                        "id": "listen",
                        "type": "listen",
                        "timeout": 5,
                        "next": "process"
                    },
                    {
                        "id": "process",
                        "type": "ai_response",
                        "provider": "openai",
                        "model": "gpt-4",
                        "next": "respond"
                    },
                    {
                        "id": "respond",
                        "type": "say",
                        "next": "listen"
                    }
                ]
            },
            "rendez_vous": {
                "name": "Prise de Rendez-vous",
                "description": "Gestion automatique des rendez-vous",
                "steps": [
                    {
                        "id": "welcome",
                        "type": "say",
                        "message": "Service de prise de rendez-vous. Pour quel service souhaitez-vous prendre rendez-vous ?",
                        "next": "get_service"
                    },
                    {
                        "id": "get_service",
                        "type": "listen",
                        "next": "confirm_service"
                    },
                    {
                        "id": "confirm_service",
                        "type": "ai_response",
                        "system_prompt": "Tu es un assistant de prise de rendez-vous. Confirme le service demandé et demande la date souhaitée.",
                        "next": "get_date"
                    }
                ]
            },
            "support": {
                "name": "Support Technique",
                "description": "Assistance technique automatisée",
                "steps": [
                    {
                        "id": "welcome",
                        "type": "say",
                        "message": "Support technique. Décrivez votre problème, je vais vous aider.",
                        "next": "get_problem"
                    },
                    {
                        "id": "get_problem",
                        "type": "listen",
                        "next": "analyze"
                    },
                    {
                        "id": "analyze",
                        "type": "ai_response",
                        "system_prompt": "Tu es un technicien de support. Analyse le problème et propose une solution claire et concise.",
                        "next": "provide_solution"
                    }
                ]
            },
            "information": {
                "name": "Demande d'Information",
                "description": "Réponses aux questions générales",
                "steps": [
                    {
                        "id": "welcome",
                        "type": "say",
                        "message": "Service d'information. Quelle information recherchez-vous ?",
                        "next": "get_question"
                    },
                    {
                        "id": "get_question",
                        "type": "listen",
                        "next": "answer"
                    },
                    {
                        "id": "answer",
                        "type": "ai_response",
                        "system_prompt": "Tu es un assistant d'information. Réponds de manière claire, concise et professionnelle.",
                        "next": "ask_more"
                    },
                    {
                        "id": "ask_more",
                        "type": "say",
                        "message": "Avez-vous d'autres questions ?",
                        "next": "check_more"
                    }
                ]
            }
        }
    
    def create_conversation(self, call_sid: str, flow_type: str = "accueil") -> Dict:
        """
        Crée une nouvelle conversation
        
        Args:
            call_sid: ID de l'appel Twilio
            flow_type: Type de flux d'appel
            
        Returns:
            Dictionnaire de la conversation
        """
        conversation = {
            'call_sid': call_sid,
            'flow_type': flow_type,
            'current_step': 0,
            'messages': [],
            'context': {},
            'start_time': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.conversations[call_sid] = conversation
        return conversation
    
    async def process_voice_input(
        self,
        call_sid: str,
        audio_content: bytes
    ) -> Optional[str]:
        """
        Traite l'entrée vocale
        
        Args:
            call_sid: ID de l'appel
            audio_content: Contenu audio
            
        Returns:
            Texte transcrit ou None
        """
        # Transcription
        transcript = google_stt_manager.transcribe_audio(audio_content)
        
        if transcript and call_sid in self.conversations:
            self.conversations[call_sid]['messages'].append({
                'role': 'user',
                'content': transcript,
                'timestamp': datetime.now().isoformat()
            })
        
        return transcript
    
    async def generate_ai_response(
        self,
        call_sid: str,
        user_input: str,
        system_prompt: Optional[str] = None
    ) -> Optional[str]:
        """
        Génère une réponse IA
        
        Args:
            call_sid: ID de l'appel
            user_input: Entrée utilisateur
            system_prompt: Prompt système personnalisé
            
        Returns:
            Réponse de l'IA
        """
        if call_sid not in self.conversations:
            return None
        
        conversation = self.conversations[call_sid]
        
        # Prompt système par défaut
        if not system_prompt:
            system_prompt = """Tu es un assistant vocal professionnel et courtois.
            Réponds de manière claire, concise et naturelle.
            Tes réponses doivent être adaptées à une conversation téléphonique.
            Limite tes réponses à 2-3 phrases maximum."""
        
        # Contexte de la conversation
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation['messages'][-5:])  # 5 derniers messages
        messages.append({"role": "user", "content": user_input})
        
        # Génération de la réponse
        try:
            response = await ai_manager.get_response(
                provider_name="openai",
                messages=messages,
                model="gpt-4"
            )
            
            if response:
                conversation['messages'].append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat()
                })
                
                return response
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse: {e}")
        
        return None
    
    def generate_voice_response(
        self,
        text: str,
        voice_name: str = "fr-FR-Neural2-A"
    ) -> Optional[bytes]:
        """
        Génère une réponse vocale
        
        Args:
            text: Texte à synthétiser
            voice_name: Nom de la voix
            
        Returns:
            Audio en bytes
        """
        return google_tts_manager.synthesize_for_phone(text, voice_name)
    
    async def handle_call_step(
        self,
        call_sid: str,
        step: Dict,
        user_input: Optional[str] = None
    ) -> Dict:
        """
        Gère une étape du flux d'appel
        
        Args:
            call_sid: ID de l'appel
            step: Étape du flux
            user_input: Entrée utilisateur (si disponible)
            
        Returns:
            Résultat de l'étape
        """
        result = {
            'type': step['type'],
            'success': False,
            'message': None,
            'audio': None,
            'next_step': step.get('next')
        }
        
        if step['type'] == 'say':
            # Dire un message
            message = step['message']
            audio = self.generate_voice_response(message)
            result['success'] = audio is not None
            result['message'] = message
            result['audio'] = audio
        
        elif step['type'] == 'listen':
            # Écouter l'utilisateur
            result['success'] = True
            result['message'] = "En attente de l'entrée utilisateur..."
        
        elif step['type'] == 'ai_response':
            # Générer une réponse IA
            if user_input:
                system_prompt = step.get('system_prompt')
                ai_response = await self.generate_ai_response(
                    call_sid,
                    user_input,
                    system_prompt
                )
                
                if ai_response:
                    audio = self.generate_voice_response(ai_response)
                    result['success'] = True
                    result['message'] = ai_response
                    result['audio'] = audio
        
        return result
    
    def get_conversation(self, call_sid: str) -> Optional[Dict]:
        """Récupère une conversation"""
        return self.conversations.get(call_sid)
    
    def end_conversation(self, call_sid: str):
        """Termine une conversation"""
        if call_sid in self.conversations:
            self.conversations[call_sid]['status'] = 'ended'
            self.conversations[call_sid]['end_time'] = datetime.now().isoformat()
    
    def save_conversation(self, call_sid: str, filepath: str = "voice_conversations.json"):
        """Sauvegarde une conversation"""
        if call_sid in self.conversations:
            try:
                # Charger les conversations existantes
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        all_conversations = json.load(f)
                else:
                    all_conversations = {}
                
                # Ajouter la nouvelle conversation
                all_conversations[call_sid] = self.conversations[call_sid]
                
                # Sauvegarder
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(all_conversations, f, ensure_ascii=False, indent=2)
                
                return True
            except Exception as e:
                print(f"Erreur lors de la sauvegarde: {e}")
                return False
        
        return False
    
    def get_call_flows(self) -> Dict:
        """Retourne les flux d'appels disponibles"""
        return self.call_flows
    
    def add_custom_flow(self, flow_id: str, flow_config: Dict):
        """Ajoute un flux d'appel personnalisé"""
        self.call_flows[flow_id] = flow_config


# Instance globale
voice_conversation_manager = VoiceConversationManager()
