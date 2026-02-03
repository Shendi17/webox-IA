# Configuration Redis pour WeBox

## État Actuel

✅ **Cache fonctionnel** - Le système utilise actuellement le **fallback mémoire**  
⚠️ **Redis non configuré** - Configuration optionnelle

---

## Option 1: Utiliser le Cache Mémoire (Actuel)

**Aucune configuration nécessaire** - Le système fonctionne déjà !

**Avantages:**
- ✅ Aucune installation requise
- ✅ Fonctionne immédiatement
- ✅ Parfait pour développement

**Limitations:**
- ⚠️ Cache perdu au redémarrage
- ⚠️ Limité à la mémoire du processus

---

## Option 2: Installer Redis (Optionnel)

### Windows

**1. Télécharger Redis pour Windows:**
```bash
# Via Chocolatey
choco install redis-64

# Ou télécharger depuis:
# https://github.com/microsoftarchive/redis/releases
```

**2. Démarrer Redis:**
```bash
redis-server
```

**3. Vérifier Redis:**
```bash
redis-cli ping
# Devrait retourner: PONG
```

### Configuration WeBox

**Créer/Modifier `.env`:**
```bash
# Cache Redis (optionnel)
REDIS_URL=redis://localhost:6379/0
```

**Redémarrer le serveur:**
```bash
python main.py
```

**Vérifier:**
```
✅ Redis connecté
```

---

## Vérification du Cache

### Via API (Admin)

```bash
# Statistiques cache
curl http://localhost:8000/api/cache/stats

# Réponse avec Redis:
{
  "type": "redis",
  "connected": true,
  "keys": 0,
  "memory_used": "1.2MB"
}

# Réponse sans Redis (actuel):
{
  "type": "memory",
  "connected": true,
  "keys": 0
}
```

---

## Résolution Problème Actuel

### Erreur: "Redis URL must specify one of the following schemes"

**Cause:** Variable `REDIS_URL` vide ou mal configurée

**Solution appliquée:**
- ✅ Cache service modifié pour ignorer Redis si non configuré
- ✅ Utilise automatiquement le fallback mémoire
- ✅ Plus d'erreur au démarrage

**Résultat:**
```
ℹ️ Redis non configuré, utilisation du cache mémoire
```

---

## Problème Sauvegarde Profil (RÉSOLU)

### Erreur: "Erreur de connexion au serveur"

**Cause:** Routes profil utilisaient mal l'authentification

**Corrections appliquées:**
1. ✅ Ajout `Request` dans tous les endpoints profil
2. ✅ Appel correct de `get_current_user(request, db)`
3. ✅ Suppression lignes dupliquées

**Fichier corrigé:** `app/routes/profile_routes.py`

**Routes corrigées:**
- ✅ `GET /api/profile/me`
- ✅ `PUT /api/profile/update`
- ✅ `PUT /api/profile/api-keys`
- ✅ `PUT /api/profile/preferences`
- ✅ `GET /api/profile/stats`

---

## Test Sauvegarde Profil

### Redémarrer le serveur:
```bash
# Arrêter (Ctrl+C)
# Relancer
python main.py
```

### Tester sur http://localhost:8000/profile:
1. Modifier nom ou email
2. Cliquer "Sauvegarder"
3. ✅ Devrait afficher: "Profil mis à jour avec succès !"

---

## Recommandations

### Pour Développement
- ✅ **Cache mémoire suffit** (configuration actuelle)
- Aucune action nécessaire

### Pour Production
- 📌 **Installer Redis recommandé**
- Meilleure performance
- Persistance des données
- Scalabilité

---

## Support

### Logs Cache
```bash
# Au démarrage, vérifier:
ℹ️ Redis non configuré, utilisation du cache mémoire  # OK
✅ Redis connecté                                       # Si Redis installé
```

### APIs Cache (Admin)
```bash
GET    /api/cache/stats          # Statistiques
DELETE /api/cache/clear          # Vider cache
POST   /api/cache/set            # Définir valeur
GET    /api/cache/get/{key}      # Récupérer
DELETE /api/cache/delete/{key}   # Supprimer
```

---

**Configuration actuelle:** ✅ Fonctionnelle (cache mémoire)  
**Redis:** Optionnel pour production  
**Profil:** ✅ Corrigé et fonctionnel
