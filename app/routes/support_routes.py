"""
Routes pour la page Support et formulaire de contact
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB
from app.database import get_db
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    category: str = "general"  # general, technical, billing, other


@router.get("/support", response_class=HTMLResponse)
async def support_page(
    request: Request,
    current_user: UserDB = Depends(get_current_user)
):
    """Page Support - Centre d'aide et assistance"""
    return templates.TemplateResponse(
        "pages/support.html",
        {
            "request": request,
            "user": current_user,
            "title": "Support - WeBox Multi-IA",
            "page": "support"
        }
    )


@router.post("/api/support/contact")
async def submit_contact_form(
    contact: ContactRequest,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    API pour soumettre un formulaire de contact
    Enregistre le message et envoie une notification
    """
    try:
        # Pour l'instant, enregistrer dans un fichier log
        # En production, enregistrer en DB et envoyer email
        
        log_dir = "logs"
        import os
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "contact_messages.log")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"Date: {datetime.utcnow().isoformat()}\n")
            f.write(f"De: {contact.name} ({contact.email})\n")
            f.write(f"Utilisateur: {current_user.email}\n")
            f.write(f"Catégorie: {contact.category}\n")
            f.write(f"Sujet: {contact.subject}\n")
            f.write(f"Message:\n{contact.message}\n")
            f.write(f"{'='*70}\n")
        
        return {
            "success": True,
            "message": "Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.",
            "ticket_id": f"TICKET-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'envoi du message: {str(e)}"
        )
