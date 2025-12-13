"""Système d'authentification pour WeBox Multi-IA"""
import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# Fichier de stockage des utilisateurs
USERS_FILE = "data/users.json"


def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Charge les utilisateurs depuis le fichier JSON"""
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


def save_users(users):
    """Sauvegarde les utilisateurs dans le fichier JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def register_user(email: str, password: str, name: str) -> tuple[bool, str]:
    """Enregistre un nouvel utilisateur"""
    users = load_users()
    
    if email in users:
        return False, "Cet email est déjà utilisé"
    
    users[email] = {
        "name": name,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users(users)
    return True, "Compte créé avec succès !"


def login_user(email: str, password: str, remember_me: bool = True) -> tuple[bool, str]:
    """Authentifie un utilisateur"""
    users = load_users()
    
    if email not in users:
        return False, "Email ou mot de passe incorrect"
    
    if users[email]["password"] != hash_password(password):
        return False, "Email ou mot de passe incorrect"
    
    # Mettre à jour la dernière connexion
    users[email]["last_login"] = datetime.now().isoformat()
    save_users(users)
    
    return True, users[email]["name"]


def is_authenticated():
    """Vérifie si l'utilisateur est authentifié"""
    from modules.core.session_manager import check_authentication
    return check_authentication()


def get_current_user():
    """Retourne l'utilisateur actuel"""
    return st.session_state.get("user_name", None)


def get_current_email():
    """Retourne l'email de l'utilisateur actuel"""
    return st.session_state.get("user_email", None)


def logout():
    """Déconnecte l'utilisateur"""
    from modules.core.session_manager import logout_with_session
    logout_with_session()
