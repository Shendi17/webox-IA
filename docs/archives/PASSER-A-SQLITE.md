# 🔄 Passage Temporaire à SQLite

## Problème
Impossible de résoudre le problème d'encodage PostgreSQL sur Windows.
L'erreur `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9` persiste malgré toutes les tentatives.

## Solution Temporaire
Utiliser SQLite pour débloquer le développement, puis revenir à PostgreSQL plus tard.

## Avantages SQLite
- ✅ Pas de problème d'encodage
- ✅ Pas de serveur à gérer
- ✅ Fichier unique portable
- ✅ Compatible avec SQLAlchemy
- ✅ Parfait pour le développement

## Migration Facile
SQLAlchemy permet de changer de base de données en modifiant juste la DATABASE_URL.
Toutes les tables et données peuvent être exportées/importées facilement.

## Retour à PostgreSQL
Quand le problème sera résolu (réinstallation propre de PostgreSQL ou utilisation de Docker avec WSL activé), on pourra revenir à PostgreSQL en 5 minutes.

---

**Veux-tu que je configure SQLite maintenant pour qu'on puisse continuer ?**
