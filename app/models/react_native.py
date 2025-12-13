from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base

class ReactNativeProject(Base):
    __tablename__ = "react_native_projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations générales
    name = Column(String(255), nullable=False)
    description = Column(Text)
    app_name = Column(String(255), nullable=False)
    package_name = Column(String(255))  # com.example.app
    
    # Configuration
    template = Column(String(100))  # social, fitness, food, finance, productivity
    platform = Column(String(50), default="both")  # ios, android, both
    navigation_type = Column(String(50), default="stack")  # stack, tab, drawer
    
    # Contenu
    screens = Column(JSON)  # Liste des écrans générés
    components = Column(JSON)  # Composants personnalisés
    features = Column(JSON)  # Fonctionnalités activées
    
    # Assets
    icon_url = Column(String(500))
    splash_screen_url = Column(String(500))
    screenshots = Column(JSON)
    
    # Code généré
    app_js = Column(Text)  # Code App.js principal
    navigation_js = Column(Text)  # Configuration navigation
    theme_js = Column(Text)  # Thème et styles
    
    # Packages
    dependencies = Column(JSON)  # Liste des dépendances npm
    
    # Statut
    status = Column(String(50), default="draft")  # draft, generating, ready, building
    generation_progress = Column(Integer, default=0)
    
    # Build
    build_android = Column(Boolean, default=False)
    build_ios = Column(Boolean, default=False)
    apk_url = Column(String(500))
    ipa_url = Column(String(500))
    
    # Statistiques
    downloads_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "app_name": self.app_name,
            "package_name": self.package_name,
            "template": self.template,
            "platform": self.platform,
            "navigation_type": self.navigation_type,
            "screens": self.screens,
            "components": self.components,
            "features": self.features,
            "icon_url": self.icon_url,
            "splash_screen_url": self.splash_screen_url,
            "screenshots": self.screenshots,
            "dependencies": self.dependencies,
            "status": self.status,
            "generation_progress": self.generation_progress,
            "build_android": self.build_android,
            "build_ios": self.build_ios,
            "apk_url": self.apk_url,
            "ipa_url": self.ipa_url,
            "downloads_count": self.downloads_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
