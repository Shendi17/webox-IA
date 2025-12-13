"""
Controller d'authentification
"""

from fastapi import Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.models.user import (
    UserCreate, UserLogin, create_user, get_user_by_email,
    verify_password, update_last_login
)
from app.middleware.auth import create_access_token
from datetime import timedelta


async def register_controller(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...)
):
    """Contrôleur d'inscription"""
    try:
        user_data = UserCreate(email=email, password=password, name=name)
        success, message = create_user(user_data)
        
        if not success:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": message}
            )
        
        return JSONResponse(
            content={"success": True, "message": message, "redirect": "/login"}
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(e)}
        )


async def login_controller(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False)
):
    """Contrôleur de connexion"""
    # Vérifier les credentials
    user = get_user_by_email(email)
    
    if not user or not verify_password(password, user.hashed_password):
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Email ou mot de passe incorrect"}
        )
    
    # Mettre à jour la dernière connexion
    update_last_login(email)
    
    # Créer le token JWT
    access_token_expires = timedelta(days=7 if remember_me else 1)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "name": user.name,
            "role": user.role,
            "user_id": user.id,
            "is_admin": user.is_admin if hasattr(user, 'is_admin') else (user.role == "admin")
        },
        expires_delta=access_token_expires
    )
    
    # Créer la réponse avec le cookie
    response = JSONResponse(
        content={
            "success": True,
            "message": f"Bienvenue {user.name} !",
            "redirect": "/dashboard"
        }
    )
    
    # Définir le cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=access_token_expires.total_seconds() if remember_me else None,
        samesite="lax"
    )
    
    return response


async def logout_controller(request: Request):
    """Contrôleur de déconnexion"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response
