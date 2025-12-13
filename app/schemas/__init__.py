"""
Schémas Pydantic pour l'API
Date : 30 Octobre 2025
"""

from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationResponse,
    MessageResponse
)

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "ChatRequest",
    "ChatResponse",
    "ConversationCreate",
    "ConversationResponse",
    "MessageResponse"
]
