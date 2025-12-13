"""
Modèles SQLAlchemy pour les Influenceurs IA
Date : 15 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
from app.database import Base


class AIInfluencerDB(Base):
    """
    Modèle pour les influenceurs IA virtuels
    Table: ai_influencers
    """
    __tablename__ = "ai_influencers"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations du personnage
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    niche = Column(String(100), nullable=True)  # fitness, fashion, tech, lifestyle, etc.
    
    # Apparence
    gender = Column(String(20), nullable=True)  # male, female, non-binary
    ethnicity = Column(String(50), nullable=True)
    age_range = Column(String(20), nullable=True)  # 18-25, 26-35, etc.
    style = Column(String(100), nullable=True)  # casual, professional, sporty, etc.
    
    # Visage de référence
    face_image_url = Column(Text, nullable=True)
    face_embedding = Column(JSON, nullable=True)  # Vecteur d'embedding pour cohérence
    
    # Personnalité
    personality_traits = Column(JSON, nullable=True)  # ['energetic', 'friendly', 'professional']
    tone_of_voice = Column(String(50), nullable=True)  # casual, professional, funny, etc.
    
    # Paramètres de génération
    generation_settings = Column(JSON, nullable=True)
    
    # Statistiques
    total_posts = Column(Integer, default=0)
    total_images = Column(Integer, default=0)
    
    # Statut
    is_active = Column(Boolean, default=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AIInfluencer(id={self.id}, name='{self.name}', niche='{self.niche}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "niche": self.niche,
            "gender": self.gender,
            "ethnicity": self.ethnicity,
            "age_range": self.age_range,
            "style": self.style,
            "face_image_url": self.face_image_url,
            "personality_traits": self.personality_traits,
            "tone_of_voice": self.tone_of_voice,
            "generation_settings": self.generation_settings,
            "total_posts": self.total_posts,
            "total_images": self.total_images,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class InfluencerContentDB(Base):
    """
    Modèle pour le contenu généré par les influenceurs IA
    Table: influencer_content
    """
    __tablename__ = "influencer_content"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    influencer_id = Column(Integer, nullable=False, index=True)
    
    # Type de contenu
    content_type = Column(String(50), nullable=False)  # image, video, carousel
    
    # Contenu
    prompt = Column(Text, nullable=False)
    generated_url = Column(Text, nullable=True)
    caption = Column(Text, nullable=True)
    hashtags = Column(JSON, nullable=True)
    
    # Paramètres de génération
    pose = Column(String(100), nullable=True)  # standing, sitting, action, etc.
    location = Column(String(100), nullable=True)  # gym, beach, office, etc.
    outfit = Column(String(100), nullable=True)  # sportswear, casual, formal, etc.
    
    # Métadonnées
    generation_params = Column(JSON, nullable=True)
    cost = Column(Float, default=0.0)
    
    # Statut
    status = Column(String(50), default='pending')  # pending, generating, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<InfluencerContent(id={self.id}, type='{self.content_type}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "influencer_id": self.influencer_id,
            "content_type": self.content_type,
            "prompt": self.prompt,
            "generated_url": self.generated_url,
            "caption": self.caption,
            "hashtags": self.hashtags,
            "pose": self.pose,
            "location": self.location,
            "outfit": self.outfit,
            "generation_params": self.generation_params,
            "cost": self.cost,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
