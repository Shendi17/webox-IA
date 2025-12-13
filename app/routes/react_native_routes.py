from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json
from app.database import get_db
from app.models.react_native import ReactNativeProject
from app.services.react_native_service import ReactNativeService

router = APIRouter(prefix="/api/react-native", tags=["react-native"])
rn_service = ReactNativeService()

# Modèles Pydantic
class ReactNativeCreate(BaseModel):
    name: str
    description: str
    app_name: str
    package_name: str
    template: str
    platform: str = "both"
    navigation_type: str = "stack"
    build_android: bool = False
    build_ios: bool = False

# Routes métadonnées
@router.get("/templates")
async def get_templates():
    """Obtenir la liste des templates React Native"""
    try:
        templates = rn_service.get_templates()
        return {"success": True, "templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/navigation-types")
async def get_navigation_types():
    """Obtenir les types de navigation"""
    try:
        types = rn_service.get_navigation_types()
        return {"success": True, "navigation_types": types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes CRUD
@router.post("/create")
async def create_project(
    project_data: ReactNativeCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Créer un nouveau projet React Native"""
    try:
        project = ReactNativeProject(
            user_id=1,
            name=project_data.name,
            description=project_data.description,
            app_name=project_data.app_name,
            package_name=project_data.package_name,
            template=project_data.template,
            platform=project_data.platform,
            navigation_type=project_data.navigation_type,
            build_android=project_data.build_android,
            build_ios=project_data.build_ios,
            status="generating"
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        background_tasks.add_task(
            generate_rn_project_task,
            project.id,
            project_data.template,
            project_data.app_name,
            project_data.navigation_type
        )
        
        return {
            "success": True,
            "project": project.to_dict(),
            "message": "Projet en cours de génération..."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_projects(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lister les projets React Native"""
    try:
        total = db.query(ReactNativeProject).count()
        projects = db.query(ReactNativeProject).order_by(
            ReactNativeProject.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "projects": [p.to_dict() for p in projects],
            "total": total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}")
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Obtenir un projet spécifique"""
    try:
        project = db.query(ReactNativeProject).filter(
            ReactNativeProject.id == project_id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        return {
            "success": True,
            "project": project.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Supprimer un projet"""
    try:
        project = db.query(ReactNativeProject).filter(
            ReactNativeProject.id == project_id
        ).first()
        
        if project:
            db.delete(project)
            db.commit()
        
        return {"success": True, "message": "Projet supprimé"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}/download")
async def download_project(project_id: int, db: Session = Depends(get_db)):
    """Télécharger le code du projet"""
    try:
        project = db.query(ReactNativeProject).filter(
            ReactNativeProject.id == project_id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        # Préparer les fichiers
        files = {
            "App.js": project.app_js or "",
            "navigation.js": project.navigation_js or "",
            "package.json": rn_service.generate_package_json(
                project.app_name,
                project.dependencies or {}
            )
        }
        
        # Ajouter les screens
        if project.screens:
            for screen in project.screens:
                files[f"screens/{screen['name']}.js"] = screen.get('code', '')
        
        return {
            "success": True,
            "files": files
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_projects = db.query(ReactNativeProject).count()
        total_downloads = db.query(ReactNativeProject).with_entities(
            db.func.sum(ReactNativeProject.downloads_count)
        ).scalar() or 0
        android_projects = db.query(ReactNativeProject).filter(
            ReactNativeProject.build_android == True
        ).count()
        ios_projects = db.query(ReactNativeProject).filter(
            ReactNativeProject.build_ios == True
        ).count()
        
        return {
            "success": True,
            "stats": {
                "total_projects": total_projects,
                "total_downloads": total_downloads,
                "android_projects": android_projects,
                "ios_projects": ios_projects
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tâche en arrière-plan
async def generate_rn_project_task(project_id: int, template: str,
                                   app_name: str, navigation_type: str):
    """Tâche de génération de projet React Native"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        project = db.query(ReactNativeProject).filter(
            ReactNativeProject.id == project_id
        ).first()
        if not project:
            return
        
        # Générer le code
        project.generation_progress = 25
        db.commit()
        
        code_result = await rn_service.generate_app_code(
            template, app_name, navigation_type
        )
        
        if code_result["success"]:
            code = code_result["code"]
            
            # Générer l'icône
            project.generation_progress = 50
            db.commit()
            
            icon_result = await rn_service.generate_icon(app_name, template)
            
            if icon_result["success"]:
                project.icon_url = icon_result["icon_url"]
                project.splash_screen_url = icon_result["icon_url"]
            
            # Sauvegarder le code
            project.app_js = code.get("app_js")
            project.navigation_js = code.get("navigation_js")
            project.screens = code.get("screens", [])
            project.components = code.get("components", [])
            project.dependencies = code.get("dependencies", {})
            
            project.status = "ready"
            project.generation_progress = 100
            db.commit()
        else:
            project.status = "error"
            db.commit()
            
    except Exception as e:
        print(f"Erreur génération React Native: {e}")
        project.status = "error"
        db.commit()
    finally:
        db.close()
