"""
Routes pour les fonctionnalités de sécurité
Réinitialisation mot de passe, vérification email, etc.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from app.middleware.auth import get_current_user_from_token
from app.middleware.rate_limiter import rate_limit_strict
from app.services.password_reset_service import password_reset_service
from app.services.email_verification_service import email_verification_service

router = APIRouter(tags=["security"])
templates = Jinja2Templates(directory="templates")


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class EmailVerificationResend(BaseModel):
    email: EmailStr


# ========== RÉINITIALISATION MOT DE PASSE ==========

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Page de demande de réinitialisation"""
    return templates.TemplateResponse("auth/forgot_password.html", {
        "request": request,
        "error": None
    })


@router.post("/api/auth/forgot-password", dependencies=[Depends(rate_limit_strict(max_requests=3, window_seconds=300))])
async def request_password_reset(request: PasswordResetRequest):
    """
    Demander une réinitialisation de mot de passe
    Rate limit: 3 requêtes par 5 minutes
    """
    result = password_reset_service.request_password_reset(request.email)
    
    # Toujours retourner success pour ne pas révéler si l'email existe
    return {
        "success": True,
        "message": "Si cet email existe, un lien de réinitialisation a été envoyé"
    }


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str):
    """Page de réinitialisation avec token"""
    # Valider le token
    token_data = password_reset_service.validate_token(token)
    
    if not token_data:
        return templates.TemplateResponse("auth/reset_password.html", {
            "request": request,
            "error": "Token invalide ou expiré",
            "token": None
        })
    
    return templates.TemplateResponse("auth/reset_password.html", {
        "request": request,
        "error": None,
        "token": token
    })


@router.post("/api/auth/reset-password", dependencies=[Depends(rate_limit_strict(max_requests=5, window_seconds=300))])
async def confirm_password_reset(request: PasswordResetConfirm):
    """
    Confirmer la réinitialisation avec le nouveau mot de passe
    Rate limit: 5 requêtes par 5 minutes
    """
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins 6 caractères"
        )
    
    result = password_reset_service.reset_password(request.token, request.new_password)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


# ========== VÉRIFICATION EMAIL ==========

@router.get("/verify-email", response_class=HTMLResponse)
async def verify_email_page(request: Request, token: str):
    """Page de vérification d'email avec token"""
    result = email_verification_service.verify_email(token)
    
    if result["success"]:
        return templates.TemplateResponse("auth/email_verified.html", {
            "request": request,
            "success": True,
            "message": result["message"]
        })
    else:
        return templates.TemplateResponse("auth/email_verified.html", {
            "request": request,
            "success": False,
            "error": result["error"]
        })


@router.post("/api/auth/resend-verification", dependencies=[Depends(rate_limit_strict(max_requests=3, window_seconds=300))])
async def resend_verification_email(
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Renvoyer l'email de vérification
    Rate limit: 3 requêtes par 5 minutes
    """
    result = email_verification_service.resend_verification_email(current_user["id"])
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/api/auth/verification-status")
async def check_verification_status(
    current_user: dict = Depends(get_current_user_from_token)
):
    """Vérifier le statut de vérification de l'email"""
    from app.database import SessionLocal
    from app.models.user_db import UserDB
    
    db = SessionLocal()
    
    try:
        user = db.query(UserDB).filter(UserDB.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return {
            "email": user.email,
            "verified": user.email_verified,
            "verified_at": user.email_verified_at.isoformat() if user.email_verified_at else None
        }
        
    finally:
        db.close()
