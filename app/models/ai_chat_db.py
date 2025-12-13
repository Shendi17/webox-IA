"""
Modèles de base de données pour le chat IA
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class AIConversation(Base):
    """Conversation avec l'IA"""
    __tablename__ = "ai_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    title = Column(String(255), nullable=True)
    context = Column(JSON, nullable=True)  # Contexte du projet
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AIConversation(id={self.id}, project_id={self.project_id}, title='{self.title}')>"


class AIMessage(Base):
    """Message dans une conversation"""
    __tablename__ = "ai_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' ou 'assistant'
    content = Column(Text, nullable=False)
    actions = Column(JSON, nullable=True)  # Actions effectuées par l'IA
    message_metadata = Column(JSON, nullable=True)  # Métadonnées (tokens, durée, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    conversation = relationship("AIConversation", back_populates="messages")
    
    def __repr__(self):
        return f"<AIMessage(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"


class AIAction(Base):
    """Actions effectuées par l'IA"""
    __tablename__ = "ai_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("ai_messages.id"), nullable=False, index=True)
    action_type = Column(String(50), nullable=False)  # 'create_file', 'modify_file', etc.
    action_data = Column(JSON, nullable=False)  # Données de l'action
    status = Column(String(20), default='pending')  # 'pending', 'completed', 'failed'
    result = Column(JSON, nullable=True)  # Résultat de l'action
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<AIAction(id={self.id}, type='{self.action_type}', status='{self.status}')>"
