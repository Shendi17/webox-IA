"""
Middleware d'authentification JWT
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Configuration JWT
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crée un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Vérifie et décode un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user_from_cookie(request: Request) -> Optional[dict]:
    """Récupère l'utilisateur depuis le cookie"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    payload = verify_token(token)
    if not payload:
        return None
    
    return {
        "email": payload.get("sub"),
        "name": payload.get("name"),
        "role": payload.get("role", "user"),
        "is_admin": payload.get("is_admin", False),
        "user_id": payload.get("user_id")
    }


def require_auth(request: Request):
    """Middleware pour vérifier l'authentification"""
    user = get_current_user_from_cookie(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié"
        )
    return user


def redirect_if_not_authenticated(request: Request):
    """Redirige vers login si non authentifié"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return user


def get_current_user_from_token(request: Request):
    """
    Récupère l'utilisateur depuis le token (pour l'API)
    Retourne un dict avec les infos utilisateur
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié"
        )
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    
    # Retourner les infos utilisateur depuis le token
    return {
        "email": payload.get("sub"),
        "name": payload.get("name"),
        "role": payload.get("role", "user"),
        "id": payload.get("user_id", 1)  # ID utilisateur
    }


def require_admin(request: Request):
    """
    Vérifie que l'utilisateur est admin
    Retourne les infos utilisateur si admin, sinon lève une exception
    """
    user = get_current_user_from_token(request)
    
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )
    
    return user
