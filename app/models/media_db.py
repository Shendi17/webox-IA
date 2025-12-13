"""
Modèle Media SQLAlchemy - Fichiers uploadés
Date : 2 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from datetime import datetime
from app.database import Base


class MediaDB(Base):
    """
    Modèle pour les fichiers média
    Table: media
    """
    __tablename__ = "media"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)  # Nom original
    stored_filename = Column(String(255), unique=True, nullable=False)  # Nom stocké (unique)
    file_path = Column(String(500), nullable=False)  # Chemin complet
    file_type = Column(String(100), nullable=False)  # image, video, audio, document, other
    mime_type = Column(String(100), nullable=False)  # image/png, video/mp4, etc.
    file_size = Column(BigInteger, nullable=False)  # Taille en bytes
    
    # Métadonnées
    user_id = Column(Integer, nullable=True)  # ID de l'utilisateur
    user_email = Column(String(255), nullable=True)  # Email de l'utilisateur
    
    # Dimensions (pour images/vidéos)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)  # Durée en secondes (pour vidéos/audio)
    
    # URL publique
    public_url = Column(String(500), nullable=True)
    
    # Statut
    is_public = Column(Boolean, default=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Media(id={self.id}, filename='{self.filename}')>"
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "mime_type": self.mime_type,
            "file_size": self.file_size,
            "file_size_mb": round(self.file_size / (1024 * 1024), 2),
            "width": self.width,
            "height": self.height,
            "duration": self.duration,
            "public_url": self.public_url,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_email": self.user_email
        }
