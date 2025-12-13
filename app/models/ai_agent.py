from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
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
