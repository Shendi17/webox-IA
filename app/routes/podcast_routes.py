from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.podcast import Podcast
from app.services.podcast_service import PodcastService

router = APIRouter(prefix="/api/podcasts", tags=["podcasts"])
podcast_service = PodcastService()

# Modèles Pydantic
class PodcastCreate(BaseModel):
    topic: str
    style: str = "conversational"
    duration: int = 5  # minutes
    language: str = "fr"
    voice: str = "alloy"
    background_music: Optional[str] = None
    music_volume: int = 20

class PodcastUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

# Routes
@router.get("/voices")
async def get_voices():
    """Obtenir la liste des voix disponibles"""
    try:
        voices = podcast_service.get_available_voices()
        return {
            "success": True,
            "voices": voices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/styles")
async def get_styles():
    """Obtenir la liste des styles disponibles"""
    try:
        styles = podcast_service.get_podcast_styles()
        return {
            "success": True,
            "styles": styles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_podcast(podcast_data: PodcastCreate, db: Session = Depends(get_db)):
    """Générer un nouveau podcast"""
    try:
        # Créer l'entrée dans la base de données
        new_podcast = Podcast(
            user_id=1,  # TODO: Récupérer l'utilisateur authentifié
            topic=podcast_data.topic,
            style=podcast_data.style,
            duration=podcast_data.duration * 60,  # Convertir en secondes
            language=podcast_data.language,
            voice_id=podcast_data.voice,
            background_music=podcast_data.background_music,
            music_volume=podcast_data.music_volume,
            status="generating"
        )
        
        db.add(new_podcast)
        db.commit()
        db.refresh(new_podcast)
        
        # Générer le podcast
        result = podcast_service.generate_full_podcast({
            "topic": podcast_data.topic,
            "style": podcast_data.style,
            "duration": podcast_data.duration,
            "language": podcast_data.language,
            "voice": podcast_data.voice
        })
        
        if not result.get("success"):
            new_podcast.status = "failed"
            db.commit()
            return {
                "success": False,
                "error": result.get("error"),
                "podcast_id": new_podcast.id
            }
        
        # Mettre à jour le podcast avec les résultats
        script = result.get("script", {})
        new_podcast.title = script.get("title", podcast_data.topic)
        new_podcast.description = f"Podcast sur {podcast_data.topic}"
        new_podcast.script = str(script)
        new_podcast.segments = script.get("segments", [])
        new_podcast.cover_url = result.get("cover_url")
        new_podcast.cover_prompt = result.get("cover_prompt")
        new_podcast.audio_url = result.get("audio_file")
        new_podcast.audio_size = result.get("audio_size")
        new_podcast.generation_time = result.get("generation_time")
        new_podcast.status = "completed"
        
        db.commit()
        db.refresh(new_podcast)
        
        return {
            "success": True,
            "message": "Podcast généré avec succès",
            "podcast": new_podcast.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_podcasts(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lister les podcasts"""
    try:
        query = db.query(Podcast)
        
        if status:
            query = query.filter(Podcast.status == status)
        
        total = query.count()
        podcasts = query.order_by(Podcast.created_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "podcasts": [p.to_dict() for p in podcasts],
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{podcast_id}")
async def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    """Obtenir un podcast spécifique"""
    try:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        
        if not podcast:
            raise HTTPException(status_code=404, detail="Podcast non trouvé")
        
        return {
            "success": True,
            "podcast": podcast.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{podcast_id}")
async def update_podcast(
    podcast_id: int,
    podcast_update: PodcastUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un podcast"""
    try:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        
        if not podcast:
            raise HTTPException(status_code=404, detail="Podcast non trouvé")
        
        # Mettre à jour les champs
        if podcast_update.title:
            podcast.title = podcast_update.title
        if podcast_update.description:
            podcast.description = podcast_update.description
        if podcast_update.status:
            podcast.status = podcast_update.status
        
        db.commit()
        db.refresh(podcast)
        
        return {
            "success": True,
            "message": "Podcast mis à jour",
            "podcast": podcast.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{podcast_id}")
async def delete_podcast(podcast_id: int, db: Session = Depends(get_db)):
    """Supprimer un podcast"""
    try:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        
        if not podcast:
            raise HTTPException(status_code=404, detail="Podcast non trouvé")
        
        db.delete(podcast)
        db.commit()
        
        return {
            "success": True,
            "message": "Podcast supprimé"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{podcast_id}/play")
async def play_podcast(podcast_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de lectures"""
    try:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        
        if not podcast:
            raise HTTPException(status_code=404, detail="Podcast non trouvé")
        
        podcast.plays_count += 1
        db.commit()
        
        return {
            "success": True,
            "plays_count": podcast.plays_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{podcast_id}/download")
async def download_podcast(podcast_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de téléchargements"""
    try:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        
        if not podcast:
            raise HTTPException(status_code=404, detail="Podcast non trouvé")
        
        podcast.downloads_count += 1
        db.commit()
        
        return {
            "success": True,
            "downloads_count": podcast.downloads_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_podcasts = db.query(Podcast).count()
        completed_podcasts = db.query(Podcast).filter(Podcast.status == "completed").count()
        total_plays = db.query(Podcast).with_entities(db.func.sum(Podcast.plays_count)).scalar() or 0
        total_downloads = db.query(Podcast).with_entities(db.func.sum(Podcast.downloads_count)).scalar() or 0
        
        return {
            "success": True,
            "stats": {
                "total_podcasts": total_podcasts,
                "completed_podcasts": completed_podcasts,
                "total_plays": total_plays,
                "total_downloads": total_downloads
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
