"""
Routes API pour les assistants vocaux
Date : 2 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.voice_assistant_db import VoiceAssistantDB, VoiceCallDB
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/api/voice", tags=["Voice"])


# ========== MODÈLES PYDANTIC ==========

class AssistantCreate(BaseModel):
    """Modèle pour créer un assistant vocal"""
    client_name: str
    client_email: Optional[str] = None
    twilio_phone_number: str
    ai_model: str = "gpt-4"
    ai_context: str
    ai_personality: str = "professional"
    voice_provider: str = "elevenlabs"
    voice_language: str = "fr-FR"


class AssistantUpdate(BaseModel):
    """Modèle pour mettre à jour un assistant"""
    client_name: Optional[str] = None
    ai_context: Optional[str] = None
    ai_personality: Optional[str] = None
    voice_provider: Optional[str] = None
    is_active: Optional[bool] = None


# ========== ROUTES ASSISTANTS ==========

@router.get("/assistants")
async def get_assistants(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des assistants vocaux
    """
    query = db.query(VoiceAssistantDB)
    
    # Si pas admin, ne voir que ses propres assistants
    if not current_user.is_admin:
        query = query.filter(VoiceAssistantDB.owner_id == current_user.id)
    
    assistants = query.order_by(VoiceAssistantDB.created_at.desc()).all()
    
    return {
        "success": True,
        "assistants": [assistant.to_dict() for assistant in assistants]
    }


