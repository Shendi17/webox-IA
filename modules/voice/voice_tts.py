"""Module de synthèse vocale (Text-to-Speech) avec Google Cloud"""
import os
from typing import Optional, List, Dict
from google.cloud import texttospeech_v1
from google.oauth2 import service_account
import base64


class GoogleTTSManager:
    """Gestionnaire de synthèse vocale avec Google Cloud Text-to-Speech"""
    
    # Voix disponibles en français
    FRENCH_VOICES = {
        "fr-FR-Standard-A": {"gender": "FEMALE", "description": "Voix féminine standard"},
        "fr-FR-Standard-B": {"gender": "MALE", "description": "Voix masculine standard"},
        "fr-FR-Standard-C": {"gender": "FEMALE", "description": "Voix féminine standard 2"},
        "fr-FR-Standard-D": {"gender": "MALE", "description": "Voix masculine standard 2"},
        "fr-FR-Wavenet-A": {"gender": "FEMALE", "description": "Voix féminine WaveNet (haute qualité)"},
        "fr-FR-Wavenet-B": {"gender": "MALE", "description": "Voix masculine WaveNet (haute qualité)"},
        "fr-FR-Wavenet-C": {"gender": "FEMALE", "description": "Voix féminine WaveNet 2"},
        "fr-FR-Wavenet-D": {"gender": "MALE", "description": "Voix masculine WaveNet 2"},
        "fr-FR-Neural2-A": {"gender": "FEMALE", "description": "Voix féminine Neural2 (très haute qualité)"},
        "fr-FR-Neural2-B": {"gender": "MALE", "description": "Voix masculine Neural2 (très haute qualité)"},
    }
    
    def __init__(self):
        """Initialise le client Google Cloud Text-to-Speech"""
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            self.client = texttospeech_v1.TextToSpeechClient(credentials=credentials)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        """Vérifie si Google Cloud TTS est configuré"""
        return self.client is not None
    
    def synthesize_speech(
        self,
        text: str,
        voice_name: str = "fr-FR-Neural2-A",
        language_code: str = "fr-FR",
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
        audio_encoding: str = "MP3"
    ) -> Optional[bytes]:
        """
        Synthétise du texte en audio
        
        Args:
            text: Texte à synthétiser
            voice_name: Nom de la voix à utiliser
            language_code: Code de langue
            speaking_rate: Vitesse de parole (0.25 à 4.0)
            pitch: Hauteur de la voix (-20.0 à 20.0)
            audio_encoding: Format audio (MP3, LINEAR16, OGG_OPUS, MULAW)
            
        Returns:
            Contenu audio en bytes ou None si erreur
        """
        if not self.is_configured():
            raise ValueError("Google Cloud TTS n'est pas configuré")
        
        try:
            # Configuration du texte
            synthesis_input = texttospeech_v1.SynthesisInput(text=text)
            
            # Configuration de la voix
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )
            
            # Mapping des encodages
            encoding_map = {
                "MP3": texttospeech_v1.AudioEncoding.MP3,
                "LINEAR16": texttospeech_v1.AudioEncoding.LINEAR16,
                "OGG_OPUS": texttospeech_v1.AudioEncoding.OGG_OPUS,
                "MULAW": texttospeech_v1.AudioEncoding.MULAW,
            }
            
            # Configuration audio
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=encoding_map.get(audio_encoding, texttospeech_v1.AudioEncoding.MP3),
                speaking_rate=speaking_rate,
                pitch=pitch
            )
            
            # Synthèse
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            print(f"Erreur lors de la synthèse vocale: {e}")
            return None
    
    def synthesize_to_file(
        self,
        text: str,
        output_path: str,
        voice_name: str = "fr-FR-Neural2-A",
        **kwargs
    ) -> bool:
        """
        Synthétise du texte et sauvegarde dans un fichier
        
        Args:
            text: Texte à synthétiser
            output_path: Chemin du fichier de sortie
            voice_name: Nom de la voix
            **kwargs: Arguments supplémentaires pour synthesize_speech
            
        Returns:
            True si succès, False sinon
        """
        audio_content = self.synthesize_speech(text, voice_name, **kwargs)
        
        if audio_content:
            try:
                with open(output_path, "wb") as out:
                    out.write(audio_content)
                return True
            except Exception as e:
                print(f"Erreur lors de la sauvegarde: {e}")
                return False
        
        return False
    
    def synthesize_ssml(
        self,
        ssml: str,
        voice_name: str = "fr-FR-Neural2-A",
        language_code: str = "fr-FR",
        audio_encoding: str = "MP3"
    ) -> Optional[bytes]:
        """
        Synthétise du SSML (Speech Synthesis Markup Language) en audio
        
        Args:
            ssml: Texte SSML à synthétiser
            voice_name: Nom de la voix
            language_code: Code de langue
            audio_encoding: Format audio
            
        Returns:
            Contenu audio en bytes ou None si erreur
        """
        if not self.is_configured():
            raise ValueError("Google Cloud TTS n'est pas configuré")
        
        try:
            synthesis_input = texttospeech_v1.SynthesisInput(ssml=ssml)
            
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name
            )
            
            encoding_map = {
                "MP3": texttospeech_v1.AudioEncoding.MP3,
                "LINEAR16": texttospeech_v1.AudioEncoding.LINEAR16,
                "OGG_OPUS": texttospeech_v1.AudioEncoding.OGG_OPUS,
                "MULAW": texttospeech_v1.AudioEncoding.MULAW,
            }
            
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=encoding_map.get(audio_encoding, texttospeech_v1.AudioEncoding.MP3)
            )
            
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            print(f"Erreur lors de la synthèse SSML: {e}")
            return None
    
    def get_available_voices(self, language_code: str = "fr-FR") -> List[Dict]:
        """
        Récupère la liste des voix disponibles
        
        Args:
            language_code: Code de langue pour filtrer
            
        Returns:
            Liste des voix disponibles
        """
        if not self.is_configured():
            return []
        
        try:
            response = self.client.list_voices(language_code=language_code)
            
            voices = []
            for voice in response.voices:
                voices.append({
                    'name': voice.name,
                    'language_codes': voice.language_codes,
                    'gender': texttospeech_v1.SsmlVoiceGender(voice.ssml_gender).name,
                    'natural_sample_rate': voice.natural_sample_rate_hertz
                })
            
            return voices
            
        except Exception as e:
            print(f"Erreur lors de la récupération des voix: {e}")
            return []
    
    def get_french_voices(self) -> Dict[str, Dict]:
        """
        Retourne les voix françaises prédéfinies
        
        Returns:
            Dictionnaire des voix françaises
        """
        return self.FRENCH_VOICES
    
    def synthesize_for_phone(
        self,
        text: str,
        voice_name: str = "fr-FR-Neural2-A"
    ) -> Optional[bytes]:
        """
        Synthétise du texte optimisé pour téléphone (format MULAW)
        
        Args:
            text: Texte à synthétiser
            voice_name: Nom de la voix
            
        Returns:
            Contenu audio en bytes (format MULAW 8kHz)
        """
        return self.synthesize_speech(
            text=text,
            voice_name=voice_name,
            audio_encoding="MULAW",
            speaking_rate=0.95  # Légèrement plus lent pour la clarté
        )


# Instance globale
google_tts_manager = GoogleTTSManager()
