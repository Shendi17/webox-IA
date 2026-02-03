"""
Modèles SQLAlchemy pour les Outils Business
Date : 15 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
from app.database import Base


class GeneratedLogoDB(Base):
    """
    Modèle pour les logos générés
    Table: generated_logos
    """
    __tablename__ = "generated_logos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations du logo
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=True)  # tech, food, fashion, etc.
    style = Column(String(100), nullable=True)  # minimalist, modern, vintage, etc.
    colors = Column(JSON, nullable=True)  # ['#FF5733', '#3498DB']
    symbols = Column(Text, nullable=True)
    
    # Génération
    prompt = Column(Text, nullable=False)
    variations = Column(JSON, nullable=True)  # URLs des 4 variations
    selected_variation = Column(Integer, default=0)
    
    # Pack complet
    logo_main_url = Column(Text, nullable=True)
    logo_horizontal_url = Column(Text, nullable=True)
    logo_vertical_url = Column(Text, nullable=True)
    logo_icon_url = Column(Text, nullable=True)
    favicon_url = Column(Text, nullable=True)
    
    # Métadonnées
    cost = Column(Float, default=0.0)
    status = Column(String(50), default='pending')
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "industry": self.industry,
            "style": self.style,
            "colors": self.colors,
            "variations": self.variations,
            "logo_main_url": self.logo_main_url,
            "cost": self.cost,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PresentationDB(Base):
    """
    Modèle pour les présentations générées
    Table: presentations
    """
    __tablename__ = "presentations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    title = Column(String(255), nullable=False)
    topic = Column(Text, nullable=False)
    audience = Column(String(100), nullable=True)  # investors, clients, team
    tone = Column(String(50), nullable=True)  # professional, creative, technical
    
    # Structure
    num_slides = Column(Integer, default=10)
    template = Column(String(100), nullable=True)  # modern, corporate, startup
    
    # Contenu
    slides = Column(JSON, nullable=True)  # Structure complète
    generated_images = Column(JSON, nullable=True)  # URLs des images générées
    
    # Export
    pptx_url = Column(Text, nullable=True)
    pdf_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    
    # Métadonnées
    cost = Column(Float, default=0.0)
    status = Column(String(50), default='pending')
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "topic": self.topic,
            "num_slides": self.num_slides,
            "template": self.template,
            "slides": self.slides,
            "pptx_url": self.pptx_url,
            "pdf_url": self.pdf_url,
            "cost": self.cost,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class LandingPageDB(Base):
    """
    Modèle pour les landing pages
    Table: landing_pages
    """
    __tablename__ = "landing_pages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Design
    template = Column(String(100), nullable=True)  # saas, ecommerce, agency
    colors = Column(JSON, nullable=True)
    
    # Contenu
    sections = Column(JSON, nullable=True)  # hero, features, pricing, cta, etc.
    html_content = Column(Text, nullable=True)
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    meta_keywords = Column(JSON, nullable=True)
    
    # Analytics
    views = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    
    # Statut
    is_published = Column(Boolean, default=False)
    published_url = Column(Text, nullable=True)
    
    # Métadonnées
    cost = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "slug": self.slug,
            "title": self.title,
            "template": self.template,
            "is_published": self.is_published,
            "published_url": self.published_url,
            "views": self.views,
            "conversions": self.conversions,
            "conversion_rate": self.conversion_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
