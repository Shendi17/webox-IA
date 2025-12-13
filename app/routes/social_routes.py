"""
Routes API pour les Réseaux Sociaux
Date : 15 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.models.social_db import SocialAccountDB, ScheduledPostDB, PostAnalyticsDB
from app.middleware.auth import get_current_user_from_token
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/social", tags=["social"])


# ============================================
# MODÈLES PYDANTIC
# ============================================

class PostCreate(BaseModel):
    content: str
    media_urls: Optional[List[str]] = []
    platforms: List[str]
    hashtags: Optional[List[str]] = []
    scheduled_time: Optional[datetime] = None

class GenerateCaptionRequest(BaseModel):
    topic: str
    tone: str = "professional"  # professional, casual, funny, inspirational
    platform: str = "instagram"

class GenerateHashtagsRequest(BaseModel):
    content: str
    platform: str = "instagram"
    count: int = 10


# ============================================
# PAGE PRINCIPALE
# ============================================

@router.get("", response_class=HTMLResponse)
async def social_page(
    request: Request,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Page de gestion des réseaux sociaux
    """
    return templates.TemplateResponse(
        "dashboard/social.html",
        {"request": request, "user": current_user}
    )


# ============================================
# GESTION DES COMPTES
# ============================================

@router.get("/api/accounts")
async def get_accounts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Liste des comptes de réseaux sociaux connectés
    """
    accounts = db.query(SocialAccountDB).filter(
        SocialAccountDB.user_id == current_user["id"]
    ).all()
    
    return {
        "success": True,
        "accounts": [acc.to_dict() for acc in accounts]
    }


@router.post("/api/connect/{platform}")
async def connect_platform(
    platform: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Initier la connexion OAuth à une plateforme
    """
    # Simulation - en production, rediriger vers OAuth
    if platform not in ['instagram', 'facebook', 'twitter', 'linkedin', 'tiktok', 'youtube']:
        raise HTTPException(status_code=400, detail="Plateforme non supportée")
    
    # Créer un compte fictif pour la démo
    account = SocialAccountDB(
        user_id=current_user["id"],
        platform=platform,
        account_name=f"@demo_{platform}",
        account_id=f"demo_{platform}_123",
        access_token="demo_token",
        is_active=True
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    
    return {
        "success": True,
        "message": f"Compte {platform} connecté",
        "account": account.to_dict()
    }


@router.delete("/api/disconnect/{account_id}")
async def disconnect_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Déconnecter un compte
    """
    account = db.query(SocialAccountDB).filter(
        SocialAccountDB.id == account_id,
        SocialAccountDB.user_id == current_user["id"]
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    
    db.delete(account)
    db.commit()
    
    return {"success": True, "message": "Compte déconnecté"}


# ============================================
# GESTION DES POSTS
# ============================================

@router.post("/api/posts")
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Créer un post programmé
    """
    # Vérifier que l'utilisateur a les comptes connectés
    for platform in post.platforms:
        account = db.query(SocialAccountDB).filter(
            SocialAccountDB.user_id == current_user["id"],
            SocialAccountDB.platform == platform,
            SocialAccountDB.is_active == True
        ).first()
        
        if not account:
            raise HTTPException(
                status_code=400,
                detail=f"Compte {platform} non connecté"
            )
    
    # Créer le post
    scheduled_post = ScheduledPostDB(
        user_id=current_user["id"],
        content=post.content,
        media_urls=post.media_urls,
        platforms=post.platforms,
        hashtags=post.hashtags,
        scheduled_time=post.scheduled_time or datetime.utcnow(),
        status="scheduled" if post.scheduled_time else "draft"
    )
    
    db.add(scheduled_post)
    db.commit()
    db.refresh(scheduled_post)
    
    return {
        "success": True,
        "post": scheduled_post.to_dict()
    }


@router.get("/api/posts")
async def get_posts(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Liste des posts
    """
    query = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.user_id == current_user["id"]
    )
    
    if status:
        query = query.filter(ScheduledPostDB.status == status)
    
    posts = query.order_by(
        ScheduledPostDB.scheduled_time.desc()
    ).offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "posts": [post.to_dict() for post in posts],
        "total": query.count()
    }


@router.get("/api/posts/{post_id}")
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Détails d'un post
    """
    post = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.id == post_id,
        ScheduledPostDB.user_id == current_user["id"]
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    
    return {"success": True, "post": post.to_dict()}


@router.put("/api/posts/{post_id}")
async def update_post(
    post_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Modifier un post
    """
    post = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.id == post_id,
        ScheduledPostDB.user_id == current_user["id"]
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    
    post.content = post_data.content
    post.media_urls = post_data.media_urls
    post.platforms = post_data.platforms
    post.hashtags = post_data.hashtags
    if post_data.scheduled_time:
        post.scheduled_time = post_data.scheduled_time
    
    db.commit()
    db.refresh(post)
    
    return {"success": True, "post": post.to_dict()}


@router.delete("/api/posts/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Supprimer un post
    """
    post = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.id == post_id,
        ScheduledPostDB.user_id == current_user["id"]
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    
    db.delete(post)
    db.commit()
    
    return {"success": True, "message": "Post supprimé"}


@router.post("/api/posts/{post_id}/publish")
async def publish_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Publier un post immédiatement
    """
    post = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.id == post_id,
        ScheduledPostDB.user_id == current_user["id"]
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post non trouvé")
    
    # Simulation de publication
    post.status = "published"
    post.published_at = datetime.utcnow()
    post.platform_post_ids = {platform: f"demo_{platform}_post_123" for platform in post.platforms}
    
    db.commit()
    db.refresh(post)
    
    return {
        "success": True,
        "message": "Post publié",
        "post": post.to_dict()
    }


# ============================================
# GÉNÉRATION IA
# ============================================

@router.post("/api/generate/caption")
async def generate_caption(
    request: GenerateCaptionRequest,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer une caption avec GPT-4
    """
    # Simulation - en production, utiliser GPT-4
    import asyncio
    await asyncio.sleep(1)
    
    captions = {
        "professional": f"🎯 {request.topic}\n\nDécouvrez comment transformer votre approche et atteindre vos objectifs. #Business #Success",
        "casual": f"Hey ! 👋 On parle de {request.topic} aujourd'hui. C'est trop cool ! 🔥 #Lifestyle",
        "funny": f"😂 Quand tu réalises que {request.topic}... LOL! #Humour #Fun",
        "inspirational": f"✨ {request.topic}\n\nChaque jour est une nouvelle opportunité de grandir. Croyez en vous ! 💪 #Motivation"
    }
    
    caption = captions.get(request.tone, captions["professional"])
    
    return {
        "success": True,
        "caption": caption,
        "cost": 0.03
    }


@router.post("/api/generate/hashtags")
async def generate_hashtags(
    request: GenerateHashtagsRequest,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer des hashtags avec GPT-4
    """
    # Simulation - en production, utiliser GPT-4
    import asyncio
    await asyncio.sleep(0.5)
    
    hashtags = [
        "#trending", "#viral", "#instagood", "#photooftheday",
        "#love", "#beautiful", "#happy", "#fashion",
        "#style", "#inspiration"
    ][:request.count]
    
    return {
        "success": True,
        "hashtags": hashtags,
        "cost": 0.01
    }


@router.get("/api/suggest/times")
async def suggest_best_times(
    platform: str = "instagram",
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Suggérer les meilleurs moments de publication
    """
    best_times = {
        "instagram": {
            "monday": ["09:00", "18:00"],
            "tuesday": ["10:00", "19:00"],
            "wednesday": ["11:00", "20:00"],
            "thursday": ["10:00", "18:00"],
            "friday": ["09:00", "17:00"],
            "saturday": ["11:00", "19:00"],
            "sunday": ["10:00", "18:00"]
        },
        "facebook": {
            "monday": ["13:00", "19:00"],
            "tuesday": ["12:00", "18:00"],
            "wednesday": ["13:00", "19:00"],
            "thursday": ["12:00", "18:00"],
            "friday": ["13:00", "17:00"],
            "saturday": ["12:00", "18:00"],
            "sunday": ["13:00", "19:00"]
        }
    }
    
    return {
        "success": True,
        "platform": platform,
        "best_times": best_times.get(platform, best_times["instagram"])
    }


# ============================================
# STATISTIQUES
# ============================================

@router.get("/api/stats/overview")
async def get_stats_overview(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Vue d'ensemble des statistiques
    """
    # Compter les posts
    total_posts = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.user_id == current_user["id"]
    ).count()
    
    published_posts = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.user_id == current_user["id"],
        ScheduledPostDB.status == "published"
    ).count()
    
    scheduled_posts = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.user_id == current_user["id"],
        ScheduledPostDB.status == "scheduled"
    ).count()
    
    # Compter les comptes
    connected_accounts = db.query(SocialAccountDB).filter(
        SocialAccountDB.user_id == current_user["id"],
        SocialAccountDB.is_active == True
    ).count()
    
    return {
        "success": True,
        "stats": {
            "total_posts": total_posts,
            "published_posts": published_posts,
            "scheduled_posts": scheduled_posts,
            "connected_accounts": connected_accounts,
            "total_engagement": 0,  # À calculer depuis post_analytics
            "avg_engagement_rate": 0.0
        }
    }


@router.get("/api/stats/{platform}")
async def get_platform_stats(
    platform: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Statistiques par plateforme
    """
    # Récupérer les posts de cette plateforme
    posts = db.query(ScheduledPostDB).filter(
        ScheduledPostDB.user_id == current_user["id"],
        ScheduledPostDB.platforms.contains([platform])
    ).all()
    
    return {
        "success": True,
        "platform": platform,
        "total_posts": len(posts),
        "stats": {
            "views": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0
        }
    }
