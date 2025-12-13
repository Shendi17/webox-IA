"""
Modèles SQLAlchemy pour le Website Builder
Date : 15 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
from app.database import Base


class WebsiteDB(Base):
    """
    Modèle pour les sites web
    Table: websites
    """
    __tablename__ = "websites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    subdomain = Column(String(100), nullable=False, unique=True)  # monsite.webox.app
    custom_domain = Column(String(255), nullable=True)  # www.monsite.com
    
    # Configuration
    site_type = Column(String(50), nullable=True)  # business, portfolio, blog, ecommerce, landing
    industry = Column(String(100), nullable=True)  # tech, food, fashion, etc.
    template = Column(String(100), nullable=True)  # modern, classic, minimal, creative
    
    # Design
    colors = Column(JSON, nullable=True)  # Palette de couleurs
    # Format: {"primary": "#667eea", "secondary": "#764ba2", "accent": "#ffd700"}
    fonts = Column(JSON, nullable=True)  # Polices
    # Format: {"heading": "Montserrat", "body": "Open Sans"}
    
    # Contenu
    pages = Column(JSON, nullable=True)  # Liste des pages
    # Format: [
    #   {
    #     "id": "home",
    #     "title": "Accueil",
    #     "slug": "/",
    #     "sections": [...],
    #     "meta": {...}
    #   }
    # ]
    
    # Navigation
    menu = Column(JSON, nullable=True)  # Menu de navigation
    footer = Column(JSON, nullable=True)  # Footer
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    meta_keywords = Column(JSON, nullable=True)
    favicon_url = Column(Text, nullable=True)
    
    # Features
    has_blog = Column(Boolean, default=False)
    has_ecommerce = Column(Boolean, default=False)
    has_contact_form = Column(Boolean, default=True)
    has_chatbot = Column(Boolean, default=False)
    has_analytics = Column(Boolean, default=True)
    
    # Analytics
    total_visits = Column(Integer, default=0)
    total_page_views = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    
    # Statut
    is_published = Column(Boolean, default=False)
    published_url = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_published_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "subdomain": self.subdomain,
            "custom_domain": self.custom_domain,
            "site_type": self.site_type,
            "industry": self.industry,
            "template": self.template,
            "colors": self.colors,
            "fonts": self.fonts,
            "pages": self.pages,
            "has_blog": self.has_blog,
            "has_ecommerce": self.has_ecommerce,
            "is_published": self.is_published,
            "published_url": self.published_url,
            "total_visits": self.total_visits,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class WebsitePageDB(Base):
    """
    Modèle pour les pages de site
    Table: website_pages
    """
    __tablename__ = "website_pages"
    
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)  # /about, /services, etc.
    
    # Contenu
    sections = Column(JSON, nullable=True)  # Sections de la page
    # Format: [
    #   {
    #     "type": "hero",
    #     "content": {...},
    #     "style": {...}
    #   }
    # ]
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    
    # Statut
    is_published = Column(Boolean, default=True)
    order = Column(Integer, default=0)  # Ordre dans le menu
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "website_id": self.website_id,
            "title": self.title,
            "slug": self.slug,
            "sections": self.sections,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "is_published": self.is_published,
            "order": self.order
        }


class BlogPostDB(Base):
    """
    Modèle pour les articles de blog
    Table: blog_posts
    """
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    excerpt = Column(Text, nullable=True)
    
    # Contenu
    content = Column(Text, nullable=False)  # HTML ou Markdown
    featured_image = Column(Text, nullable=True)
    
    # Catégories et tags
    category = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)
    
    # Auteur
    author_name = Column(String(255), nullable=True)
    author_image = Column(Text, nullable=True)
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    
    # Analytics
    views = Column(Integer, default=0)
    
    # Statut
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "website_id": self.website_id,
            "title": self.title,
            "slug": self.slug,
            "excerpt": self.excerpt,
            "content": self.content,
            "featured_image": self.featured_image,
            "category": self.category,
            "tags": self.tags,
            "author_name": self.author_name,
            "views": self.views,
            "is_published": self.is_published,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class WebsiteAnalyticsDB(Base):
    """
    Modèle pour les analytics de site
    Table: website_analytics
    """
    __tablename__ = "website_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, nullable=False, index=True)
    
    # Métriques
    date = Column(DateTime, default=datetime.utcnow, index=True)
    visits = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    page_views = Column(Integer, default=0)
    avg_time_on_site = Column(Integer, default=0)  # secondes
    bounce_rate = Column(Float, default=0.0)
    
    # Sources
    sources = Column(JSON, nullable=True)  # {"direct": 50, "google": 30, "social": 20}
    
    # Pages populaires
    top_pages = Column(JSON, nullable=True)  # [{"page": "/about", "views": 100}]
    
    def to_dict(self):
        return {
            "id": self.id,
            "website_id": self.website_id,
            "date": self.date.isoformat() if self.date else None,
            "visits": self.visits,
            "unique_visitors": self.unique_visitors,
            "page_views": self.page_views,
            "avg_time_on_site": self.avg_time_on_site,
            "bounce_rate": self.bounce_rate,
            "sources": self.sources,
            "top_pages": self.top_pages
        }
