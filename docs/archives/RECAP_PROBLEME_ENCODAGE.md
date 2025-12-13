# 🔴 Problème d'Encodage Critique - Session 31 Octobre 2025

## Problème Identifié

**Erreur :** `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 103`

### Origine
Le problème vient de **psycopg2** qui essaie de lire un fichier de configuration PostgreSQL Windows avec un encodage incorrect. Le byte `0xe9` correspond au caractère `é` en Latin-1/Windows-1252.

### Fichiers Potentiellement Concernés
- `%APPDATA%\postgresql\pgpass.conf`
- `%APPDATA%\postgresql\pg_service.conf`
- Variables d'environnement système Windows

## Solutions Tentées (Toutes Échouées)

1. ❌ Encodage du mot de passe dans `.env`
2. ❌ Recréation du fichier `.env` en UTF-8
3. ❌ Hardcoding de la DATABASE_URL dans `database.py`
4. ❌ Ajout de `client_encoding` dans les paramètres de connexion
5. ❌ Variables d'environnement PowerShell
6. ❌ Redémarrage complet de Python

## Cause Racine

Le problème est **au niveau du système Windows** :
- PostgreSQL a probablement été installé avec un encodage Windows-1252
- Les fichiers de configuration PostgreSQL utilisent cet encodage
- psycopg2 essaie de les lire en UTF-8 et échoue

## Solutions Possibles

### Solution 1 : Réinstaller PostgreSQL avec UTF-8
```bash
# Désinstaller PostgreSQL
# Réinstaller avec --locale=en_US.UTF-8
```

### Solution 2 : Utiliser Docker PostgreSQL
```bash
docker run --name webox-postgres \
  -e POSTGRES_USER=webox_user \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=webox_db \
  -e POSTGRES_INITDB_ARGS="--encoding=UTF8" \
  -p 5432:5432 \
  -d postgres:16
```

### Solution 3 : Modifier l'Encodage PostgreSQL
```sql
-- Se connecter à PostgreSQL
ALTER DATABASE webox_db SET client_encoding TO 'UTF8';
ALTER ROLE webox_user SET client_encoding TO 'UTF8';
```

### Solution 4 : Utiliser SQLite Temporairement
```python
# Dans database.py
DATABASE_URL = "sqlite:///./webox.db"
```

## Recommandation

**Utiliser Docker PostgreSQL** est la solution la plus propre et rapide :
- Installation en 2 minutes
- Encodage UTF-8 garanti
- Isolation complète
- Pas de conflit avec le système

## Impact

- ❌ Impossible de se connecter à l'application
- ❌ Impossible d'utiliser PostgreSQL
- ✅ Le reste du code fonctionne (interface, routes, etc.)

## Prochaine Action

**CHOIX 1 : Docker PostgreSQL** (Recommandé - 5 minutes)
**CHOIX 2 : SQLite temporaire** (Rapide - 2 minutes)
**CHOIX 3 : Réinstaller PostgreSQL** (Long - 30 minutes)

---

**Date :** 31 Octobre 2025 00:45  
**Durée du problème :** 1h30  
**Statut :** Bloquant
