# ✅ SOLUTION - Redis Timeout au Démarrage

**Date:** 25 Mars 2026  
**Problème:** Le serveur se ferme immédiatement après démarrage

---

## 🔍 DIAGNOSTIC

Le serveur démarre puis s'arrête immédiatement avec:
```
INFO:     Application startup complete.
INFO:     Shutting down
```

**Cause:** Redis est configuré dans `.env` mais ne répond pas:
```
REDIS_URL=redis://localhost:6379/0
```

Le `cache_service` essaie de se connecter à Redis au démarrage et timeout, causant l'arrêt du serveur.

---

## ✅ SOLUTION RAPIDE

### Option 1: Désactiver Redis (Recommandé)

Ouvrir le fichier `.env` et **commenter** la ligne `REDIS_URL`:

**Avant:**
```env
# Redis (optionnel, pour cache)
REDIS_URL=redis://localhost:6379/0
```

**Après:**
```env
# Redis (optionnel, pour cache)
# REDIS_URL=redis://localhost:6379/0
```

**Résultat:** Le serveur utilisera le cache mémoire (fallback automatique)

---

### Option 2: Démarrer Redis

Si vous voulez utiliser Redis:

#### Windows
```bash
# Installer Redis via Chocolatey
choco install redis-64

# Ou télécharger depuis
# https://github.com/microsoftarchive/redis/releases

# Démarrer Redis
redis-server
```

#### Docker (Plus simple)
```bash
docker run -d -p 6379:6379 redis:latest
```

---

## 🚀 APRÈS CORRECTION

### Redémarrer le serveur

```bash
.\start.ps1
```

**Résultat attendu:**
```
✅ Tout est prêt!
🌐 Démarrage du serveur sur:
   - http://webox.local:8000/
INFO:     Application startup complete.
```

Le serveur devrait rester actif et accessible.

---

## 📊 AMÉLIORATION APPLIQUÉE

J'ai également réduit les timeouts Redis dans `cache_service.py`:

**Avant:**
```python
socket_connect_timeout=2
```

**Après:**
```python
socket_connect_timeout=1,
socket_timeout=1
```

**Résultat:** Si Redis ne répond pas, le serveur bascule sur le cache mémoire en 1 seconde au lieu de bloquer.

---

## 🎯 CACHE MÉMOIRE VS REDIS

### Cache Mémoire (Fallback)
- ✅ Aucune installation requise
- ✅ Fonctionne immédiatement
- ⚠️ Perdu au redémarrage du serveur
- ⚠️ Non partagé entre processus

### Redis
- ✅ Persistant
- ✅ Partagé entre processus
- ✅ Meilleure performance
- ⚠️ Nécessite installation et configuration

**Pour le développement:** Le cache mémoire suffit largement.

---

## 🧪 VÉRIFICATION

### Après redémarrage

1. Le serveur démarre et reste actif
2. Vous voyez soit:
   - `ℹ️ Redis non configuré, utilisation du cache mémoire`
   - OU `✅ Redis connecté`
3. Le site http://webox.local:8000/ est accessible
4. Pas de "chargement infini"

---

## 📝 RÉSUMÉ

**Problème:** Redis configuré mais non disponible → timeout → serveur s'arrête

**Solution:** Commenter `REDIS_URL` dans `.env`

**Action:**
1. Ouvrir `.env`
2. Commenter la ligne: `# REDIS_URL=redis://localhost:6379/0`
3. Sauvegarder
4. Redémarrer: `.\start.ps1`

**Résultat:** ✅ Serveur accessible sur http://webox.local:8000/

---

**Statut:** ✅ **CORRECTION APPLIQUÉE (timeouts réduits)**  
**Action requise:** **COMMENTER REDIS_URL DANS .ENV**  
**Temps estimé:** 30 secondes
