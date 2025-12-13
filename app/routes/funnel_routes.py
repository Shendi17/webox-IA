"""
Routes API pour les Tunnels de Vente (Phase 5B)
Date : 15 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from app.models.funnel_db import FunnelDB, FunnelAnalyticsDB, FunnelContactDB
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class FunnelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    template: Optional[str] = "custom"
    steps: Optional[List[Dict]] = []
    automations: Optional[List[Dict]] = []

class FunnelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[List[Dict]] = None
    automations: Optional[List[Dict]] = None
    is_active: Optional[bool] = None


# ============================================================================
# PAGE HTML
# ============================================================================

@router.get("/funnels", response_class=HTMLResponse)
async def funnels_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page de gestion des tunnels de vente"""
    return templates.TemplateResponse("dashboard/funnels.html", {
        "request": request,
        "user": user
    })


# ============================================================================
# FUNNELS - CRUD
# ============================================================================

@router.post("/api/funnels/create")
async def create_funnel(
    funnel: FunnelCreate,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Créer un nouveau tunnel"""
    try:
        new_funnel = FunnelDB(
            user_id=user["id"],
            name=funnel.name,
            description=funnel.description,
            template=funnel.template,
            steps=funnel.steps,
            automations=funnel.automations
        )
        
        db.add(new_funnel)
        db.commit()
        db.refresh(new_funnel)
        
        return {
            "success": True,
            "message": "Tunnel créé avec succès !",
            "funnel_id": new_funnel.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/funnels/list")
async def list_funnels(
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des tunnels"""
    try:
        funnels = db.query(FunnelDB).filter(
            FunnelDB.user_id == user["id"]
        ).order_by(FunnelDB.created_at.desc()).all()
        
        return {
            "success": True,
            "funnels": [f.to_dict() for f in funnels]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/funnels/{funnel_id}")
async def get_funnel(
    funnel_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Détails d'un tunnel"""
    try:
        funnel = db.query(FunnelDB).filter(
            FunnelDB.id == funnel_id,
            FunnelDB.user_id == user["id"]
        ).first()
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Tunnel non trouvé")
        
        return {
            "success": True,
            "funnel": funnel.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/funnels/{funnel_id}")
async def update_funnel(
    funnel_id: int,
    funnel_data: FunnelUpdate,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Modifier un tunnel"""
    try:
        funnel = db.query(FunnelDB).filter(
            FunnelDB.id == funnel_id,
            FunnelDB.user_id == user["id"]
        ).first()
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Tunnel non trouvé")
        
        if funnel_data.name:
            funnel.name = funnel_data.name
        if funnel_data.description:
            funnel.description = funnel_data.description
        if funnel_data.steps is not None:
            funnel.steps = funnel_data.steps
        if funnel_data.automations is not None:
            funnel.automations = funnel_data.automations
        if funnel_data.is_active is not None:
            funnel.is_active = funnel_data.is_active
        
        funnel.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": "Tunnel mis à jour"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/funnels/{funnel_id}")
async def delete_funnel(
    funnel_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Supprimer un tunnel"""
    try:
        funnel = db.query(FunnelDB).filter(
            FunnelDB.id == funnel_id,
            FunnelDB.user_id == user["id"]
        ).first()
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Tunnel non trouvé")
        
        db.delete(funnel)
        db.commit()
        
        return {
            "success": True,
            "message": "Tunnel supprimé"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TEMPLATES DE TUNNELS
# ============================================================================

@router.get("/api/funnels/templates/list")
async def get_funnel_templates():
    """Liste des templates de tunnels prédéfinis"""
    templates = [
        {
            "id": "lead-gen",
            "name": "Lead Generation",
            "description": "Capturer des leads qualifiés",
            "icon": "🎯",
            "steps": [
                {"type": "ad", "name": "Publicité Facebook/Google"},
                {"type": "landing-page", "name": "Landing Page Capture"},
                {"type": "email", "name": "Email de Bienvenue"},
                {"type": "email-sequence", "name": "Séquence Nurturing (5 emails)"},
                {"type": "offer", "name": "Offre Commerciale"}
            ]
        },
        {
            "id": "product-sale",
            "name": "Vente Produit",
            "description": "Vendre un produit ou service",
            "icon": "💰",
            "steps": [
                {"type": "ad", "name": "Publicité Produit"},
                {"type": "landing-page", "name": "Page Produit"},
                {"type": "checkout", "name": "Page de Paiement"},
                {"type": "upsell", "name": "Upsell"},
                {"type": "confirmation", "name": "Confirmation + Onboarding"}
            ]
        },
        {
            "id": "webinar",
            "name": "Webinaire",
            "description": "Organiser un webinaire de vente",
            "icon": "🎥",
            "steps": [
                {"type": "ad", "name": "Publicité Webinaire"},
                {"type": "landing-page", "name": "Page Inscription"},
                {"type": "email", "name": "Confirmation Inscription"},
                {"type": "email-sequence", "name": "Rappels (3 emails)"},
                {"type": "webinar", "name": "Webinaire Live"},
                {"type": "offer", "name": "Offre Limitée"},
                {"type": "replay", "name": "Replay + Relance"}
            ]
        },
        {
            "id": "launch",
            "name": "Lancement Produit",
            "description": "Lancer un nouveau produit",
            "icon": "🚀",
            "steps": [
                {"type": "teasing", "name": "Teasing (3 jours)"},
                {"type": "landing-page", "name": "Waitlist"},
                {"type": "email-sequence", "name": "Pré-lancement (7 jours)"},
                {"type": "presale", "name": "Pré-vente (48h)"},
                {"type": "launch", "name": "Lancement Officiel"},
                {"type": "follow-up", "name": "Suivi Post-Lancement"}
            ]
        },
        {
            "id": "ecommerce",
            "name": "E-commerce",
            "description": "Tunnel e-commerce complet",
            "icon": "🛍️",
            "steps": [
                {"type": "ad", "name": "Publicité Produit"},
                {"type": "product-page", "name": "Fiche Produit"},
                {"type": "cart", "name": "Panier"},
                {"type": "checkout", "name": "Checkout"},
                {"type": "upsell", "name": "Upsell/Cross-sell"},
                {"type": "confirmation", "name": "Confirmation"},
                {"type": "email-sequence", "name": "Post-Achat (3 emails)"}
            ]
        }
    ]
    
    return {
        "success": True,
        "templates": templates
    }

@router.post("/api/funnels/create-from-template")
async def create_funnel_from_template(
    template_id: str,
    name: str,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Créer un tunnel à partir d'un template"""
    try:
        # Récupérer le template
        templates_response = await get_funnel_templates()
        templates_list = templates_response["templates"]
        template = next((t for t in templates_list if t["id"] == template_id), None)
        
        if not template:
            raise HTTPException(status_code=404, detail="Template non trouvé")
        
        # Créer le tunnel
        new_funnel = FunnelDB(
            user_id=user["id"],
            name=name,
            description=template["description"],
            template=template_id,
            steps=template["steps"]
        )
        
        db.add(new_funnel)
        db.commit()
        db.refresh(new_funnel)
        
        return {
            "success": True,
            "message": f"Tunnel '{name}' créé à partir du template {template['name']} !",
            "funnel_id": new_funnel.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ANALYTICS
# ============================================================================

@router.get("/api/funnels/{funnel_id}/analytics")
async def get_funnel_analytics(
    funnel_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Analytics d'un tunnel"""
    try:
        funnel = db.query(FunnelDB).filter(
            FunnelDB.id == funnel_id,
            FunnelDB.user_id == user["id"]
        ).first()
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Tunnel non trouvé")
        
        # Analytics par étape
        step_analytics = db.query(FunnelAnalyticsDB).filter(
            FunnelAnalyticsDB.funnel_id == funnel_id
        ).all()
        
        return {
            "success": True,
            "funnel": funnel.to_dict(),
            "step_analytics": [a.to_dict() for a in step_analytics]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/funnels/{funnel_id}/contacts")
async def get_funnel_contacts(
    funnel_id: int,
    limit: int = 50,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des contacts dans un tunnel"""
    try:
        funnel = db.query(FunnelDB).filter(
            FunnelDB.id == funnel_id,
            FunnelDB.user_id == user["id"]
        ).first()
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Tunnel non trouvé")
        
        contacts = db.query(FunnelContactDB).filter(
            FunnelContactDB.funnel_id == funnel_id
        ).order_by(FunnelContactDB.created_at.desc()).limit(limit).all()
        
        return {
            "success": True,
            "contacts": [c.to_dict() for c in contacts]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/funnels/{funnel_id}/publish")
async def publish_funnel(
    funnel_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Publier/Activer un tunnel"""
    try:
        funnel = db.query(FunnelDB).filter(
            FunnelDB.id == funnel_id,
            FunnelDB.user_id == user["id"]
        ).first()
        
        if not funnel:
            raise HTTPException(status_code=404, detail="Tunnel non trouvé")
        
        funnel.is_published = True
        funnel.is_active = True
        db.commit()
        
        return {
            "success": True,
            "message": "Tunnel publié et activé !"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
