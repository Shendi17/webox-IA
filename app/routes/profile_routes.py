"""
Routes API pour la gestion du profil utilisateur
Date : 2 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict
from datetime import datetime
import hashlib
from cryptography.fernet import Fernet
import os
import base64

from app.database import get_db
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])

# Clé de chiffrement pour les API keys (à stocker dans .env en production)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY if isinstance(ENCRYPTION_KEY, bytes) else ENCRYPTION_KEY.encode())


# ========== MODÈLES PYDANTIC ==========

class ProfileUpdate(BaseModel):
    """Modèle pour mise à jour du profil"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    
    @validator('name')
    def name_not_empty(cls, v):
        if v is not None and len(v.strip()) < 2:
            raise ValueError('Le nom doit contenir au moins 2 caractères')
        return v.strip() if v else v
    
    @validator('new_password')
    def password_strength(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('Le mot de passe doit contenir au moins 6 caractères')
        return v


class APIKeysUpdate(BaseModel):
    """Modèle pour mise à jour des clés API"""
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    google_key: Optional[str] = None
    mistral_key: Optional[str] = None
    groq_key: Optional[str] = None


class PreferencesUpdate(BaseModel):
    """Modèle pour mise à jour des préférences"""
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications: Optional[bool] = None
    default_ai: Optional[str] = None
    preferences: Optional[Dict] = None


# ========== FONCTIONS UTILITAIRES ==========

def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe"""
    return hash_password(plain_password) == hashed_password


def encrypt_api_key(api_key: str) -> str:
    """Chiffre une clé API"""
    if not api_key:
        return ""
    return cipher_suite.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """Déchiffre une clé API"""
    if not encrypted_key:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_key.encode()).decode()
    except:
        return ""


# ========== ROUTES API ==========

@router.get("/me")
async def get_profile(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Récupère le profil de l'utilisateur connecté
    """
    current_user = await get_current_user(request, db)
    current_user = await get_current_user(request, db)
    # Déchiffrer les clés API pour l'affichage (masquées)
    api_keys = current_user.api_keys or {}
    masked_keys = {}
    
    for key_name, encrypted_value in api_keys.items():
        if encrypted_value:
            decrypted = decrypt_api_key(encrypted_value)
            # Masquer la clé (afficher seulement les 4 premiers et 4 derniers caractères)
            if len(decrypted) > 8:
                masked_keys[key_name] = f"{decrypted[:4]}...{decrypted[-4:]}"
            else:
                masked_keys[key_name] = "****"
        else:
            masked_keys[key_name] = ""
    
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "name": current_user.name,
            "role": current_user.role,
            "is_premium": current_user.is_premium,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
            "preferences": current_user.preferences or {},
            "api_keys": masked_keys,
            "has_api_keys": {
                "openai": bool(api_keys.get("openai_key")),
                "anthropic": bool(api_keys.get("anthropic_key")),
                "google": bool(api_keys.get("google_key")),
                "mistral": bool(api_keys.get("mistral_key")),
                "groq": bool(api_keys.get("groq_key"))
            }
        }
    }


@router.put("/update")
async def update_profile(
    request: Request,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour le profil de l'utilisateur
    """
    current_user = await get_current_user(request, db)
    current_user = await get_current_user(request, db)
    
    try:
        # Vérifier le mot de passe actuel si changement de mot de passe
        if profile_data.new_password:
            if not profile_data.current_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Le mot de passe actuel est requis pour changer le mot de passe"
                )
            
            if not verify_password(profile_data.current_password, current_user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Mot de passe actuel incorrect"
                )
            
            # Mettre à jour le mot de passe
            current_user.hashed_password = hash_password(profile_data.new_password)
        
        # Mettre à jour le nom
        if profile_data.name:
            current_user.name = profile_data.name
        
        # Mettre à jour l'email
        if profile_data.email and profile_data.email != current_user.email:
            # Vérifier que l'email n'est pas déjà utilisé
            existing_user = db.query(UserDB).filter(UserDB.email == profile_data.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cet email est déjà utilisé"
                )
            current_user.email = profile_data.email
        
        # Mettre à jour la date de modification
        current_user.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "success": True,
            "message": "Profil mis à jour avec succès",
            "user": current_user.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du profil: {str(e)}"
        )


@router.put("/api-keys")
async def update_api_keys(
    request: Request,
    keys_data: APIKeysUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour les clés API de l'utilisateur (chiffrées)
    """
    current_user = await get_current_user(request, db)
    
    try:
        # Récupérer les clés actuelles
        api_keys = current_user.api_keys or {}
        
        # Mettre à jour les clés fournies (chiffrées)
        if keys_data.openai_key is not None:
            api_keys["openai_key"] = encrypt_api_key(keys_data.openai_key) if keys_data.openai_key else ""
        
        if keys_data.anthropic_key is not None:
            api_keys["anthropic_key"] = encrypt_api_key(keys_data.anthropic_key) if keys_data.anthropic_key else ""
        
        if keys_data.google_key is not None:
            api_keys["google_key"] = encrypt_api_key(keys_data.google_key) if keys_data.google_key else ""
        
        if keys_data.mistral_key is not None:
            api_keys["mistral_key"] = encrypt_api_key(keys_data.mistral_key) if keys_data.mistral_key else ""
        
        if keys_data.groq_key is not None:
            api_keys["groq_key"] = encrypt_api_key(keys_data.groq_key) if keys_data.groq_key else ""
        
        # Sauvegarder
        current_user.api_keys = api_keys
        current_user.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Clés API mises à jour avec succès",
            "has_api_keys": {
                "openai": bool(api_keys.get("openai_key")),
                "anthropic": bool(api_keys.get("anthropic_key")),
                "google": bool(api_keys.get("google_key")),
                "mistral": bool(api_keys.get("mistral_key")),
                "groq": bool(api_keys.get("groq_key"))
            }
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour des clés API: {str(e)}"
        )


@router.put("/preferences")
async def update_preferences(
    request: Request,
    prefs_data: PreferencesUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour les préférences de l'utilisateur
    """
    current_user = await get_current_user(request, db)
    
    try:
        # Récupérer les préférences actuelles
        preferences = current_user.preferences or {}
        
        # Mettre à jour les préférences fournies
        if prefs_data.theme is not None:
            preferences["theme"] = prefs_data.theme
        
        if prefs_data.language is not None:
            preferences["language"] = prefs_data.language
        
        if prefs_data.notifications is not None:
            preferences["notifications"] = prefs_data.notifications
        
        if prefs_data.default_ai is not None:
            preferences["default_ai"] = prefs_data.default_ai
        
        if prefs_data.preferences is not None:
            preferences.update(prefs_data.preferences)
        
        # Sauvegarder
        current_user.preferences = preferences
        current_user.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Préférences mises à jour avec succès",
            "preferences": preferences
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour des préférences: {str(e)}"
        )


@router.get("/stats")
async def get_user_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques de l'utilisateur
    """
    current_user = await get_current_user(request, db)
    current_user = await get_current_user(request, db)
    # Compter les conversations
    conversations_count = len(current_user.conversations) if current_user.conversations else 0
    
    # Compter les prompts
    prompts_count = len(current_user.prompts) if current_user.prompts else 0
    
    return {
        "success": True,
        "stats": {
            "conversations": conversations_count,
            "prompts": prompts_count,
            "member_since": current_user.created_at.isoformat() if current_user.created_at else None,
            "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
            "is_premium": current_user.is_premium
        }
    }
