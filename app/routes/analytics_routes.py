from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
analytics_service = AnalyticsService()

@router.get("/global")
async def get_global_stats(db: Session = Depends(get_db)):
    """Statistiques globales"""
    try:
        result = analytics_service.get_global_stats(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends")
async def get_trends(days: int = 30, db: Session = Depends(get_db)):
    """Tendances d'utilisation"""
    try:
        result = analytics_service.get_usage_trends(db, days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance")
async def get_performance():
    """Métriques de performance"""
    try:
        result = analytics_service.get_performance_metrics()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/costs")
async def get_costs(db: Session = Depends(get_db)):
    """Estimation des coûts"""
    try:
        result = analytics_service.get_cost_estimation(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/google-analytics/{tracking_id}")
async def get_ga_code(tracking_id: str):
    """Code Google Analytics"""
    try:
        code = analytics_service.generate_google_analytics_code(tracking_id)
        return {
            "success": True,
            "code": code,
            "tracking_id": tracking_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
