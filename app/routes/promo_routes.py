"""
Routes API pour les codes promo
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user_from_token, require_admin
from app.services.promo_code_service import promo_service

router = APIRouter(prefix="/api/promo", tags=["promo"])


class PromoCodeCreate(BaseModel):
    code: str
    discount_type: str  # "percentage" ou "fixed"
    discount_value: float
    min_amount: float = 0.0
    max_uses: Optional[int] = None
    expires_at: Optional[str] = None
    description: str = ""


class PromoCodeValidate(BaseModel):
    code: str
    cart_total: float


@router.post("/validate")
async def validate_promo_code(request: PromoCodeValidate):
    """
    Valider un code promo
    Public - accessible sans authentification
    """
    result = promo_service.validate_code(request.code, request.cart_total)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.post("/create")
async def create_promo_code(
    request: PromoCodeCreate,
    current_user: dict = Depends(require_admin)
):
    """
    Créer un nouveau code promo
    Admin uniquement
    """
    result = promo_service.create_code(
        code=request.code,
        discount_type=request.discount_type,
        discount_value=request.discount_value,
        min_amount=request.min_amount,
        max_uses=request.max_uses,
        expires_at=request.expires_at,
        description=request.description
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/list")
async def list_promo_codes(
    active_only: bool = False,
    current_user: dict = Depends(require_admin)
):
    """
    Lister tous les codes promo
    Admin uniquement
    """
    codes = promo_service.list_codes(active_only=active_only)
    return {"codes": codes, "total": len(codes)}


@router.get("/{code}")
async def get_promo_code(
    code: str,
    current_user: dict = Depends(require_admin)
):
    """
    Récupérer les informations d'un code promo
    Admin uniquement
    """
    promo = promo_service.get_code(code)
    
    if not promo:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")
    
    return promo


@router.delete("/{code}")
async def delete_promo_code(
    code: str,
    current_user: dict = Depends(require_admin)
):
    """
    Supprimer un code promo
    Admin uniquement
    """
    success = promo_service.delete_code(code)
    
    if not success:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")
    
    return {"message": "Code promo supprimé avec succès"}


@router.patch("/{code}/deactivate")
async def deactivate_promo_code(
    code: str,
    current_user: dict = Depends(require_admin)
):
    """
    Désactiver un code promo
    Admin uniquement
    """
    success = promo_service.deactivate_code(code)
    
    if not success:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")
    
    return {"message": "Code promo désactivé avec succès"}
