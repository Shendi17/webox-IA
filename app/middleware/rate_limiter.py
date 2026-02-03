"""
Middleware de rate limiting
Limite le nombre de requêtes par IP/utilisateur
"""
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time


class RateLimiter:
    """Rate limiter simple basé sur la mémoire"""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
        self.cleanup_interval = 300  # Nettoyage toutes les 5 minutes
        self.last_cleanup = time.time()
    
    def _cleanup_old_requests(self):
        """Nettoie les anciennes requêtes pour libérer la mémoire"""
        current_time = time.time()
        
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        # Supprimer les entrées vides ou très anciennes
        keys_to_delete = []
        for key, timestamps in self.requests.items():
            # Garder seulement les timestamps des dernières 24h
            recent_timestamps = [
                ts for ts in timestamps 
                if current_time - ts < 86400
            ]
            
            if not recent_timestamps:
                keys_to_delete.append(key)
            else:
                self.requests[key] = recent_timestamps
        
        for key in keys_to_delete:
            del self.requests[key]
        
        self.last_cleanup = current_time
    
    def is_rate_limited(
        self, 
        identifier: str, 
        max_requests: int, 
        window_seconds: int
    ) -> Tuple[bool, int]:
        """
        Vérifie si l'identifiant a dépassé la limite
        
        Args:
            identifier: IP ou user_id
            max_requests: Nombre max de requêtes
            window_seconds: Fenêtre de temps en secondes
            
        Returns:
            (is_limited, remaining_requests)
        """
        self._cleanup_old_requests()
        
        current_time = time.time()
        
        # Initialiser si nouveau
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Filtrer les requêtes dans la fenêtre de temps
        window_start = current_time - window_seconds
        recent_requests = [
            ts for ts in self.requests[identifier]
            if ts > window_start
        ]
        
        self.requests[identifier] = recent_requests
        
        # Vérifier la limite
        if len(recent_requests) >= max_requests:
            return True, 0
        
        # Ajouter la requête actuelle
        self.requests[identifier].append(current_time)
        
        remaining = max_requests - len(recent_requests) - 1
        return False, remaining
    
    def get_reset_time(self, identifier: str, window_seconds: int) -> int:
        """
        Obtient le temps restant avant reset
        
        Returns:
            Secondes avant reset
        """
        if identifier not in self.requests or not self.requests[identifier]:
            return 0
        
        oldest_request = min(self.requests[identifier])
        reset_time = oldest_request + window_seconds
        remaining = max(0, int(reset_time - time.time()))
        
        return remaining


# Instance globale
rate_limiter = RateLimiter()


# Décorateurs pour différents niveaux de rate limiting
def rate_limit_strict(max_requests: int = 10, window_seconds: int = 60):
    """Rate limit strict (ex: login, register)"""
    async def dependency(request: Request):
        client_ip = request.client.host
        
        is_limited, remaining = rate_limiter.is_rate_limited(
            identifier=client_ip,
            max_requests=max_requests,
            window_seconds=window_seconds
        )
        
        if is_limited:
            reset_time = rate_limiter.get_reset_time(client_ip, window_seconds)
            raise HTTPException(
                status_code=429,
                detail=f"Trop de requêtes. Réessayez dans {reset_time} secondes.",
                headers={"Retry-After": str(reset_time)}
            )
        
        # Ajouter les headers de rate limit
        request.state.rate_limit_remaining = remaining
        request.state.rate_limit_limit = max_requests
        
        return True
    
    return dependency


def rate_limit_moderate(max_requests: int = 60, window_seconds: int = 60):
    """Rate limit modéré (ex: API génération)"""
    async def dependency(request: Request):
        client_ip = request.client.host
        
        is_limited, remaining = rate_limiter.is_rate_limited(
            identifier=client_ip,
            max_requests=max_requests,
            window_seconds=window_seconds
        )
        
        if is_limited:
            reset_time = rate_limiter.get_reset_time(client_ip, window_seconds)
            raise HTTPException(
                status_code=429,
                detail=f"Limite de requêtes atteinte. Réessayez dans {reset_time} secondes.",
                headers={"Retry-After": str(reset_time)}
            )
        
        request.state.rate_limit_remaining = remaining
        request.state.rate_limit_limit = max_requests
        
        return True
    
    return dependency


def rate_limit_relaxed(max_requests: int = 300, window_seconds: int = 60):
    """Rate limit relaxé (ex: lecture, recherche)"""
    async def dependency(request: Request):
        client_ip = request.client.host
        
        is_limited, remaining = rate_limiter.is_rate_limited(
            identifier=client_ip,
            max_requests=max_requests,
            window_seconds=window_seconds
        )
        
        if is_limited:
            reset_time = rate_limiter.get_reset_time(client_ip, window_seconds)
            raise HTTPException(
                status_code=429,
                detail=f"Limite de requêtes atteinte. Réessayez dans {reset_time} secondes.",
                headers={"Retry-After": str(reset_time)}
            )
        
        request.state.rate_limit_remaining = remaining
        request.state.rate_limit_limit = max_requests
        
        return True
    
    return dependency
