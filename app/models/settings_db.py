"""
Modèle Settings SQLAlchemy - Configuration globale de l'application
Date : 2 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from datetime import datetime
from app.database import Base


class SettingsDB(Base):
    """
    Modèle pour les paramètres globaux de l'application
    Table: settings
    """
    __tablename__ = "settings"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)  # Nom du paramètre
    value = Column(Text, nullable=True)  # Valeur (peut être JSON stringifié)
    category = Column(String(100), default="general")  # Catégorie (api_keys, billing, etc.)
    is_encrypted = Column(Boolean, default=False)  # Si la valeur est chiffrée
    description = Column(Text, nullable=True)  # Description du paramètre
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(String(255), nullable=True)  # Email de l'admin qui a modifié
    
    def __repr__(self):
        return f"<Settings(key='{self.key}', category='{self.category}')>"
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "category": self.category,
            "is_encrypted": self.is_encrypted,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by
        }
