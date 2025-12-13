"""
Routes API pour les Influenceurs IA
Date : 15 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.models.influencer_db import AIInfluencerDB, InfluencerContentDB
from app.middleware.auth import get_current_user_from_token

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/influencers", tags=["influencers"])


# ============================================
# MODÈLES PYDANTIC
# ============================================

class InfluencerCreate(BaseModel):
    name: str
    description: Optional[str] = None
    niche: str  # fitness, fashion, tech, lifestyle, beauty, travel
    gender: str  # male, female, non-binary
    ethnicity: Optional[str] = "caucasian"
    age_range: str = "25-35"
    style: str = "casual"
    personality_traits: Optional[List[str]] = []
    tone_of_voice: str = "friendly"

class ContentGenerate(BaseModel):
    influencer_id: int
    content_type: str = "image"  # image, video, carousel
    prompt: str
    pose: Optional[str] = "standing"
    location: Optional[str] = "studio"
    outfit: Optional[str] = "casual"
    generate_caption: bool = True


# ============================================
# PAGE PRINCIPALE
# ============================================

@router.get("", response_class=HTMLResponse)
async def influencers_page(
    request: Request,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Page de gestion des influenceurs IA
    """
    return templates.TemplateResponse(
        "dashboard/influencers.html",
        {"request": request, "user": current_user}
    )


# ============================================
# GESTION DES INFLUENCEURS
# ============================================

