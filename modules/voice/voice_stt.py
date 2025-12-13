"""Module de reconnaissance vocale (Speech-to-Text) avec Google Cloud"""
import os
from typing import Optional
from google.cloud import speech_v1
from google.oauth2 import service_account
import io


class GoogleSTTManager:
    """Gestionnaire de reconnaissance vocale avec Google Cloud Speech-to-Text"""
    
    def __init__(self):
        """Initialise le client Google Cloud Speech-to-Text"""
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            self.client = speech_v1.SpeechClient(credentials=credentials)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        """Vérifie si Google Cloud STT est configuré"""
        return self.client is not None
    
    def transcribe_audio(
        self,
        audio_content: bytes,
        language_code: str = "fr-FR",
        sample_rate_hertz: int = 8000,
        encoding: str = "MULAW"
    ) -> Optional[str]:
        """
        Transcrit un fichier audio en texte
        
        Args:
            audio_content: Contenu audio en bytes
            language_code: Code de langue (fr-FR, en-US, etc.)
            sample_rate_hertz: Taux d'échantillonnage
            encoding: Format d'encodage (MULAW pour Twilio)
            
        Returns:
            Texte transcrit ou None si erreur
        """
        if not self.is_configured():
            raise ValueError("Google Cloud STT n'est pas configuré")
        
        try:
            # Configuration de l'audio
            audio = speech_v1.RecognitionAudio(content=audio_content)
            
            # Mapping des encodages
            encoding_map = {
                "MULAW": speech_v1.RecognitionConfig.AudioEncoding.MULAW,
                "LINEAR16": speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                "FLAC": speech_v1.RecognitionConfig.AudioEncoding.FLAC,
                "MP3": speech_v1.RecognitionConfig.AudioEncoding.MP3,
                "OGG_OPUS": speech_v1.RecognitionConfig.AudioEncoding.OGG_OPUS,
            }
            
            config = speech_v1.RecognitionConfig(
                encoding=encoding_map.get(encoding, speech_v1.RecognitionConfig.AudioEncoding.MULAW),
                sample_rate_hertz=sample_rate_hertz,
                language_code=language_code,
                enable_automatic_punctuation=True,
                model="phone_call",  # Optimisé pour les appels téléphoniques
            )
            
            # Transcription
            response = self.client.recognize(config=config, audio=audio)
            
            # Récupération du texte
            if response.results:
                transcript = " ".join([
                    result.alternatives[0].transcript
                    for result in response.results
                ])
                return transcript
            
            return None
            
        except Exception as e:
            print(f"Erreur lors de la transcription: {e}")
            return None
    
    def transcribe_audio_file(
        self,
        audio_file_path: str,
        language_code: str = "fr-FR"
    ) -> Optional[str]:
        """
        Transcrit un fichier audio depuis un chemin
        
        Args:
            audio_file_path: Chemin vers le fichier audio
            language_code: Code de langue
            
        Returns:
            Texte transcrit ou None si erreur
        """
        if not self.is_configured():
            raise ValueError("Google Cloud STT n'est pas configuré")
        
        try:
            with io.open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
            
            return self.transcribe_audio(
                audio_content=content,
                language_code=language_code,
                encoding="LINEAR16",
                sample_rate_hertz=16000
            )
            
        except Exception as e:
            print(f"Erreur lors de la transcription du fichier: {e}")
            return None
    
    def transcribe_streaming(
        self,
        audio_stream,
        language_code: str = "fr-FR",
        sample_rate_hertz: int = 16000
    ):
        """
        Transcrit un flux audio en temps réel
        
        Args:
            audio_stream: Générateur de chunks audio
            language_code: Code de langue
            sample_rate_hertz: Taux d'échantillonnage
            
        Yields:
            Résultats de transcription en temps réel
        """
        if not self.is_configured():
            raise ValueError("Google Cloud STT n'est pas configuré")
        
        try:
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate_hertz,
                language_code=language_code,
                enable_automatic_punctuation=True,
            )
            
            streaming_config = speech_v1.StreamingRecognitionConfig(
                config=config,
                interim_results=True
            )
            
            requests = (
                speech_v1.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in audio_stream
            )
            
            responses = self.client.streaming_recognize(streaming_config, requests)
            
            for response in responses:
                for result in response.results:
                    yield {
                        'transcript': result.alternatives[0].transcript,
                        'is_final': result.is_final,
                        'confidence': result.alternatives[0].confidence if result.is_final else 0
                    }
                    
        except Exception as e:
            print(f"Erreur lors de la transcription en streaming: {e}")
            yield None


# Instance globale
google_stt_manager = GoogleSTTManager()
