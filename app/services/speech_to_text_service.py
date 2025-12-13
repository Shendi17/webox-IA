"""
Service Speech-to-Text pour la transcription audio
"""
import os
from typing import Dict, Optional
import openai

class SpeechToTextService:
    """Service de transcription audio en texte"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def transcribe_audio_whisper(self, audio_file_path: str, language: str = "fr") -> Dict:
        """
        Transcrire l'audio en texte avec Whisper (OpenAI)
        
        Args:
            audio_file_path: Chemin vers le fichier audio
            language: Code de langue (fr, en, etc.)
        
        Returns:
            Dict avec success, transcript, et éventuellement error
        """
        try:
            if not self.openai_api_key:
                return {
                    "success": False,
                    "error": "Clé API OpenAI non configurée"
                }
            
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language=language
                )
            
            return {
                "success": True,
                "transcript": transcript.text,
                "language": language
            }
        
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"Fichier audio non trouvé: {audio_file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de transcription: {str(e)}"
            }
    
    def transcribe_audio_bytes(self, audio_bytes: bytes, language: str = "fr") -> Dict:
        """
        Transcrire l'audio depuis des bytes
        
        Args:
            audio_bytes: Contenu audio en bytes
            language: Code de langue
        
        Returns:
            Dict avec success, transcript, et éventuellement error
        """
        try:
            if not self.openai_api_key:
                return {
                    "success": False,
                    "error": "Clé API OpenAI non configurée"
                }
            
            # Sauvegarder temporairement
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name
            
            # Transcrire
            result = self.transcribe_audio_whisper(temp_path, language)
            
            # Nettoyer
            os.unlink(temp_path)
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de transcription: {str(e)}"
            }
    
    def transcribe_twilio_audio(self, recording_url: str, language: str = "fr") -> Dict:
        """
        Transcrire un enregistrement Twilio
        
        Args:
            recording_url: URL de l'enregistrement Twilio
            language: Code de langue
        
        Returns:
            Dict avec success, transcript, et éventuellement error
        """
        try:
            import requests
            
            # Télécharger l'audio
            response = requests.get(recording_url)
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"Impossible de télécharger l'audio: {response.status_code}"
                }
            
            # Transcrire
            return self.transcribe_audio_bytes(response.content, language)
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de téléchargement/transcription: {str(e)}"
            }
