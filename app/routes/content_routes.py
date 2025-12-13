"""
Routes API pour le Content Engine
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user
from app.services.content_generator_service import ContentGeneratorService
from app.models.content_db import Content, ContentType, ContentStatus, SocialPlatform, ContentCalendar

router = APIRouter(prefix="/api/content", tags=["Content Engine"])


# ==================== SCHEMAS ====================

class BlogGenerateRequest(BaseModel):
    """Schéma pour générer un article de blog"""
    topic: str
    keywords: Optional[List[str]] = []
    length: int = 2000
    tone: str = "professionnel"
    include_images: bool = True


class SocialGenerateRequest(BaseModel):
    """Schéma pour générer des posts sociaux"""
    platform: str
    topic: str
    count: int = 5
    format: str = "post"
    tone: str = "engageant"


class EmailGenerateRequest(BaseModel):
    """Schéma pour générer un email"""
    email_type: str
    topic: str
    target_audience: str = "général"
    tone: str = "professionnel"


class VideoScriptRequest(BaseModel):
    """Schéma pour générer un script vidéo"""
    topic: str
    duration: int = 60
    style: str = "éducatif"
    platform: str = "youtube"


class ContentCreate(BaseModel):
    """Schéma pour créer un contenu"""
    title: str
    content_type: str
    content: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = []
    hashtags: Optional[List[str]] = []
    platform: Optional[str] = None


class ContentUpdate(BaseModel):
    """Schéma pour mettre à jour un contenu"""
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class CalendarEntryCreate(BaseModel):
    """Schéma pour créer une entrée de calendrier"""
    title: str
    description: Optional[str] = None
    content_type: str
    platform: Optional[str] = None
    scheduled_date: datetime
    is_recurring: bool = False


# ==================== ROUTES GÉNÉRATION ====================

@router.post("/generate/blog")
async def generate_blog(
    data: BlogGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Générer un article de blog avec IA
    
    Args:
        data: Paramètres de génération
    
    Returns:
        Article généré
    """
    try:
        generator = ContentGeneratorService()
        
        result = generator.generate_blog_article(
            topic=data.topic,
            keywords=data.keywords,
            length=data.length,
            tone=data.tone,
            include_images=data.include_images
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        article = result["content"]
        
        # Créer le contenu dans la base
        content = Content(
            title=article["title"],
            content_type=ContentType.BLOG,
            content=article["content"],
            meta_description=article.get("meta_description"),
            keywords=article.get("keywords"),
            word_count=article.get("word_count"),
            reading_time=article.get("reading_time"),
            author_id=current_user.id,
            author_name=current_user.name,
            generation_params=data.dict(),
            ai_model="gpt-4"
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        return {
            "success": True,
            "content": content.to_dict(),
            "images_suggestions": article.get("images_suggestions", [])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/social")
async def generate_social(
    data: SocialGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Générer des posts pour réseaux sociaux
    
    Args:
        data: Paramètres de génération
    
    Returns:
        Posts générés
    """
    try:
        generator = ContentGeneratorService()
        
        result = generator.generate_social_posts(
            platform=data.platform,
            topic=data.topic,
            count=data.count,
            format=data.format,
            tone=data.tone
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Créer les contenus dans la base
        created_contents = []
        
        for post in result.get("posts", []):
            content = Content(
                title=f"{data.topic} - {data.platform}",
                content_type=ContentType.SOCIAL,
                format=data.format,
                content=post.get("text"),
                hashtags=post.get("hashtags"),
                platform=SocialPlatform[data.platform.upper()],
                platform_specific={"visual_suggestion": post.get("visual_suggestion")},
                author_id=current_user.id,
                author_name=current_user.name,
                generation_params=data.dict(),
                ai_model="gpt-4"
            )
            
            db.add(content)
            db.flush()
            created_contents.append(content.to_dict())
        
        db.commit()
        
        return {
            "success": True,
            "contents": created_contents,
            "count": len(created_contents)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/email")
async def generate_email(
    data: EmailGenerateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Générer un email
    
    Args:
        data: Paramètres de génération
    
    Returns:
        Email généré
    """
    try:
        generator = ContentGeneratorService()
        
        result = generator.generate_email(
            email_type=data.email_type,
            topic=data.topic,
            target_audience=data.target_audience,
            tone=data.tone
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        email = result["email"]
        
        # Créer le contenu dans la base
        content = Content(
            title=email["subject"],
            content_type=ContentType.EMAIL,
            format=data.email_type,
            content=email["content"],
            summary=email.get("preheader"),
            author_id=current_user.id,
            author_name=current_user.name,
            generation_params=data.dict(),
            ai_model="gpt-4"
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        return {
            "success": True,
            "content": content.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/video-script")
async def generate_video_script(
    data: VideoScriptRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Générer un script vidéo
    
    Args:
        data: Paramètres de génération
    
    Returns:
        Script généré
    """
    try:
        generator = ContentGeneratorService()
        
        result = generator.generate_video_script(
            topic=data.topic,
            duration=data.duration,
            style=data.style,
            platform=data.platform
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        script = result["script"]
        
        # Créer le contenu dans la base
        content = Content(
            title=f"Script: {data.topic}",
            content_type=ContentType.VIDEO,
            format="script",
            content=script["content"],
            platform=SocialPlatform[data.platform.upper()] if data.platform.upper() in SocialPlatform.__members__ else None,
            author_id=current_user.id,
            author_name=current_user.name,
            generation_params=data.dict(),
            ai_model="gpt-4"
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        return {
            "success": True,
            "content": content.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ROUTES CRUD CONTENUS ====================

@router.post("/contents")
async def create_content(
    data: ContentCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un contenu manuellement"""
    try:
        content = Content(
            title=data.title,
            content_type=ContentType[data.content_type.upper()],
            content=data.content,
            summary=data.summary,
            keywords=data.keywords,
            hashtags=data.hashtags,
            platform=SocialPlatform[data.platform.upper()] if data.platform else None,
            author_id=current_user.id,
            author_name=current_user.name
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        return {
            "success": True,
            "content": content.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contents")
async def list_contents(
    content_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lister les contenus"""
    try:
        query = db.query(Content).filter(Content.author_id == current_user.id)
        
        if content_type:
            query = query.filter(Content.content_type == ContentType[content_type.upper()])
        
        if status:
            query = query.filter(Content.status == ContentStatus[status.upper()])
        
        query = query.order_by(Content.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        contents = query.all()
        
        return {
            "success": True,
            "contents": [c.to_dict() for c in contents],
            "total": len(contents)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contents/{content_id}")
async def get_content(
    content_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir un contenu"""
    try:
        content = db.query(Content).filter(
            Content.id == content_id,
            Content.author_id == current_user.id
        ).first()
        
        if not content:
            raise HTTPException(status_code=404, detail="Contenu non trouvé")
        
        return {
            "success": True,
            "content": content.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/contents/{content_id}")
async def update_content(
    content_id: int,
    data: ContentUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un contenu"""
    try:
        content = db.query(Content).filter(
            Content.id == content_id,
            Content.author_id == current_user.id
        ).first()
        
        if not content:
            raise HTTPException(status_code=404, detail="Contenu non trouvé")
        
        # Mettre à jour les champs
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        
        for key, value in update_data.items():
            if key == "status":
                value = ContentStatus[value.upper()]
            setattr(content, key, value)
        
        content.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(content)
        
        return {
            "success": True,
            "content": content.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/contents/{content_id}")
async def delete_content(
    content_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un contenu"""
    try:
        content = db.query(Content).filter(
            Content.id == content_id,
            Content.author_id == current_user.id
        ).first()
        
        if not content:
            raise HTTPException(status_code=404, detail="Contenu non trouvé")
        
        db.delete(content)
        db.commit()
        
        return {
            "success": True,
            "message": "Contenu supprimé"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ROUTES CALENDRIER ====================

@router.post("/calendar")
async def create_calendar_entry(
    data: CalendarEntryCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer une entrée de calendrier"""
    try:
        entry = ContentCalendar(
            title=data.title,
            description=data.description,
            content_type=ContentType[data.content_type.upper()],
            platform=SocialPlatform[data.platform.upper()] if data.platform else None,
            scheduled_date=data.scheduled_date,
            is_recurring=data.is_recurring,
            author_id=current_user.id
        )
        
        db.add(entry)
        db.commit()
        db.refresh(entry)
        
        return {
            "success": True,
            "entry": entry.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar")
async def get_calendar(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir le calendrier éditorial"""
    try:
        query = db.query(ContentCalendar).filter(ContentCalendar.author_id == current_user.id)
        
        if start_date:
            query = query.filter(ContentCalendar.scheduled_date >= start_date)
        
        if end_date:
            query = query.filter(ContentCalendar.scheduled_date <= end_date)
        
        query = query.order_by(ContentCalendar.scheduled_date)
        
        entries = query.all()
        
        return {
            "success": True,
            "entries": [e.to_dict() for e in entries]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
