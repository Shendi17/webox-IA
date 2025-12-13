"""
Routes API pour le Marketing & Business
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user
from app.middleware.auth import get_current_user_from_token
from app.services.funnel_service import FunnelService
from app.services.crm_service import CRMService
from app.services.email_campaign_service import EmailCampaignService

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/api/marketing", tags=["Marketing"])
router_pages = APIRouter(tags=["Marketing Pages"])


# ==================== PAGES HTML ====================

@router_pages.get("/funnels", response_class=HTMLResponse)
async def funnels_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page de gestion des tunnels de vente"""
    return templates.TemplateResponse("dashboard/funnels.html", {
        "request": request,
        "user": user
    })


@router_pages.get("/email-marketing", response_class=HTMLResponse)
async def email_marketing_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page d'email marketing"""
    return templates.TemplateResponse("dashboard/email_marketing.html", {
        "request": request,
        "user": user
    })


@router_pages.get("/crm", response_class=HTMLResponse)
async def crm_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page CRM"""
    return templates.TemplateResponse("dashboard/crm.html", {
        "request": request,
        "user": user
    })


@router_pages.get("/marketing-dashboard", response_class=HTMLResponse)
async def marketing_dashboard_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Dashboard Marketing"""
    return templates.TemplateResponse("dashboard/marketing_dashboard.html", {
        "request": request,
        "user": user
    })


# ==================== SCHEMAS FUNNELS ====================

class FunnelCreate(BaseModel):
    """Schéma pour créer un tunnel"""
    name: str
    description: Optional[str] = None
    funnel_type: str
    is_template: bool = False


