"""
Service de logging centralisé
Gère les logs système, erreurs et événements
"""
import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogCategory(str, Enum):
    AUTH = "auth"
    API = "api"
    GENERATION = "generation"
    PAYMENT = "payment"
    SECURITY = "security"
    SYSTEM = "system"
    DATABASE = "database"


class LoggingService:
    """Service centralisé de logging"""
    
    def __init__(self):
        self.logs_dir = "logs"
        self._ensure_logs_dir()
        self._setup_loggers()
    
    def _ensure_logs_dir(self):
        """Créer le dossier de logs"""
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Créer sous-dossiers par catégorie
        for category in LogCategory:
            os.makedirs(os.path.join(self.logs_dir, category.value), exist_ok=True)
    
    def _setup_loggers(self):
        """Configurer les loggers Python"""
        # Logger principal
        self.logger = logging.getLogger("webox")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler fichier général
        general_handler = logging.FileHandler(
            os.path.join(self.logs_dir, "app.log"),
            encoding="utf-8"
        )
        general_handler.setLevel(logging.INFO)
        
        # Handler fichier erreurs
        error_handler = logging.FileHandler(
            os.path.join(self.logs_dir, "errors.log"),
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        general_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        
        self.logger.addHandler(general_handler)
        self.logger.addHandler(error_handler)
    
    def log(
        self,
        level: LogLevel,
        category: LogCategory,
        message: str,
        user_id: Optional[int] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """
        Logger un événement
        
        Args:
            level: Niveau de log
            category: Catégorie
            message: Message
            user_id: ID utilisateur (optionnel)
            extra_data: Données supplémentaires (optionnel)
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "category": category.value,
            "message": message,
            "user_id": user_id,
            "extra_data": extra_data or {}
        }
        
        # Logger avec Python logging
        log_method = getattr(self.logger, level.value.lower())
        log_method(f"[{category.value}] {message}")
        
        # Sauvegarder en JSON pour analyse
        self._save_json_log(category, log_entry)
    
    def _save_json_log(self, category: LogCategory, log_entry: Dict):
        """Sauvegarder le log en JSON"""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        log_file = os.path.join(
            self.logs_dir,
            category.value,
            f"{date_str}.json"
        )
        
        try:
            # Lire les logs existants
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Ajouter le nouveau log
            logs.append(log_entry)
            
            # Sauvegarder
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erreur sauvegarde log JSON: {e}")
    
    def log_auth(self, action: str, user_id: Optional[int] = None, success: bool = True, ip: str = None):
        """Logger une action d'authentification"""
        level = LogLevel.INFO if success else LogLevel.WARNING
        extra_data = {"action": action, "success": success, "ip": ip}
        
        self.log(
            level=level,
            category=LogCategory.AUTH,
            message=f"Auth: {action} - {'Success' if success else 'Failed'}",
            user_id=user_id,
            extra_data=extra_data
        )
    
    def log_api_call(
        self,
        endpoint: str,
        method: str,
        user_id: Optional[int] = None,
        status_code: int = 200,
        duration_ms: Optional[float] = None
    ):
        """Logger un appel API"""
        level = LogLevel.INFO if status_code < 400 else LogLevel.WARNING
        extra_data = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms
        }
        
        self.log(
            level=level,
            category=LogCategory.API,
            message=f"API {method} {endpoint} - {status_code}",
            user_id=user_id,
            extra_data=extra_data
        )
    
    def log_generation(
        self,
        generation_type: str,
        user_id: int,
        success: bool = True,
        cost: float = 0.0,
        duration_s: Optional[float] = None,
        error: Optional[str] = None
    ):
        """Logger une génération IA"""
        level = LogLevel.INFO if success else LogLevel.ERROR
        extra_data = {
            "type": generation_type,
            "success": success,
            "cost": cost,
            "duration_s": duration_s,
            "error": error
        }
        
        self.log(
            level=level,
            category=LogCategory.GENERATION,
            message=f"Generation {generation_type} - {'Success' if success else 'Failed'}",
            user_id=user_id,
            extra_data=extra_data
        )
    
    def log_payment(
        self,
        user_id: int,
        amount: float,
        currency: str = "EUR",
        success: bool = True,
        payment_method: str = "stripe",
        transaction_id: Optional[str] = None
    ):
        """Logger une transaction de paiement"""
        level = LogLevel.INFO if success else LogLevel.ERROR
        extra_data = {
            "amount": amount,
            "currency": currency,
            "success": success,
            "payment_method": payment_method,
            "transaction_id": transaction_id
        }
        
        self.log(
            level=level,
            category=LogCategory.PAYMENT,
            message=f"Payment {amount}{currency} - {'Success' if success else 'Failed'}",
            user_id=user_id,
            extra_data=extra_data
        )
    
    def log_security_event(
        self,
        event_type: str,
        severity: str = "medium",
        user_id: Optional[int] = None,
        ip: Optional[str] = None,
        details: Optional[str] = None
    ):
        """Logger un événement de sécurité"""
        level_map = {
            "low": LogLevel.INFO,
            "medium": LogLevel.WARNING,
            "high": LogLevel.ERROR,
            "critical": LogLevel.CRITICAL
        }
        level = level_map.get(severity, LogLevel.WARNING)
        
        extra_data = {
            "event_type": event_type,
            "severity": severity,
            "ip": ip,
            "details": details
        }
        
        self.log(
            level=level,
            category=LogCategory.SECURITY,
            message=f"Security: {event_type} ({severity})",
            user_id=user_id,
            extra_data=extra_data
        )
    
    def log_error(
        self,
        error: Exception,
        context: str = "",
        user_id: Optional[int] = None,
        extra_data: Optional[Dict] = None
    ):
        """Logger une erreur"""
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            **(extra_data or {})
        }
        
        self.log(
            level=LogLevel.ERROR,
            category=LogCategory.SYSTEM,
            message=f"Error: {type(error).__name__} - {str(error)}",
            user_id=user_id,
            extra_data=error_data
        )
    
    def get_logs(
        self,
        category: Optional[LogCategory] = None,
        date: Optional[str] = None,
        level: Optional[LogLevel] = None,
        limit: int = 100
    ) -> list:
        """
        Récupérer les logs avec filtres
        
        Returns:
            Liste des logs
        """
        if not date:
            date = datetime.utcnow().strftime("%Y-%m-%d")
        
        logs = []
        
        # Déterminer les catégories à lire
        categories = [category] if category else list(LogCategory)
        
        for cat in categories:
            log_file = os.path.join(
                self.logs_dir,
                cat.value,
                f"{date}.json"
            )
            
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        cat_logs = json.load(f)
                        
                        # Filtrer par niveau si spécifié
                        if level:
                            cat_logs = [
                                log for log in cat_logs
                                if log.get("level") == level.value
                            ]
                        
                        logs.extend(cat_logs)
                        
                except Exception as e:
                    print(f"Erreur lecture logs {cat.value}: {e}")
        
        # Trier par timestamp (plus récent en premier)
        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return logs[:limit]
    
    def get_stats(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtenir des statistiques sur les logs
        
        Returns:
            Statistiques
        """
        logs = self.get_logs(date=date, limit=10000)
        
        stats = {
            "total": len(logs),
            "by_level": {},
            "by_category": {},
            "errors": 0,
            "warnings": 0
        }
        
        for log in logs:
            level = log.get("level", "INFO")
            category = log.get("category", "system")
            
            stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            if level == "ERROR" or level == "CRITICAL":
                stats["errors"] += 1
            elif level == "WARNING":
                stats["warnings"] += 1
        
        return stats


# Instance globale
logging_service = LoggingService()
