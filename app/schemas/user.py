"""
Schémas Pydantic pour les utilisateurs
Date : 30 Octobre 2025
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schéma pour créer un utilisateur"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2, max_length=100)


class UserLogin(BaseModel):
    """Schéma pour la connexion"""
    email: EmailStr
    password: str
    remember_me: bool = False


class UserUpdate(BaseModel):
    """Schéma pour mettre à jour un utilisateur"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    preferences: Optional[dict] = None
    settings: Optional[dict] = None


class UserResponse(BaseModel):
    """Schéma de réponse utilisateur (sans mot de passe)"""
    id: int
    email: str
    username: str
    name: str
    is_active: bool
    is_admin: bool
    is_premium: bool
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None
    preferences: dict = {}
    settings: dict = {}
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Données contenues dans le token"""
    email: Optional[str] = None
    user_id: Optional[int] = None
