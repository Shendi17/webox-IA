"""
Modèle User SQLAlchemy - Base de données PostgreSQL
Date : 30 Octobre 2025
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.conversation_db import ConversationDB
    from app.models.prompt_db import PromptDB
    from app.models.product_db import CartItemDB, OrderDB


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
    
    # Vérification email
    email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    
    # 2FA (Authentification à deux facteurs)
    twofa_enabled = Column(Boolean, default=False)
    twofa_secret = Column(String(255), nullable=True)
    twofa_backup_codes = Column(JSON, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Préférences et configuration
    preferences = Column(JSON, default={})  # Préférences UI, thème, etc.
    api_keys = Column(JSON, default={})  # Clés API chiffrées de l'utilisateur
    settings = Column(JSON, default={})  # Paramètres divers
    
    # Relations (commentées temporairement pour éviter les erreurs de dépendances circulaires)
    # conversations = relationship("ConversationDB", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    # prompts = relationship("PromptDB", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    # cart_items = relationship("CartItemDB", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    # orders = relationship("OrderDB", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    
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
            "email_verified": self.email_verified,
            "email_verified_at": self.email_verified_at.isoformat() if self.email_verified_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "preferences": self.preferences,
            "settings": self.settings
        }