@router.post("/api/create")
async def create_influencer(
    influencer: InfluencerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Créer un nouvel influenceur IA
    """
    # Créer l'influenceur
    new_influencer = AIInfluencerDB(
        user_id=current_user["id"],
        name=influencer.name,
        description=influencer.description,
        niche=influencer.niche,
        gender=influencer.gender,
        ethnicity=influencer.ethnicity,
        age_range=influencer.age_range,
        style=influencer.style,
        personality_traits=influencer.personality_traits,
        tone_of_voice=influencer.tone_of_voice,
        generation_settings={
            "model": "stable-diffusion-xl",
            "quality": "high",
            "consistency": "strict"
        }
    )
    
    db.add(new_influencer)
    db.commit()
    db.refresh(new_influencer)
    
    return {
        "success": True,
        "influencer": new_influencer.to_dict(),
        "message": f"Influenceur {influencer.name} créé !"
    }


@router.get("/api/list")
async def list_influencers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Liste des influenceurs de l'utilisateur
    """
    influencers = db.query(AIInfluencerDB).filter(
        AIInfluencerDB.user_id == current_user["id"],
        AIInfluencerDB.is_active == True
    ).all()
    
    return {
        "success": True,
        "influencers": [inf.to_dict() for inf in influencers]
    }


@router.get("/api/{influencer_id}")
async def get_influencer(
    influencer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Détails d'un influenceur
    """
    influencer = db.query(AIInfluencerDB).filter(
        AIInfluencerDB.id == influencer_id,
        AIInfluencerDB.user_id == current_user["id"]
    ).first()
    
    if not influencer:
        raise HTTPException(status_code=404, detail="Influenceur non trouvé")
    
    return {
        "success": True,
        "influencer": influencer.to_dict()
    }


@router.put("/api/{influencer_id}")
async def update_influencer(
    influencer_id: int,
    data: InfluencerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Modifier un influenceur
    """
    influencer = db.query(AIInfluencerDB).filter(
        AIInfluencerDB.id == influencer_id,
        AIInfluencerDB.user_id == current_user["id"]
    ).first()
    
    if not influencer:
        raise HTTPException(status_code=404, detail="Influenceur non trouvé")
    
    influencer.name = data.name
    influencer.description = data.description
    influencer.niche = data.niche
    influencer.style = data.style
    influencer.personality_traits = data.personality_traits
    influencer.tone_of_voice = data.tone_of_voice
    
    db.commit()
    db.refresh(influencer)
    
    return {
        "success": True,
        "influencer": influencer.to_dict()
    }


@router.delete("/api/{influencer_id}")
async def delete_influencer(
    influencer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Supprimer un influenceur
    """
    influencer = db.query(AIInfluencerDB).filter(
        AIInfluencerDB.id == influencer_id,
        AIInfluencerDB.user_id == current_user["id"]
    ).first()
    
    if not influencer:
        raise HTTPException(status_code=404, detail="Influenceur non trouvé")
    
    influencer.is_active = False
    db.commit()
    
    return {"success": True, "message": "Influenceur supprimé"}


# ============================================
# GÉNÉRATION DE CONTENU
# ============================================

@router.post("/api/generate")
async def generate_content(
    request: ContentGenerate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer du contenu pour un influenceur
    """
    # Vérifier que l'influenceur existe
    influencer = db.query(AIInfluencerDB).filter(
        AIInfluencerDB.id == request.influencer_id,
        AIInfluencerDB.user_id == current_user["id"]
    ).first()
    
    if not influencer:
        raise HTTPException(status_code=404, detail="Influenceur non trouvé")
    
    # Créer le contenu
    content = InfluencerContentDB(
        user_id=current_user["id"],
        influencer_id=request.influencer_id,
        content_type=request.content_type,
        prompt=request.prompt,
        pose=request.pose,
        location=request.location,
        outfit=request.outfit,
        status="pending",
        generation_params={
            "model": "stable-diffusion-xl",
            "face_consistency": True,
            "quality": "high"
        }
    )
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    # Lancer la génération en arrière-plan
    background_tasks.add_task(_generate_content_task, content.id, db)
    
    return {
        "success": True,
        "content": content.to_dict(),
        "message": "Génération lancée"
    }


async def _generate_content_task(content_id: int, db: Session):
    """
    Tâche de génération de contenu (simulation)
    """
    import asyncio
    
    content = db.query(InfluencerContentDB).filter(
        InfluencerContentDB.id == content_id
    ).first()
    
    if not content:
        return
    
    try:
        content.status = "generating"
        db.commit()
        
        # Simulation de génération (3 secondes)
        await asyncio.sleep(3)
        
        # En production, utiliser Stable Diffusion avec face embedding
        content.generated_url = f"/uploads/influencer_{content.influencer_id}_content_{content.id}.jpg"
        
        # Générer caption si demandé
        if content.content_type == "image":
            content.caption = f"✨ {content.prompt} #AI #DigitalInfluencer"
            content.hashtags = ["#AI", "#DigitalInfluencer", "#VirtualModel"]
        
        content.cost = 0.30
        content.status = "completed"
        content.completed_at = datetime.utcnow()
        
        # Mettre à jour les stats de l'influenceur
        influencer = db.query(AIInfluencerDB).filter(
            AIInfluencerDB.id == content.influencer_id
        ).first()
        
        if influencer:
            influencer.total_posts += 1
            if content.content_type == "image":
                influencer.total_images += 1
        
        db.commit()
        
    except Exception as e:
        content.status = "failed"
        content.error_message = str(e)
        db.commit()


@router.get("/api/content")
async def list_content(
    influencer_id: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Liste du contenu généré
    """
    query = db.query(InfluencerContentDB).filter(
        InfluencerContentDB.user_id == current_user["id"]
    )
    
    if influencer_id:
        query = query.filter(InfluencerContentDB.influencer_id == influencer_id)
    
    content = query.order_by(
        InfluencerContentDB.created_at.desc()
    ).limit(limit).all()
    
    return {
        "success": True,
        "content": [c.to_dict() for c in content]
    }


@router.get("/api/content/{content_id}")
async def get_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Détails d'un contenu
    """
    content = db.query(InfluencerContentDB).filter(
        InfluencerContentDB.id == content_id,
        InfluencerContentDB.user_id == current_user["id"]
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Contenu non trouvé")
    
    return {
        "success": True,
        "content": content.to_dict()
    }


# ============================================
# STATISTIQUES
# ============================================

@router.get("/api/stats")
async def get_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Statistiques des influenceurs
    """
    total_influencers = db.query(AIInfluencerDB).filter(
        AIInfluencerDB.user_id == current_user["id"],
        AIInfluencerDB.is_active == True
    ).count()
    
    total_content = db.query(InfluencerContentDB).filter(
        InfluencerContentDB.user_id == current_user["id"]
    ).count()
    
    completed_content = db.query(InfluencerContentDB).filter(
        InfluencerContentDB.user_id == current_user["id"],
        InfluencerContentDB.status == "completed"
    ).count()
    
    return {
        "success": True,
        "stats": {
            "total_influencers": total_influencers,
            "total_content": total_content,
            "completed_content": completed_content,
            "pending_content": total_content - completed_content
        }
    }
