"""
Routes API pour Voice Automation - Piloter WeBox par voix
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.services.voice_automation_service import VoiceAutomationService
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter(prefix="/api/voice-automation", tags=["Voice Automation"])


# ==================== SCHEMAS ====================

class VoiceCommandText(BaseModel):
    """Commande vocale en texte"""
    command: str
    user_context: Optional[dict] = None


class ExecuteAction(BaseModel):
    """Exécuter une action"""
    action: str
    parameters: dict


# ==================== ROUTES ====================

@router.post("/process-audio")
async def process_voice_audio(
    audio: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Traiter un fichier audio de commande vocale
    
    Args:
        audio: Fichier audio (WAV, MP3, etc.)
    
    Returns:
        Résultat de la commande + audio de réponse
    """
    try:
        # Lire l'audio
        audio_bytes = await audio.read()
        
        # Traiter la commande
        service = VoiceAutomationService()
        result = service.process_voice_command(
            audio_bytes,
            user_context={"user_id": current_user.id}
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        # Retourner le résultat
        return {
            "success": True,
            "transcript": result["transcript"],
            "action": result["action"],
            "parameters": result.get("parameters", {}),
            "response": result["response"],
            "has_audio": result.get("audio_response") is not None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-text")
async def process_voice_text(
    data: VoiceCommandText,
    current_user: UserDB = Depends(get_current_user)
):
    """
    Traiter une commande vocale en texte (pour tests)
    
    Args:
        data: Commande en texte
    
    Returns:
        Résultat de la commande
    """
    try:
        service = VoiceAutomationService()
        
        # Analyser la commande
        analysis = service.analyze_command(
            data.command,
            user_context=data.user_context or {"user_id": current_user.id}
        )
        
        if not analysis.get("success"):
            raise HTTPException(status_code=400, detail="Commande non comprise")
        
        return {
            "success": True,
            "action": analysis["action"],
            "parameters": analysis.get("parameters", {}),
            "response": analysis["response"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_action(
    data: ExecuteAction,
    current_user: UserDB = Depends(get_current_user)
):
    """
    Exécuter une action déterminée
    
    Args:
        data: Action et paramètres
    
    Returns:
        Résultat de l'exécution
    """
    try:
        service = VoiceAutomationService()
        
        # Exécuter l'action
        result = service.execute_action(
            data.action,
            data.parameters,
            user_id=current_user.id
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audio-response/{command_id}")
async def get_audio_response(command_id: str):
    """
    Récupérer l'audio de réponse d'une commande
    
    Args:
        command_id: ID de la commande
    
    Returns:
        Audio MP3
    """
    # À implémenter: stocker et récupérer les audios
    raise HTTPException(status_code=501, detail="Non implémenté")
