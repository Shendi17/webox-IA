"""
Routes pour la gestion du cache
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import require_admin
from app.services.cache_service import cache_service

router = APIRouter(prefix="/api/cache", tags=["Cache"])


class CacheSetRequest(BaseModel):
    """Requête pour définir une valeur dans le cache"""
    key: str
    value: dict
    ttl: Optional[int] = 3600


@router.get("/stats")
async def get_cache_stats(
    current_user: dict = Depends(require_admin)
):
    """
    Obtenir les statistiques du cache (admin uniquement)
    """
    try:
        stats = cache_service.get_stats()
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_cache(
    pattern: Optional[str] = None,
    current_user: dict = Depends(require_admin)
):
    """
    Vider le cache (admin uniquement)
    
    Args:
        pattern: Pattern optionnel (ex: "user:*")
    """
    try:
        if pattern:
            count = cache_service.clear_pattern(pattern)
            message = f"{count} clé(s) supprimée(s)"
        else:
            # Vider tout le cache
            count = cache_service.clear_pattern("*")
            message = f"Cache vidé ({count} clés)"
        
        return {
            "success": True,
            "message": message,
            "count": count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set")
async def set_cache_value(
    request: CacheSetRequest,
    current_user: dict = Depends(require_admin)
):
    """
    Définir une valeur dans le cache (admin uniquement)
    """
    try:
        success = cache_service.set(request.key, request.value, request.ttl)
        
        if not success:
            raise HTTPException(status_code=500, detail="Impossible de définir la valeur")
        
        return {
            "success": True,
            "message": f"Valeur définie pour la clé '{request.key}'"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{key}")
async def get_cache_value(
    key: str,
    current_user: dict = Depends(require_admin)
):
    """
    Récupérer une valeur du cache (admin uniquement)
    """
    try:
        value = cache_service.get(key)
        
        if value is None:
            raise HTTPException(status_code=404, detail="Clé non trouvée ou expirée")
        
        return {
            "success": True,
            "key": key,
            "value": value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{key}")
async def delete_cache_value(
    key: str,
    current_user: dict = Depends(require_admin)
):
    """
    Supprimer une clé du cache (admin uniquement)
    """
    try:
        success = cache_service.delete(key)
        
        if not success:
            raise HTTPException(status_code=500, detail="Impossible de supprimer la clé")
        
        return {
            "success": True,
            "message": f"Clé '{key}' supprimée"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
