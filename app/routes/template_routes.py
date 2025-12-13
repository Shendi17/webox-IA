"""
Routes API pour les templates
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.services.template_service import TemplateService
import os

router = APIRouter(prefix="/api/templates", tags=["Templates"])


# ==================== SCHEMAS ====================

class CreateFromTemplateRequest(BaseModel):
    template_id: str
    project_name: str
    customization: Optional[dict] = None


# ==================== ROUTES ====================

@router.get("/list")
async def list_templates():
    """Lister tous les templates disponibles"""
    try:
        service = TemplateService("")
        return service.list_templates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{template_id}")
async def get_template_details(template_id: str):
    """Obtenir les détails d'un template"""
    try:
        service = TemplateService("")
        return service.get_template_details(template_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
async def create_from_template(data: CreateFromTemplateRequest, db: Session = Depends(get_db)):
    """Créer un projet à partir d'un template"""
    try:
        # Créer le chemin du projet
        base_path = os.path.join(os.getcwd(), "projects")
        project_path = os.path.join(base_path, data.project_name)
        
        # Créer le projet
        service = TemplateService(base_path)
        result = service.create_project_from_template(
            data.template_id,
            data.project_name,
            project_path,
            data.customization
        )
        
        if result["success"]:
            # Créer l'entrée dans la base de données
            from app.models.web_project_db import WebProject
            
            project = WebProject(
                name=data.project_name,
                description=f"Projet créé depuis le template {data.template_id}",
                project_type="static",
                local_path=project_path
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            
            result["project_id"] = project.id
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
