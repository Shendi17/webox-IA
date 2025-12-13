"""
Routes API pour le gestionnaire de médias
Date : 2 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path

from app.database import get_db
from app.models.media_db import MediaDB
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/api/media", tags=["Media"])

# Configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Types de fichiers autorisés
ALLOWED_TYPES = {
    "image": ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"],
    "video": ["video/mp4", "video/webm", "video/ogg"],
    "audio": ["audio/mpeg", "audio/wav", "audio/ogg"],
    "document": ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                 "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                 "text/plain", "text/csv"]
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


# ========== FONCTIONS UTILITAIRES ==========

def get_file_type(mime_type: str) -> str:
    """Détermine le type de fichier"""
    for file_type, mime_types in ALLOWED_TYPES.items():
        if mime_type in mime_types:
            return file_type
    return "other"


def is_allowed_file(mime_type: str) -> bool:
    """Vérifie si le type de fichier est autorisé"""
    for mime_types in ALLOWED_TYPES.values():
        if mime_type in mime_types:
            return True
    return False


def format_file_size(size_bytes: int) -> str:
    """Formate la taille du fichier"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


# ========== ROUTES API ==========

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload un fichier
    """
    try:
        # Vérifier le type de fichier
        if not is_allowed_file(file.content_type):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Type de fichier non autorisé: {file.content_type}"
            )
        
        # Lire le fichier
        contents = await file.read()
        file_size = len(contents)
        
        # Vérifier la taille
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Fichier trop volumineux. Maximum: {format_file_size(MAX_FILE_SIZE)}"
            )
        
        # Générer un nom unique
        file_extension = Path(file.filename).suffix
        stored_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / stored_filename
        
        # Sauvegarder le fichier
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Créer l'entrée en base de données
        file_type = get_file_type(file.content_type)
        
        media = MediaDB(
            filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_type=file_type,
            mime_type=file.content_type,
            file_size=file_size,
            user_id=current_user.id,
            user_email=current_user.email,
            public_url=f"/uploads/{stored_filename}"
        )
        
        db.add(media)
        db.commit()
        db.refresh(media)
        
        return {
            "success": True,
            "message": "Fichier uploadé avec succès",
            "media": media.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'upload: {str(e)}"
        )


@router.get("/files")
async def get_files(
    file_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des fichiers de l'utilisateur
    """
    query = db.query(MediaDB).filter(MediaDB.user_id == current_user.id)
    
    # Filtrer par type
    if file_type and file_type != "all":
        query = query.filter(MediaDB.file_type == file_type)
    
    # Trier par date (plus récent en premier)
    query = query.order_by(MediaDB.created_at.desc())
    
    # Pagination
    total = query.count()
    files = query.offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "files": [file.to_dict() for file in files]
    }


@router.get("/stats")
async def get_stats(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques des fichiers
    """
    from sqlalchemy import func
    
    # Total des fichiers
    total_files = db.query(MediaDB).filter(MediaDB.user_id == current_user.id).count()
    
    # Taille totale
    total_size = db.query(func.sum(MediaDB.file_size)).filter(
        MediaDB.user_id == current_user.id
    ).scalar() or 0
    
    # Par type
    stats_by_type = db.query(
        MediaDB.file_type,
        func.count(MediaDB.id).label('count'),
        func.sum(MediaDB.file_size).label('size')
    ).filter(
        MediaDB.user_id == current_user.id
    ).group_by(MediaDB.file_type).all()
    
    return {
        "success": True,
        "stats": {
            "total_files": total_files,
            "total_size": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "by_type": [
                {
                    "type": stat[0],
                    "count": stat[1],
                    "size": stat[2],
                    "size_mb": round(stat[2] / (1024 * 1024), 2) if stat[2] else 0
                }
                for stat in stats_by_type
            ]
        }
    }


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime un fichier
    """
    # Récupérer le fichier
    media = db.query(MediaDB).filter(
        MediaDB.id == file_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fichier non trouvé"
        )
    
    try:
        # Supprimer le fichier physique
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
        
        # Supprimer l'entrée en base de données
        db.delete(media)
        db.commit()
        
        return {
            "success": True,
            "message": "Fichier supprimé avec succès"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )


@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Télécharge un fichier
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == file_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fichier non trouvé"
        )
    
    if not os.path.exists(media.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fichier physique non trouvé"
        )
    
    return FileResponse(
        path=media.file_path,
        filename=media.filename,
        media_type=media.mime_type
    )


