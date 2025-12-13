from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func
from sqlalchemy.orm import Session

class AnalyticsService:
    
    def get_global_stats(self, db: Session) -> Dict:
        """Statistiques globales de la plateforme"""
        from app.models.podcast import Podcast
        from app.models.avatar import Avatar
        from app.models.series import Series
        from app.models.pwa import PWAProject
        from app.models.react_native import ReactNativeProject
        from app.models.ai_agent import AgentConversation
        
        try:
            stats = {
                "podcasts": {
                    "total": db.query(Podcast).count(),
                    "today": db.query(Podcast).filter(
                        func.date(Podcast.created_at) == datetime.now().date()
                    ).count(),
                    "total_plays": db.query(func.sum(Podcast.plays_count)).scalar() or 0,
                    "total_downloads": db.query(func.sum(Podcast.downloads_count)).scalar() or 0
                },
                "avatars": {
                    "total": db.query(Avatar).count(),
                    "today": db.query(Avatar).filter(
                        func.date(Avatar.created_at) == datetime.now().date()
                    ).count(),
                    "total_downloads": db.query(func.sum(Avatar.downloads_count)).scalar() or 0
                },
                "series": {
                    "total": db.query(Series).count(),
                    "today": db.query(Series).filter(
                        func.date(Series.created_at) == datetime.now().date()
                    ).count(),
                    "total_views": db.query(func.sum(Series.views_count)).scalar() or 0
                },
                "pwa": {
                    "total": db.query(PWAProject).count(),
                    "deployed": db.query(PWAProject).filter(
                        PWAProject.status == "deployed"
                    ).count(),
                    "total_installs": db.query(func.sum(PWAProject.installs_count)).scalar() or 0
                },
                "react_native": {
                    "total": db.query(ReactNativeProject).count(),
                    "total_downloads": db.query(func.sum(ReactNativeProject.downloads_count)).scalar() or 0
                },
                "ai_agent": {
                    "total_conversations": db.query(AgentConversation).count(),
                    "total_messages": db.query(AgentConversation).with_entities(
                        func.sum(AgentConversation.messages_count)
                    ).scalar() or 0,
                    "total_tokens": db.query(AgentConversation).with_entities(
                        func.sum(AgentConversation.tokens_used)
                    ).scalar() or 0
                }
            }
            
            return {
                "success": True,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur analytics : {str(e)}"
            }
    
    def get_usage_trends(self, db: Session, days: int = 30) -> Dict:
        """Tendances d'utilisation sur N jours"""
        from app.models.podcast import Podcast
        from app.models.avatar import Avatar
        from app.models.series import Series
        
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            # Créations par jour
            daily_creations = []
            for i in range(days):
                date = start_date + timedelta(days=i)
                
                podcasts = db.query(Podcast).filter(
                    func.date(Podcast.created_at) == date.date()
                ).count()
                
                avatars = db.query(Avatar).filter(
                    func.date(Avatar.created_at) == date.date()
                ).count()
                
                series = db.query(Series).filter(
                    func.date(Series.created_at) == date.date()
                ).count()
                
                daily_creations.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "podcasts": podcasts,
                    "avatars": avatars,
                    "series": series,
                    "total": podcasts + avatars + series
                })
            
            return {
                "success": True,
                "trends": daily_creations,
                "period": f"{days} days"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur trends : {str(e)}"
            }
    
    def get_performance_metrics(self) -> Dict:
        """Métriques de performance du système"""
        import psutil
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "success": True,
                "metrics": {
                    "cpu": {
                        "usage_percent": cpu_percent,
                        "cores": psutil.cpu_count()
                    },
                    "memory": {
                        "total_gb": round(memory.total / (1024**3), 2),
                        "used_gb": round(memory.used / (1024**3), 2),
                        "percent": memory.percent
                    },
                    "disk": {
                        "total_gb": round(disk.total / (1024**3), 2),
                        "used_gb": round(disk.used / (1024**3), 2),
                        "percent": disk.percent
                    }
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": True,
                "metrics": {
                    "cpu": {"usage_percent": 0, "cores": 0},
                    "memory": {"total_gb": 0, "used_gb": 0, "percent": 0},
                    "disk": {"total_gb": 0, "used_gb": 0, "percent": 0}
                },
                "note": "psutil non installé - pip install psutil"
            }
    
    def get_cost_estimation(self, db: Session) -> Dict:
        """Estimation des coûts d'utilisation"""
        from app.models.podcast import Podcast
        from app.models.avatar import Avatar
        from app.models.series import Series, Episode
        from app.models.pwa import PWAProject
        from app.models.react_native import ReactNativeProject
        
        try:
            # Coûts unitaires
            COST_PODCAST = 0.14
            COST_AVATAR = 0.04
            COST_SERIES_EPISODE = 0.25
            COST_PWA = 0.04
            COST_RN = 0.04
            
            podcasts_count = db.query(Podcast).count()
            avatars_count = db.query(Avatar).count()
            episodes_count = db.query(Episode).count()
            pwa_count = db.query(PWAProject).count()
            rn_count = db.query(ReactNativeProject).count()
            
            total_cost = (
                podcasts_count * COST_PODCAST +
                avatars_count * COST_AVATAR +
                episodes_count * COST_SERIES_EPISODE +
                pwa_count * COST_PWA +
                rn_count * COST_RN
            )
            
            return {
                "success": True,
                "costs": {
                    "podcasts": round(podcasts_count * COST_PODCAST, 2),
                    "avatars": round(avatars_count * COST_AVATAR, 2),
                    "series": round(episodes_count * COST_SERIES_EPISODE, 2),
                    "pwa": round(pwa_count * COST_PWA, 2),
                    "react_native": round(rn_count * COST_RN, 2),
                    "total": round(total_cost, 2)
                },
                "currency": "USD"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur coûts : {str(e)}"
            }
    
    def generate_google_analytics_code(self, tracking_id: str) -> str:
        """Génère le code Google Analytics"""
        return f"""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={tracking_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{tracking_id}');
</script>
<!-- End Google Analytics -->
"""
