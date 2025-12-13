"""Module de téléphonie vocale avec Twilio"""
import os
from typing import Optional, Dict, List
from datetime import datetime
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
import json


class TwilioVoiceManager:
    """Gestionnaire de téléphonie vocale avec Twilio"""
    
    def __init__(self):
        """Initialise le client Twilio"""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        """Vérifie si Twilio est configuré"""
        return self.client is not None and self.phone_number is not None
    
    def make_call(self, to_number: str, message: str) -> Optional[str]:
        """
        Effectue un appel sortant
        
        Args:
            to_number: Numéro à appeler
            message: Message à dire
            
        Returns:
            SID de l'appel ou None si erreur
        """
        if not self.is_configured():
            raise ValueError("Twilio n'est pas configuré")
        
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.phone_number,
                twiml=f'<Response><Say language="fr-FR">{message}</Say></Response>'
            )
            return call.sid
        except Exception as e:
            print(f"Erreur lors de l'appel: {e}")
            return None
    
    def create_voice_response(self, message: str, gather: bool = False) -> str:
        """
        Crée une réponse vocale TwiML
        
        Args:
            message: Message à dire
            gather: Si True, attend une réponse de l'utilisateur
            
        Returns:
            XML TwiML
        """
        response = VoiceResponse()
        
        if gather:
            gather_obj = Gather(
                input='speech',
                language='fr-FR',
                speech_timeout='auto',
                action='/voice/process',
                method='POST'
            )
            gather_obj.say(message, language='fr-FR')
            response.append(gather_obj)
            response.say("Je n'ai pas entendu de réponse. Au revoir.", language='fr-FR')
        else:
            response.say(message, language='fr-FR')
        
        return str(response)
    
    def get_call_details(self, call_sid: str) -> Optional[Dict]:
        """
        Récupère les détails d'un appel
        
        Args:
            call_sid: SID de l'appel
            
        Returns:
            Dictionnaire avec les détails de l'appel
        """
        if not self.is_configured():
            return None
        
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                'sid': call.sid,
                'from': call.from_,
                'to': call.to,
                'status': call.status,
                'duration': call.duration,
                'start_time': call.start_time,
                'end_time': call.end_time,
                'price': call.price,
                'direction': call.direction
            }
        except Exception as e:
            print(f"Erreur lors de la récupération des détails: {e}")
            return None
    
    def get_call_recordings(self, call_sid: str) -> List[Dict]:
        """
        Récupère les enregistrements d'un appel
        
        Args:
            call_sid: SID de l'appel
            
        Returns:
            Liste des enregistrements
        """
        if not self.is_configured():
            return []
        
        try:
            recordings = self.client.recordings.list(call_sid=call_sid)
            return [{
                'sid': r.sid,
                'duration': r.duration,
                'date_created': r.date_created,
                'uri': r.uri
            } for r in recordings]
        except Exception as e:
            print(f"Erreur lors de la récupération des enregistrements: {e}")
            return []
    
    def list_recent_calls(self, limit: int = 20) -> List[Dict]:
        """
        Liste les appels récents
        
        Args:
            limit: Nombre maximum d'appels à retourner
            
        Returns:
            Liste des appels récents
        """
        if not self.is_configured():
            return []
        
        try:
            calls = self.client.calls.list(limit=limit)
            return [{
                'sid': call.sid,
                'from': call.from_,
                'to': call.to,
                'status': call.status,
                'duration': call.duration,
                'start_time': call.start_time,
                'direction': call.direction
            } for call in calls]
        except Exception as e:
            print(f"Erreur lors de la récupération des appels: {e}")
            return []
    
    def send_sms(self, to_number: str, message: str) -> Optional[str]:
        """
        Envoie un SMS
        
        Args:
            to_number: Numéro destinataire
            message: Message à envoyer
            
        Returns:
            SID du message ou None si erreur
        """
        if not self.is_configured():
            raise ValueError("Twilio n'est pas configuré")
        
        try:
            message = self.client.messages.create(
                to=to_number,
                from_=self.phone_number,
                body=message
            )
            return message.sid
        except Exception as e:
            print(f"Erreur lors de l'envoi du SMS: {e}")
            return None


# Instance globale
twilio_manager = TwilioVoiceManager()
