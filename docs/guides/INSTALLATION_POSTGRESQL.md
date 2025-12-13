# 🐘 Installation PostgreSQL - Guide Complet

**Date :** 30 Octobre 2025  
**Problème :** Chocolatey nécessite des droits administrateur

---

## ⚠️ PROBLÈME RENCONTRÉ

```
vcredist140 not installed. An error occurred during installation:
Unable to obtain lock file access...
```

**Cause :** 
1. Chocolatey nécessite PowerShell en mode Administrateur
2. Un fichier de verrouillage bloque l'installation

---

## ✅ SOLUTION 1 : Installation Manuelle (RECOMMANDÉ)

### Étape 1 : Télécharger PostgreSQL

**Lien :** https://www.postgresql.org/download/windows/

1. Cliquer sur "Download the installer"
2. Choisir la version **PostgreSQL 16.x** (dernière version)
3. Télécharger le fichier `.exe` (environ 300 MB)

### Étape 2 : Installer PostgreSQL

1. **Lancer l'installateur** (double-clic sur le fichier téléchargé)

2. **Suivre l'assistant d'installation :**
   - Installation Directory : `C:\Program Files\PostgreSQL\16` (par défaut)
   - Composants : Cocher tous (PostgreSQL Server, pgAdmin 4, Stack Builder, Command Line Tools)
   - Data Directory : `C:\Program Files\PostgreSQL\16\data` (par défaut)
   - **Mot de passe :** Choisir un mot de passe pour l'utilisateur `postgres` (noter ce mot de passe !)
   - Port : `5432` (par défaut)
   - Locale : `French, France` ou `Default locale`

3. **Terminer l'installation**
   - Décocher "Launch Stack Builder" (pas nécessaire)
   - Cliquer sur "Finish"

### Étape 3 : Vérifier l'Installation

```powershell
# Ouvrir PowerShell (pas besoin d'admin)
# Vérifier que PostgreSQL est installé
psql --version

# Si la commande n'est pas trouvée, ajouter au PATH :
# Panneau de configuration → Système → Paramètres système avancés → Variables d'environnement
# Ajouter : C:\Program Files\PostgreSQL\16\bin
```

### Étape 4 : Créer la Base de Données

```powershell
# Se connecter à PostgreSQL (remplacer 'votre_mot_de_passe' par celui choisi)
psql -U postgres

# Dans psql, exécuter :
CREATE DATABASE webox_db;
CREATE USER webox_user WITH PASSWORD 'VotreMotDePasseSecurise123!';
GRANT ALL PRIVILEGES ON DATABASE webox_db TO webox_user;

# Quitter psql
\q
```

### Étape 5 : Tester la Connexion

```powershell
# Se connecter avec le nouvel utilisateur
psql -U webox_user -d webox_db

# Si ça fonctionne, vous verrez :
# webox_db=>

# Quitter
\q
```

### Étape 6 : Configurer .env

```env
# Ajouter dans .env
DATABASE_URL=postgresql://webox_user:VotreMotDePasseSecurise123!@localhost:5432/webox_db
```

---

## ✅ SOLUTION 2 : Utiliser Chocolatey en Mode Administrateur

### Étape 1 : Ouvrir PowerShell en Administrateur

1. **Clic droit** sur l'icône PowerShell
2. Sélectionner **"Exécuter en tant qu'administrateur"**
3. Accepter l'UAC (Contrôle de compte d'utilisateur)

### Étape 2 : Supprimer le Fichier de Verrouillage

```powershell
# Supprimer le fichier de verrouillage
Remove-Item -Path "C:\ProgramData\chocolatey\lib\3abd6af79ba28beb24475afe445e051e0e995ef9" -Force -ErrorAction SilentlyContinue

# Vérifier
Write-Host "Fichier de verrouillage supprimé" -ForegroundColor Green
```

### Étape 3 : Installer PostgreSQL

```powershell
# Installer PostgreSQL via Chocolatey
choco install postgresql -y

# Attendre la fin de l'installation (peut prendre 5-10 minutes)
```

### Étape 4 : Configurer PostgreSQL

```powershell
# Le mot de passe par défaut est souvent "postgres"
# Se connecter
psql -U postgres

# Créer la base de données
CREATE DATABASE webox_db;
CREATE USER webox_user WITH PASSWORD 'VotreMotDePasseSecurise123!';
GRANT ALL PRIVILEGES ON DATABASE webox_db TO webox_user;
\q
```

