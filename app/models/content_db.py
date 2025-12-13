"""
Modèles SQLAlchemy pour le Content Engine
Date : 23 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class ContentType(str, enum.Enum):
    """Types de contenus"""
    BLOG = "blog"
    SOCIAL = "social"
    VIDEO = "video"
    AUDIO = "audio"
    EMAIL = "email"
    LANDING = "landing"
    AD = "ad"
    OTHER = "other"


class ContentStatus(str, enum.Enum):
    """Statuts de contenu"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class SocialPlatform(str, enum.Enum):
    """Plateformes sociales"""
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    PINTEREST = "pinterest"


class Content(Base):
    """
    Modèle pour les contenus générés
    Table: contents
    """
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations de base
    title = Column(String(500), nullable=False)
    slug = Column(String(500), nullable=True, index=True)
    
    # Type et format
    content_type = Column(Enum(ContentType), nullable=False, index=True)
    format = Column(String(100), nullable=True)  # article, carousel, reel, etc.
    
    # Contenu
    content = Column(Text, nullable=True)  # Contenu principal (texte, HTML, markdown)
    summary = Column(Text, nullable=True)  # Résumé/description
    
    # Métadonnées
    keywords = Column(JSON, nullable=True)  # Liste de mots-clés
    hashtags = Column(JSON, nullable=True)  # Liste de hashtags
    tags = Column(JSON, nullable=True)  # Tags personnalisés
    
    # SEO
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(500), nullable=True)
    seo_score = Column(Integer, default=0)  # Score SEO 0-100
    
    # Médias
    featured_image = Column(String(500), nullable=True)
    images = Column(JSON, nullable=True)  # Liste d'URLs d'images
    video_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    
    # Réseaux sociaux
    platform = Column(Enum(SocialPlatform), nullable=True)
    platform_specific = Column(JSON, nullable=True)  # Données spécifiques à la plateforme
    
    # Statut et publication
    status = Column(Enum(ContentStatus), default=ContentStatus.DRAFT, index=True)
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    
    # Paramètres de génération
    generation_params = Column(JSON, nullable=True)  # Paramètres utilisés pour la génération
    ai_model = Column(String(100), nullable=True)  # Modèle IA utilisé
    
    # Statistiques
    word_count = Column(Integer, default=0)
    reading_time = Column(Integer, default=0)  # En minutes
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    
    # Auteur
    author_id = Column(Integer, nullable=False, index=True)
    author_name = Column(String(255), nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    calendar_entries = relationship("ContentCalendar", back_populates="content", cascade="all, delete-orphan")
    analytics = relationship("ContentAnalytics", back_populates="content", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', type={self.content_type})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content_type": self.content_type.value if self.content_type else None,
            "format": self.format,
            "content": self.content,
            "summary": self.summary,
            "keywords": self.keywords,
            "hashtags": self.hashtags,
            "tags": self.tags,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "seo_score": self.seo_score,
            "featured_image": self.featured_image,
            "images": self.images,
            "platform": self.platform.value if self.platform else None,
            "status": self.status.value if self.status else None,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "word_count": self.word_count,
            "reading_time": self.reading_time,
            "views": self.views,
            "likes": self.likes,
            "shares": self.shares,
            "author_name": self.author_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ContentTemplate(Base):
    """
    Modèle pour les templates de contenus
    Table: content_templates
    """
    __tablename__ = "content_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Type
    content_type = Column(Enum(ContentType), nullable=False, index=True)
    format = Column(String(100), nullable=True)
    
    # Template
    template_content = Column(Text, nullable=False)  # Template avec variables
    variables = Column(JSON, nullable=True)  # Liste des variables disponibles
    
    # Configuration
    default_params = Column(JSON, nullable=True)  # Paramètres par défaut
    
    # Catégorie
    category = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)
    
    # Statistiques
    usage_count = Column(Integer, default=0)
    
    # Auteur
    author_id = Column(Integer, nullable=False)
    is_public = Column(Boolean, default=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ContentTemplate(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "content_type": self.content_type.value if self.content_type else None,
            "format": self.format,
            "template_content": self.template_content,
            "variables": self.variables,
            "category": self.category,
            "usage_count": self.usage_count,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ContentCalendar(Base):
    """
    Modèle pour le calendrier éditorial
    Table: content_calendar
    """
    __tablename__ = "content_calendar"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec le contenu
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    
    # Informations
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    
    # Type et plateforme
    content_type = Column(Enum(ContentType), nullable=False)
    platform = Column(Enum(SocialPlatform), nullable=True)
    
    # Planification
    scheduled_date = Column(DateTime, nullable=False, index=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String(255), nullable=True)  # Format iCal RRULE
    
    # Statut
    status = Column(String(50), default="planned")  # planned, in_progress, completed, cancelled
    
    # Assignation
    assigned_to = Column(Integer, nullable=True)
    
    # Auteur
    author_id = Column(Integer, nullable=False, index=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relations
    content = relationship("Content", back_populates="calendar_entries")
    
    def __repr__(self):
        return f"<ContentCalendar(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "content_id": self.content_id,
            "title": self.title,
            "description": self.description,
            "content_type": self.content_type.value if self.content_type else None,
            "platform": self.platform.value if self.platform else None,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "is_recurring": self.is_recurring,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class ContentAnalytics(Base):
    """
    Modèle pour les analytics de contenus
    Table: content_analytics
    """
    __tablename__ = "content_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec le contenu
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, index=True)
    
    # Date
    date = Column(DateTime, nullable=False, index=True)
    
    # Métriques d'engagement
    views = Column(Integer, default=0)
    unique_views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    
    # Métriques de temps
    avg_time_spent = Column(Integer, default=0)  # En secondes
    bounce_rate = Column(Float, default=0.0)  # Pourcentage
    
    # Métriques de conversion
    conversions = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)  # Pourcentage
    revenue = Column(Float, default=0.0)
    
    # Métriques SEO
    organic_traffic = Column(Integer, default=0)
    search_impressions = Column(Integer, default=0)
    search_clicks = Column(Integer, default=0)
    avg_position = Column(Float, default=0.0)
    
    # Source de trafic
    traffic_sources = Column(JSON, nullable=True)  # {source: count}
    
    # Données brutes
    raw_data = Column(JSON, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    content = relationship("Content", back_populates="analytics")
    
    def __repr__(self):
        return f"<ContentAnalytics(id={self.id}, content_id={self.content_id})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "content_id": self.content_id,
            "date": self.date.isoformat() if self.date else None,
            "views": self.views,
            "likes": self.likes,
            "shares": self.shares,
            "comments": self.comments,
            "clicks": self.clicks,
            "conversions": self.conversions,
            "conversion_rate": self.conversion_rate,
            "organic_traffic": self.organic_traffic,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
