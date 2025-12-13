"""
Modèle Article SQLAlchemy - Articles de blog
Date : 2 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ArticleDB(Base):
    """
    Modèle article de blog
    Table: articles
    """
    __tablename__ = "articles"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    excerpt = Column(Text, nullable=True)  # Résumé
    content = Column(Text, nullable=False)  # Contenu complet
    image_url = Column(String(500), nullable=True)  # URL de l'image
    
    # Catégorie
    category = Column(String(100), default="Nouveautés")  # Nouveautés, Tutoriels, Guides, Outils, Analyses
    
    # Auteur
    author_id = Column(Integer, nullable=True)  # Pas de FK pour éviter les dépendances
    author_name = Column(String(255), default="WeBox Team")
    
    # Métadonnées
    views = Column(Integer, default=0)
    reading_time = Column(Integer, default=5)  # En minutes
    is_published = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # Article à la une
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "excerpt": self.excerpt,
            "content": self.content,
            "image_url": self.image_url,
            "category": self.category,
            "author_name": self.author_name,
            "views": self.views,
            "reading_time": self.reading_time,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None
        }
