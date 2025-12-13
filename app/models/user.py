"""
Modèle User - Gestion des utilisateurs
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import hashlib
import json
import os

# Fichier de stockage
USERS_FILE = "data/users.json"


class UserCreate(BaseModel):
    """Modèle pour la création d'un utilisateur"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2)


class UserLogin(BaseModel):
    """Modèle pour la connexion"""
    email: EmailStr
    password: str
    remember_me: bool = False


class User(BaseModel):
    """Modèle utilisateur complet"""
    email: EmailStr
    name: str
    created_at: str
    last_login: Optional[str] = None
    role: str = "user"
    
    class Config:
        from_attributes = True


class UserInDB(User):
    """Utilisateur avec mot de passe hashé"""
    password: str


def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    """Charge les utilisateurs depuis le fichier JSON"""
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Créer un compte admin par défaut
    admin_users = {
        "admin@webox.com": {
            "name": "Administrateur",
            "password": hash_password("admin123"),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "role": "admin"
        }
    }
    save_users(admin_users)
    return admin_users


def save_users(users: dict):
    """Sauvegarde les utilisateurs dans le fichier JSON"""
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def get_user_by_email(email: str) -> Optional['UserDB']:
    """Récupère un utilisateur par son email depuis la base de données"""
    from app.database import SessionLocal
    from app.models.user_db import UserDB
    
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.email == email).first()
        return user
    finally:
        db.close()


def create_user(user_data: UserCreate) -> tuple[bool, str]:
    """Crée un nouvel utilisateur"""
    users = load_users()
    
    if user_data.email in users:
        return False, "Cet email est déjà utilisé"
    
    users[user_data.email] = {
        "name": user_data.name,
        "password": hash_password(user_data.password),
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "role": "user"
    }
    
    save_users(users)
    return True, "Compte créé avec succès !"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe"""
    from werkzeug.security import check_password_hash
    return check_password_hash(hashed_password, plain_password)


def update_last_login(email: str):
    """Met à jour la dernière connexion"""
    users = load_users()
    if email in users:
        users[email]["last_login"] = datetime.now().isoformat()
        save_users(users)
