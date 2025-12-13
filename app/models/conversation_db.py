"""
Modèles Conversation et Message SQLAlchemy
Date : 30 Octobre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ConversationDB(Base):
    """
    Modèle Conversation pour PostgreSQL
    Table: conversations
    """
    __tablename__ = "conversations"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    folder = Column(String(100), default="Général")
    
    # Nouvelles fonctionnalités
    is_favorite = Column(Boolean, default=False)  # Favori
    tags = Column(JSON, default=[])  # Tags personnalisés
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Métadonnées
    meta_data = Column(JSON, default={})  # Tags, catégories, etc.
    
    # Relations
    user = relationship("UserDB", back_populates="conversations")
    messages = relationship("MessageDB", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, title='{self.title}', user_id={self.user_id})>"
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "folder": self.folder,
            "is_favorite": self.is_favorite if hasattr(self, 'is_favorite') else False,
            "tags": self.tags if hasattr(self, 'tags') and self.tags else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "meta_data": self.meta_data,
            "message_count": len(self.messages) if self.messages else 0
        }


class MessageDB(Base):
    """
    Modèle Message pour PostgreSQL
    Table: messages
    """
    __tablename__ = "messages"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # Réponses multi-IA (JSON)
    ai_responses = Column(JSON, nullable=True)  # {"GPT-4": "...", "Claude": "...", ...}
    ai_provider = Column(String(50), nullable=True)  # Provider utilisé
    ai_model = Column(String(100), nullable=True)  # Modèle utilisé
    
    # Métadonnées
    tokens_used = Column(Integer, nullable=True)  # Nombre de tokens
    response_time = Column(Integer, nullable=True)  # Temps de réponse en ms
    meta_data = Column(JSON, default={})  # Autres métadonnées
    
    # Date
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    conversation = relationship("ConversationDB", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "ai_responses": self.ai_responses,
            "ai_provider": self.ai_provider,
            "ai_model": self.ai_model,
            "tokens_used": self.tokens_used,
            "response_time": self.response_time,
            "meta_data": self.meta_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