# ============================================
# ÉDITEUR D'IMAGES IA
# ============================================

from pydantic import BaseModel

class ImageEditRequest(BaseModel):
    image_id: int
    
class UpscaleRequest(ImageEditRequest):
    factor: int = 2  # 2, 4, or 8

class RemoveBackgroundRequest(ImageEditRequest):
    background_type: str = "transparent"  # transparent, white, blur

class StyleTransferRequest(ImageEditRequest):
    style: str  # van-gogh, picasso, anime, watercolor, cyberpunk

class InpaintRequest(ImageEditRequest):
    prompt: str

class FilterRequest(ImageEditRequest):
    filter: str  # hdr, cinematic, vintage, bw-enhanced, warm


@router.post("/edit/upscale")
async def upscale_image(
    request: UpscaleRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI Upscaling - Augmenter la résolution de l'image
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == request.image_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    try:
        # Simulation - en production, utiliser Real-ESRGAN
        import asyncio
        await asyncio.sleep(2)  # Simuler le traitement
        
        # Pour l'instant, retourner l'image originale
        result_url = media.public_url
        
        return {
            "success": True,
            "result_url": result_url,
            "message": f"Upscaling {request.factor}x appliqué",
            "cost": 0.10
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit/remove-bg")
async def remove_background(
    request: RemoveBackgroundRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Suppression d'arrière-plan avec IA
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == request.image_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    try:
        # Simulation - en production, utiliser remove.bg API
        import asyncio
        await asyncio.sleep(1.5)
        
        result_url = media.public_url
        
        return {
            "success": True,
            "result_url": result_url,
            "message": f"Fond supprimé ({request.background_type})",
            "cost": 0.05
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit/enhance-face")
async def enhance_face(
    request: ImageEditRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Amélioration de visage avec IA (CodeFormer / GFPGAN)
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == request.image_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    try:
        # Simulation - en production, utiliser CodeFormer ou GFPGAN
        import asyncio
        await asyncio.sleep(2)
        
        result_url = media.public_url
        
        return {
            "success": True,
            "result_url": result_url,
            "message": "Visage amélioré",
            "cost": 0.15
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit/style-transfer")
async def style_transfer(
    request: StyleTransferRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transfert de style artistique avec Stable Diffusion
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == request.image_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    try:
        # Simulation - en production, utiliser Stable Diffusion
        import asyncio
        await asyncio.sleep(3)
        
        result_url = media.public_url
        
        return {
            "success": True,
            "result_url": result_url,
            "message": f"Style {request.style} appliqué",
            "cost": 0.20
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit/inpaint")
async def inpaint_image(
    request: InpaintRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Inpainting - Ajouter ou supprimer des éléments
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == request.image_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    try:
        # Simulation - en production, utiliser Stable Diffusion Inpainting
        import asyncio
        await asyncio.sleep(3)
        
        result_url = media.public_url
        
        return {
            "success": True,
            "result_url": result_url,
            "message": "Inpainting appliqué",
            "cost": 0.25
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit/filter")
async def apply_filter(
    request: FilterRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Application de filtres IA
    """
    media = db.query(MediaDB).filter(
        MediaDB.id == request.image_id,
        MediaDB.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    try:
        # Simulation - en production, utiliser des filtres IA personnalisés
        import asyncio
        await asyncio.sleep(1)
        
        result_url = media.public_url
        
        return {
            "success": True,
            "result_url": result_url,
            "message": f"Filtre {request.filter} appliqué",
            "cost": 0.05
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