class FunnelUpdate(BaseModel):
    """Schéma pour mettre à jour un tunnel"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class FunnelPageCreate(BaseModel):
    """Schéma pour créer une page de tunnel"""
    name: str
    page_type: str
    html_content: Optional[str] = ""
    css_content: Optional[str] = ""
    js_content: Optional[str] = ""
    order: int = 0
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class FunnelGenerateRequest(BaseModel):
    """Schéma pour générer un tunnel avec IA"""
    funnel_type: str
    topic: str
    target_audience: str


# ==================== ROUTES FUNNELS ====================

@router.post("/funnels")
async def create_funnel(
    data: FunnelCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un tunnel de vente"""
    result = FunnelService.create_funnel(
        db=db,
        funnel_data=data.dict(),
        author_id=current_user.id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/funnels")
async def list_funnels(
    is_template: Optional[bool] = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lister les tunnels"""
    funnels = FunnelService.list_funnels(
        db=db,
        author_id=current_user.id,
        is_template=is_template
    )
    
    return {
        "success": True,
        "funnels": [f.to_dict() for f in funnels]
    }


@router.get("/funnels/{funnel_id}")
async def get_funnel(
    funnel_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir un tunnel"""
    funnel = FunnelService.get_funnel(db, funnel_id, current_user.id)
    
    if not funnel:
        raise HTTPException(status_code=404, detail="Tunnel non trouvé")
    
    return {
        "success": True,
        "funnel": funnel.to_dict()
    }


@router.put("/funnels/{funnel_id}")
async def update_funnel(
    funnel_id: int,
    data: FunnelUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un tunnel"""
    result = FunnelService.update_funnel(
        db=db,
        funnel_id=funnel_id,
        author_id=current_user.id,
        update_data=data.dict(exclude_unset=True)
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.delete("/funnels/{funnel_id}")
async def delete_funnel(
    funnel_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un tunnel"""
    result = FunnelService.delete_funnel(db, funnel_id, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.post("/funnels/{funnel_id}/pages")
async def add_funnel_page(
    funnel_id: int,
    data: FunnelPageCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ajouter une page au tunnel"""
    result = FunnelService.add_page(
        db=db,
        funnel_id=funnel_id,
        author_id=current_user.id,
        page_data=data.dict()
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/funnels/{funnel_id}/stats")
async def get_funnel_stats(
    funnel_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir les statistiques d'un tunnel"""
    result = FunnelService.get_funnel_stats(db, funnel_id, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.post("/funnels/generate")
async def generate_funnel(
    data: FunnelGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Générer un tunnel complet avec IA"""
    result = FunnelService.generate_funnel_with_ai(
        db=db,
        funnel_type=data.funnel_type,
        topic=data.topic,
        target_audience=data.target_audience,
        author_id=current_user.id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


# ==================== SCHEMAS CRM ====================

class LeadCreate(BaseModel):
    """Schéma pour créer un lead"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: str = "new"
    source: Optional[str] = None
    estimated_value: float = 0.0
    tags: Optional[List[str]] = []
    notes: Optional[str] = None


class LeadUpdate(BaseModel):
    """Schéma pour mettre à jour un lead"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
    estimated_value: Optional[float] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


class InteractionCreate(BaseModel):
    """Schéma pour créer une interaction"""
    interaction_type: str
    subject: Optional[str] = None
    content: Optional[str] = None


# ==================== ROUTES CRM ====================

@router.post("/leads")
async def create_lead(
    data: LeadCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un lead"""
    result = CRMService.create_lead(
        db=db,
        lead_data=data.dict(),
        author_id=current_user.id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/leads")
async def list_leads(
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lister les leads"""
    leads = CRMService.list_leads(
        db=db,
        author_id=current_user.id,
        status=status,
        search=search
    )
    
    return {
        "success": True,
        "leads": [l.to_dict() for l in leads]
    }


@router.get("/leads/{lead_id}")
async def get_lead(
    lead_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir un lead"""
    lead = CRMService.get_lead(db, lead_id, current_user.id)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead non trouvé")
    
    return {
        "success": True,
        "lead": lead.to_dict()
    }


@router.put("/leads/{lead_id}")
async def update_lead(
    lead_id: int,
    data: LeadUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un lead"""
    result = CRMService.update_lead(
        db=db,
        lead_id=lead_id,
        author_id=current_user.id,
        update_data=data.dict(exclude_unset=True)
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.delete("/leads/{lead_id}")
async def delete_lead(
    lead_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un lead"""
    result = CRMService.delete_lead(db, lead_id, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.post("/leads/{lead_id}/interactions")
async def add_interaction(
    lead_id: int,
    data: InteractionCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ajouter une interaction à un lead"""
    result = CRMService.add_interaction(
        db=db,
        lead_id=lead_id,
        author_id=current_user.id,
        interaction_data=data.dict()
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/leads/{lead_id}/interactions")
async def get_lead_interactions(
    lead_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir les interactions d'un lead"""
    interactions = CRMService.get_lead_interactions(db, lead_id, current_user.id)
    
    return {
        "success": True,
        "interactions": [i.to_dict() for i in interactions]
    }


@router.post("/leads/{lead_id}/score")
async def update_lead_score(
    lead_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour le score d'un lead"""
    result = CRMService.update_lead_score(db, lead_id, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/pipeline/stats")
async def get_pipeline_stats(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir les statistiques du pipeline"""
    result = CRMService.get_pipeline_stats(db, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


# ==================== SCHEMAS EMAIL CAMPAIGNS ====================

class CampaignCreate(BaseModel):
    """Schéma pour créer une campagne"""
    name: str
    subject: str
    preheader: Optional[str] = None
    html_content: str
    text_content: Optional[str] = None
    from_name: Optional[str] = None
    from_email: Optional[str] = None
    reply_to: Optional[str] = None


class CampaignUpdate(BaseModel):
    """Schéma pour mettre à jour une campagne"""
    name: Optional[str] = None
    subject: Optional[str] = None
    html_content: Optional[str] = None
    status: Optional[str] = None


class CampaignGenerateRequest(BaseModel):
    """Schéma pour générer une campagne avec IA"""
    campaign_type: str
    topic: str
    target_audience: str
    tone: str = "professionnel"


class CampaignScheduleRequest(BaseModel):
    """Schéma pour planifier une campagne"""
    scheduled_at: datetime


# ==================== ROUTES EMAIL CAMPAIGNS ====================

@router.post("/campaigns")
async def create_campaign(
    data: CampaignCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer une campagne email"""
    result = EmailCampaignService.create_campaign(
        db=db,
        campaign_data=data.dict(),
        author_id=current_user.id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/campaigns")
async def list_campaigns(
    status: Optional[str] = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lister les campagnes"""
    campaigns = EmailCampaignService.list_campaigns(
        db=db,
        author_id=current_user.id,
        status=status
    )
    
    return {
        "success": True,
        "campaigns": [c.to_dict() for c in campaigns]
    }


@router.get("/campaigns/{campaign_id}")
async def get_campaign(
    campaign_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir une campagne"""
    campaign = EmailCampaignService.get_campaign(db, campaign_id, current_user.id)
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")
    
    return {
        "success": True,
        "campaign": campaign.to_dict()
    }


@router.put("/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: int,
    data: CampaignUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour une campagne"""
    result = EmailCampaignService.update_campaign(
        db=db,
        campaign_id=campaign_id,
        author_id=current_user.id,
        update_data=data.dict(exclude_unset=True)
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.delete("/campaigns/{campaign_id}")
async def delete_campaign(
    campaign_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer une campagne"""
    result = EmailCampaignService.delete_campaign(db, campaign_id, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.post("/campaigns/{campaign_id}/schedule")
async def schedule_campaign(
    campaign_id: int,
    data: CampaignScheduleRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Planifier l'envoi d'une campagne"""
    result = EmailCampaignService.schedule_campaign(
        db=db,
        campaign_id=campaign_id,
        author_id=current_user.id,
        scheduled_at=data.scheduled_at
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(
    campaign_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Envoyer une campagne"""
    result = EmailCampaignService.send_campaign(db, campaign_id, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.post("/campaigns/generate")
async def generate_campaign(
    data: CampaignGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Générer une campagne email avec IA"""
    result = EmailCampaignService.generate_campaign_with_ai(
        db=db,
        campaign_type=data.campaign_type,
        topic=data.topic,
        target_audience=data.target_audience,
        tone=data.tone,
        author_id=current_user.id
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result


@router.get("/campaigns/stats/global")
async def get_campaigns_stats(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir les statistiques globales des campagnes"""
    result = EmailCampaignService.get_campaign_stats(db, current_user.id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    
    return result
