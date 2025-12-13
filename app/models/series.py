from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations générales
    title = Column(String(255), nullable=False)
    description = Column(Text)
    genre = Column(String(100))  # Drama, Comedy, Sci-Fi, Fantasy, etc.
    target_audience = Column(String(100))  # Kids, Teens, Adults, All
    
    # Configuration
    num_episodes = Column(Integer, default=10)
    episode_duration = Column(Integer, default=5)  # minutes
    style = Column(String(100))  # realistic, cartoon, anime, comic
    
    # Contenu généré
    synopsis = Column(Text)  # Synopsis général de la série
    characters = Column(JSON)  # Liste des personnages principaux
    storyline = Column(Text)  # Arc narratif principal
    
    # Métadonnées
    cover_image_url = Column(String(500))
    thumbnail_url = Column(String(500))
    tags = Column(JSON)  # Tags pour recherche
    
    # Statut
    status = Column(String(50), default="draft")  # draft, generating, completed, published
    generation_progress = Column(Integer, default=0)  # 0-100
    
    # Statistiques
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # Paramètres de génération
    ai_model = Column(String(50), default="gemini-2.0-flash")
    image_model = Column(String(50), default="dall-e-3")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "target_audience": self.target_audience,
            "num_episodes": self.num_episodes,
            "episode_duration": self.episode_duration,
            "style": self.style,
            "synopsis": self.synopsis,
            "characters": self.characters,
            "storyline": self.storyline,
            "cover_image_url": self.cover_image_url,
            "thumbnail_url": self.thumbnail_url,
            "tags": self.tags,
            "status": self.status,
            "generation_progress": self.generation_progress,
            "views_count": self.views_count,
            "likes_count": self.likes_count,
            "shares_count": self.shares_count,
            "ai_model": self.ai_model,
            "image_model": self.image_model,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None
        }


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    episode_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Contenu
    script = Column(Text)  # Script complet de l'épisode
    scenes = Column(JSON)  # Liste des scènes avec descriptions
    
    # Images générées
    thumbnail_url = Column(String(500))
    scene_images = Column(JSON)  # URLs des images de scènes
    
    # Métadonnées
    duration = Column(Integer)  # minutes
    characters_featured = Column(JSON)  # Personnages dans cet épisode
    
    # Statut
    status = Column(String(50), default="draft")  # draft, generating, completed
    generation_progress = Column(Integer, default=0)
    
    # Statistiques
    views_count = Column(Integer, default=0)
    completion_rate = Column(Integer, default=0)  # % de visionnage
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "series_id": self.series_id,
            "episode_number": self.episode_number,
            "title": self.title,
            "description": self.description,
            "script": self.script,
            "scenes": self.scenes,
            "thumbnail_url": self.thumbnail_url,
            "scene_images": self.scene_images,
            "duration": self.duration,
            "characters_featured": self.characters_featured,
            "status": self.status,
            "generation_progress": self.generation_progress,
            "views_count": self.views_count,
            "completion_rate": self.completion_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    scene_number = Column(Integer, nullable=False)
    title = Column(String(255))
    
    # Contenu
    description = Column(Text, nullable=False)
    dialogue = Column(Text)
    action = Column(Text)
    
    # Image
    image_url = Column(String(500))
    image_prompt = Column(Text)
    
    # Métadonnées
    location = Column(String(255))  # Lieu de la scène
    time_of_day = Column(String(50))  # day, night, dawn, dusk
    mood = Column(String(100))  # happy, sad, tense, mysterious, etc.
    characters_present = Column(JSON)
    
    # Statut
    status = Column(String(50), default="draft")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "episode_id": self.episode_id,
            "scene_number": self.scene_number,
            "title": self.title,
            "description": self.description,
            "dialogue": self.dialogue,
            "action": self.action,
            "image_url": self.image_url,
            "image_prompt": self.image_prompt,
            "location": self.location,
            "time_of_day": self.time_of_day,
            "mood": self.mood,
            "characters_present": self.characters_present,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
