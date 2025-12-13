"""
Schémas Pydantic pour le chat et les conversations
Date : 30 Octobre 2025
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Requête pour envoyer un message"""
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=10000)
    selected_providers: List[str] = Field(default=["GPT-4"])
    selected_models: Dict[str, str] = Field(default={"GPT-4": "gpt-4-turbo"})
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, ge=1, le=4000)
    stream: bool = False


class ChatResponse(BaseModel):
    """Réponse du chat"""
    conversation_id: int
    message_id: int
    user_message: str
    ai_responses: Dict[str, str]  # {"GPT-4": "réponse...", "Claude": "réponse..."}
    tokens_used: Optional[int] = None
    response_time: Optional[int] = None
    created_at: datetime


class ConversationCreate(BaseModel):
    """Créer une nouvelle conversation"""
    title: str = Field(..., min_length=1, max_length=255)
    folder: str = Field(default="Général", max_length=100)


class ConversationUpdate(BaseModel):
    """Mettre à jour une conversation"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    folder: Optional[str] = Field(None, max_length=100)


class ConversationResponse(BaseModel):
    """Réponse conversation"""
    id: int
    user_id: int
    title: str
    folder: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Réponse message"""
    id: int
    conversation_id: int
    role: str  # user, assistant, system
    content: str
    ai_responses: Optional[Dict[str, str]] = None
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    """Conversation avec ses messages"""
    messages: List[MessageResponse] = []
