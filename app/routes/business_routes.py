"""
Routes API pour les Outils Business (Phase 5)
- Création de Logos
- Création de Présentations
- Email Marketing
- Landing Pages

Date : 15 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from app.models.business_db import GeneratedLogoDB, PresentationDB, LandingPageDB
from app.models.marketing_db import EmailCampaign, CampaignStatus
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class LogoGenerationRequest(BaseModel):
    company_name: str
    industry: Optional[str] = "tech"
    style: Optional[str] = "modern"
    colors: Optional[List[str]] = ["#667eea", "#764ba2"]
    symbols: Optional[str] = None

class PresentationGenerationRequest(BaseModel):
    title: str
    topic: str
    num_slides: Optional[int] = 10
    audience: Optional[str] = "clients"
    tone: Optional[str] = "professional"
    template: Optional[str] = "modern"

class EmailCampaignRequest(BaseModel):
    name: str
    subject: str
    preview_text: Optional[str] = None
    content_html: str
    recipients: Optional[List[str]] = []
    scheduled_time: Optional[str] = None

class LandingPageRequest(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    template: Optional[str] = "saas"
    colors: Optional[List[str]] = ["#667eea", "#764ba2"]
    sections: Optional[dict] = None


# ============================================================================
# PAGES HTML
# ============================================================================

@router.get("/presentations", response_class=HTMLResponse)
async def presentations_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page de création de présentations"""
    return templates.TemplateResponse("dashboard/presentations.html", {
        "request": request,
        "user": user
    })

# DEPRECATED : Route déplacée vers marketing_routes.py
# @router.get("/email-marketing", response_class=HTMLResponse)
# async def email_marketing_page(request: Request, user: dict = Depends(get_current_user_from_token)):
#     """Page d'email marketing"""
#     return templates.TemplateResponse("dashboard/email_marketing.html", {
#         "request": request,
#         "user": user
#     })

@router.get("/landing-pages", response_class=HTMLResponse)
async def landing_pages_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page de création de landing pages"""
    return templates.TemplateResponse("dashboard/landing_pages.html", {
        "request": request,
        "user": user
    })


# ============================================================================
# LOGOS - API ROUTES
# ============================================================================

@router.post("/api/logos/generate")
async def generate_logo(
    request: LogoGenerationRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Générer un logo avec IA"""
    try:
        # Créer l'entrée en base
        logo = GeneratedLogoDB(
            user_id=user["id"],
            company_name=request.company_name,
            industry=request.industry,
            style=request.style,
            colors=request.colors,
            symbols=request.symbols,
            prompt=f"Professional logo for {request.company_name}, {request.industry} industry, {request.style} style",
            status="generating",
            cost=0.50
        )
        
        db.add(logo)
        db.commit()
        db.refresh(logo)
        
        # Simuler génération en arrière-plan
        background_tasks.add_task(simulate_logo_generation, logo.id, db)
        
        return {
            "success": True,
            "message": "Génération du logo lancée !",
            "logo_id": logo.id,
            "estimated_time": "30 secondes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/logos/list")
