"""
Utilitaires pour la gestion des clés API
Date : 2 Novembre 2025
"""

from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import os
from typing import Optional, Dict

from app.models.user_db import UserDB
from app.models.settings_db import SettingsDB


# Clé de chiffrement
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY if isinstance(ENCRYPTION_KEY, bytes) else ENCRYPTION_KEY.encode())


def decrypt_value(encrypted_value: str) -> str:
    """Déchiffre une valeur"""
    if not encrypted_value:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_value.encode()).decode()
    except:
        return ""


def get_api_key(db: Session, user: UserDB, provider: str) -> Optional[str]:
    """
    Récupère la clé API pour un provider donné
    
    Logique :
    1. Si l'utilisateur a une clé personnelle -> utiliser celle-ci
    2. Sinon, utiliser la clé globale (admin)
    3. Si aucune clé n'est disponible -> retourner None
    
    Args:
        db: Session de base de données
        user: Utilisateur connecté
        provider: Provider (openai, anthropic, google, mistral, groq)
    
    Returns:
        La clé API déchiffrée ou None
    """
    
    # 1. Vérifier si l'utilisateur a une clé personnelle
    if user.api_keys and user.api_keys.get(f"{provider}_key"):
        personal_key = decrypt_value(user.api_keys.get(f"{provider}_key"))
        if personal_key:
            print(f"🔑 Utilisation de la clé personnelle de {user.email} pour {provider}")
            return personal_key
    
    # 2. Récupérer la clé globale (admin)
    global_key_setting = db.query(SettingsDB).filter(
        SettingsDB.key == f"global_{provider}_key"
    ).first()
    
    if global_key_setting and global_key_setting.value:
        global_key = decrypt_value(global_key_setting.value)
        if global_key:
            print(f"🌐 Utilisation de la clé globale pour {provider}")
            return global_key
    
    # 3. Aucune clé disponible
    print(f"⚠️ Aucune clé API disponible pour {provider}")
    return None


def get_all_api_keys(db: Session, user: UserDB) -> Dict[str, Optional[str]]:
    """
    Récupère toutes les clés API disponibles pour un utilisateur
    
    Returns:
        Dictionnaire {provider: api_key}
    """
    providers = ["openai", "anthropic", "google", "mistral", "groq"]
    
    return {
        provider: get_api_key(db, user, provider)
        for provider in providers
    }


def has_api_access(db: Session, user: UserDB, provider: str) -> bool:
    """
    Vérifie si un utilisateur a accès à un provider
    
    Returns:
        True si l'utilisateur a accès (clé personnelle ou globale)
    """
    return get_api_key(db, user, provider) is not None


def get_api_key_source(db: Session, user: UserDB, provider: str) -> str:
    """
    Retourne la source de la clé API (personal, global, none)
    
    Returns:
        "personal", "global" ou "none"
    """
    # Vérifier clé personnelle
    if user.api_keys and user.api_keys.get(f"{provider}_key"):
        personal_key = decrypt_value(user.api_keys.get(f"{provider}_key"))
        if personal_key:
            return "personal"
    
    # Vérifier clé globale
    global_key_setting = db.query(SettingsDB).filter(
        SettingsDB.key == f"global_{provider}_key"
    ).first()
    
    if global_key_setting and global_key_setting.value:
        global_key = decrypt_value(global_key_setting.value)
        if global_key:
            return "global"
    
    return "none"
