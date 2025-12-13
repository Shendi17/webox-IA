import os
from typing import Dict, List
from openai import OpenAI

class VideoExportService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    async def generate_voice_for_dialogue(self, dialogue: str, character_name: str, 
                                         voice: str = "alloy") -> Dict:
        """Génère la voix pour un dialogue"""
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=dialogue
            )
            
            # Sauvegarder temporairement
            audio_path = f"temp/audio_{character_name}_{hash(dialogue)}.mp3"
            os.makedirs("temp", exist_ok=True)
            response.stream_to_file(audio_path)
            
            return {
                "success": True,
                "audio_path": audio_path,
                "duration": len(dialogue) * 0.1  # Approximation
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur génération voix : {str(e)}"
            }
    
    async def generate_background_music(self, mood: str, duration: int) -> Dict:
        """Génère ou sélectionne une musique de fond"""
        # Mapping des moods vers des styles musicaux
        music_styles = {
            "happy": "upbeat, cheerful, positive",
            "sad": "melancholic, slow, emotional",
            "tense": "suspenseful, dramatic, intense",
            "mysterious": "ambient, enigmatic, dark",
            "romantic": "soft, gentle, romantic",
            "action": "energetic, fast-paced, dynamic"
        }
        
        style = music_styles.get(mood, "ambient, neutral")
        
        return {
            "success": True,
            "music_style": style,
            "duration": duration,
            "message": "Musique de fond suggérée (intégration API musicale à ajouter)"
        }
    
    async def export_episode_to_video(self, episode_data: Dict, 
                                     include_voice: bool = True,
                                     include_music: bool = True) -> Dict:
        """Exporte un épisode en vidéo"""
        try:
            scenes = episode_data.get("scenes", [])
            video_segments = []
            
            for scene in scenes:
                segment = {
                    "image": scene.get("image_url"),
                    "duration": 5,  # 5 secondes par scène
                    "text": scene.get("description")
                }
                
                # Ajouter la voix si demandé
                if include_voice and scene.get("dialogue"):
                    voice_result = await self.generate_voice_for_dialogue(
                        scene["dialogue"],
                        scene.get("characters_present", ["narrator"])[0]
                    )
                    if voice_result["success"]:
                        segment["audio"] = voice_result["audio_path"]
                        segment["duration"] = voice_result["duration"]
                
                video_segments.append(segment)
            
            # Ajouter la musique de fond
            if include_music:
                total_duration = sum(s["duration"] for s in video_segments)
                music_result = await self.generate_background_music(
                    episode_data.get("mood", "neutral"),
                    int(total_duration)
                )
                if music_result["success"]:
                    episode_data["background_music"] = music_result
            
            return {
                "success": True,
                "video_segments": video_segments,
                "total_duration": sum(s["duration"] for s in video_segments),
                "message": "Vidéo prête à être compilée (nécessite FFmpeg)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur export vidéo : {str(e)}"
            }
    
    def get_voice_options(self) -> List[Dict]:
        """Retourne les voix disponibles"""
        return [
            {"id": "alloy", "name": "Alloy", "gender": "neutral", "description": "Voix neutre polyvalente"},
            {"id": "echo", "name": "Echo", "gender": "male", "description": "Voix masculine"},
            {"id": "fable", "name": "Fable", "gender": "male", "description": "Voix masculine expressive"},
            {"id": "onyx", "name": "Onyx", "gender": "male", "description": "Voix masculine profonde"},
            {"id": "nova", "name": "Nova", "gender": "female", "description": "Voix féminine"},
            {"id": "shimmer", "name": "Shimmer", "gender": "female", "description": "Voix féminine douce"}
        ]
    
    def compile_video_with_ffmpeg(self, segments: List[Dict], output_path: str) -> Dict:
        """Compile les segments en vidéo avec FFmpeg (placeholder)"""
        # Cette fonction nécessite FFmpeg installé
        # Commande exemple : ffmpeg -loop 1 -i image.jpg -i audio.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output.mp4
        
        return {
            "success": True,
            "output_path": output_path,
            "message": "Compilation vidéo (nécessite FFmpeg installé sur le serveur)"
        }
