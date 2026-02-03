"""
Routes pour l'authentification à deux facteurs (2FA)
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_db import UserDB
from app.middleware.auth import get_current_user_from_token
from app.services.twofa_service import twofa_service

router = APIRouter(prefix="/api/2fa", tags=["2FA"])
templates = Jinja2Templates(directory="templates")


class Enable2FARequest(BaseModel):
    """Requête pour activer 2FA"""
    pass


class Verify2FARequest(BaseModel):
    """Requête pour vérifier un code 2FA"""
    token: str


class Disable2FARequest(BaseModel):
    """Requête pour désactiver 2FA"""
    token: str


@router.post("/enable")
async def enable_2fa(
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Activer 2FA pour l'utilisateur
    Génère un secret et un QR code
    """
    try:
        user = db.query(UserDB).filter(UserDB.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        if user.twofa_enabled:
            raise HTTPException(status_code=400, detail="2FA déjà activé")
        
        # Générer un nouveau secret
        secret = twofa_service.generate_secret()
        
        # Générer le QR code
        qr_code = twofa_service.generate_qr_code(user.email, secret)
        
        # Générer les codes de secours
        backup_codes = twofa_service.generate_backup_codes()
        
        # Sauvegarder temporairement (sera confirmé après vérification)
        user.twofa_secret = secret
        user.twofa_backup_codes = backup_codes
        db.commit()
        
        return {
            "success": True,
            "message": "Scannez le QR code avec votre application d'authentification",
            "qr_code": qr_code,
            "secret": secret,  # Pour saisie manuelle
            "backup_codes": backup_codes
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.post("/verify")
async def verify_2fa(
    request: Verify2FARequest,
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Vérifier le code 2FA et activer définitivement
    """
    try:
        user = db.query(UserDB).filter(UserDB.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        if not user.twofa_secret:
            raise HTTPException(status_code=400, detail="2FA non initialisé")
        
        # Vérifier le code
        is_valid = twofa_service.verify_token(user.twofa_secret, request.token)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Code invalide")
        
        # Activer 2FA
        user.twofa_enabled = True
        db.commit()
        
        return {
            "success": True,
            "message": "2FA activé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.post("/disable")
async def disable_2fa(
    request: Disable2FARequest,
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Désactiver 2FA
    """
    try:
        user = db.query(UserDB).filter(UserDB.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        if not user.twofa_enabled:
            raise HTTPException(status_code=400, detail="2FA non activé")
        
        # Vérifier le code
        is_valid = twofa_service.verify_token(user.twofa_secret, request.token)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Code invalide")
        
        # Désactiver 2FA
        user.twofa_enabled = False
        user.twofa_secret = None
        user.twofa_backup_codes = None
        db.commit()
        
        return {
            "success": True,
            "message": "2FA désactivé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.get("/status")
async def get_2fa_status(
    current_user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Obtenir le statut 2FA de l'utilisateur
    """
    try:
        user = db.query(UserDB).filter(UserDB.id == current_user["id"]).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return {
            "success": True,
            "enabled": user.twofa_enabled,
            "has_backup_codes": bool(user.twofa_backup_codes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.post("/verify-login")
async def verify_2fa_login(
    request: Verify2FARequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Vérifier le code 2FA lors de la connexion
    (Utilisé par auth_routes.py)
    """
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        
        if not user or not user.twofa_enabled:
            raise HTTPException(status_code=400, detail="2FA non activé")
        
        # Vérifier le code
        is_valid = twofa_service.verify_token(user.twofa_secret, request.token)
        
        # Vérifier aussi les codes de secours
        if not is_valid and user.twofa_backup_codes:
            if request.token in user.twofa_backup_codes:
                # Code de secours valide, le supprimer
                user.twofa_backup_codes.remove(request.token)
                db.commit()
                is_valid = True
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Code invalide")
        
        return {
            "success": True,
            "message": "Code 2FA valide"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")