---

## ✅ SOLUTION 3 : Utiliser Docker (ALTERNATIVE)

Si vous avez Docker installé :

```powershell
# Lancer PostgreSQL dans un conteneur Docker
docker run --name webox-postgres `
  -e POSTGRES_USER=webox_user `
  -e POSTGRES_PASSWORD=VotreMotDePasseSecurise123! `
  -e POSTGRES_DB=webox_db `
  -p 5432:5432 `
  -d postgres:16

# Vérifier que le conteneur fonctionne
docker ps

# Se connecter
docker exec -it webox-postgres psql -U webox_user -d webox_db
```

**Avantages Docker :**
- Pas besoin d'installation système
- Facile à supprimer/recréer
- Isolation complète

---

## 🔧 DÉPANNAGE

### Problème : "psql: command not found"

**Solution :** Ajouter PostgreSQL au PATH

```powershell
# Ajouter temporairement
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

# Ou ajouter définitivement :
# Panneau de configuration → Système → Variables d'environnement
# Variable PATH → Ajouter : C:\Program Files\PostgreSQL\16\bin
```

### Problème : "password authentication failed"

**Solution :** Vérifier le mot de passe

```powershell
# Réinitialiser le mot de passe
psql -U postgres
ALTER USER postgres WITH PASSWORD 'nouveau_mot_de_passe';
\q
```

### Problème : "could not connect to server"

**Solution :** Démarrer le service PostgreSQL

```powershell
# Vérifier le statut du service
Get-Service postgresql*

# Démarrer le service
Start-Service postgresql-x64-16

# Ou via l'interface graphique :
# services.msc → postgresql-x64-16 → Démarrer
```

---

## 📝 APRÈS L'INSTALLATION

### 1. Installer les Dépendances Python

```powershell
# Installer psycopg2 (driver PostgreSQL pour Python)
pip install psycopg2-binary

# Installer SQLAlchemy et Alembic
pip install sqlalchemy alembic
```

### 2. Tester la Connexion depuis Python

```python
# test_db.py
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://webox_user:VotreMotDePasseSecurise123!@localhost:5432/webox_db"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Connexion réussie à PostgreSQL !")
    connection.close()
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
```

```powershell
# Tester
python test_db.py
```

### 3. Configurer Alembic

```powershell
# Initialiser Alembic
cd app
alembic init alembic

# Éditer alembic.ini
# Remplacer :
# sqlalchemy.url = driver://user:pass@localhost/dbname
# Par :
# sqlalchemy.url = postgresql://webox_user:VotreMotDePasseSecurise123!@localhost:5432/webox_db
```

---

## 🎯 RECOMMANDATION

**Je recommande la SOLUTION 1 (Installation Manuelle)** car :
- ✅ Pas besoin de droits administrateur
- ✅ Interface graphique (pgAdmin 4) incluse
- ✅ Plus stable
- ✅ Facile à désinstaller si besoin

**Temps d'installation :** 10-15 minutes

---

## 📊 CHECKLIST

### Installation
- [ ] PostgreSQL téléchargé
- [ ] PostgreSQL installé
- [ ] Mot de passe `postgres` défini
- [ ] Service PostgreSQL démarré
- [ ] Commande `psql` accessible

### Configuration
- [ ] Base de données `webox_db` créée
- [ ] Utilisateur `webox_user` créé
- [ ] Privilèges accordés
- [ ] Connexion testée
- [ ] `.env` configuré

### Python
- [ ] `psycopg2-binary` installé
- [ ] `sqlalchemy` installé
- [ ] `alembic` installé
- [ ] Connexion Python testée
- [ ] Alembic initialisé

---

## 🔗 LIENS UTILES

- **Téléchargement :** https://www.postgresql.org/download/windows/
- **Documentation :** https://www.postgresql.org/docs/
- **pgAdmin 4 :** Interface graphique pour gérer PostgreSQL
- **Tutoriel :** https://www.postgresqltutorial.com/

---

**📅 Dernière mise à jour :** 30 Octobre 2025  
**👤 Créé par :** Cascade AI  
**🎯 Objectif :** Installer PostgreSQL pour WeBox Multi-IA
