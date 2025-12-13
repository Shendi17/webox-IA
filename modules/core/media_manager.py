"""Gestionnaire de médias pour WeBox Multi-IA"""
import os
import json
import base64
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Dossiers de stockage
MEDIA_DIR = "media"
IMAGES_DIR = os.path.join(MEDIA_DIR, "images")
AUDIO_DIR = os.path.join(MEDIA_DIR, "audio")
VIDEO_DIR = os.path.join(MEDIA_DIR, "videos")
GALLERY_FILE = os.path.join(MEDIA_DIR, "gallery.json")

# Créer les dossiers si nécessaire
for directory in [MEDIA_DIR, IMAGES_DIR, AUDIO_DIR, VIDEO_DIR]:
    os.makedirs(directory, exist_ok=True)


class MediaManager:
    """Gestionnaire de médias (images, audio, vidéo)"""
    
    def __init__(self):
        self.gallery = self.load_gallery()
    
    def load_gallery(self) -> Dict:
        """Charge la galerie depuis le fichier"""
        if os.path.exists(GALLERY_FILE):
            try:
                with open(GALLERY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"images": [], "audio": [], "videos": []}
        return {"images": [], "audio": [], "videos": []}
    
    def save_gallery(self):
        """Sauvegarde la galerie dans le fichier"""
        with open(GALLERY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.gallery, f, ensure_ascii=False, indent=2)
    
    def save_image(self, image_data: bytes, prompt: str, model: str, user_email: str) -> str:
        """Sauvegarde une image générée"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img_{timestamp}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Sauvegarder l'image
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        # Ajouter à la galerie
        image_entry = {
            "id": f"img_{timestamp}",
            "filename": filename,
            "filepath": filepath,
            "prompt": prompt,
            "model": model,
            "user": user_email,
            "created_at": datetime.now().isoformat(),
            "type": "image"
        }
        
        self.gallery["images"].insert(0, image_entry)
        self.save_gallery()
        
        return filepath
    
    def save_audio(self, audio_data: bytes, text: str, model: str, user_email: str, voice: str = "default") -> str:
        """Sauvegarde un fichier audio généré"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_{timestamp}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        # Sauvegarder l'audio
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        # Ajouter à la galerie
        audio_entry = {
            "id": f"audio_{timestamp}",
            "filename": filename,
            "filepath": filepath,
            "text": text,
            "model": model,
            "voice": voice,
            "user": user_email,
            "created_at": datetime.now().isoformat(),
            "type": "audio"
        }
        
        self.gallery["audio"].insert(0, audio_entry)
        self.save_gallery()
        
        return filepath
    
    def save_video(self, video_data: bytes, prompt: str, model: str, user_email: str) -> str:
        """Sauvegarde une vidéo générée"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_{timestamp}.mp4"
        filepath = os.path.join(VIDEO_DIR, filename)
        
        # Sauvegarder la vidéo
        with open(filepath, 'wb') as f:
            f.write(video_data)
        
        # Ajouter à la galerie
        video_entry = {
            "id": f"video_{timestamp}",
            "filename": filename,
            "filepath": filepath,
            "prompt": prompt,
            "model": model,
            "user": user_email,
            "created_at": datetime.now().isoformat(),
            "type": "video"
        }
        
        self.gallery["videos"].insert(0, video_entry)
        self.save_gallery()
        
        return filepath
    
    def get_images(self, user_email: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Récupère les images (filtrées par utilisateur si spécifié)"""
        images = self.gallery["images"]
        if user_email:
            images = [img for img in images if img.get("user") == user_email]
        return images[:limit]
    
    def get_audio(self, user_email: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Récupère les fichiers audio"""
        audio = self.gallery["audio"]
        if user_email:
            audio = [aud for aud in audio if aud.get("user") == user_email]
        return audio[:limit]
    
    def get_videos(self, user_email: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Récupère les vidéos"""
        videos = self.gallery["videos"]
        if user_email:
            videos = [vid for vid in videos if vid.get("user") == user_email]
        return videos[:limit]
    
    def delete_media(self, media_id: str, media_type: str) -> bool:
        """Supprime un média"""
        try:
            # Trouver le média
            media_list = self.gallery[f"{media_type}s"]
            media = next((m for m in media_list if m["id"] == media_id), None)
            
            if media:
                # Supprimer le fichier
                if os.path.exists(media["filepath"]):
                    os.remove(media["filepath"])
                
                # Supprimer de la galerie
                media_list.remove(media)
                self.save_gallery()
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
    
    def get_stats(self, user_email: Optional[str] = None) -> Dict:
        """Récupère les statistiques"""
        images = self.get_images(user_email)
        audio = self.get_audio(user_email)
        videos = self.get_videos(user_email)
        
        return {
            "total_images": len(images),
            "total_audio": len(audio),
            "total_videos": len(videos),
            "total_media": len(images) + len(audio) + len(videos)
        }
    
    def image_to_base64(self, filepath: str) -> str:
        """Convertit une image en base64 pour affichage"""
        try:
            with open(filepath, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            return ""


# Instance globale
media_manager = MediaManager()
