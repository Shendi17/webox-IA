"""
Routes API pour la Bibliothèque de Prompts
Date : 1er Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from app.models.prompt_db import PromptDB

router = APIRouter(prefix="/api/prompts", tags=["Prompts"])


# Schémas Pydantic
class PromptCreate(BaseModel):
    title: str
    content: str
    category: str = "Général"
    tags: List[str] = []
    is_public: bool = False
    is_favorite: bool = False


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None
    is_favorite: Optional[bool] = None


class PromptResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    category: str
    tags: List[str]
    is_public: bool
    is_favorite: bool
    usage_count: int
    created_at: str
    updated_at: str


@router.get("/", response_model=List[PromptResponse])
async def get_prompts(
    category: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer tous les prompts de l'utilisateur
    """
    query = db.query(PromptDB).filter(PromptDB.user_id == current_user["id"])
    
    # Filtres
    if category:
        query = query.filter(PromptDB.category == category)
    
    if is_favorite is not None:
        query = query.filter(PromptDB.is_favorite == is_favorite)
    
    if search:
        query = query.filter(
            (PromptDB.title.ilike(f"%{search}%")) |
            (PromptDB.content.ilike(f"%{search}%")) |
            (PromptDB.tags.ilike(f"%{search}%"))
        )
    
    prompts = query.order_by(PromptDB.updated_at.desc()).all()
    
    return [PromptResponse(**prompt.to_dict()) for prompt in prompts]


@router.get("/categories")
async def get_categories(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer toutes les catégories de prompts
    """
    categories = db.query(PromptDB.category).filter(
        PromptDB.user_id == current_user["id"]
    ).distinct().all()
    
    return [cat[0] for cat in categories if cat[0]]


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer un prompt spécifique
    """
    prompt = db.query(PromptDB).filter(
        PromptDB.id == prompt_id,
        PromptDB.user_id == current_user["id"]
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    
    return PromptResponse(**prompt.to_dict())


@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt_data: PromptCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Créer un nouveau prompt
    """
    new_prompt = PromptDB(
        user_id=current_user["id"],
        title=prompt_data.title,
        content=prompt_data.content,
        category=prompt_data.category,
        tags=",".join(prompt_data.tags) if prompt_data.tags else "",
        is_public=prompt_data.is_public,
        is_favorite=prompt_data.is_favorite
    )
    
    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)
    
    return PromptResponse(**new_prompt.to_dict())


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    prompt_data: PromptUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Mettre à jour un prompt
    """
    prompt = db.query(PromptDB).filter(
        PromptDB.id == prompt_id,
        PromptDB.user_id == current_user["id"]
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    
    # Mettre à jour les champs
    if prompt_data.title is not None:
        prompt.title = prompt_data.title
    if prompt_data.content is not None:
        prompt.content = prompt_data.content
    if prompt_data.category is not None:
        prompt.category = prompt_data.category
    if prompt_data.tags is not None:
        prompt.tags = ",".join(prompt_data.tags)
    if prompt_data.is_public is not None:
        prompt.is_public = prompt_data.is_public
    if prompt_data.is_favorite is not None:
        prompt.is_favorite = prompt_data.is_favorite
    
    db.commit()
    db.refresh(prompt)
    
    return PromptResponse(**prompt.to_dict())


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Supprimer un prompt
    """
    prompt = db.query(PromptDB).filter(
        PromptDB.id == prompt_id,
        PromptDB.user_id == current_user["id"]
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    
    db.delete(prompt)
    db.commit()
    
    return {"message": "Prompt supprimé avec succès"}


@router.post("/{prompt_id}/use")
async def use_prompt(
    prompt_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Incrémenter le compteur d'utilisation d'un prompt
    """
    prompt = db.query(PromptDB).filter(
        PromptDB.id == prompt_id,
        PromptDB.user_id == current_user["id"]
    ).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    
    prompt.usage_count += 1
    db.commit()
    
    return {"message": "Compteur d'utilisation mis à jour"}
