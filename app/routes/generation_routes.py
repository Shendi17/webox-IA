"""
Routes API pour la Génération Multi-Média
Date : 10 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import os
import httpx
from openai import OpenAI

from app.middleware.auth import get_current_user_from_token
from app.database import get_db
from app.models.generation_db import GeneratedImageDB, GeneratedVideoDB, GeneratedAudioDB
from app.models.user_db import UserDB

router = APIRouter(prefix="/api/generation", tags=["Generation"])


# ============================================
# SCHÉMAS PYDANTIC
# ============================================

class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    model: str = "dall-e-3"  # dall-e-3, dall-e-2, stable-diffusion
    size: str = "1024x1024"
    style: Optional[str] = "natural"  # natural, vivid
    quality: str = "standard"  # standard, hd


class VideoGenerationRequest(BaseModel):
    prompt: str
    model: str = "runway"  # runway, pika, luma
    duration: int = 5
    resolution: str = "1080p"
    fps: int = 24


class AudioGenerationRequest(BaseModel):
    prompt: str
    model: str = "elevenlabs"  # elevenlabs, suno, udio
    audio_type: str = "speech"  # speech, music, sound_effect
    voice_id: Optional[str] = None
    language: str = "fr"
    duration: Optional[int] = None


# ============================================
# GÉNÉRATION D'IMAGES
# ============================================

@router.post("/image")
async def generate_image(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer une image avec l'IA choisie
    
    Modèles supportés :
    - dall-e-3 : DALL-E 3 (OpenAI)
    - dall-e-2 : DALL-E 2 (OpenAI)
    - stable-diffusion : Stable Diffusion (Stability AI)
    """
    try:
        # Créer l'entrée en DB
        db_image = GeneratedImageDB(
            user_id=current_user["id"],
            user_email=current_user.get("email"),
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            model=request.model,
            size=request.size,
            style=request.style,
            quality=request.quality,
            status="generating"
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            _generate_image_task,
            db_image.id,
            request,
            current_user
        )
        
        return {
            "id": db_image.id,
            "status": "generating",
            "message": "Génération d'image lancée",
            "prompt": request.prompt,
            "model": request.model
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création : {str(e)}")


async def _generate_image_task(image_id: int, request: ImageGenerationRequest, user: dict):
    """
    Tâche en arrière-plan pour générer l'image
    """
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        db_image = db.query(GeneratedImageDB).filter(GeneratedImageDB.id == image_id).first()
        
        if request.model.startswith("dall-e"):
            # Utiliser DALL-E (OpenAI)
            image_url, cost = await _generate_with_dalle(request, user)
            
        elif request.model == "stable-diffusion":
            # Utiliser Stable Diffusion (Stability AI)
            image_url, cost = await _generate_with_stable_diffusion(request, user)
            
        else:
            raise ValueError(f"Modèle non supporté : {request.model}")
        
        # Télécharger l'image localement (optionnel)
        local_path = await _download_image(image_url, image_id)
        
        # Mettre à jour en DB
        db_image.image_url = image_url
        db_image.local_path = local_path
        db_image.cost = cost
        db_image.status = "completed"
        db_image.completed_at = datetime.utcnow()
        
        # Extraire les dimensions (si possible)
        if local_path:
            from PIL import Image
            with Image.open(local_path) as img:
                db_image.width, db_image.height = img.size
                db_image.file_size = os.path.getsize(local_path)
        
        db.commit()
        
    except Exception as e:
        db_image.status = "failed"
        db_image.error_message = str(e)
        db.commit()
        
    finally:
        db.close()


async def _generate_with_dalle(request: ImageGenerationRequest, user: dict) -> tuple:
    """
    Générer une image avec DALL-E
    """
    try:
        # Récupérer la clé API OpenAI de l'utilisateur
        api_key = os.getenv("OPENAI_API_KEY")  # TODO: Récupérer depuis le profil utilisateur
        
        if not api_key:
            raise ValueError("Clé API OpenAI non configurée")
        
        client = OpenAI(api_key=api_key)
        
        # Générer l'image
        response = client.images.generate(
            model=request.model,
            prompt=request.prompt,
            size=request.size,
            quality=request.quality,
            style=request.style if request.model == "dall-e-3" else None,
            n=1
        )
        
        image_url = response.data[0].url
        
        # Calculer le coût
        if request.model == "dall-e-3":
            if request.quality == "hd":
                cost = 0.080 if request.size == "1024x1024" else 0.120
            else:
                cost = 0.040 if request.size == "1024x1024" else 0.080
        else:  # dall-e-2
            cost = 0.020 if request.size == "1024x1024" else 0.018
        
        return image_url, cost
        
    except Exception as e:
        raise Exception(f"Erreur DALL-E : {str(e)}")


async def _generate_with_stable_diffusion(request: ImageGenerationRequest, user: dict) -> tuple:
    """
    Générer une image avec Stable Diffusion (Stability AI)
    """
    try:
        api_key = os.getenv("STABILITY_API_KEY")
        
        if not api_key:
            raise ValueError("Clé API Stability AI non configurée")
        
        # TODO: Implémenter l'appel à l'API Stability AI
        # Pour l'instant, retourner une erreur
        raise NotImplementedError("Stable Diffusion pas encore implémenté")
        
    except Exception as e:
        raise Exception(f"Erreur Stable Diffusion : {str(e)}")


async def _download_image(image_url: str, image_id: int) -> str:
    """
    Télécharger l'image localement
    """
    try:
        # Créer le dossier si nécessaire
        output_dir = "generated/images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Télécharger l'image
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            response.raise_for_status()
            
            # Sauvegarder
            file_path = os.path.join(output_dir, f"image_{image_id}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            return file_path
            
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None


@router.get("/image/{image_id}")
async def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer les informations d'une image générée
    """
    image = db.query(GeneratedImageDB).filter(
        GeneratedImageDB.id == image_id,
        GeneratedImageDB.user_id == current_user["id"]
    ).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    return image.to_dict()


@router.get("/images")
async def list_images(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Lister les images générées par l'utilisateur
    """
    images = db.query(GeneratedImageDB).filter(
        GeneratedImageDB.user_id == current_user["id"]
    ).order_by(GeneratedImageDB.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "images": [img.to_dict() for img in images],
        "total": db.query(GeneratedImageDB).filter(
            GeneratedImageDB.user_id == current_user["id"]
        ).count()
    }


# ============================================
# GÉNÉRATION DE VIDÉOS
# ============================================

@router.post("/video")
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer une vidéo avec Runway ML, Pika ou Luma
    """
    try:
        # Créer l'entrée en DB
        db_video = GeneratedVideoDB(
            user_id=current_user["id"],
            user_email=current_user.get("email"),
            prompt=request.prompt,
            model=request.model,
            duration=request.duration,
            resolution=request.resolution,
            fps=request.fps,
            status="generating"
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            _generate_video_task,
            db_video.id,
            request,
            current_user
        )
        
        return {
            "id": db_video.id,
            "status": "generating",
            "message": "Génération de vidéo lancée",
            "prompt": request.prompt,
            "model": request.model,
            "estimated_time": f"{request.duration * 10}s"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")


async def _generate_video_task(video_id: int, request: VideoGenerationRequest, user: dict):
    """
    Tâche en arrière-plan pour générer la vidéo
    """
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        db_video = db.query(GeneratedVideoDB).filter(GeneratedVideoDB.id == video_id).first()
        
        if request.model == "runway":
            video_url, cost = await _generate_with_runway(request, user)
        elif request.model == "pika":
            video_url, cost = await _generate_with_pika(request, user)
        elif request.model == "luma":
            video_url, cost = await _generate_with_luma(request, user)
        else:
            raise ValueError(f"Modèle non supporté : {request.model}")
        
        # Télécharger la vidéo localement
        local_path = await _download_video(video_url, video_id)
        
        # Mettre à jour en DB
        db_video.video_url = video_url
        db_video.local_path = local_path
        db_video.cost = cost
        db_video.status = "completed"
        db_video.completed_at = datetime.utcnow()
        
        if local_path:
            db_video.file_size = os.path.getsize(local_path)
        
        db.commit()
        
    except Exception as e:
        db_video.status = "failed"
        db_video.error_message = str(e)
        db.commit()
        
    finally:
        db.close()


async def _generate_with_runway(request: VideoGenerationRequest, user: dict) -> tuple:
    """
    Générer une vidéo avec Runway ML
    """
    # Simulation pour l'instant
    import asyncio
    await asyncio.sleep(2)  # Simuler le temps de génération
    
    video_url = "https://example.com/video_runway.mp4"
    cost = 0.50 * request.duration  # $0.50 par seconde
    
    return video_url, cost


async def _generate_with_pika(request: VideoGenerationRequest, user: dict) -> tuple:
    """
    Générer une vidéo avec Pika Labs
    """
    import asyncio
    await asyncio.sleep(2)
    
    video_url = "https://example.com/video_pika.mp4"
    cost = 0.30 * request.duration
    
    return video_url, cost


async def _generate_with_luma(request: VideoGenerationRequest, user: dict) -> tuple:
    """
    Générer une vidéo avec Luma AI
    """
    import asyncio
    await asyncio.sleep(2)
    
    video_url = "https://example.com/video_luma.mp4"
    cost = 0.40 * request.duration
    
    return video_url, cost


async def _download_video(video_url: str, video_id: int) -> str:
    """
    Télécharger la vidéo localement
    """
    try:
        output_dir = "generated/videos"
        os.makedirs(output_dir, exist_ok=True)
        
        # Pour la simulation, créer un fichier vide
        file_path = os.path.join(output_dir, f"video_{video_id}.mp4")
        with open(file_path, "wb") as f:
            f.write(b"")
        
        return file_path
        
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None


@router.get("/video/{video_id}")
async def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer les informations d'une vidéo générée
    """
    video = db.query(GeneratedVideoDB).filter(
        GeneratedVideoDB.id == video_id,
        GeneratedVideoDB.user_id == current_user["id"]
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    
    return video.to_dict()


@router.get("/videos")
async def list_videos(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Lister les vidéos générées par l'utilisateur
    """
    videos = db.query(GeneratedVideoDB).filter(
        GeneratedVideoDB.user_id == current_user["id"]
    ).order_by(GeneratedVideoDB.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "videos": [video.to_dict() for video in videos],
        "total": db.query(GeneratedVideoDB).filter(
            GeneratedVideoDB.user_id == current_user["id"]
        ).count()
    }


# ============================================
# GÉNÉRATION D'AUDIO
# ============================================

@router.post("/audio")
async def generate_audio(
    request: AudioGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer de l'audio avec ElevenLabs, Suno ou Udio
    """
    try:
        # Créer l'entrée en DB
        db_audio = GeneratedAudioDB(
            user_id=current_user["id"],
            user_email=current_user.get("email"),
            prompt=request.prompt,
            model=request.model,
            audio_type=request.audio_type,
            voice_id=request.voice_id,
            language=request.language,
            duration=request.duration,
            status="generating"
        )
        db.add(db_audio)
        db.commit()
        db.refresh(db_audio)
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            _generate_audio_task,
            db_audio.id,
            request,
            current_user
        )
        
        return {
            "id": db_audio.id,
            "status": "generating",
            "message": "Génération d'audio lancée",
            "prompt": request.prompt,
            "model": request.model
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")


async def _generate_audio_task(audio_id: int, request: AudioGenerationRequest, user: dict):
    """
    Tâche en arrière-plan pour générer l'audio
    """
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        db_audio = db.query(GeneratedAudioDB).filter(GeneratedAudioDB.id == audio_id).first()
        
        if request.model == "elevenlabs":
            audio_url, cost, duration = await _generate_with_elevenlabs(request, user)
        elif request.model == "suno":
            audio_url, cost, duration = await _generate_with_suno(request, user)
        elif request.model == "udio":
            audio_url, cost, duration = await _generate_with_udio(request, user)
        else:
            raise ValueError(f"Modèle non supporté : {request.model}")
        
        # Télécharger l'audio localement
        local_path = await _download_audio(audio_url, audio_id)
        
        # Mettre à jour en DB
        db_audio.audio_url = audio_url
        db_audio.local_path = local_path
        db_audio.cost = cost
        db_audio.duration = duration
        db_audio.status = "completed"
        db_audio.completed_at = datetime.utcnow()
        
        if local_path:
            db_audio.file_size = os.path.getsize(local_path)
        
        db.commit()
        
    except Exception as e:
        db_audio.status = "failed"
        db_audio.error_message = str(e)
        db.commit()
        
    finally:
        db.close()


async def _generate_with_elevenlabs(request: AudioGenerationRequest, user: dict) -> tuple:
    """
    Générer de l'audio avec ElevenLabs (Speech)
    """
    import asyncio
    await asyncio.sleep(1)
    
    audio_url = "https://example.com/audio_elevenlabs.mp3"
    duration = len(request.prompt.split()) * 0.5  # ~0.5s par mot
    cost = 0.10 * (duration / 60)  # $0.10 par minute
    
    return audio_url, cost, int(duration)


async def _generate_with_suno(request: AudioGenerationRequest, user: dict) -> tuple:
    """
    Générer de la musique avec Suno AI
    """
    import asyncio
    await asyncio.sleep(2)
    
    audio_url = "https://example.com/audio_suno.mp3"
    duration = request.duration or 30
    cost = 0.20 * (duration / 60)
    
    return audio_url, cost, duration


async def _generate_with_udio(request: AudioGenerationRequest, user: dict) -> tuple:
    """
    Générer de la musique avec Udio
    """
    import asyncio
    await asyncio.sleep(2)
    
    audio_url = "https://example.com/audio_udio.mp3"
    duration = request.duration or 30
    cost = 0.15 * (duration / 60)
    
    return audio_url, cost, duration


async def _download_audio(audio_url: str, audio_id: int) -> str:
    """
    Télécharger l'audio localement
    """
    try:
        output_dir = "generated/audio"
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, f"audio_{audio_id}.mp3")
        with open(file_path, "wb") as f:
            f.write(b"")
        
        return file_path
        
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None


@router.get("/audio/{audio_id}")
async def get_audio(
    audio_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer les informations d'un audio généré
    """
    audio = db.query(GeneratedAudioDB).filter(
        GeneratedAudioDB.id == audio_id,
        GeneratedAudioDB.user_id == current_user["id"]
    ).first()
    
    if not audio:
        raise HTTPException(status_code=404, detail="Audio non trouvé")
    
    return audio.to_dict()


@router.get("/audios")
async def list_audios(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Lister les audios générés par l'utilisateur
    """
    audios = db.query(GeneratedAudioDB).filter(
        GeneratedAudioDB.user_id == current_user["id"]
    ).order_by(GeneratedAudioDB.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "audios": [audio.to_dict() for audio in audios],
        "total": db.query(GeneratedAudioDB).filter(
            GeneratedAudioDB.user_id == current_user["id"]
        ).count()
    }


# ============================================
# GÉNÉRATION D'EBOOKS
# ============================================

class EbookGenerationRequest(BaseModel):
    title: str
    topic: str
    num_chapters: int = 5
    language: str = "fr"
    style: str = "informative"  # informative, narrative, academic
    target_audience: str = "general"


@router.post("/ebook")
async def generate_ebook(
    request: EbookGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer un eBook complet avec GPT-4
    """
    try:
        from app.models.generation_db import GeneratedEbookDB
        
        # Créer l'entrée en DB
        db_ebook = GeneratedEbookDB(
            user_id=current_user["id"],
            user_email=current_user.get("email"),
            title=request.title,
            topic=request.topic,
            num_chapters=request.num_chapters,
            language=request.language,
            style=request.style,
            target_audience=request.target_audience,
            status="generating"
        )
        db.add(db_ebook)
        db.commit()
        db.refresh(db_ebook)
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            _generate_ebook_task,
            db_ebook.id,
            request,
            current_user
        )
        
        return {
            "id": db_ebook.id,
            "status": "generating",
            "message": "Génération d'eBook lancée",
            "title": request.title,
            "estimated_time": f"{request.num_chapters * 30}s"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")


async def _generate_ebook_task(ebook_id: int, request: EbookGenerationRequest, user: dict):
    """
    Tâche en arrière-plan pour générer l'eBook
    """
    from app.database import SessionLocal
    from app.models.generation_db import GeneratedEbookDB
    
    db = SessionLocal()
    
    try:
        db_ebook = db.query(GeneratedEbookDB).filter(GeneratedEbookDB.id == ebook_id).first()
        
        # Générer le contenu avec GPT-4
        content, cost = await _generate_ebook_content(request, user)
        
        # Générer le PDF
        pdf_path = await _generate_pdf(content, request.title, ebook_id)
        
        # Mettre à jour en DB
        db_ebook.content = content
        db_ebook.pdf_path = pdf_path
        db_ebook.cost = cost
        db_ebook.status = "completed"
        db_ebook.completed_at = datetime.utcnow()
        
        if pdf_path:
            db_ebook.file_size = os.path.getsize(pdf_path)
            db_ebook.page_count = content.count("\n\n") // 10  # Estimation
        
        db.commit()
        
    except Exception as e:
        db_ebook.status = "failed"
        db_ebook.error_message = str(e)
        db.commit()
        
    finally:
        db.close()


async def _generate_ebook_content(request: EbookGenerationRequest, user: dict) -> tuple:
    """
    Générer le contenu de l'eBook avec GPT-4
    """
    import asyncio
    await asyncio.sleep(2)
    
    # Simulation
    content = f"# {request.title}\n\n"
    content += f"## Introduction\n\nCe livre traite de {request.topic}.\n\n"
    
    for i in range(1, request.num_chapters + 1):
        content += f"## Chapitre {i}\n\nContenu du chapitre {i}...\n\n"
    
    content += "## Conclusion\n\nMerci d'avoir lu ce livre.\n"
    
    cost = 0.10 * request.num_chapters
    
    return content, cost


async def _generate_pdf(content: str, title: str, ebook_id: int) -> str:
    """
    Générer un PDF à partir du contenu Markdown
    """
    try:
        output_dir = "generated/ebooks"
        os.makedirs(output_dir, exist_ok=True)
        
        pdf_path = os.path.join(output_dir, f"ebook_{ebook_id}.pdf")
        
        # Simulation - créer un fichier vide
        with open(pdf_path, "wb") as f:
            f.write(b"")
        
        return pdf_path
        
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        return None


# ============================================
# GÉNÉRATION DE VIDÉOS SHORTS
# ============================================

class ShortVideoRequest(BaseModel):
    topic: str
    duration: int = 60  # secondes
    style: str = "educational"  # educational, entertaining, promotional
    voice: str = "alloy"
    music: bool = True


@router.post("/short")
async def generate_short_video(
    request: ShortVideoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer une vidéo short complète (script + voix + vidéo + musique)
    """
    try:
        from app.models.generation_db import GeneratedShortDB
        
        # Créer l'entrée en DB
        db_short = GeneratedShortDB(
            user_id=current_user["id"],
            user_email=current_user.get("email"),
            topic=request.topic,
            duration=request.duration,
            style=request.style,
            voice=request.voice,
            music=request.music,
            status="generating"
        )
        db.add(db_short)
        db.commit()
        db.refresh(db_short)
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            _generate_short_task,
            db_short.id,
            request,
            current_user
        )
        
        return {
            "id": db_short.id,
            "status": "generating",
            "message": "Génération de vidéo short lancée",
            "topic": request.topic,
            "estimated_time": "120s"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")


async def _generate_short_task(short_id: int, request: ShortVideoRequest, user: dict):
    """
    Pipeline complet de génération de vidéo short
    """
    from app.database import SessionLocal
    from app.models.generation_db import GeneratedShortDB
    
    db = SessionLocal()
    
    try:
        db_short = db.query(GeneratedShortDB).filter(GeneratedShortDB.id == short_id).first()
        
        # Étape 1: Générer le script
        script = await _generate_script(request)
        db_short.script = script
        db.commit()
        
        # Étape 2: Générer la voix-off
        audio_url = await _generate_voiceover(script, request.voice)
        db_short.audio_url = audio_url
        db.commit()
        
        # Étape 3: Générer les visuels
        video_url = await _generate_visuals(script, request.duration)
        db_short.video_url = video_url
        db.commit()
        
        # Étape 4: Ajouter la musique (optionnel)
        if request.music:
            music_url = await _add_background_music(video_url)
        
        # Finaliser
        db_short.status = "completed"
        db_short.completed_at = datetime.utcnow()
        db_short.cost = 0.80  # Coût total estimé
        db.commit()
        
    except Exception as e:
        db_short.status = "failed"
        db_short.error_message = str(e)
        db.commit()
        
    finally:
        db.close()


async def _generate_script(request: ShortVideoRequest) -> str:
    import asyncio
    await asyncio.sleep(1)
    return f"Script pour vidéo short sur {request.topic}"


async def _generate_voiceover(script: str, voice: str) -> str:
    import asyncio
    await asyncio.sleep(1)
    return "https://example.com/voiceover.mp3"


async def _generate_visuals(script: str, duration: int) -> str:
    import asyncio
    await asyncio.sleep(2)
    return "https://example.com/short_video.mp4"


async def _add_background_music(video_url: str) -> str:
    import asyncio
    await asyncio.sleep(1)
    return "https://example.com/music.mp3"


# ============================================
# GÉNÉRATION DE PUBLICITÉS VIDÉO
# ============================================

class AdGenerationRequest(BaseModel):
    product_name: str
    product_description: str
    product_image_url: str
    ad_type: str = "product-showcase"  # product-showcase, lifestyle, testimonial, promo, comparison
    duration: int = 30  # 15, 30, 60 secondes
    style: str = "modern"  # modern, elegant, dynamic, minimal, luxury
    voice: str = "professional-female"
    cta: Optional[str] = None
    options: Optional[Dict[str, bool]] = {
        "music": True,
        "effects": True,
        "text_overlay": True,
        "logo": False,
        "captions": False
    }


@router.post("/ad")
async def generate_ad(
    request: AdGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer une publicité vidéo professionnelle à partir d'une photo produit
    """
    try:
        from app.models.generation_db import GeneratedAdDB
        
        # Créer l'entrée en DB
        db_ad = GeneratedAdDB(
            user_id=current_user["id"],
            user_email=current_user.get("email"),
            product_name=request.product_name,
            product_description=request.product_description,
            product_image_url=request.product_image_url,
            ad_type=request.ad_type,
            duration=request.duration,
            style=request.style,
            voice=request.voice,
            cta=request.cta,
            options=request.options,
            status="generating"
        )
        db.add(db_ad)
        db.commit()
        db.refresh(db_ad)
        
        # Lancer la génération en arrière-plan
        background_tasks.add_task(
            _generate_ad_task,
            db_ad.id,
            request,
            current_user
        )
        
        return {
            "id": db_ad.id,
            "status": "generating",
            "message": "Génération de publicité lancée",
            "product_name": request.product_name,
            "estimated_time": f"{request.duration * 3}s"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")


async def _generate_ad_task(ad_id: int, request: AdGenerationRequest, user: dict):
    """
    Pipeline complet de génération de publicité
    """
    from app.database import SessionLocal
    from app.models.generation_db import GeneratedAdDB
    
    db = SessionLocal()
    
    try:
        db_ad = db.query(GeneratedAdDB).filter(GeneratedAdDB.id == ad_id).first()
        
        # Étape 1: Générer le script publicitaire
        script = await _generate_ad_script(request)
        db_ad.script = script
        db.commit()
        
        # Étape 2: Générer la voix-off
        if request.voice != "none":
            audio_url = await _generate_ad_voiceover(script, request.voice)
            db_ad.audio_url = audio_url
            db.commit()
        
        # Étape 3: Créer la vidéo avec le produit
        video_url = await _generate_ad_video(request)
        db_ad.video_url = video_url
        db.commit()
        
        # Étape 4: Ajouter les effets et musique
        if request.options.get("music"):
            music_url = await _add_ad_music(video_url, request.style)
        
        if request.options.get("effects"):
            video_url = await _add_ad_effects(video_url, request.style)
        
        # Finaliser
        db_ad.status = "completed"
        db_ad.completed_at = datetime.utcnow()
        db_ad.cost = _calculate_ad_cost(request)
        db.commit()
        
    except Exception as e:
        db_ad.status = "failed"
        db_ad.error_message = str(e)
        db.commit()
        
    finally:
        db.close()


async def _generate_ad_script(request: AdGenerationRequest) -> str:
    """
    Générer un script publicitaire avec GPT-4
    """
    import asyncio
    await asyncio.sleep(1)
    
    # Simulation - en production, utiliser GPT-4
    scripts = {
        "product-showcase": f"Découvrez {request.product_name}. {request.product_description}. {request.cta or 'Commandez maintenant !'}",
        "lifestyle": f"Imaginez votre vie avec {request.product_name}. {request.product_description}. {request.cta or 'Transformez votre quotidien !'}",
        "testimonial": f"Des milliers de clients adorent {request.product_name}. {request.product_description}. {request.cta or 'Rejoignez-les !'}",
        "promo": f"Offre exclusive sur {request.product_name} ! {request.product_description}. {request.cta or 'Profitez-en maintenant !'}",
        "comparison": f"Avant / Après avec {request.product_name}. {request.product_description}. {request.cta or 'Essayez la différence !'}"
    }
    
    return scripts.get(request.ad_type, scripts["product-showcase"])


async def _generate_ad_voiceover(script: str, voice: str) -> str:
    """
    Générer la voix-off avec ElevenLabs
    """
    import asyncio
    await asyncio.sleep(1)
    return "https://example.com/ad_voiceover.mp3"


async def _generate_ad_video(request: AdGenerationRequest) -> str:
    """
    Créer la vidéo publicitaire avec Runway ML
    """
    import asyncio
    await asyncio.sleep(2)
    return "https://example.com/ad_video.mp4"


async def _add_ad_music(video_url: str, style: str) -> str:
    """
    Ajouter une musique de fond appropriée
    """
    import asyncio
    await asyncio.sleep(1)
    return "https://example.com/ad_music.mp3"


async def _add_ad_effects(video_url: str, style: str) -> str:
    """
    Ajouter des effets visuels et transitions
    """
    import asyncio
    await asyncio.sleep(1)
    return video_url


def _calculate_ad_cost(request: AdGenerationRequest) -> float:
    """
    Calculer le coût de la publicité
    """
    base_cost = 2.00  # Coût de base
    
    # Coût par durée
    duration_cost = request.duration * 0.10
    
    # Coût des options
    options_cost = 0
    if request.options.get("music"):
        options_cost += 0.50
    if request.options.get("effects"):
        options_cost += 0.75
    if request.options.get("text_overlay"):
        options_cost += 0.25
    if request.options.get("captions"):
        options_cost += 0.50
    
    return base_cost + duration_cost + options_cost


@router.get("/ad/{ad_id}")
async def get_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer les informations d'une publicité générée
    """
    from app.models.generation_db import GeneratedAdDB
    
    ad = db.query(GeneratedAdDB).filter(
        GeneratedAdDB.id == ad_id,
        GeneratedAdDB.user_id == current_user["id"]
    ).first()
    
    if not ad:
        raise HTTPException(status_code=404, detail="Publicité non trouvée")
    
    return ad.to_dict()


@router.get("/ads")
async def list_ads(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Lister les publicités générées par l'utilisateur
    """
    from app.models.generation_db import GeneratedAdDB
    
    ads = db.query(GeneratedAdDB).filter(
        GeneratedAdDB.user_id == current_user["id"]
    ).order_by(GeneratedAdDB.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "ads": [ad.to_dict() for ad in ads],
        "total": db.query(GeneratedAdDB).filter(
            GeneratedAdDB.user_id == current_user["id"]
        ).count()
    }


# ============================================
# GALERIE DES GÉNÉRATIONS
# ============================================

@router.get("/gallery")
async def get_gallery(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user_from_token)
):
    """
    Récupérer toutes les générations pour la galerie
    """
    # Récupérer les images
    images = db.query(GeneratedImageDB).filter(
        GeneratedImageDB.user_id == current_user.id
    ).order_by(GeneratedImageDB.created_at.desc()).limit(50).all()
    
    # Récupérer les vidéos
    videos = db.query(GeneratedVideoDB).filter(
        GeneratedVideoDB.user_id == current_user.id
    ).order_by(GeneratedVideoDB.created_at.desc()).limit(50).all()
    
    # Récupérer les audios
    audios = db.query(GeneratedAudioDB).filter(
        GeneratedAudioDB.user_id == current_user.id
    ).order_by(GeneratedAudioDB.created_at.desc()).limit(50).all()
    
    # Combiner toutes les générations
    items = []
    
    for img in images:
        items.append({
            "id": img.id,
            "type": "image",
            "url": img.image_url or "https://via.placeholder.com/400x400?text=Image",
            "prompt": img.prompt,
            "model": img.model,
            "created_at": img.created_at.isoformat() if img.created_at else None
        })
    
    for vid in videos:
        items.append({
            "id": vid.id,
            "type": "video",
            "url": vid.video_url or "https://via.placeholder.com/400x400?text=Video",
            "prompt": vid.prompt,
            "model": vid.model,
            "created_at": vid.created_at.isoformat() if vid.created_at else None
        })
    
    for aud in audios:
        items.append({
            "id": aud.id,
            "type": "audio",
            "url": "https://via.placeholder.com/400x400?text=Audio",
            "prompt": aud.text,
            "model": aud.model,
            "created_at": aud.created_at.isoformat() if aud.created_at else None
        })
    
    # Trier par date
    items.sort(key=lambda x: x["created_at"] or "", reverse=True)
    
    # Statistiques
    total_cost = sum([
        img.cost or 0 for img in images
    ]) + sum([
        vid.cost or 0 for vid in videos
    ]) + sum([
        aud.cost or 0 for aud in audios
    ])
    
    # Modèle le plus utilisé
    models = [img.model for img in images] + [vid.model for vid in videos] + [aud.model for aud in audios]
    most_used = max(set(models), key=models.count) if models else "-"
    
    return {
        "items": items,
        "stats": {
            "total": len(items),
            "cost": f"${total_cost:.2f}",
            "most_used_model": most_used
        }
    }


@router.delete("/{item_id}")
async def delete_generation(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user_from_token)
):
    """
    Supprimer une génération
    """
    # Essayer de supprimer dans chaque table
    image = db.query(GeneratedImageDB).filter(
        GeneratedImageDB.id == item_id,
        GeneratedImageDB.user_id == current_user.id
    ).first()
    
    if image:
        db.delete(image)
        db.commit()
        return {"success": True, "message": "Image supprimée"}
    
    video = db.query(GeneratedVideoDB).filter(
        GeneratedVideoDB.id == item_id,
        GeneratedVideoDB.user_id == current_user.id
    ).first()
    
    if video:
        db.delete(video)
        db.commit()
        return {"success": True, "message": "Vidéo supprimée"}
    
    audio = db.query(GeneratedAudioDB).filter(
        GeneratedAudioDB.id == item_id,
        GeneratedAudioDB.user_id == current_user.id
    ).first()
    
    if audio:
        db.delete(audio)
        db.commit()
        return {"success": True, "message": "Audio supprimé"}
    
    raise HTTPException(status_code=404, detail="Génération non trouvée")


@router.get("/export")
async def export_gallery(
    format: str = "zip",
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user_from_token)
):
    """
    Exporter toutes les générations
    """
    # TODO: Implémenter l'export réel en ZIP/JSON/CSV
    # Pour l'instant, retourner un message
    
    if format == "json":
        # Récupérer toutes les générations
        gallery_data = await get_gallery(db, current_user)
        
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content=gallery_data,
            headers={
                "Content-Disposition": "attachment; filename=webox_generations.json"
            }
        )
    
    elif format == "csv":
        # TODO: Générer un CSV
        raise HTTPException(status_code=501, detail="Export CSV non encore implémenté")
    
    elif format == "zip":
        # TODO: Créer un ZIP avec toutes les images/vidéos
        raise HTTPException(status_code=501, detail="Export ZIP non encore implémenté")
    
    else:
        raise HTTPException(status_code=400, detail="Format non supporté")
