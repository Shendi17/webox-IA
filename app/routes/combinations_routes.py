"""
Routes pour la page Combinaisons IA et l'exécution de workflows
Date : 12 Novembre 2025
"""

from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from app.middleware.auth import get_current_user_from_cookie, require_auth
from app.database import get_db
from app.models.generation_db import WorkflowDB, WorkflowExecutionDB
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ==================== MODÈLES PYDANTIC ====================

class WorkflowStep(BaseModel):
    """Une étape d'un workflow"""
    step_number: int
    ai_provider: str  # gpt4, claude, dalle, etc.
    prompt: str
    use_previous_output: bool = False
    parameters: Optional[Dict[str, Any]] = {}


class WorkflowCreate(BaseModel):
    """Création d'un nouveau workflow"""
    name: str
    description: Optional[str] = None
    steps: List[WorkflowStep]
    is_template: bool = False


class WorkflowExecute(BaseModel):
    """Exécution d'un workflow"""
    workflow_id: Optional[int] = None
    steps: Optional[List[WorkflowStep]] = None
    initial_input: Optional[str] = None


# ==================== TEMPLATES PRÉDÉFINIS ====================

WORKFLOW_TEMPLATES = {
    "content-creation": {
        "name": "Création de Contenu",
        "description": "Génère un article avec image et narration audio",
        "steps": [
            {
                "step_number": 1,
                "ai_provider": "gpt4",
                "prompt": "Rédige un article de blog de 500 mots sur {topic}",
                "use_previous_output": False,
                "parameters": {"model": "gpt-4-turbo", "temperature": 0.7}
            },
            {
                "step_number": 2,
                "ai_provider": "dalle",
                "prompt": "Crée une image d'illustration pour cet article : {step1_output}",
                "use_previous_output": True,
                "parameters": {"size": "1024x1024", "quality": "standard"}
            },
            {
                "step_number": 3,
                "ai_provider": "elevenlabs",
                "prompt": "Génère une narration audio de l'article : {step1_output}",
                "use_previous_output": True,
                "parameters": {"voice": "alloy", "language": "fr"}
            }
        ]
    },
    "video-production": {
        "name": "Production Vidéo",
        "description": "Script + storyboard + vidéo",
        "steps": [
            {
                "step_number": 1,
                "ai_provider": "claude",
                "prompt": "Écris un script vidéo de 2 minutes sur {topic}",
                "use_previous_output": False,
                "parameters": {"model": "claude-3-sonnet", "temperature": 0.8}
            },
            {
                "step_number": 2,
                "ai_provider": "midjourney",
                "prompt": "Crée un storyboard visuel pour ce script : {step1_output}",
                "use_previous_output": True,
                "parameters": {"style": "cinematic"}
            },
            {
                "step_number": 3,
                "ai_provider": "runway",
                "prompt": "Génère une vidéo basée sur ce storyboard : {step2_output}",
                "use_previous_output": True,
                "parameters": {"duration": 10, "resolution": "1080p"}
            }
        ]
    },
    "marketing-campaign": {
        "name": "Campagne Marketing",
        "description": "Texte publicitaire + visuels + voix-off",
        "steps": [
            {
                "step_number": 1,
                "ai_provider": "gpt4",
                "prompt": "Crée un texte publicitaire accrocheur pour {product}",
                "use_previous_output": False,
                "parameters": {"model": "gpt-4-turbo", "temperature": 0.9}
            },
            {
                "step_number": 2,
                "ai_provider": "dalle",
                "prompt": "Crée une image publicitaire pour : {step1_output}",
                "use_previous_output": True,
                "parameters": {"size": "1792x1024", "quality": "hd"}
            },
            {
                "step_number": 3,
                "ai_provider": "elevenlabs",
                "prompt": "Génère une voix-off professionnelle : {step1_output}",
                "use_previous_output": True,
                "parameters": {"voice": "nova", "language": "fr"}
            }
        ]
    },
    "educational-content": {
        "name": "Contenu Éducatif",
        "description": "Cours structuré + illustrations + narration",
        "steps": [
            {
                "step_number": 1,
                "ai_provider": "claude",
                "prompt": "Structure un cours complet sur {topic} avec introduction, 3 chapitres et conclusion",
                "use_previous_output": False,
                "parameters": {"model": "claude-3-opus", "temperature": 0.6}
            },
            {
                "step_number": 2,
                "ai_provider": "midjourney",
                "prompt": "Crée des illustrations pédagogiques pour ce cours : {step1_output}",
                "use_previous_output": True,
                "parameters": {"style": "educational"}
            },
            {
                "step_number": 3,
                "ai_provider": "openai-tts",
                "prompt": "Génère une narration audio du cours : {step1_output}",
                "use_previous_output": True,
                "parameters": {"voice": "fable", "language": "fr"}
            }
        ]
    },
    "social-media-pack": {
        "name": "Pack Réseaux Sociaux",
        "description": "Posts + visuels + hashtags",
        "steps": [
            {
                "step_number": 1,
                "ai_provider": "gpt4",
                "prompt": "Crée 5 posts pour réseaux sociaux sur {topic} avec hashtags",
                "use_previous_output": False,
                "parameters": {"model": "gpt-4-turbo", "temperature": 0.8}
            },
            {
                "step_number": 2,
                "ai_provider": "dalle",
                "prompt": "Crée 5 visuels accrocheurs pour ces posts : {step1_output}",
                "use_previous_output": True,
                "parameters": {"size": "1024x1024", "quality": "standard"}
            }
        ]
    }
}


