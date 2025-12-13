"""
Routes API pour Git
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel

from app.database import get_db
from app.models.web_project_db import WebProject
from app.services.git_service import GitService

router = APIRouter(prefix="/api/git", tags=["Git"])


# ==================== SCHEMAS ====================

class GitInitRequest(BaseModel):
    project_id: int


class GitStatusRequest(BaseModel):
    project_id: int


class GitAddRequest(BaseModel):
    project_id: int
    files: Optional[List[str]] = None


class GitCommitRequest(BaseModel):
    project_id: int
    message: str
    author_name: Optional[str] = None
    author_email: Optional[str] = None


class GitPushRequest(BaseModel):
    project_id: int
    remote: str = "origin"
    branch: Optional[str] = None


class GitPullRequest(BaseModel):
    project_id: int
    remote: str = "origin"
    branch: Optional[str] = None


class GitBranchRequest(BaseModel):
    project_id: int
    branch_name: str
    checkout: bool = True


class GitCheckoutRequest(BaseModel):
    project_id: int
    branch_name: str


class GitRemoteRequest(BaseModel):
    project_id: int
    name: str
    url: str


class GitLogRequest(BaseModel):
    project_id: int
    limit: int = 20


class GitDiffRequest(BaseModel):
    project_id: int
    file_path: Optional[str] = None


# ==================== HELPER ====================

def get_git_service(project_id: int, db: Session) -> GitService:
    """Obtenir le service Git pour un projet"""
    project = db.query(WebProject).filter(WebProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    return GitService(project.local_path)


# ==================== ROUTES ====================

@router.post("/init")
async def git_init(data: GitInitRequest, db: Session = Depends(get_db)):
    """Initialiser un dépôt Git"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.init()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/status")
async def git_status(data: GitStatusRequest, db: Session = Depends(get_db)):
    """Obtenir le statut Git"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.status()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add")
async def git_add(data: GitAddRequest, db: Session = Depends(get_db)):
    """Ajouter des fichiers au staging"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.add(data.files)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/commit")
async def git_commit(data: GitCommitRequest, db: Session = Depends(get_db)):
    """Créer un commit"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.commit(data.message, data.author_name, data.author_email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/push")
async def git_push(data: GitPushRequest, db: Session = Depends(get_db)):
    """Pousser vers le dépôt distant"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.push(data.remote, data.branch)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pull")
async def git_pull(data: GitPullRequest, db: Session = Depends(get_db)):
    """Tirer depuis le dépôt distant"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.pull(data.remote, data.branch)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/branches")
async def git_branches(data: GitStatusRequest, db: Session = Depends(get_db)):
    """Lister les branches"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.branches()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/branch/create")
async def git_create_branch(data: GitBranchRequest, db: Session = Depends(get_db)):
    """Créer une nouvelle branche"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.create_branch(data.branch_name, data.checkout)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checkout")
async def git_checkout(data: GitCheckoutRequest, db: Session = Depends(get_db)):
    """Changer de branche"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.checkout(data.branch_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/log")
async def git_log(data: GitLogRequest, db: Session = Depends(get_db)):
    """Obtenir l'historique des commits"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.log(data.limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/diff")
async def git_diff(data: GitDiffRequest, db: Session = Depends(get_db)):
    """Obtenir les différences"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.diff(data.file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/remote/add")
async def git_remote_add(data: GitRemoteRequest, db: Session = Depends(get_db)):
    """Ajouter un dépôt distant"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.remote_add(data.name, data.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/remotes")
async def git_remotes(data: GitStatusRequest, db: Session = Depends(get_db)):
    """Lister les dépôts distants"""
    try:
        git_service = get_git_service(data.project_id, db)
        result = git_service.remotes()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/commit/generate-message")
async def git_generate_commit_message(data: GitStatusRequest, db: Session = Depends(get_db)):
    """Générer un message de commit intelligent"""
    try:
        git_service = get_git_service(data.project_id, db)
        
        # Obtenir le statut
        status = git_service.status()
        if not status.get("success"):
            return status
        
        # Générer le message
        message = git_service.generate_commit_message(status)
        
        return {
            "success": True,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
