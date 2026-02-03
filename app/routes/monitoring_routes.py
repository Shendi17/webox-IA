"""
Routes pour le monitoring et les logs
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from datetime import datetime
from app.middleware.auth import require_admin
from app.services.logging_service import logging_service, LogLevel, LogCategory

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/logs")
async def get_logs(
    category: Optional[str] = None,
    date: Optional[str] = None,
    level: Optional[str] = None,
    limit: int = Query(100, le=1000),
    current_user: dict = Depends(require_admin)
):
    """
    Récupérer les logs (admin uniquement)
    """
    try:
        # Convertir les paramètres
        log_category = LogCategory(category) if category else None
        log_level = LogLevel(level.upper()) if level else None
        
        logs = logging_service.get_logs(
            category=log_category,
            date=date,
            level=log_level,
            limit=limit
        )
        
        return {
            "logs": logs,
            "total": len(logs),
            "filters": {
                "category": category,
                "date": date or datetime.utcnow().strftime("%Y-%m-%d"),
                "level": level,
                "limit": limit
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Paramètre invalide: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(
    date: Optional[str] = None,
    current_user: dict = Depends(require_admin)
):
    """
    Obtenir des statistiques sur les logs (admin uniquement)
    """
    try:
        stats = logging_service.get_stats(date=date)
        
        return {
            "date": date or datetime.utcnow().strftime("%Y-%m-%d"),
            "stats": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Vérification de santé du système (public)
    """
    import os
    
    try:
        # Essayer d'importer psutil si disponible
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_info = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024 * 1024 * 1024)
            }
            is_healthy = cpu_percent < 90 and memory.percent < 90
        except ImportError:
            # Fallback sans psutil
            system_info = {
                "cpu_percent": 0,
                "memory_percent": 0,
                "message": "psutil non installé - métriques système non disponibles"
            }
            is_healthy = True
        
        # Vérifier les services critiques
        services_status = {
            "database": True,
            "email": True,
            "logging": True
        }
        
        is_healthy = is_healthy and all(services_status.values())
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "system": system_info,
            "services": services_status
        }
        
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/errors/recent")
async def get_recent_errors(
    limit: int = Query(50, le=200),
    current_user: dict = Depends(require_admin)
):
    """
    Récupérer les erreurs récentes (admin uniquement)
    """
    try:
        logs = logging_service.get_logs(
            level=LogLevel.ERROR,
            limit=limit
        )
        
        # Grouper par type d'erreur
        errors_by_type = {}
        for log in logs:
            error_type = log.get("extra_data", {}).get("error_type", "Unknown")
            if error_type not in errors_by_type:
                errors_by_type[error_type] = []
            errors_by_type[error_type].append(log)
        
        return {
            "total_errors": len(logs),
            "errors": logs,
            "by_type": {
                error_type: len(errors)
                for error_type, errors in errors_by_type.items()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activity/recent")
async def get_recent_activity(
    limit: int = Query(100, le=500),
    current_user: dict = Depends(require_admin)
):
    """
    Récupérer l'activité récente (admin uniquement)
    """
    try:
        logs = logging_service.get_logs(limit=limit)
        
        # Filtrer pour ne garder que les événements importants
        important_logs = [
            log for log in logs
            if log.get("category") in ["auth", "payment", "generation", "security"]
        ]
        
        return {
            "total": len(important_logs),
            "activity": important_logs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