@router.get("/assistants/{assistant_id}")
async def get_assistant(
    assistant_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère un assistant vocal par son ID
    """
    assistant = db.query(VoiceAssistantDB).filter(
        VoiceAssistantDB.id == assistant_id
    ).first()
    
    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant non trouvé"
        )
    
    # Vérifier les permissions
    if not current_user.is_admin and assistant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    return {
        "success": True,
        "assistant": assistant.to_dict()
    }


@router.post("/assistants")
async def create_assistant(
    data: AssistantCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel assistant vocal
    """
    try:
        # Vérifier que le numéro n'existe pas déjà
        existing = db.query(VoiceAssistantDB).filter(
            VoiceAssistantDB.twilio_phone_number == data.twilio_phone_number
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce numéro Twilio est déjà utilisé"
            )
        
        # Créer l'assistant
        assistant = VoiceAssistantDB(
            client_name=data.client_name,
            client_email=data.client_email,
            twilio_phone_number=data.twilio_phone_number,
            ai_model=data.ai_model,
            ai_context=data.ai_context,
            ai_personality=data.ai_personality,
            voice_provider=data.voice_provider,
            voice_language=data.voice_language,
            owner_id=current_user.id,
            owner_email=current_user.email
        )
        
        db.add(assistant)
        db.commit()
        db.refresh(assistant)
        
        return {
            "success": True,
            "message": "Assistant vocal créé avec succès",
            "assistant": assistant.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.put("/assistants/{assistant_id}")
async def update_assistant(
    assistant_id: int,
    data: AssistantUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour un assistant vocal
    """
    assistant = db.query(VoiceAssistantDB).filter(
        VoiceAssistantDB.id == assistant_id
    ).first()
    
    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant non trouvé"
        )
    
    # Vérifier les permissions
    if not current_user.is_admin and assistant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    try:
        # Mettre à jour les champs
        if data.client_name:
            assistant.client_name = data.client_name
        if data.ai_context:
            assistant.ai_context = data.ai_context
        if data.ai_personality:
            assistant.ai_personality = data.ai_personality
        if data.voice_provider:
            assistant.voice_provider = data.voice_provider
        if data.is_active is not None:
            assistant.is_active = data.is_active
        
        assistant.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(assistant)
        
        return {
            "success": True,
            "message": "Assistant mis à jour avec succès",
            "assistant": assistant.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )


@router.delete("/assistants/{assistant_id}")
async def delete_assistant(
    assistant_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime un assistant vocal
    """
    assistant = db.query(VoiceAssistantDB).filter(
        VoiceAssistantDB.id == assistant_id
    ).first()
    
    if not assistant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assistant non trouvé"
        )
    
    # Vérifier les permissions
    if not current_user.is_admin and assistant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès non autorisé"
        )
    
    try:
        db.delete(assistant)
        db.commit()
        
        return {
            "success": True,
            "message": "Assistant supprimé avec succès"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )


# ========== ROUTES APPELS ==========

@router.get("/calls")
async def get_calls(
    assistant_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère l'historique des appels
    """
    query = db.query(VoiceCallDB)
    
    # Filtrer par assistant si spécifié
    if assistant_id:
        query = query.filter(VoiceCallDB.assistant_id == assistant_id)
    
    # Si pas admin, ne voir que les appels de ses assistants
    if not current_user.is_admin:
        assistant_ids = db.query(VoiceAssistantDB.id).filter(
            VoiceAssistantDB.owner_id == current_user.id
        ).all()
        assistant_ids = [aid[0] for aid in assistant_ids]
        query = query.filter(VoiceCallDB.assistant_id.in_(assistant_ids))
    
    # Trier par date
    query = query.order_by(VoiceCallDB.started_at.desc())
    
    # Pagination
    total = query.count()
    calls = query.offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "calls": [call.to_dict() for call in calls]
    }


@router.get("/stats")
async def get_stats(
    assistant_id: Optional[int] = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques des appels
    """
    query = db.query(VoiceCallDB)
    
    # Filtrer par assistant si spécifié
    if assistant_id:
        query = query.filter(VoiceCallDB.assistant_id == assistant_id)
    
    # Si pas admin, ne voir que les stats de ses assistants
    if not current_user.is_admin:
        assistant_ids = db.query(VoiceAssistantDB.id).filter(
            VoiceAssistantDB.owner_id == current_user.id
        ).all()
        assistant_ids = [aid[0] for aid in assistant_ids]
        query = query.filter(VoiceCallDB.assistant_id.in_(assistant_ids))
    
    # Calculer les stats
    total_calls = query.count()
    total_duration = query.with_entities(func.sum(VoiceCallDB.duration)).scalar() or 0
    avg_duration = query.with_entities(func.avg(VoiceCallDB.duration)).scalar() or 0
    avg_satisfaction = query.filter(VoiceCallDB.satisfaction_score.isnot(None)).with_entities(
        func.avg(VoiceCallDB.satisfaction_score)
    ).scalar() or 0
    
    # Appels par statut
    calls_by_status = db.query(
        VoiceCallDB.status,
        func.count(VoiceCallDB.id).label('count')
    ).filter(
        VoiceCallDB.id.in_(query.with_entities(VoiceCallDB.id))
    ).group_by(VoiceCallDB.status).all()
    
    return {
        "success": True,
        "stats": {
            "total_calls": total_calls,
            "total_duration": int(total_duration),
            "average_duration": round(avg_duration, 2),
            "average_satisfaction": round(avg_satisfaction, 2),
            "calls_by_status": [
                {"status": status, "count": count}
                for status, count in calls_by_status
            ]
        }
    }


# ========== WEBHOOKS TWILIO ==========

@router.post("/webhook/incoming")
async def twilio_incoming_call(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook Twilio pour les appels entrants
    """
    # TODO: Implémenter la logique Twilio
    # 1. Récupérer les données de l'appel
    # 2. Trouver l'assistant correspondant au numéro
    # 3. Créer une entrée dans voice_calls
    # 4. Retourner TwiML pour démarrer la conversation
    
    return Response(
        content="""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say language="fr-FR">Bonjour, je suis votre assistant vocal. Comment puis-je vous aider ?</Say>
            <Gather input="speech" action="/api/voice/webhook/process" language="fr-FR" />
        </Response>""",
        media_type="application/xml"
    )


@router.post("/webhook/process")
async def twilio_process_speech(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook Twilio pour traiter la parole
    """
    # TODO: Implémenter la logique de traitement
    # 1. Récupérer la transcription de Twilio
    # 2. Envoyer à l'IA (GPT-4, Claude, etc.)
    # 3. Convertir la réponse en audio (TTS)
    # 4. Retourner TwiML avec la réponse
    
    return Response(
        content="""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say language="fr-FR">Je traite votre demande...</Say>
        </Response>""",
        media_type="application/xml"
    )
