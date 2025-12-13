import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import google.generativeai as genai
from openai import OpenAI

class PodcastService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        
        # Configuration Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configuration OpenAI (pour DALL-E et TTS)
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Dossiers de stockage
        self.audio_dir = Path("static/podcasts/audio")
        self.cover_dir = Path("static/podcasts/covers")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.cover_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_script(self, topic: str, style: str, duration: int, language: str = "fr") -> Dict:
        """
        Génère un script de podcast avec Gemini
        
        Args:
            topic: Sujet du podcast
            style: Style (conversational, educational, storytelling, interview)
            duration: Durée cible en minutes
            language: Langue (fr, en, es, etc.)
        
        Returns:
            Dict avec script et segments
        """
        try:
            # Calculer le nombre de mots approximatif (150 mots/minute en français)
            target_words = duration * 150
            
            # Prompts par style
            style_prompts = {
                "conversational": "un style conversationnel et décontracté, comme une discussion entre amis",
                "educational": "un style éducatif et informatif, clair et structuré",
                "storytelling": "un style narratif captivant, avec des anecdotes et des histoires",
                "interview": "un style interview avec questions-réponses dynamiques"
            }
            
            style_desc = style_prompts.get(style, style_prompts["conversational"])
            
            prompt = f"""Tu es un expert en création de podcasts. Crée un script de podcast complet sur le sujet suivant :

SUJET : {topic}
STYLE : {style_desc}
DURÉE CIBLE : {duration} minutes (environ {target_words} mots)
LANGUE : {language}

Le script doit contenir :
1. Une introduction accrocheuse (30 secondes)
2. Le contenu principal divisé en 3-5 segments
3. Une conclusion mémorable (30 secondes)

Pour chaque segment, indique :
- Le titre du segment
- Le contenu (texte à lire)
- La durée estimée

Format de réponse en JSON :
{{
    "title": "Titre du podcast",
    "introduction": "Texte de l'introduction...",
    "segments": [
        {{
            "title": "Titre du segment",
            "content": "Contenu du segment...",
            "duration": 120
        }}
    ],
    "conclusion": "Texte de la conclusion...",
    "total_words": 450,
    "estimated_duration": 180
}}

Crée un contenu engageant, informatif et professionnel."""

            if self.gemini_api_key:
                response = self.gemini_model.generate_content(prompt)
                script_text = response.text
                
                # Extraire le JSON de la réponse
                if "```json" in script_text:
                    script_text = script_text.split("```json")[1].split("```")[0].strip()
                elif "```" in script_text:
                    script_text = script_text.split("```")[1].split("```")[0].strip()
                
                script_data = json.loads(script_text)
                
                return {
                    "success": True,
                    "script": script_data,
                    "model": "gemini-2.0-flash"
                }
            else:
                return {
                    "success": False,
                    "error": "Clé API Gemini non configurée"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération du script : {str(e)}"
            }
    
    def generate_cover_art(self, title: str, topic: str, style: str) -> Dict:
        """
        Génère une image de couverture avec DALL-E 3
        
        Args:
            title: Titre du podcast
            topic: Sujet
            style: Style visuel
        
        Returns:
            Dict avec URL de l'image
        """
        try:
            if not self.openai_api_key:
                return {
                    "success": False,
                    "error": "Clé API OpenAI non configurée"
                }
            
            # Créer un prompt pour DALL-E
            prompt = f"""Create a professional podcast cover art for a podcast titled "{title}" about {topic}.
Style: Modern, clean, professional podcast artwork.
Include: Microphone icon, wave patterns, vibrant colors.
Text: "{title}" in bold, readable font.
Aspect: Square format, suitable for podcast platforms."""

            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            return {
                "success": True,
                "image_url": image_url,
                "prompt": prompt
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération de la couverture : {str(e)}"
            }
    
    def text_to_speech(self, text: str, voice: str = "alloy", output_file: str = None) -> Dict:
        """
        Convertit le texte en audio avec OpenAI TTS
        
        Args:
            text: Texte à convertir
            voice: Voix à utiliser (alloy, echo, fable, onyx, nova, shimmer)
            output_file: Chemin du fichier de sortie
        
        Returns:
            Dict avec chemin du fichier audio
        """
        try:
            if not self.openai_api_key:
                return {
                    "success": False,
                    "error": "Clé API OpenAI non configurée"
                }
            
            if not output_file:
                output_file = self.audio_dir / f"podcast_{int(time.time())}.mp3"
            
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            response.stream_to_file(output_file)
            
            # Obtenir la taille du fichier
            file_size = os.path.getsize(output_file)
            
            return {
                "success": True,
                "audio_file": str(output_file),
                "file_size": file_size
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération audio : {str(e)}"
            }
    
    def generate_full_podcast(self, podcast_data: Dict) -> Dict:
        """
        Génère un podcast complet (script + audio + cover)
        
        Args:
            podcast_data: Données du podcast (topic, style, duration, etc.)
        
        Returns:
            Dict avec toutes les données générées
        """
        start_time = time.time()
        
        try:
            # 1. Générer le script
            script_result = self.generate_script(
                topic=podcast_data.get("topic"),
                style=podcast_data.get("style", "conversational"),
                duration=podcast_data.get("duration", 5),
                language=podcast_data.get("language", "fr")
            )
            
            if not script_result.get("success"):
                return script_result
            
            script = script_result["script"]
            
            # 2. Générer la couverture
            cover_result = self.generate_cover_art(
                title=script.get("title", podcast_data.get("topic")),
                topic=podcast_data.get("topic"),
                style=podcast_data.get("style", "conversational")
            )
            
            # 3. Assembler le texte complet pour TTS
            full_text = f"{script['introduction']}\n\n"
            for segment in script['segments']:
                full_text += f"{segment['content']}\n\n"
            full_text += script['conclusion']
            
            # 4. Générer l'audio
            audio_result = self.text_to_speech(
                text=full_text,
                voice=podcast_data.get("voice", "alloy")
            )
            
            generation_time = int(time.time() - start_time)
            
            return {
                "success": True,
                "script": script,
                "cover_url": cover_result.get("image_url") if cover_result.get("success") else None,
                "cover_prompt": cover_result.get("prompt") if cover_result.get("success") else None,
                "audio_file": audio_result.get("audio_file") if audio_result.get("success") else None,
                "audio_size": audio_result.get("file_size") if audio_result.get("success") else None,
                "generation_time": generation_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération du podcast : {str(e)}"
            }
    
    def get_available_voices(self) -> List[Dict]:
        """
        Retourne la liste des voix disponibles
        """
        return [
            {"id": "alloy", "name": "Alloy", "gender": "neutral", "language": "multi"},
            {"id": "echo", "name": "Echo", "gender": "male", "language": "multi"},
            {"id": "fable", "name": "Fable", "gender": "neutral", "language": "multi"},
            {"id": "onyx", "name": "Onyx", "gender": "male", "language": "multi"},
            {"id": "nova", "name": "Nova", "gender": "female", "language": "multi"},
            {"id": "shimmer", "name": "Shimmer", "gender": "female", "language": "multi"}
        ]
    
    def get_podcast_styles(self) -> List[Dict]:
        """
        Retourne la liste des styles disponibles
        """
        return [
            {
                "id": "conversational",
                "name": "Conversationnel",
                "description": "Style décontracté, comme une discussion entre amis",
                "icon": "💬"
            },
            {
                "id": "educational",
                "name": "Éducatif",
                "description": "Style informatif et structuré pour apprendre",
                "icon": "📚"
            },
            {
                "id": "storytelling",
                "name": "Narratif",
                "description": "Style captivant avec histoires et anecdotes",
                "icon": "📖"
            },
            {
                "id": "interview",
                "name": "Interview",
                "description": "Style questions-réponses dynamique",
                "icon": "🎤"
            }
        ]
