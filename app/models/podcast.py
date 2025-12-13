from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    topic = Column(String(200))
    style = Column(String(50))  # conversational, educational, storytelling, interview
    duration = Column(Integer)  # en secondes
    language = Column(String(10), default="fr")
    
    # Script et contenu
    script = Column(Text)
    segments = Column(JSON)  # Liste des segments du podcast
    
    # Audio
    voice_id = Column(String(100))
    voice_name = Column(String(100))
    audio_url = Column(String(500))
    audio_size = Column(Integer)  # en bytes
    
    # Cover art
    cover_url = Column(String(500))
    cover_prompt = Column(Text)
    
    # Musique
    background_music = Column(String(200))
    music_volume = Column(Integer, default=20)  # 0-100
    
    # Métadonnées
    status = Column(String(20), default="draft")  # draft, generating, completed, failed
    generation_time = Column(Integer)  # temps de génération en secondes
    settings = Column(JSON)  # paramètres additionnels
    
    # Statistiques
    plays_count = Column(Integer, default=0)
    downloads_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "topic": self.topic,
            "style": self.style,
            "duration": self.duration,
            "language": self.language,
            "script": self.script,
            "segments": self.segments,
            "voice_id": self.voice_id,
            "voice_name": self.voice_name,
            "audio_url": self.audio_url,
            "audio_size": self.audio_size,
            "cover_url": self.cover_url,
            "cover_prompt": self.cover_prompt,
            "background_music": self.background_music,
            "music_volume": self.music_volume,
            "status": self.status,
            "generation_time": self.generation_time,
            "settings": self.settings,
            "plays_count": self.plays_count,
            "downloads_count": self.downloads_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
