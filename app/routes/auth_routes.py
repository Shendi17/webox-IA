"""
Routes d'authentification
"""

from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from app.controllers.auth_controller import (
    register_controller,
    login_controller,
    logout_controller
)
from app.middleware.auth import get_current_user_from_cookie
from app.database import get_db
from app.models.user_db import UserDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ========== FONCTION POUR LES ROUTES API ==========

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> UserDB:
    """
    Récupère l'utilisateur connecté depuis le cookie de session
    Pour les routes API
    """
    user_data = get_current_user_from_cookie(request)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié"
        )
    
    # Récupérer l'utilisateur complet depuis la base de données
    user = db.query(UserDB).filter(UserDB.email == user_data.get("email")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé"
        )
    
    return user


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Page de connexion"""
    # Si déjà connecté, rediriger vers dashboard
    user = get_current_user_from_cookie(request)
    if user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard", status_code=302)
    
    return templates.TemplateResponse("auth/login.html", {
        "request": request
    })


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False)
):
    """Traitement de la connexion"""
    return await login_controller(request, email, password, remember_me)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Page d'inscription"""
    # Si déjà connecté, rediriger vers dashboard
    user = get_current_user_from_cookie(request)
    if user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard", status_code=302)
    
    return templates.TemplateResponse("auth/register.html", {
        "request": request
    })


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...)
):
    """Traitement de l'inscription"""
    return await register_controller(request, email, password, name)


@router.get("/logout")
async def logout(request: Request):
    """Déconnexion"""
    return await logout_controller(request)


@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Page de connexion administrateur"""
    # Si déjà connecté en tant qu'admin, rediriger vers dashboard
    user = get_current_user_from_cookie(request)
    if user and user.get("is_admin"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard", status_code=302)
    
    return templates.TemplateResponse("auth/admin_login.html", {
        "request": request
    })


@router.post("/admin/login")
async def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False)
):
    """Traitement de la connexion administrateur"""
    from fastapi.responses import JSONResponse
    from app.models.user import get_user_by_email, verify_password
    from app.middleware.auth import create_access_token
    from datetime import timedelta
    
    # Vérifier les credentials
    user = get_user_by_email(email)
    
    if not user:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Email ou mot de passe incorrect"}
        )
    
    if not verify_password(password, user.hashed_password):
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Email ou mot de passe incorrect"}
        )
    
    # Vérifier que l'utilisateur est admin
    if not user.is_admin and user.role != "admin":
        return JSONResponse(
            status_code=403,
            content={"success": False, "message": "Accès réservé aux administrateurs"}
        )
    
    # Créer le token JWT
    access_token_expires = timedelta(days=7 if remember_me else 1)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "name": user.name,
            "role": user.role,
            "user_id": user.id,
            "is_admin": True
        },
        expires_delta=access_token_expires
    )
    
    # Créer la réponse avec le cookie
    response = JSONResponse(
        content={
            "success": True,
            "message": f"Bienvenue Administrateur {user.name} !",
            "redirect": "/dashboard"
        }
    )
    
    # Définir le cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=int(access_token_expires.total_seconds()) if remember_me else None,
        samesite="lax"
    )
    
    return response
