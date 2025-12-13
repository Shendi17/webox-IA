from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.avatar import Avatar
from app.services.avatar_service import AvatarService

router = APIRouter(prefix="/api/avatars", tags=["avatars"])
avatar_service = AvatarService()

# Modèles Pydantic
class AvatarCreate(BaseModel):
    name: str
    description: Optional[str] = None
    style: str = "realistic"
    gender: str = "neutral"
    age_range: str = "adult"
    hair_color: Optional[str] = None
    hair_style: Optional[str] = None
    eye_color: Optional[str] = None
    skin_tone: Optional[str] = None
    accessories: Optional[List[str]] = None
    clothing: Optional[str] = None
    background: Optional[str] = None
    category: Optional[str] = "profile"
    tags: Optional[List[str]] = None

class AvatarUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[int] = None
    tags: Optional[List[str]] = None

# Routes
@router.get("/styles")
async def get_styles():
    """Obtenir la liste des styles disponibles"""
    try:
        styles = avatar_service.get_avatar_styles()
        return {
            "success": True,
            "styles": styles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customization-options")
async def get_customization_options():
    """Obtenir toutes les options de personnalisation"""
    try:
        options = avatar_service.get_customization_options()
        return {
            "success": True,
            "options": options
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories():
    """Obtenir les catégories d'avatars"""
    try:
        categories = avatar_service.get_avatar_categories()
        return {
            "success": True,
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_avatar(avatar_data: AvatarCreate, db: Session = Depends(get_db)):
    """Générer un nouvel avatar"""
    try:
        # Créer l'entrée dans la base de données
        new_avatar = Avatar(
            user_id=1,  # TODO: Récupérer l'utilisateur authentifié
            name=avatar_data.name,
            description=avatar_data.description,
            style=avatar_data.style,
            gender=avatar_data.gender,
            age_range=avatar_data.age_range,
            hair_color=avatar_data.hair_color,
            hair_style=avatar_data.hair_style,
            eye_color=avatar_data.eye_color,
            skin_tone=avatar_data.skin_tone,
            accessories=avatar_data.accessories,
            clothing=avatar_data.clothing,
            background=avatar_data.background,
            category=avatar_data.category,
            tags=avatar_data.tags
        )
        
        db.add(new_avatar)
        db.commit()
        db.refresh(new_avatar)
        
        # Générer l'avatar
        result = avatar_service.generate_avatar({
            "style": avatar_data.style,
            "gender": avatar_data.gender,
            "age_range": avatar_data.age_range,
            "description": avatar_data.description,
            "hair_color": avatar_data.hair_color,
            "hair_style": avatar_data.hair_style,
            "eye_color": avatar_data.eye_color,
            "skin_tone": avatar_data.skin_tone,
            "accessories": avatar_data.accessories,
            "clothing": avatar_data.clothing,
            "background": avatar_data.background
        })
        
        if not result.get("success"):
            db.delete(new_avatar)
            db.commit()
            return {
                "success": False,
                "error": result.get("error")
            }
        
        # Mettre à jour l'avatar avec les résultats
        new_avatar.image_url = result.get("image_url")
        new_avatar.prompt = result.get("prompt")
        new_avatar.ai_model = result.get("ai_model")
        new_avatar.generation_time = result.get("generation_time")
        
        db.commit()
        db.refresh(new_avatar)
        
        return {
            "success": True,
            "message": "Avatar généré avec succès",
            "avatar": new_avatar.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_avatars(
    skip: int = 0,
    limit: int = 20,
    style: Optional[str] = None,
    category: Optional[str] = None,
    is_public: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Lister les avatars"""
    try:
        query = db.query(Avatar)
        
        if style:
            query = query.filter(Avatar.style == style)
        if category:
            query = query.filter(Avatar.category == category)
        if is_public is not None:
            query = query.filter(Avatar.is_public == is_public)
        
        total = query.count()
        avatars = query.order_by(Avatar.created_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "avatars": [a.to_dict() for a in avatars],
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{avatar_id}")
async def get_avatar(avatar_id: int, db: Session = Depends(get_db)):
    """Obtenir un avatar spécifique"""
    try:
        avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar non trouvé")
        
        return {
            "success": True,
            "avatar": avatar.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{avatar_id}")
async def update_avatar(
    avatar_id: int,
    avatar_update: AvatarUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un avatar"""
    try:
        avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar non trouvé")
        
        # Mettre à jour les champs
        if avatar_update.name:
            avatar.name = avatar_update.name
        if avatar_update.description:
            avatar.description = avatar_update.description
        if avatar_update.is_public is not None:
            avatar.is_public = avatar_update.is_public
        if avatar_update.tags:
            avatar.tags = avatar_update.tags
        
        db.commit()
        db.refresh(avatar)
        
        return {
            "success": True,
            "message": "Avatar mis à jour",
            "avatar": avatar.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{avatar_id}")
async def delete_avatar(avatar_id: int, db: Session = Depends(get_db)):
    """Supprimer un avatar"""
    try:
        avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar non trouvé")
        
        db.delete(avatar)
        db.commit()
        
        return {
            "success": True,
            "message": "Avatar supprimé"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{avatar_id}/download")
async def download_avatar(avatar_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de téléchargements"""
    try:
        avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar non trouvé")
        
        avatar.downloads_count += 1
        db.commit()
        
        return {
            "success": True,
            "downloads_count": avatar.downloads_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{avatar_id}/share")
async def share_avatar(avatar_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de partages"""
    try:
        avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
        
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar non trouvé")
        
        avatar.shares_count += 1
        db.commit()
        
        return {
            "success": True,
            "shares_count": avatar.shares_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_avatars = db.query(Avatar).count()
        total_downloads = db.query(Avatar).with_entities(db.func.sum(Avatar.downloads_count)).scalar() or 0
        total_shares = db.query(Avatar).with_entities(db.func.sum(Avatar.shares_count)).scalar() or 0
        public_avatars = db.query(Avatar).filter(Avatar.is_public == 1).count()
        
        # Stats par style
        styles_stats = {}
        for style in ["realistic", "cartoon", "anime", "pixel-art", "3d"]:
            count = db.query(Avatar).filter(Avatar.style == style).count()
            styles_stats[style] = count
        
        return {
            "success": True,
            "stats": {
                "total_avatars": total_avatars,
                "total_downloads": total_downloads,
                "total_shares": total_shares,
                "public_avatars": public_avatars,
                "styles_stats": styles_stats
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
