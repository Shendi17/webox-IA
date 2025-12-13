from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
import json
from app.database import get_db
from app.models.series import Series, Episode, Scene
from app.services.series_service import SeriesService

router = APIRouter(prefix="/api/series", tags=["series"])
series_service = SeriesService()

# Modèles Pydantic
class SeriesCreate(BaseModel):
    title: str
    description: str
    genre: str
    target_audience: str
    num_episodes: int = 10
    episode_duration: int = 5
    style: str = "realistic"

class EpisodeGenerate(BaseModel):
    series_id: int
    episode_number: int

class SceneImageGenerate(BaseModel):
    scene_id: int

# Routes pour les métadonnées
@router.get("/genres")
async def get_genres():
    """Obtenir la liste des genres"""
    try:
        genres = series_service.get_genres()
        return {"success": True, "genres": genres}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/styles")
async def get_styles():
    """Obtenir la liste des styles visuels"""
    try:
        styles = series_service.get_styles()
        return {"success": True, "styles": styles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audiences")
async def get_audiences():
    """Obtenir la liste des publics cibles"""
    try:
        audiences = series_service.get_target_audiences()
        return {"success": True, "audiences": audiences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes CRUD Séries
@router.post("/create")
async def create_series(
    series_data: SeriesCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle série et générer le concept"""
    try:
        # Créer la série
        series = Series(
            user_id=1,  # TODO: Récupérer l'utilisateur authentifié
            title=series_data.title,
            description=series_data.description,
            genre=series_data.genre,
            target_audience=series_data.target_audience,
            num_episodes=series_data.num_episodes,
            episode_duration=series_data.episode_duration,
            style=series_data.style,
            status="generating"
        )
        
        db.add(series)
        db.commit()
        db.refresh(series)
        
        # Générer le concept en arrière-plan
        background_tasks.add_task(
            generate_series_concept_task,
            series.id,
            series_data.title,
            series_data.description,
            series_data.genre,
            series_data.target_audience,
            series_data.num_episodes
        )
        
        return {
            "success": True,
            "series": series.to_dict(),
            "message": "Série en cours de génération..."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_series(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    genre: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lister les séries"""
    try:
        query = db.query(Series)
        
        if status:
            query = query.filter(Series.status == status)
        if genre:
            query = query.filter(Series.genre == genre)
        
        total = query.count()
        series = query.order_by(Series.created_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "series": [s.to_dict() for s in series],
            "total": total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{series_id}")
async def get_series(series_id: int, db: Session = Depends(get_db)):
    """Obtenir une série spécifique"""
    try:
        series = db.query(Series).filter(Series.id == series_id).first()
        
        if not series:
            raise HTTPException(status_code=404, detail="Série non trouvée")
        
        # Récupérer les épisodes
        episodes = db.query(Episode).filter(
            Episode.series_id == series_id
        ).order_by(Episode.episode_number).all()
        
        return {
            "success": True,
            "series": series.to_dict(),
            "episodes": [e.to_dict() for e in episodes]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{series_id}")
async def delete_series(series_id: int, db: Session = Depends(get_db)):
    """Supprimer une série"""
    try:
        # Supprimer les scènes
        episodes = db.query(Episode).filter(Episode.series_id == series_id).all()
        for episode in episodes:
            db.query(Scene).filter(Scene.episode_id == episode.id).delete()
        
        # Supprimer les épisodes
        db.query(Episode).filter(Episode.series_id == series_id).delete()
        
        # Supprimer la série
        series = db.query(Series).filter(Series.id == series_id).first()
        if series:
            db.delete(series)
            db.commit()
        
        return {"success": True, "message": "Série supprimée"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes Episodes
@router.get("/{series_id}/episodes")
async def get_episodes(series_id: int, db: Session = Depends(get_db)):
    """Obtenir les épisodes d'une série"""
    try:
        episodes = db.query(Episode).filter(
            Episode.series_id == series_id
        ).order_by(Episode.episode_number).all()
        
        return {
            "success": True,
            "episodes": [e.to_dict() for e in episodes]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/episodes/{episode_id}")
async def get_episode(episode_id: int, db: Session = Depends(get_db)):
    """Obtenir un épisode spécifique"""
    try:
        episode = db.query(Episode).filter(Episode.id == episode_id).first()
        
        if not episode:
            raise HTTPException(status_code=404, detail="Épisode non trouvé")
        
        # Récupérer les scènes
        scenes = db.query(Scene).filter(
            Scene.episode_id == episode_id
        ).order_by(Scene.scene_number).all()
        
        return {
            "success": True,
            "episode": episode.to_dict(),
            "scenes": [s.to_dict() for s in scenes]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/episodes/{episode_id}/generate-script")
async def generate_episode_script(
    episode_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Générer le script d'un épisode"""
    try:
        episode = db.query(Episode).filter(Episode.id == episode_id).first()
        if not episode:
            raise HTTPException(status_code=404, detail="Épisode non trouvé")
        
        series = db.query(Series).filter(Series.id == episode.series_id).first()
        
        # Générer en arrière-plan
        background_tasks.add_task(
            generate_episode_script_task,
            episode_id,
            series.title,
            episode.episode_number,
            episode.title,
            episode.description,
            series.characters,
            episode.duration
        )
        
        episode.status = "generating"
        db.commit()
        
        return {
            "success": True,
            "message": "Génération du script en cours..."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scenes/{scene_id}/generate-image")
async def generate_scene_image(
    scene_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Générer l'image d'une scène"""
    try:
        scene = db.query(Scene).filter(Scene.id == scene_id).first()
        if not scene:
            raise HTTPException(status_code=404, detail="Scène non trouvée")
        
        episode = db.query(Episode).filter(Episode.id == scene.episode_id).first()
        series = db.query(Series).filter(Series.id == episode.series_id).first()
        
        # Générer en arrière-plan
        background_tasks.add_task(
            generate_scene_image_task,
            scene_id,
            scene.description,
            series.style,
            scene.characters_present or [],
            scene.location or "",
            scene.mood or "neutral"
        )
        
        return {
            "success": True,
            "message": "Génération de l'image en cours..."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{series_id}/view")
async def increment_views(series_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de vues"""
    try:
        series = db.query(Series).filter(Series.id == series_id).first()
        if series:
            series.views_count += 1
            db.commit()
        
        return {"success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{series_id}/like")
async def increment_likes(series_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de likes"""
    try:
        series = db.query(Series).filter(Series.id == series_id).first()
        if series:
            series.likes_count += 1
            db.commit()
        
        return {"success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_series = db.query(Series).count()
        total_episodes = db.query(Episode).count()
        total_scenes = db.query(Scene).count()
        total_views = db.query(Series).with_entities(
            db.func.sum(Series.views_count)
        ).scalar() or 0
        
        return {
            "success": True,
            "stats": {
                "total_series": total_series,
                "total_episodes": total_episodes,
                "total_scenes": total_scenes,
                "total_views": total_views
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tâches en arrière-plan
async def generate_series_concept_task(series_id: int, title: str, description: str,
                                      genre: str, target_audience: str, num_episodes: int):
    """Tâche de génération du concept de série"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        series = db.query(Series).filter(Series.id == series_id).first()
        if not series:
            return
        
        # Générer le concept
        result = await series_service.generate_series_concept(
            title, description, genre, target_audience, num_episodes
        )
        
        if result["success"]:
            concept = result["concept"]
            
            # Mettre à jour la série
            series.synopsis = concept.get("synopsis")
            series.characters = concept.get("characters")
            series.storyline = json.dumps(concept.get("storyline"))
            series.generation_progress = 50
            
            # Générer la cover
            cover_result = await series_service.generate_cover_image(
                title, concept.get("synopsis", ""), genre, series.style
            )
            
            if cover_result["success"]:
                series.cover_image_url = cover_result["image_url"]
            
            # Créer les épisodes
            for ep_data in concept.get("episodes", []):
                episode = Episode(
                    series_id=series_id,
                    episode_number=ep_data["number"],
                    title=ep_data["title"],
                    description=ep_data["summary"],
                    duration=series.episode_duration,
                    characters_featured=concept.get("characters", [])
                )
                db.add(episode)
            
            series.status = "completed"
            series.generation_progress = 100
            db.commit()
        else:
            series.status = "error"
            db.commit()
            
    except Exception as e:
        print(f"Erreur génération série: {e}")
        series.status = "error"
        db.commit()
    finally:
        db.close()


async def generate_episode_script_task(episode_id: int, series_title: str,
                                       episode_number: int, episode_title: str,
                                       episode_summary: str, characters: List[Dict],
                                       duration: int):
    """Tâche de génération du script d'épisode"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        episode = db.query(Episode).filter(Episode.id == episode_id).first()
        if not episode:
            return
        
        # Générer le script
        result = await series_service.generate_episode_script(
            series_title, episode_number, episode_title,
            episode_summary, characters, duration
        )
        
        if result["success"]:
            script_data = result["script"]
            
            episode.script = script_data.get("script")
            episode.generation_progress = 50
            
            # Créer les scènes
            for scene_data in script_data.get("scenes", []):
                scene = Scene(
                    episode_id=episode_id,
                    scene_number=scene_data["number"],
                    title=scene_data.get("title"),
                    description=scene_data["description"],
                    dialogue=scene_data.get("dialogue"),
                    action=scene_data.get("action"),
                    location=scene_data.get("location"),
                    time_of_day=scene_data.get("time_of_day"),
                    mood=scene_data.get("mood"),
                    characters_present=scene_data.get("characters")
                )
                db.add(scene)
            
            episode.status = "completed"
            episode.generation_progress = 100
            db.commit()
        else:
            episode.status = "error"
            db.commit()
            
    except Exception as e:
        print(f"Erreur génération épisode: {e}")
        episode.status = "error"
        db.commit()
    finally:
        db.close()


async def generate_scene_image_task(scene_id: int, description: str, style: str,
                                    characters: List[str], location: str, mood: str):
    """Tâche de génération d'image de scène"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        scene = db.query(Scene).filter(Scene.id == scene_id).first()
        if not scene:
            return
        
        # Générer l'image
        result = await series_service.generate_scene_image(
            description, style, characters, location, mood
        )
        
        if result["success"]:
            scene.image_url = result["image_url"]
            scene.image_prompt = result["prompt"]
            scene.status = "completed"
            db.commit()
        else:
            scene.status = "error"
            db.commit()
            
    except Exception as e:
        print(f"Erreur génération image: {e}")
        scene.status = "error"
        db.commit()
    finally:
        db.close()
