from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base

class PWAProject(Base):
    __tablename__ = "pwa_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations générales
    name = Column(String(255), nullable=False)
    description = Column(Text)
    app_name = Column(String(255), nullable=False)  # Nom affiché de l'app
    short_name = Column(String(50))  # Nom court pour l'écran d'accueil
    
    # Configuration
    template = Column(String(100))  # landing, portfolio, blog, ecommerce, dashboard
    theme_color = Column(String(20), default="#667eea")
    background_color = Column(String(20), default="#ffffff")
    
    # Contenu
    pages = Column(JSON)  # Liste des pages générées
    features = Column(JSON)  # Fonctionnalités activées
    content = Column(JSON)  # Contenu personnalisé
    
    # Assets
    icon_url = Column(String(500))
    logo_url = Column(String(500))
    screenshots = Column(JSON)
    
    # Manifest PWA
    manifest_json = Column(JSON)
    service_worker_js = Column(Text)
    
    # Déploiement
    domain = Column(String(255))  # Domaine personnalisé
    subdomain = Column(String(100))  # Sous-domaine webox
    deploy_url = Column(String(500))  # URL de déploiement
    
    # Statut
    status = Column(String(50), default="draft")  # draft, generating, ready, deployed
    generation_progress = Column(Integer, default=0)
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(Text)
    keywords = Column(JSON)
    
    # Analytics
    views_count = Column(Integer, default=0)
    installs_count = Column(Integer, default=0)
    
    # Paramètres techniques
    offline_mode = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=False)
    cache_strategy = Column(String(50), default="network-first")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deployed_at = Column(DateTime(timezone=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "app_name": self.app_name,
            "short_name": self.short_name,
            "template": self.template,
            "theme_color": self.theme_color,
            "background_color": self.background_color,
            "pages": self.pages,
            "features": self.features,
            "content": self.content,
            "icon_url": self.icon_url,
            "logo_url": self.logo_url,
            "screenshots": self.screenshots,
            "manifest_json": self.manifest_json,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "deploy_url": self.deploy_url,
            "status": self.status,
            "generation_progress": self.generation_progress,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "keywords": self.keywords,
            "views_count": self.views_count,
            "installs_count": self.installs_count,
            "offline_mode": self.offline_mode,
            "push_notifications": self.push_notifications,
            "cache_strategy": self.cache_strategy,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deployed_at": self.deployed_at.isoformat() if self.deployed_at else None
        }
