"""
Service Text-to-Speech pour la synthèse vocale
"""
import os
import requests
from typing import Dict, Optional
import openai

class TextToSpeechService:
    """Service de synthèse vocale (texte vers audio)"""
    
    def __init__(self):
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate_speech_elevenlabs(
        self, 
        text: str, 
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        language: str = "fr"
    ) -> Dict:
        """
        Générer de l'audio avec ElevenLabs
        
        Args:
            text: Texte à synthétiser
            voice_id: ID de la voix ElevenLabs
            language: Code de langue
        
        Returns:
            Dict avec success, audio_content (bytes), et éventuellement error
        """
        try:
            if not self.elevenlabs_api_key:
                return {
                    "success": False,
                    "error": "Clé API ElevenLabs non configurée"
                }
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "audio_content": response.content,
                    "format": "mp3"
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur ElevenLabs: {response.status_code} - {response.text}"
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Timeout lors de la génération audio"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération audio: {str(e)}"
            }
    
    def generate_speech_openai(
        self, 
        text: str, 
        voice: str = "alloy",
        model: str = "tts-1"
    ) -> Dict:
        """
        Générer de l'audio avec OpenAI TTS
        
        Args:
            text: Texte à synthétiser
            voice: Voix OpenAI (alloy, echo, fable, onyx, nova, shimmer)
            model: Modèle TTS (tts-1 ou tts-1-hd)
        
        Returns:
            Dict avec success, audio_content (bytes), et éventuellement error
        """
        try:
            if not self.openai_api_key:
                return {
                    "success": False,
                    "error": "Clé API OpenAI non configurée"
                }
            
            response = openai.Audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            
            return {
                "success": True,
                "audio_content": response.content,
                "format": "mp3"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur OpenAI TTS: {str(e)}"
            }
    
    def generate_speech(
        self, 
        text: str, 
        provider: str = "elevenlabs",
        voice_id: str = None,
        language: str = "fr"
    ) -> Dict:
        """
        Générer de l'audio (méthode unifiée)
        
        Args:
            text: Texte à synthétiser
            provider: Provider (elevenlabs ou openai)
            voice_id: ID de la voix
            language: Code de langue
        
        Returns:
            Dict avec success, audio_content, et éventuellement error
        """
        if provider == "elevenlabs":
            voice = voice_id or "21m00Tcm4TlvDq8ikWAM"
            return self.generate_speech_elevenlabs(text, voice, language)
        elif provider == "openai":
            voice = voice_id or "alloy"
            return self.generate_speech_openai(text, voice)
        else:
            return {
                "success": False,
                "error": f"Provider non supporté: {provider}"
            }
    
    def save_audio_to_file(self, audio_content: bytes, file_path: str) -> Dict:
        """
        Sauvegarder l'audio dans un fichier
        
        Args:
            audio_content: Contenu audio en bytes
            file_path: Chemin du fichier de destination
        
        Returns:
            Dict avec success et éventuellement error
        """
        try:
            with open(file_path, 'wb') as f:
                f.write(audio_content)
            
            return {
                "success": True,
                "file_path": file_path
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de sauvegarde: {str(e)}"
            }
