"""
Service de Cache avec Redis (avec fallback en mémoire)
"""
import json
import time
from typing import Any, Optional
from datetime import timedelta


class CacheService:
    """Service de cache avec Redis ou fallback mémoire"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}  # Fallback en mémoire
        self.cache_ttl = {}  # TTL pour le cache mémoire
        self._init_redis()
    
    def _init_redis(self):
        """Initialiser la connexion Redis"""
        try:
            import redis
            import os
            
            # Essayer de se connecter à Redis
            redis_url = os.getenv("REDIS_URL", "")
            
            if not redis_url:
                # Pas de Redis configuré, utiliser fallback
                print("ℹ️ Redis non configuré, utilisation du cache mémoire")
                self.redis_client = None
                return
            
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2
            )
            
            # Tester la connexion
            self.redis_client.ping()
            print("✅ Redis connecté")
            
        except Exception as e:
            print(f"⚠️ Redis non disponible, utilisation du cache mémoire: {e}")
            self.redis_client = None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Stocker une valeur dans le cache
        
        Args:
            key: Clé du cache
            value: Valeur à stocker (sera sérialisée en JSON)
            ttl: Durée de vie en secondes (défaut: 1h)
            
        Returns:
            True si succès
        """
        try:
            serialized = json.dumps(value)
            
            if self.redis_client:
                # Utiliser Redis
                self.redis_client.setex(key, ttl, serialized)
            else:
                # Fallback mémoire
                self.memory_cache[key] = serialized
                self.cache_ttl[key] = time.time() + ttl
            
            return True
            
        except Exception as e:
            print(f"Erreur cache set: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Récupérer une valeur du cache
        
        Args:
            key: Clé du cache
            
        Returns:
            Valeur désérialisée ou None si non trouvée/expirée
        """
        try:
            if self.redis_client:
                # Utiliser Redis
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Fallback mémoire
                if key in self.memory_cache:
                    # Vérifier TTL
                    if time.time() < self.cache_ttl.get(key, 0):
                        return json.loads(self.memory_cache[key])
                    else:
                        # Expiré, supprimer
                        del self.memory_cache[key]
                        del self.cache_ttl[key]
            
            return None
            
        except Exception as e:
            print(f"Erreur cache get: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Supprimer une clé du cache
        
        Args:
            key: Clé à supprimer
            
        Returns:
            True si succès
        """
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                if key in self.cache_ttl:
                    del self.cache_ttl[key]
            
            return True
            
        except Exception as e:
            print(f"Erreur cache delete: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Vérifier si une clé existe
        
        Args:
            key: Clé à vérifier
            
        Returns:
            True si la clé existe et n'est pas expirée
        """
        try:
            if self.redis_client:
                return self.redis_client.exists(key) > 0
            else:
                if key in self.memory_cache:
                    # Vérifier TTL
                    return time.time() < self.cache_ttl.get(key, 0)
                return False
                
        except Exception as e:
            print(f"Erreur cache exists: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Supprimer toutes les clés correspondant à un pattern
        
        Args:
            pattern: Pattern (ex: "user:*")
            
        Returns:
            Nombre de clés supprimées
        """
        try:
            count = 0
            
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    count = self.redis_client.delete(*keys)
            else:
                # Fallback mémoire avec pattern simple
                import fnmatch
                keys_to_delete = [
                    k for k in self.memory_cache.keys()
                    if fnmatch.fnmatch(k, pattern)
                ]
                for key in keys_to_delete:
                    del self.memory_cache[key]
                    if key in self.cache_ttl:
                        del self.cache_ttl[key]
                count = len(keys_to_delete)
            
            return count
            
        except Exception as e:
            print(f"Erreur cache clear_pattern: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """
        Obtenir des statistiques sur le cache
        
        Returns:
            Dictionnaire avec les stats
        """
        try:
            if self.redis_client:
                info = self.redis_client.info()
                return {
                    "type": "redis",
                    "connected": True,
                    "keys": self.redis_client.dbsize(),
                    "memory_used": info.get("used_memory_human", "N/A"),
                    "hits": info.get("keyspace_hits", 0),
                    "misses": info.get("keyspace_misses", 0)
                }
            else:
                # Stats mémoire
                active_keys = sum(
                    1 for key in self.memory_cache.keys()
                    if time.time() < self.cache_ttl.get(key, 0)
                )
                return {
                    "type": "memory",
                    "connected": True,
                    "keys": active_keys,
                    "total_keys": len(self.memory_cache)
                }
                
        except Exception as e:
            return {
                "type": "unknown",
                "connected": False,
                "error": str(e)
            }
    
    def cleanup_expired(self):
        """Nettoyer les clés expirées du cache mémoire"""
        if not self.redis_client:
            current_time = time.time()
            expired_keys = [
                key for key, ttl in self.cache_ttl.items()
                if current_time >= ttl
            ]
            for key in expired_keys:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                del self.cache_ttl[key]


# Instance globale
cache_service = CacheService()


# Décorateur pour mettre en cache les résultats de fonctions
def cached(ttl: int = 3600, key_prefix: str = ""):
    """
    Décorateur pour mettre en cache les résultats de fonctions
    
    Args:
        ttl: Durée de vie du cache en secondes
        key_prefix: Préfixe pour la clé de cache
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Générer une clé de cache
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Vérifier le cache
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Exécuter la fonction
            result = await func(*args, **kwargs)
            
            # Mettre en cache
            cache_service.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator
