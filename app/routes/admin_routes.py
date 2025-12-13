"""
Routes API pour l'administration (réservées aux admins)
Date : 2 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from cryptography.fernet import Fernet
import os

from app.database import get_db
from app.models.user_db import UserDB
from app.models.settings_db import SettingsDB
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# Clé de chiffrement
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY if isinstance(ENCRYPTION_KEY, bytes) else ENCRYPTION_KEY.encode())


# ========== MODÈLES PYDANTIC ==========

class GlobalAPIKeysUpdate(BaseModel):
    """Modèle pour mise à jour des clés API globales"""
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    google_key: Optional[str] = None
    mistral_key: Optional[str] = None
    groq_key: Optional[str] = None


# ========== FONCTIONS UTILITAIRES ==========

def encrypt_value(value: str) -> str:
    """Chiffre une valeur"""
    if not value:
        return ""
    return cipher_suite.encrypt(value.encode()).decode()


def decrypt_value(encrypted_value: str) -> str:
    """Déchiffre une valeur"""
    if not encrypted_value:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_value.encode()).decode()
    except:
        return ""


def get_or_create_setting(db: Session, key: str, category: str = "api_keys", default_value: str = "") -> SettingsDB:
    """Récupère ou crée un paramètre"""
    setting = db.query(SettingsDB).filter(SettingsDB.key == key).first()
    if not setting:
        setting = SettingsDB(
            key=key,
            value=default_value,
            category=category,
            is_encrypted=True if category == "api_keys" else False
        )
        db.add(setting)
        db.commit()
        db.refresh(setting)
    return setting


def check_admin(current_user: UserDB):
    """Vérifie que l'utilisateur est admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )


# ========== ROUTES API ==========

@router.get("/api-keys/global")
async def get_global_api_keys(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les clés API globales (admin seulement)
    """
    check_admin(current_user)
    
    # Récupérer les clés
    keys = {
        "openai": get_or_create_setting(db, "global_openai_key", "api_keys"),
        "anthropic": get_or_create_setting(db, "global_anthropic_key", "api_keys"),
        "google": get_or_create_setting(db, "global_google_key", "api_keys"),
        "mistral": get_or_create_setting(db, "global_mistral_key", "api_keys"),
        "groq": get_or_create_setting(db, "global_groq_key", "api_keys")
    }
    
    # Masquer les clés pour l'affichage
    masked_keys = {}
    has_keys = {}
    
    for provider, setting in keys.items():
        if setting.value:
            decrypted = decrypt_value(setting.value)
            if len(decrypted) > 8:
                masked_keys[provider] = f"{decrypted[:4]}...{decrypted[-4:]}"
            else:
                masked_keys[provider] = "****"
            has_keys[provider] = True
        else:
            masked_keys[provider] = ""
            has_keys[provider] = False
    
    return {
        "success": True,
        "keys": masked_keys,
        "has_keys": has_keys
    }


@router.put("/api-keys/global")
async def update_global_api_keys(
    keys_data: GlobalAPIKeysUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour les clés API globales (admin seulement)
    Ces clés seront utilisées pour TOUS les utilisateurs
    """
    check_admin(current_user)
    
    try:
        # Mettre à jour chaque clé
        if keys_data.openai_key is not None:
            setting = get_or_create_setting(db, "global_openai_key", "api_keys")
            setting.value = encrypt_value(keys_data.openai_key) if keys_data.openai_key else ""
            setting.updated_by = current_user.email
            setting.updated_at = datetime.utcnow()
        
        if keys_data.anthropic_key is not None:
            setting = get_or_create_setting(db, "global_anthropic_key", "api_keys")
            setting.value = encrypt_value(keys_data.anthropic_key) if keys_data.anthropic_key else ""
            setting.updated_by = current_user.email
            setting.updated_at = datetime.utcnow()
        
        if keys_data.google_key is not None:
            setting = get_or_create_setting(db, "global_google_key", "api_keys")
            setting.value = encrypt_value(keys_data.google_key) if keys_data.google_key else ""
            setting.updated_by = current_user.email
            setting.updated_at = datetime.utcnow()
        
        if keys_data.mistral_key is not None:
            setting = get_or_create_setting(db, "global_mistral_key", "api_keys")
            setting.value = encrypt_value(keys_data.mistral_key) if keys_data.mistral_key else ""
            setting.updated_by = current_user.email
            setting.updated_at = datetime.utcnow()
        
        if keys_data.groq_key is not None:
            setting = get_or_create_setting(db, "global_groq_key", "api_keys")
            setting.value = encrypt_value(keys_data.groq_key) if keys_data.groq_key else ""
            setting.updated_by = current_user.email
            setting.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Clés API globales mises à jour avec succès"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )


@router.get("/stats")
async def get_admin_stats(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques globales (admin seulement)
    """
    check_admin(current_user)
    
    # Compter les utilisateurs
    total_users = db.query(UserDB).count()
    premium_users = db.query(UserDB).filter(UserDB.is_premium == True).count()
    active_users = db.query(UserDB).filter(UserDB.is_active == True).count()
    
    return {
        "success": True,
        "stats": {
            "total_users": total_users,
            "premium_users": premium_users,
            "active_users": active_users,
            "free_users": total_users - premium_users
        }
    }
