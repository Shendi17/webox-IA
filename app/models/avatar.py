from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Génération
    prompt = Column(Text)  # Prompt utilisé pour la génération
    style = Column(String(50))  # realistic, cartoon, anime, pixel-art, 3d
    gender = Column(String(20))  # male, female, neutral
    age_range = Column(String(20))  # child, teen, adult, senior
    
    # Personnalisation
    hair_color = Column(String(50))
    hair_style = Column(String(50))
    eye_color = Column(String(50))
    skin_tone = Column(String(50))
    accessories = Column(JSON)  # Liste d'accessoires
    clothing = Column(String(100))
    background = Column(String(100))
    
    # Images
    image_url = Column(String(500))
    thumbnail_url = Column(String(500))
    image_size = Column(Integer)  # en bytes
    image_format = Column(String(10), default="png")  # png, jpg, svg
    
    # Métadonnées
    ai_model = Column(String(50))  # dall-e-3, stable-diffusion, flux, etc.
    generation_time = Column(Integer)  # temps en secondes
    settings = Column(JSON)  # paramètres additionnels
    
    # Statistiques
    downloads_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    is_public = Column(Integer, default=0)  # 0=privé, 1=public
    
    # Tags et catégories
    tags = Column(JSON)  # Liste de tags
    category = Column(String(50))  # profile, gaming, business, social, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "prompt": self.prompt,
            "style": self.style,
            "gender": self.gender,
            "age_range": self.age_range,
            "hair_color": self.hair_color,
            "hair_style": self.hair_style,
            "eye_color": self.eye_color,
            "skin_tone": self.skin_tone,
            "accessories": self.accessories,
            "clothing": self.clothing,
            "background": self.background,
            "image_url": self.image_url,
            "thumbnail_url": self.thumbnail_url,
            "image_size": self.image_size,
            "image_format": self.image_format,
            "ai_model": self.ai_model,
            "generation_time": self.generation_time,
            "settings": self.settings,
            "downloads_count": self.downloads_count,
            "shares_count": self.shares_count,
            "is_public": self.is_public,
            "tags": self.tags,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
