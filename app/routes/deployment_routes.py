"""
Routes API pour le déploiement
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.web_project_db import WebProject
from app.services.deployment_service import DeploymentFactory, NetlifyDeployment, VercelDeployment

router = APIRouter(prefix="/api/deployment", tags=["Deployment"])


# ==================== SCHEMAS ====================

class DeployRequest(BaseModel):
    project_id: int
    provider: str  # netlify, vercel
    site_id: Optional[str] = None
    project_name: Optional[str] = None
    framework: Optional[str] = None


class GetSitesRequest(BaseModel):
    provider: str


class GetDeploymentsRequest(BaseModel):
    provider: str
    site_id: str


# ==================== ROUTES ====================

@router.post("/deploy")
async def deploy_project(data: DeployRequest, db: Session = Depends(get_db)):
    """Déployer un projet"""
    try:
        # Obtenir le projet
        project = db.query(WebProject).filter(WebProject.id == data.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        # Configuration
        config = {
            "name": data.project_name or project.name,
            "framework": data.framework or project.project_type
        }
        
        # Déployer
        if data.provider == "netlify":
            service = NetlifyDeployment()
            result = service.deploy(project.local_path, data.site_id, config)
        elif data.provider == "vercel":
            service = VercelDeployment()
            result = service.deploy(project.local_path, data.site_id, config)
        else:
            return {"success": False, "error": f"Provider '{data.provider}' non supporté"}
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sites")
async def get_sites(data: GetSitesRequest):
    """Obtenir la liste des sites"""
    try:
        if data.provider == "netlify":
            service = NetlifyDeployment()
            return service.get_sites()
        elif data.provider == "vercel":
            service = VercelDeployment()
            return service.get_projects()
        else:
            return {"success": False, "error": f"Provider '{data.provider}' non supporté"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deployments")
async def get_deployments(data: GetDeploymentsRequest):
    """Obtenir l'historique des déploiements"""
    try:
        if data.provider == "netlify":
            service = NetlifyDeployment()
            return service.get_deploys(data.site_id)
        elif data.provider == "vercel":
            service = VercelDeployment()
            return service.get_deployments(data.site_id)
        else:
            return {"success": False, "error": f"Provider '{data.provider}' non supporté"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