async def list_logos(
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des logos générés"""
    try:
        logos = db.query(GeneratedLogoDB).filter(
            GeneratedLogoDB.user_id == user["id"]
        ).order_by(GeneratedLogoDB.created_at.desc()).limit(50).all()
        
        return {
            "success": True,
            "logos": [logo.to_dict() for logo in logos]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/logos/{logo_id}")
async def get_logo(
    logo_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Détails d'un logo"""
    try:
        logo = db.query(GeneratedLogoDB).filter(
            GeneratedLogoDB.id == logo_id,
            GeneratedLogoDB.user_id == user["id"]
        ).first()
        
        if not logo:
            raise HTTPException(status_code=404, detail="Logo non trouvé")
        
        return {
            "success": True,
            "logo": logo.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PRÉSENTATIONS - API ROUTES
# ============================================================================

@router.post("/api/presentations/generate")
async def generate_presentation(
    request: PresentationGenerationRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Générer une présentation avec IA"""
    try:
        # Créer l'entrée en base
        presentation = PresentationDB(
            user_id=user["id"],
            title=request.title,
            topic=request.topic,
            num_slides=request.num_slides,
            audience=request.audience,
            tone=request.tone,
            template=request.template,
            status="generating",
            cost=request.num_slides * 0.20  # $0.20 par slide
        )
        
        db.add(presentation)
        db.commit()
        db.refresh(presentation)
        
        # Simuler génération en arrière-plan
        background_tasks.add_task(simulate_presentation_generation, presentation.id, db)
        
        return {
            "success": True,
            "message": "Génération de la présentation lancée !",
            "presentation_id": presentation.id,
            "estimated_time": f"{request.num_slides * 5} secondes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/presentations/list")
async def list_presentations(
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des présentations"""
    try:
        presentations = db.query(PresentationDB).filter(
            PresentationDB.user_id == user["id"]
        ).order_by(PresentationDB.created_at.desc()).limit(50).all()
        
        return {
            "success": True,
            "presentations": [p.to_dict() for p in presentations]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/presentations/{presentation_id}")
async def get_presentation(
    presentation_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Détails d'une présentation"""
    try:
        presentation = db.query(PresentationDB).filter(
            PresentationDB.id == presentation_id,
            PresentationDB.user_id == user["id"]
        ).first()
        
        if not presentation:
            raise HTTPException(status_code=404, detail="Présentation non trouvée")
        
        return {
            "success": True,
            "presentation": presentation.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/presentations/{presentation_id}")
async def delete_presentation(
    presentation_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Supprimer une présentation"""
    try:
        presentation = db.query(PresentationDB).filter(
            PresentationDB.id == presentation_id,
            PresentationDB.user_id == user["id"]
        ).first()
        
        if not presentation:
            raise HTTPException(status_code=404, detail="Présentation non trouvée")
        
        db.delete(presentation)
        db.commit()
        
        return {
            "success": True,
            "message": "Présentation supprimée"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EMAIL MARKETING - API ROUTES
# ============================================================================

@router.post("/api/email-campaigns/create")
async def create_email_campaign(
    request: EmailCampaignRequest,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Créer une campagne email"""
    try:
        campaign = EmailCampaign(
            author_id=user["id"],
            name=request.name,
            subject=request.subject,
            preheader=request.preview_text or "",
            html_content=request.content_html,
            text_content=request.content_html,
            total_recipients=len(request.recipients) if request.recipients else 0,
            scheduled_at=datetime.fromisoformat(request.scheduled_time) if request.scheduled_time else None,
            status=CampaignStatus.DRAFT
        )
        
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        
        return {
            "success": True,
            "message": "Campagne créée !",
            "campaign_id": campaign.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/email-campaigns/list")
async def list_email_campaigns(
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des campagnes email"""
    try:
        campaigns = db.query(EmailCampaign).filter(
            EmailCampaign.author_id == user["id"]
        ).order_by(EmailCampaign.created_at.desc()).limit(50).all()
        
        return {
            "success": True,
            "campaigns": [c.to_dict() for c in campaigns]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/email-campaigns/{campaign_id}/send")
async def send_email_campaign(
    campaign_id: int,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Envoyer une campagne email"""
    try:
        campaign = db.query(EmailCampaign).filter(
            EmailCampaign.id == campaign_id,
            EmailCampaign.author_id == user["id"]
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campagne non trouvée")
        
        campaign.status = CampaignStatus.ACTIVE
        db.commit()
        
        # Simuler envoi en arrière-plan
        background_tasks.add_task(simulate_email_sending, campaign_id, db)
        
        return {
            "success": True,
            "message": "Envoi de la campagne lancé !"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/email-campaigns/{campaign_id}")
async def delete_email_campaign(
    campaign_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Supprimer une campagne"""
    try:
        campaign = db.query(EmailCampaign).filter(
            EmailCampaign.id == campaign_id,
            EmailCampaign.author_id == user["id"]
        ).first()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campagne non trouvée")
        
        db.delete(campaign)
        db.commit()
        
        return {
            "success": True,
            "message": "Campagne supprimée"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# LANDING PAGES - API ROUTES
# ============================================================================

@router.post("/api/landing-pages/create")
async def create_landing_page(
    request: LandingPageRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Créer une landing page"""
    try:
        # Générer slug unique
        import re
        slug = re.sub(r'[^a-z0-9]+', '-', request.name.lower()).strip('-')
        
        # Vérifier unicité
        existing = db.query(LandingPageDB).filter(LandingPageDB.slug == slug).first()
        if existing:
            slug = f"{slug}-{datetime.now().timestamp()}"
        
        landing_page = LandingPageDB(
            user_id=user["id"],
            name=request.name,
            slug=slug,
            title=request.title,
            description=request.description,
            template=request.template,
            colors=request.colors,
            sections=request.sections or {},
            is_published=False,
            cost=10.0  # $10 par landing page
        )
        
        db.add(landing_page)
        db.commit()
        db.refresh(landing_page)
        
        # Générer HTML en arrière-plan
        background_tasks.add_task(simulate_landing_page_generation, landing_page.id, db)
        
        return {
            "success": True,
            "message": "Landing page créée !",
            "landing_page_id": landing_page.id,
            "slug": slug
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/landing-pages/list")
async def list_landing_pages(
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des landing pages"""
    try:
        pages = db.query(LandingPageDB).filter(
            LandingPageDB.user_id == user["id"]
        ).order_by(LandingPageDB.created_at.desc()).limit(50).all()
        
        return {
            "success": True,
            "landing_pages": [p.to_dict() for p in pages]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/landing-pages/{page_id}/publish")
async def publish_landing_page(
    page_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Publier une landing page"""
    try:
        page = db.query(LandingPageDB).filter(
            LandingPageDB.id == page_id,
            LandingPageDB.user_id == user["id"]
        ).first()
        
        if not page:
            raise HTTPException(status_code=404, detail="Landing page non trouvée")
        
        page.is_published = True
        page.published_url = f"https://webox.pages/{page.slug}"
        db.commit()
        
        return {
            "success": True,
            "message": "Landing page publiée !",
            "url": page.published_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/landing-pages/{page_id}")
async def delete_landing_page(
    page_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Supprimer une landing page"""
    try:
        page = db.query(LandingPageDB).filter(
            LandingPageDB.id == page_id,
            LandingPageDB.user_id == user["id"]
        ).first()
        
        if not page:
            raise HTTPException(status_code=404, detail="Landing page non trouvée")
        
        db.delete(page)
        db.commit()
        
        return {
            "success": True,
            "message": "Landing page supprimée"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BACKGROUND TASKS (Simulations)
# ============================================================================

def simulate_logo_generation(logo_id: int, db: Session):
    """Simuler la génération d'un logo"""
    import time
    time.sleep(3)
    
    logo = db.query(GeneratedLogoDB).filter(GeneratedLogoDB.id == logo_id).first()
    if logo:
        logo.status = "completed"
        logo.variations = [
            "https://placeholder.com/logo1.png",
            "https://placeholder.com/logo2.png",
            "https://placeholder.com/logo3.png",
            "https://placeholder.com/logo4.png"
        ]
        logo.logo_main_url = "https://placeholder.com/logo1.png"
        db.commit()

def simulate_presentation_generation(presentation_id: int, db: Session):
    """Simuler la génération d'une présentation"""
    import time
    time.sleep(5)
    
    presentation = db.query(PresentationDB).filter(PresentationDB.id == presentation_id).first()
    if presentation:
        presentation.status = "completed"
        presentation.slides = [{"title": f"Slide {i+1}", "content": "Contenu généré par IA"} for i in range(presentation.num_slides)]
        presentation.pptx_url = "https://placeholder.com/presentation.pptx"
        presentation.pdf_url = "https://placeholder.com/presentation.pdf"
        db.commit()

def simulate_email_sending(campaign_id: int, db: Session):
    """Simuler l'envoi d'emails"""
    import time
    time.sleep(2)
    
    campaign = db.query(EmailCampaignDB).filter(EmailCampaignDB.id == campaign_id).first()
    if campaign:
        campaign.status = "sent"
        campaign.sent_count = campaign.total_recipients
        campaign.opened_count = int(campaign.total_recipients * 0.25)  # 25% taux d'ouverture
        campaign.clicked_count = int(campaign.total_recipients * 0.05)  # 5% taux de clic
        campaign.sent_at = datetime.utcnow()
        db.commit()

def simulate_landing_page_generation(page_id: int, db: Session):
    """Simuler la génération d'une landing page"""
    import time
    time.sleep(3)
    
    page = db.query(LandingPageDB).filter(LandingPageDB.id == page_id).first()
    if page:
        page.html_content = "<html><body><h1>Landing Page générée par IA</h1></body></html>"
        db.commit()
