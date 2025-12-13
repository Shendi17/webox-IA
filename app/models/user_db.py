"""
Modèle User SQLAlchemy - Base de données PostgreSQL
Date : 30 Octobre 2025
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class UserDB(Base):
    """
    Modèle utilisateur pour PostgreSQL
    Table: users
    """
    __tablename__ = "users"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    
    # Statut et rôles
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    role = Column(String(50), default="user")  # user, admin, premium
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Préférences et configuration
    preferences = Column(JSON, default={})  # Préférences UI, thème, etc.
    api_keys = Column(JSON, default={})  # Clés API chiffrées de l'utilisateur
    settings = Column(JSON, default={})  # Paramètres divers
    
    # Relations
    conversations = relationship("ConversationDB", back_populates="user", cascade="all, delete-orphan")
    prompts = relationship("PromptDB", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    def to_dict(self):
        """Convertir en dictionnaire (sans le mot de passe)"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "is_premium": self.is_premium,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "preferences": self.preferences,
            "settings": self.settings
        }
