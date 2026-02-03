from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float, Boolean
from sqlalchemy.sql import func
from app.database import Base

class AgentConversation(Base):
    __tablename__ = "agent_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    
    # Métadonnées
    title = Column(String(255))  # Titre auto-généré de la conversation
    context = Column(Text)  # Contexte de la conversation
    
    # Statistiques
    messages_count = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)
    
    # Paramètres
    model = Column(String(50), default="gemini-2.0-flash")
    temperature = Column(Integer, default=70)  # 0-100
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "title": self.title,
            "context": self.context,
            "messages_count": self.messages_count,
            "tokens_used": self.tokens_used,
            "model": self.model,
            "temperature": self.temperature,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, nullable=False, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    
    # Message
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    
    # Métadonnées
    model = Column(String(50))
    tokens = Column(Integer)
    response_time = Column(Integer)  # en millisecondes
    
    # Contexte additionnel
    extra_data = Column(JSON)  # Données additionnelles (images, fichiers, etc.)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "model": self.model,
            "tokens": self.tokens,
            "response_time": self.response_time,
            "extra_data": self.extra_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class AIAgent(Base):
    """Modèle pour les agents IA spécialisés"""
    __tablename__ = "ai_agents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)  # NULL pour agents marketplace
    
    # Informations de base
    name = Column(String(100), nullable=False)
    icon = Column(String(10), default="🤖")
    category = Column(String(50), nullable=False, index=True)  # marketing, sales, support, dev, finance
    status = Column(String(20), default="active")  # active, beta, premium
    description = Column(String(500))
    features = Column(JSON)  # Liste de fonctionnalités
    
    # Statistiques
    conversations = Column(Integer, default=0)
    tasks = Column(Integer, default=0)
    satisfaction = Column(Float, default=0.0)
    
    # Configuration IA
    model = Column(String(50), default="gpt-4")
    temperature = Column(Float, default=0.7)
    instructions = Column(Text)  # Instructions système
    
    # Marketplace
    is_marketplace = Column(Boolean, default=False, index=True)
    downloads = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    price = Column(String(20), default="Gratuit")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "icon": self.icon,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "features": self.features,
            "conversations": self.conversations,
            "tasks": self.tasks,
            "satisfaction": self.satisfaction,
            "model": self.model,
            "temperature": self.temperature,
            "instructions": self.instructions,
            "is_marketplace": self.is_marketplace,
            "downloads": self.downloads,
            "rating": self.rating,
            "price": self.price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