# ==================== ROUTES ====================

@router.get("/combinations", response_class=HTMLResponse)
async def combinations_page(request: Request, user=Depends(require_auth)):
    """Page de création de combinaisons IA"""
    return templates.TemplateResponse("dashboard/combinations.html", {
        "request": request,
        "user": user
    })


@router.get("/api/combinations/templates")
async def get_templates(user=Depends(require_auth)):
    """Récupère tous les templates de workflows prédéfinis"""
    return {
        "templates": WORKFLOW_TEMPLATES
    }


@router.post("/api/combinations/workflows")
async def create_workflow(
    workflow: WorkflowCreate,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Crée et sauvegarde un nouveau workflow"""
    try:
        # Créer le workflow en DB
        new_workflow = WorkflowDB(
            user_id=user.get("id"),
            user_email=user.get("email"),
            name=workflow.name,
            description=workflow.description,
            steps=json.dumps([step.dict() for step in workflow.steps]),
            is_template=workflow.is_template,
            execution_count=0
        )
        
        db.add(new_workflow)
        db.commit()
        db.refresh(new_workflow)
        
        return {
            "success": True,
            "workflow_id": new_workflow.id,
            "message": "Workflow créé avec succès"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du workflow: {str(e)}")


@router.get("/api/combinations/workflows")
async def get_user_workflows(
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Récupère tous les workflows de l'utilisateur"""
    try:
        workflows = db.query(WorkflowDB).filter(
            WorkflowDB.user_id == user.get("id")
        ).order_by(WorkflowDB.created_at.desc()).all()
        
        return {
            "workflows": [
                {
                    "id": w.id,
                    "name": w.name,
                    "description": w.description,
                    "steps": json.loads(w.steps) if w.steps else [],
                    "execution_count": w.execution_count,
                    "is_template": w.is_template,
                    "created_at": w.created_at.isoformat() if w.created_at else None
                }
                for w in workflows
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des workflows: {str(e)}")


@router.get("/api/combinations/workflows/{workflow_id}")
async def get_workflow(
    workflow_id: int,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Récupère un workflow spécifique"""
    workflow = db.query(WorkflowDB).filter(
        WorkflowDB.id == workflow_id,
        WorkflowDB.user_id == user.get("id")
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow non trouvé")
    
    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "steps": json.loads(workflow.steps) if workflow.steps else [],
        "execution_count": workflow.execution_count,
        "is_template": workflow.is_template,
        "created_at": workflow.created_at.isoformat() if workflow.created_at else None
    }


@router.delete("/api/combinations/workflows/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Supprime un workflow"""
    workflow = db.query(WorkflowDB).filter(
        WorkflowDB.id == workflow_id,
        WorkflowDB.user_id == user.get("id")
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow non trouvé")
    
    db.delete(workflow)
    db.commit()
    
    return {"success": True, "message": "Workflow supprimé"}


@router.post("/api/combinations/execute")
async def execute_workflow(
    execution: WorkflowExecute,
    background_tasks: BackgroundTasks,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Exécute un workflow de manière asynchrone"""
    try:
        # Récupérer les steps du workflow
        steps = []
        workflow_id = execution.workflow_id
        
        if workflow_id:
            # Charger depuis la DB
            workflow = db.query(WorkflowDB).filter(
                WorkflowDB.id == workflow_id
            ).first()
            
            if not workflow:
                raise HTTPException(status_code=404, detail="Workflow non trouvé")
            
            steps = json.loads(workflow.steps) if workflow.steps else []
            
            # Incrémenter le compteur d'exécutions
            workflow.execution_count += 1
            db.commit()
            
        elif execution.steps:
            # Utiliser les steps fournis directement
            steps = [step.dict() for step in execution.steps]
        else:
            raise HTTPException(status_code=400, detail="Aucun workflow ou steps fourni")
        
        # Créer une exécution en DB
        new_execution = WorkflowExecutionDB(
            workflow_id=workflow_id,
            user_id=user.get("id"),
            user_email=user.get("email"),
            status="pending",
            steps_data=json.dumps(steps),
            initial_input=execution.initial_input
        )
        
        db.add(new_execution)
        db.commit()
        db.refresh(new_execution)
        
        # Lancer l'exécution en arrière-plan
        background_tasks.add_task(
            execute_workflow_background,
            execution_id=new_execution.id,
            steps=steps,
            initial_input=execution.initial_input,
            user=user
        )
        
        return {
            "success": True,
            "execution_id": new_execution.id,
            "status": "pending",
            "message": "Workflow lancé en arrière-plan"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution: {str(e)}")


@router.get("/api/combinations/executions/{execution_id}")
async def get_execution_status(
    execution_id: int,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Récupère le statut d'une exécution"""
    execution = db.query(WorkflowExecutionDB).filter(
        WorkflowExecutionDB.id == execution_id,
        WorkflowExecutionDB.user_id == user.get("id")
    ).first()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Exécution non trouvée")
    
    return {
        "id": execution.id,
        "workflow_id": execution.workflow_id,
        "status": execution.status,
        "current_step": execution.current_step,
        "total_steps": execution.total_steps,
        "results": json.loads(execution.results) if execution.results else {},
        "error_message": execution.error_message,
        "started_at": execution.started_at.isoformat() if execution.started_at else None,
        "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
        "total_cost": float(execution.total_cost) if execution.total_cost else 0.0
    }


@router.get("/api/combinations/executions")
async def get_user_executions(
    limit: int = 20,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Récupère l'historique des exécutions de l'utilisateur"""
    executions = db.query(WorkflowExecutionDB).filter(
        WorkflowExecutionDB.user_id == user.get("id")
    ).order_by(WorkflowExecutionDB.created_at.desc()).limit(limit).all()
    
    return {
        "executions": [
            {
                "id": e.id,
                "workflow_id": e.workflow_id,
                "status": e.status,
                "current_step": e.current_step,
                "total_steps": e.total_steps,
                "total_cost": float(e.total_cost) if e.total_cost else 0.0,
                "created_at": e.created_at.isoformat() if e.created_at else None,
                "completed_at": e.completed_at.isoformat() if e.completed_at else None
            }
            for e in executions
        ]
    }


# ==================== FONCTIONS D'EXÉCUTION ====================

async def execute_workflow_background(
    execution_id: int,
    steps: List[Dict],
    initial_input: Optional[str],
    user: Dict
):
    """
    Exécute un workflow en arrière-plan
    Cette fonction sera appelée de manière asynchrone
    """
    from app.database import SessionLocal
    from app.ai_manager import ai_manager
    
    db = SessionLocal()
    
    try:
        # Récupérer l'exécution
        execution = db.query(WorkflowExecutionDB).filter(
            WorkflowExecutionDB.id == execution_id
        ).first()
        
        if not execution:
            return
        
        # Mettre à jour le statut
        execution.status = "running"
        execution.started_at = datetime.utcnow()
        execution.total_steps = len(steps)
        execution.current_step = 0
        db.commit()
        
        # Résultats de chaque étape
        step_results = {}
        previous_output = initial_input or ""
        total_cost = 0.0
        
        # Exécuter chaque étape séquentiellement
        for i, step in enumerate(steps, 1):
            execution.current_step = i
            db.commit()
            
            # Remplacer les variables dans le prompt
            prompt = step["prompt"]
            if step.get("use_previous_output") and previous_output:
                prompt = prompt.replace("{step" + str(i-1) + "_output}", previous_output)
                prompt = prompt.replace("{previous_output}", previous_output)
            
            if initial_input:
                prompt = prompt.replace("{topic}", initial_input)
                prompt = prompt.replace("{product}", initial_input)
                prompt = prompt.replace("{input}", initial_input)
            
            # Exécuter l'étape selon le provider
            ai_provider = step["ai_provider"]
            parameters = step.get("parameters", {})
            
            try:
                result = await execute_ai_step(
                    provider=ai_provider,
                    prompt=prompt,
                    parameters=parameters,
                    user=user
                )
                
                step_results[f"step_{i}"] = result
                previous_output = result.get("output", "")
                total_cost += result.get("cost", 0.0)
                
            except Exception as step_error:
                # Erreur dans une étape
                execution.status = "failed"
                execution.error_message = f"Erreur à l'étape {i}: {str(step_error)}"
                execution.completed_at = datetime.utcnow()
                db.commit()
                return
        
        # Workflow terminé avec succès
        execution.status = "completed"
        execution.results = json.dumps(step_results)
        execution.total_cost = total_cost
        execution.completed_at = datetime.utcnow()
        db.commit()
        
    except Exception as e:
        # Erreur globale
        if execution:
            execution.status = "failed"
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            db.commit()
    
    finally:
        db.close()


async def execute_ai_step(
    provider: str,
    prompt: str,
    parameters: Dict,
    user: Dict
) -> Dict:
    """
    Exécute une étape avec un provider IA spécifique
    """
    from app.ai_manager import ai_manager
    
    result = {
        "output": "",
        "cost": 0.0,
        "metadata": {}
    }
    
    # Providers de texte
    if provider in ["gpt4", "claude", "gemini"]:
        provider_map = {
            "gpt4": "GPT-4",
            "claude": "Claude",
            "gemini": "Gemini"
        }
        
        response = await ai_manager.generate_response(
            provider=provider_map.get(provider, "GPT-4"),
            model=parameters.get("model", "gpt-4-turbo"),
            messages=[{"role": "user", "content": prompt}],
            temperature=parameters.get("temperature", 0.7),
            user_email=user.get("email")
        )
        
        result["output"] = response
        result["cost"] = 0.03  # Coût estimé
        
    # Providers d'images
    elif provider in ["dalle", "midjourney", "stable-diffusion"]:
        # Pour l'instant, retourner un placeholder
        result["output"] = f"[Image générée avec {provider}]"
        result["cost"] = 0.04
        result["metadata"] = {"image_url": "/placeholder.png"}
        
    # Providers audio
    elif provider in ["elevenlabs", "openai-tts", "suno", "udio"]:
        # Pour l'instant, retourner un placeholder
        result["output"] = f"[Audio généré avec {provider}]"
        result["cost"] = 0.10
        result["metadata"] = {"audio_url": "/placeholder.mp3"}
        
    # Providers vidéo
    elif provider in ["runway", "pika", "luma"]:
        # Pour l'instant, retourner un placeholder
        result["output"] = f"[Vidéo générée avec {provider}]"
        result["cost"] = 0.50
        result["metadata"] = {"video_url": "/placeholder.mp4"}
    
    else:
        raise ValueError(f"Provider inconnu: {provider}")
    
    return result
