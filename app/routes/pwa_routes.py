from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json
from app.database import get_db
from app.models.pwa import PWAProject
from app.services.pwa_service import PWAService

router = APIRouter(prefix="/api/pwa", tags=["pwa"])
pwa_service = PWAService()

# Modèles Pydantic
class PWACreate(BaseModel):
    name: str
    description: str
    app_name: str
    short_name: Optional[str] = None
    template: str
    theme_color: str = "#667eea"
    background_color: str = "#ffffff"
    offline_mode: bool = True
    push_notifications: bool = False
    cache_strategy: str = "network-first"

# Routes métadonnées
@router.get("/templates")
async def get_templates():
    """Obtenir la liste des templates PWA"""
    try:
        templates = pwa_service.get_templates()
        return {"success": True, "templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/themes")
async def get_themes():
    """Obtenir les thèmes de couleurs"""
    try:
        themes = pwa_service.get_color_themes()
        return {"success": True, "themes": themes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache-strategies")
async def get_cache_strategies():
    """Obtenir les stratégies de cache"""
    try:
        strategies = pwa_service.get_cache_strategies()
        return {"success": True, "strategies": strategies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routes CRUD
@router.post("/create")
async def create_pwa(
    pwa_data: PWACreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle PWA"""
    try:
        # Créer le projet
        pwa = PWAProject(
            user_id=1,  # TODO: Récupérer l'utilisateur authentifié
            name=pwa_data.name,
            description=pwa_data.description,
            app_name=pwa_data.app_name,
            short_name=pwa_data.short_name or pwa_data.app_name[:12],
            template=pwa_data.template,
            theme_color=pwa_data.theme_color,
            background_color=pwa_data.background_color,
            offline_mode=pwa_data.offline_mode,
            push_notifications=pwa_data.push_notifications,
            cache_strategy=pwa_data.cache_strategy,
            status="generating"
        )
        
        db.add(pwa)
        db.commit()
        db.refresh(pwa)
        
        # Générer en arrière-plan
        background_tasks.add_task(
            generate_pwa_task,
            pwa.id,
            pwa_data.template,
            pwa_data.app_name,
            pwa_data.description,
            pwa_data.theme_color,
            pwa_data.background_color,
            pwa_data.cache_strategy
        )
        
        return {
            "success": True,
            "pwa": pwa.to_dict(),
            "message": "PWA en cours de génération..."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_pwas(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lister les PWAs"""
    try:
        query = db.query(PWAProject)
        
        if status:
            query = query.filter(PWAProject.status == status)
        
        total = query.count()
        pwas = query.order_by(PWAProject.created_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "pwas": [p.to_dict() for p in pwas],
            "total": total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pwa_id}")
async def get_pwa(pwa_id: int, db: Session = Depends(get_db)):
    """Obtenir une PWA spécifique"""
    try:
        pwa = db.query(PWAProject).filter(PWAProject.id == pwa_id).first()
        
        if not pwa:
            raise HTTPException(status_code=404, detail="PWA non trouvée")
        
        return {
            "success": True,
            "pwa": pwa.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pwa_id}")
async def delete_pwa(pwa_id: int, db: Session = Depends(get_db)):
    """Supprimer une PWA"""
    try:
        pwa = db.query(PWAProject).filter(PWAProject.id == pwa_id).first()
        
        if pwa:
            db.delete(pwa)
            db.commit()
        
        return {"success": True, "message": "PWA supprimée"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{pwa_id}/view")
async def increment_views(pwa_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur de vues"""
    try:
        pwa = db.query(PWAProject).filter(PWAProject.id == pwa_id).first()
        if pwa:
            pwa.views_count += 1
            db.commit()
        
        return {"success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{pwa_id}/install")
async def increment_installs(pwa_id: int, db: Session = Depends(get_db)):
    """Incrémenter le compteur d'installations"""
    try:
        pwa = db.query(PWAProject).filter(PWAProject.id == pwa_id).first()
        if pwa:
            pwa.installs_count += 1
            db.commit()
        
        return {"success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_pwas = db.query(PWAProject).count()
        total_views = db.query(PWAProject).with_entities(
            db.func.sum(PWAProject.views_count)
        ).scalar() or 0
        total_installs = db.query(PWAProject).with_entities(
            db.func.sum(PWAProject.installs_count)
        ).scalar() or 0
        deployed_pwas = db.query(PWAProject).filter(
            PWAProject.status == "deployed"
        ).count()
        
        return {
            "success": True,
            "stats": {
                "total_pwas": total_pwas,
                "total_views": total_views,
                "total_installs": total_installs,
                "deployed_pwas": deployed_pwas
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pwa_id}/download")
async def download_pwa(pwa_id: int, db: Session = Depends(get_db)):
    """Télécharger les fichiers de la PWA"""
    try:
        pwa = db.query(PWAProject).filter(PWAProject.id == pwa_id).first()
        
        if not pwa:
            raise HTTPException(status_code=404, detail="PWA non trouvée")
        
        # Préparer les fichiers
        files = {
            "manifest.json": json.dumps(pwa.manifest_json, indent=2),
            "sw.js": pwa.service_worker_js,
            "index.html": pwa.content.get("html") if pwa.content else ""
        }
        
        return {
            "success": True,
            "files": files
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tâche en arrière-plan
async def generate_pwa_task(pwa_id: int, template: str, app_name: str,
                           description: str, theme_color: str,
                           background_color: str, cache_strategy: str):
    """Tâche de génération de PWA"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        pwa = db.query(PWAProject).filter(PWAProject.id == pwa_id).first()
        if not pwa:
            return
        
        # Générer le contenu
        pwa.generation_progress = 25
        db.commit()
        
        content_result = await pwa_service.generate_content(template, app_name, description)
        
        if content_result["success"]:
            content = content_result["content"]
            
            # Générer l'icône
            pwa.generation_progress = 50
            db.commit()
            
            icon_result = await pwa_service.generate_icon(app_name, template)
            
            if icon_result["success"]:
                pwa.icon_url = icon_result["icon_url"]
                pwa.logo_url = icon_result["icon_url"]
            
            # Générer le manifest
            pwa.generation_progress = 75
            db.commit()
            
            manifest = pwa_service.generate_manifest(
                app_name,
                pwa.short_name,
                description,
                theme_color,
                background_color,
                pwa.icon_url or ""
            )
            
            # Générer le service worker
            service_worker = pwa_service.generate_service_worker(cache_strategy)
            
            # Générer le HTML
            html = pwa_service.generate_html_template(template, content, theme_color)
            
            # Sauvegarder
            pwa.content = {
                "html": html,
                "pages": content.get("pages", []),
                "sections": content.get("sections", [])
            }
            pwa.manifest_json = manifest
            pwa.service_worker_js = service_worker
            pwa.meta_title = content.get("seo", {}).get("title")
            pwa.meta_description = content.get("seo", {}).get("description")
            pwa.keywords = content.get("seo", {}).get("keywords", [])
            
            pwa.status = "ready"
            pwa.generation_progress = 100
            db.commit()
        else:
            pwa.status = "error"
            db.commit()
            
    except Exception as e:
        print(f"Erreur génération PWA: {e}")
        pwa.status = "error"
        db.commit()
    finally:
        db.close()
