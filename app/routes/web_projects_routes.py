"""
Routes API pour le Studio Web IA
Gestion complète de projets web
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import shutil
import git
from pathlib import Path

from app.database import get_db
from app.models.web_project_db import (
    WebProject, 
    ProjectFile, 
    Deployment, 
    ProjectCommit,
    ProjectAIAction,
    ProjectTemplate
)
from app.middleware.auth import get_current_user_from_cookie
from pydantic import BaseModel


router = APIRouter(prefix="/api/projects", tags=["Web Projects"])

import json


# ==================== SCHEMAS ====================

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_type: str  # static, react, vue, nextjs, django, fastapi
    template_id: Optional[int] = None
    git_repo_url: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    prod_url: Optional[str] = None
    staging_url: Optional[str] = None


class FileCreate(BaseModel):
    path: str
    content: str
    commit_message: Optional[str] = None


class FileUpdate(BaseModel):
    content: str
    commit_message: Optional[str] = None


class CommitCreate(BaseModel):
    message: str
    files: List[str]  # chemins des fichiers à committer


class DeploymentCreate(BaseModel):
    environment: str  # dev, staging, prod
    branch: Optional[str] = "main"


class AIActionCreate(BaseModel):
    prompt: str
    context: Optional[dict] = None


# ==================== HELPERS ====================

def generate_slug(name: str, db: Session) -> str:
    """Génère un slug unique à partir du nom"""
    import re
    base_slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    slug = base_slug
    counter = 1
    
    while db.query(WebProject).filter(WebProject.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug


def get_project_path(project: WebProject) -> Path:
    """Retourne le chemin du projet"""
    if project.local_path:
        return Path(project.local_path)
    
    # Sinon, créer dans le dossier projects
    base_path = Path("projects") / str(project.owner_id)
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path / project.slug


def scan_project_files(project_path: Path, project_id: int, db: Session):
    """Scanne tous les fichiers d'un projet et les ajoute en BDD"""
    files_to_add = []
    
    for file_path in project_path.rglob('*'):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(project_path))
            
            # Ignorer certains dossiers
            if any(part in relative_path for part in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']):
                continue
            
            # Lire le contenu si fichier texte
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    is_binary = False
            except:
                content = None
                is_binary = True
            
            file_obj = ProjectFile(
                project_id=project_id,
                path=relative_path,
                name=file_path.name,
                extension=file_path.suffix,
                directory=str(file_path.parent.relative_to(project_path)),
                content=content,
                size=file_path.stat().st_size,
                lines=len(content.splitlines()) if content else 0,
                is_binary=is_binary
            )
            files_to_add.append(file_obj)
    
    db.bulk_save_objects(files_to_add)
    db.commit()


# ==================== ROUTES ====================

@router.get("")
async def list_projects(
    db: Session = Depends(get_db)
):
    """Liste tous les projets (temporairement sans authentification pour les tests)"""
    try:
        projects = db.query(WebProject).filter(
            WebProject.status != "deleted"
        ).order_by(WebProject.updated_at.desc()).all()
    except Exception as e:
        print(f"Erreur lors de la récupération des projets: {e}")
        return {"projects": []}
    
    return {
        "projects": [
            {
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "description": p.description,
                "project_type": p.project_type,
                "framework": p.framework,
                "status": p.status,
                "prod_url": p.prod_url,
                "total_files": p.total_files,
                "total_lines": p.total_lines,
                "last_deploy_at": p.last_deploy_at.isoformat() if p.last_deploy_at else None,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat()
            }
            for p in projects
        ]
    }


@router.post("")
async def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    """Crée un nouveau projet"""
    
    # Vérifier l'authentification
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    # Générer le slug
    slug = generate_slug(data.name, db)
    
    # Créer le projet en BDD
    project = WebProject(
        name=data.name,
        slug=slug,
        description=data.description,
        project_type=data.project_type,
        owner_id=current_user["id"],
        storage_type="local"
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Créer le dossier du projet
    project_path = get_project_path(project)
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Mettre à jour le chemin local
    project.local_path = str(project_path)
    db.commit()
    
    # Si template, cloner ou copier
    if data.template_id:
        template = db.query(ProjectTemplate).filter(ProjectTemplate.id == data.template_id).first()
        if template and template.git_repo_url:
            # Cloner le template
            try:
                git.Repo.clone_from(template.git_repo_url, project_path)
                # Scanner les fichiers
                scan_project_files(project_path, project.id, db)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur lors du clonage: {str(e)}")
    
    # Si repo Git fourni
    elif data.git_repo_url:
        try:
            git.Repo.clone_from(data.git_repo_url, project_path)
            project.git_repo_url = data.git_repo_url
            project.storage_type = "git"
            db.commit()
            
            # Scanner les fichiers
            scan_project_files(project_path, project.id, db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors du clonage: {str(e)}")
    
    else:
        # Créer structure de base selon le type
        if data.project_type == "static":
            # Créer index.html basique
            (project_path / "index.html").write_text("""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Bienvenue sur {}</h1>
    <p>Votre projet est prêt !</p>
    <script src="script.js"></script>
</body>
</html>""".format(data.name, data.name))
            
            (project_path / "styles.css").write_text("""* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    padding: 2rem;
}

h1 {
    color: #667eea;
}""")
            
            (project_path / "script.js").write_text("""console.log('Projet démarré !');""")
            
            # Scanner les fichiers
            scan_project_files(project_path, project.id, db)
    
    # Mettre à jour les stats
    project.total_files = db.query(ProjectFile).filter(ProjectFile.project_id == project.id).count()
    project.total_lines = db.query(ProjectFile).filter(ProjectFile.project_id == project.id).with_entities(
        db.func.sum(ProjectFile.lines)
    ).scalar() or 0
    db.commit()
    
    return {
        "success": True,
        "message": "Projet créé avec succès",
        "project": {
            "id": project.id,
            "name": project.name,
            "slug": project.slug,
            "path": str(project_path)
        }
    }


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    """Récupère les détails d'un projet"""
    project = db.query(WebProject).filter(
        WebProject.id == project_id,
        WebProject.owner_id == current_user["id"]
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "slug": project.slug,
            "description": project.description,
            "project_type": project.project_type,
            "framework": project.framework,
            "status": project.status,
            "local_path": project.local_path,
            "git_repo_url": project.git_repo_url,
            "git_branch": project.git_branch,
            "prod_url": project.prod_url,
            "staging_url": project.staging_url,
            "total_files": project.total_files,
            "total_lines": project.total_lines,
            "total_size": project.total_size,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat()
        },
        "stats": {
            "commits_count": db.query(ProjectCommit).filter(ProjectCommit.project_id == project_id).count(),
            "deployments_count": db.query(Deployment).filter(Deployment.project_id == project_id).count(),
            "ai_actions_count": db.query(ProjectAIAction).filter(ProjectAIAction.project_id == project_id).count()
        }
    }


@router.put("/{project_id}")
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    """Met à jour un projet"""
    project = db.query(WebProject).filter(
        WebProject.id == project_id,
        WebProject.owner_id == current_user["id"]
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    if data.name:
        project.name = data.name
    if data.description is not None:
        project.description = data.description
    if data.status:
        project.status = data.status
    if data.prod_url:
        project.prod_url = data.prod_url
    if data.staging_url:
        project.staging_url = data.staging_url
    
    project.updated_at = datetime.utcnow()
    db.commit()
    
    return {"success": True, "message": "Projet mis à jour"}


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    """Supprime un projet (soft delete)"""
    project = db.query(WebProject).filter(
        WebProject.id == project_id,
        WebProject.owner_id == current_user["id"]
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    project.status = "deleted"
    project.archived_at = datetime.utcnow()
    db.commit()
    
    return {"success": True, "message": "Projet supprimé"}


# ==================== FICHIERS ====================

@router.get("/{project_id}/files_old")
async def list_files_old(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_cookie)
):
    """Liste tous les fichiers d'un projet (ancienne version)"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    project = db.query(WebProject).filter(
        WebProject.id == project_id,
        WebProject.owner_id == current_user["id"]
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    files = db.query(ProjectFile).filter(ProjectFile.project_id == project_id).all()
    
    return {
        "files": [
            {
                "id": f.id,
                "path": f.path,
                "name": f.name,
                "extension": f.extension,
                "size": f.size,
                "lines": f.lines,
                "is_binary": f.is_binary,
                "git_status": f.git_status,
                "updated_at": f.updated_at.isoformat()
            }
            for f in files
        ]
    }


# ==================== TEMPLATES ====================

@router.get("/templates/list")
async def list_templates(db: Session = Depends(get_db)):
    """Liste tous les templates disponibles"""
    templates = db.query(ProjectTemplate).filter(
        ProjectTemplate.published_at.isnot(None)
    ).order_by(ProjectTemplate.usage_count.desc()).all()
    
    return {
        "templates": [
            {
                "id": t.id,
                "name": t.name,
                "slug": t.slug,
                "description": t.description,
                "cover_image": t.cover_image,
                "category": t.category,
                "project_type": t.project_type,
                "framework": t.framework,
                "features": t.features,
                "is_premium": t.is_premium,
                "price": t.price,
                "usage_count": t.usage_count,
                "rating": t.rating / 100 if t.rating else 0
            }
            for t in templates
        ]
    }


# ==================== ROUTES ÉDITEUR ====================

@router.get("/{project_id}/files")
async def get_project_files(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Récupère l'arborescence des fichiers d'un projet"""
    try:
        project = db.query(WebProject).filter(WebProject.id == project_id).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        if not project.local_path:
            return {"files": []}
        
        project_path = Path(project.local_path)
        
        if not project_path.exists():
            return {"files": []}
        
        def build_tree(path: Path, base_path: Path):
            """Construit l'arborescence récursivement"""
            items = []
            
            try:
                for item in sorted(path.iterdir()):
                    # Ignorer les fichiers cachés et node_modules
                    if item.name.startswith('.') or item.name == 'node_modules':
                        continue
                    
                    relative_path = str(item.relative_to(base_path))
                    
                    if item.is_dir():
                        items.append({
                            "name": item.name,
                            "path": relative_path,
                            "is_directory": True,
                            "children": build_tree(item, base_path)
                        })
                    else:
                        items.append({
                            "name": item.name,
                            "path": relative_path,
                            "is_directory": False,
                            "size": item.stat().st_size
                        })
            except PermissionError:
                pass
            except Exception as e:
                print(f"Erreur build_tree: {e}")
            
            return items
        
        files = build_tree(project_path, project_path)
        return {"files": files}
        
    except Exception as e:
        print(f"Erreur get_project_files: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.get("/{project_id}/files/{file_path:path}")
async def get_file_content(
    project_id: int,
    file_path: str,
    db: Session = Depends(get_db)
):
    """Récupère le contenu d'un fichier"""
    try:
        project = db.query(WebProject).filter(WebProject.id == project_id).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        project_path = Path(project.local_path) if project.local_path else None
        
        if not project_path:
            raise HTTPException(status_code=404, detail="Chemin du projet non trouvé")
        
        full_path = project_path / file_path
        
        if not full_path.exists() or not full_path.is_file():
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        # Vérifier que le fichier est bien dans le projet (sécurité)
        try:
            full_path.relative_to(project_path)
        except ValueError:
            raise HTTPException(status_code=403, detail="Accès interdit")
        
        try:
            # Essayer de lire comme texte
            content = full_path.read_text(encoding='utf-8')
            is_binary = False
        except UnicodeDecodeError:
            # Fichier binaire
            content = None
            is_binary = True
        
        return {
            "name": full_path.name,
            "path": file_path,
            "content": content,
            "is_binary": is_binary,
            "size": full_path.stat().st_size
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur get_file_content: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du fichier: {str(e)}")


@router.put("/{project_id}/files/{file_path:path}")
async def update_file_content(
    project_id: int,
    file_path: str,
    content: dict,
    db: Session = Depends(get_db)
):
    """Met à jour le contenu d'un fichier"""
    project = db.query(WebProject).filter(WebProject.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    project_path = Path(project.local_path) if project.local_path else None
    
    if not project_path:
        raise HTTPException(status_code=404, detail="Chemin du projet non trouvé")
    
    full_path = project_path / file_path
    
    # Vérifier que le fichier est bien dans le projet (sécurité)
    try:
        full_path.relative_to(project_path)
    except ValueError:
        raise HTTPException(status_code=403, detail="Accès interdit")
    
    try:
        # Créer les dossiers parents si nécessaire
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Écrire le contenu
        full_path.write_text(content.get("content", ""), encoding='utf-8')
        
        # Mettre à jour la date de modification du projet
        project.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": "Fichier sauvegardé"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde: {str(e)}")
