"""Gestionnaire de sessions persistantes pour WeBox Multi-IA"""
import streamlit as st
import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict

# Fichiers de stockage
SESSIONS_FILE = "data/sessions.json"
USERS_FILE = "data/users.json"


class SessionManager:
    """Gestionnaire de sessions avec persistance"""
    
    def __init__(self):
        self.sessions = self.load_sessions()
    
    def load_sessions(self) -> Dict:
        """Charge les sessions depuis le fichier"""
        if os.path.exists(SESSIONS_FILE):
            try:
                with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_sessions(self):
        """Sauvegarde les sessions dans le fichier"""
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=2)
    
    def create_session(self, email: str) -> str:
        """Crée une nouvelle session et retourne le token"""
        # Générer un token unique
        token = secrets.token_urlsafe(32)
        
        # Créer la session
        self.sessions[token] = {
            "email": email,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        self.save_sessions()
        return token
    
    def validate_session(self, token: str) -> Optional[str]:
        """Valide un token de session et retourne l'email si valide"""
        if not token or token not in self.sessions:
            return None
        
        session = self.sessions[token]
        
        # Vérifier l'expiration
        expires_at = datetime.fromisoformat(session["expires_at"])
        if datetime.now() > expires_at:
            # Session expirée, la supprimer
            del self.sessions[token]
            self.save_sessions()
            return None
        
        # Mettre à jour la dernière activité
        session["last_activity"] = datetime.now().isoformat()
        self.save_sessions()
        
        return session["email"]
    
    def delete_session(self, token: str):
        """Supprime une session"""
        if token in self.sessions:
            del self.sessions[token]
            self.save_sessions()
    
    def cleanup_expired_sessions(self):
        """Nettoie les sessions expirées"""
        now = datetime.now()
        expired_tokens = []
        
        for token, session in self.sessions.items():
            expires_at = datetime.fromisoformat(session["expires_at"])
            if now > expires_at:
                expired_tokens.append(token)
        
        for token in expired_tokens:
            del self.sessions[token]
        
        if expired_tokens:
            self.save_sessions()


def get_session_token() -> Optional[str]:
    """Récupère le token de session depuis les query params ou le session state"""
    # D'abord vérifier le session state
    if "session_token" in st.session_state:
        return st.session_state.session_token
    
    # Ensuite vérifier les query params (pour la persistance)
    try:
        query_params = st.query_params
        if "session" in query_params:
            token = query_params["session"]
            st.session_state.session_token = token
            return token
    except:
        pass
    
    return None


def set_session_token(token: str):
    """Définit le token de session"""
    st.session_state.session_token = token
    # Ajouter le token aux query params pour la persistance
    st.query_params["session"] = token


def clear_session_token():
    """Efface le token de session"""
    if "session_token" in st.session_state:
        del st.session_state.session_token
    
    # Effacer des query params
    try:
        if "session" in st.query_params:
            del st.query_params["session"]
    except:
        pass


def init_session_state():
    """Initialise le state de session"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "remember_me" not in st.session_state:
        st.session_state.remember_me = False


def check_authentication() -> bool:
    """Vérifie si l'utilisateur est authentifié"""
    init_session_state()
    
    # Si déjà authentifié dans cette session, retourner True
    if st.session_state.authenticated:
        return True
    
    # Vérifier le token de session
    token = get_session_token()
    if token:
        session_manager = SessionManager()
        email = session_manager.validate_session(token)
        
        if email:
            # Session valide, restaurer l'authentification
            from modules.core.auth import load_users
            users = load_users()
            
            if email in users:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_name = users[email]["name"]
                st.session_state.remember_me = True
                return True
    
    return False


def login_with_session(email: str, name: str, remember_me: bool = True):
    """Connecte l'utilisateur et crée une session persistante"""
    st.session_state.authenticated = True
    st.session_state.user_email = email
    st.session_state.user_name = name
    st.session_state.remember_me = remember_me
    
    if remember_me:
        # Créer une session persistante
        session_manager = SessionManager()
        token = session_manager.create_session(email)
        set_session_token(token)


def logout_with_session():
    """Déconnecte l'utilisateur et supprime la session"""
    # Supprimer la session persistante
    token = get_session_token()
    if token:
        session_manager = SessionManager()
        session_manager.delete_session(token)
    
    # Effacer le token
    clear_session_token()
    
    # Réinitialiser le state
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.session_state.remember_me = False


# Instance globale
session_manager = SessionManager()
