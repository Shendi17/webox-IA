# 📐 PHASE 1 : STUDIO WEB IA - SPÉCIFICATIONS DÉTAILLÉES

**Date** : 22 Novembre 2025  
**Durée estimée** : 3-4 mois  
**Priorité** : CRITIQUE

---

# 🎯 OBJECTIF

Créer un studio de développement web complet, piloté par IA, permettant de :
- Gérer plusieurs projets web
- Éditer le code directement dans le navigateur
- Utiliser Git (commits, branches, PR)
- Déployer automatiquement
- Modifier/améliorer par commandes IA

---

# 📊 MODÈLES DE DONNÉES

## 1. WebProject

```python
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class WebProject(Base):
    __tablename__ = "web_projects"
    
    # Identité
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    
    # Type & Stack
    project_type = Column(String(50))  # static, react, vue, nextjs, django, fastapi, wordpress
    framework = Column(String(50))
    framework_version = Column(String(20))
    languages = Column(JSON)  # ["python", "javascript", "html", "css"]
    
    # Stockage
    storage_type = Column(String(20))  # local, git
    local_path = Column(String(500))  # chemin absolu si local
    
    # Git
    git_provider = Column(String(20))  # github, gitlab, bitbucket
    git_repo_url = Column(String(500))
    git_branch = Column(String(100), default="main")
    git_token = Column(String(500))  # chiffré
    
    # Déploiement
    deployment_provider = Column(String(50))  # vercel, netlify, vps, aws, etc.
    deployment_config = Column(JSON)  # config spécifique au provider
    prod_url = Column(String(500))
    staging_url = Column(String(500))
    dev_url = Column(String(500))
    auto_deploy = Column(Boolean, default=False)
    
    # Environnement
    environment_vars = Column(JSON)  # variables d'environnement
    build_command = Column(String(500))
    start_command = Column(String(500))
    
    # Métadonnées
    owner_id = Column(Integer, ForeignKey("users.id"))
    team_members = Column(JSON)  # [user_ids]
    status = Column(String(20), default="active")  # active, archived, maintenance
    
    # Statistiques
    total_files = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    last_build_at = Column(DateTime)
    last_deploy_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    owner = relationship("User", back_populates="web_projects")
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")
    deployments = relationship("Deployment", back_populates="project", cascade="all, delete-orphan")
    commits = relationship("ProjectCommit", back_populates="project", cascade="all, delete-orphan")
```

## 2. ProjectFile

```python
class ProjectFile(Base):
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"))
    
    # Chemin
    path = Column(String(1000), nullable=False)  # chemin relatif depuis la racine
    name = Column(String(255), nullable=False)
    extension = Column(String(20))
    
    # Contenu
    content = Column(Text)  # contenu du fichier
    size = Column(Integer)  # taille en bytes
    lines = Column(Integer)  # nombre de lignes
    
    # Métadonnées
    is_binary = Column(Boolean, default=False)
    mime_type = Column(String(100))
    encoding = Column(String(20), default="utf-8")
    
    # Git
    git_status = Column(String(20))  # untracked, modified, staged, committed
    last_commit_hash = Column(String(40))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    project = relationship("WebProject", back_populates="files")
```

## 3. Deployment

```python
class Deployment(Base):
    __tablename__ = "deployments"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"))
    
    # Déploiement
    environment = Column(String(20))  # dev, staging, prod
    provider = Column(String(50))
    deployment_id = Column(String(200))  # ID chez le provider
    url = Column(String(500))
    
    # Build
    commit_hash = Column(String(40))
    branch = Column(String(100))
    build_status = Column(String(20))  # pending, building, success, failed
    build_logs = Column(Text)
    build_duration = Column(Integer)  # secondes
    
    # Métadonnées
    triggered_by = Column(String(20))  # manual, auto, webhook
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    project = relationship("WebProject", back_populates="deployments")
```

## 4. ProjectCommit

```python
class ProjectCommit(Base):
    __tablename__ = "project_commits"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"))
    
    # Git
    commit_hash = Column(String(40), unique=True)
    branch = Column(String(100))
    message = Column(Text)
    author_name = Column(String(200))
    author_email = Column(String(200))
    
    # Changements
    files_changed = Column(Integer)
    insertions = Column(Integer)
    deletions = Column(Integer)
    changed_files = Column(JSON)  # liste des fichiers modifiés
    
    # Métadonnées
    is_merge = Column(Boolean, default=False)
    parent_hashes = Column(JSON)  # commits parents
    
    # Timestamps
    committed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    project = relationship("WebProject", back_populates="commits")
```

---

# 🎨 INTERFACES UTILISATEUR

## 1. Page "Mes Projets" (`/projects`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ 🏠 Mes Projets Web                    [➕ Nouveau] [📥 Importer] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🔍 [Rechercher...]  [Type ▼] [Stack ▼] [Statut ▼]     │
│                                                         │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│ │ 🌐 Portfolio│ │ 🛒 E-shop   │ │ 📝 Blog     │      │
│ │ Next.js     │ │ React       │ │ Django      │      │
│ │ ✅ Publié   │ │ 🔧 Dev      │ │ ✅ Publié   │      │
│ │ [Ouvrir]    │ │ [Ouvrir]    │ │ [Ouvrir]    │      │
│ └─────────────┘ └─────────────┘ └─────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Carte de Projet
- Preview (screenshot ou icône)
- Nom + description courte
- Stack (badges)
- Statut (publié, dev, maintenance)
- URL de prod (si déployé)
- Actions :
  - Ouvrir l'éditeur
  - Voir les stats
  - Paramètres
  - Déployer
  - Archiver

---

## 2. Éditeur de Projet (`/projects/{id}/editor`)

### Layout (3 colonnes)
```
┌──────────────────────────────────────────────────────────────┐
│ Portfolio - Editor                    [💾 Save] [🚀 Deploy]  │
├──────┬────────────────────────────────────────┬──────────────┤
│ 📁   │ index.html                             │ 🤖 IA        │
│ Files│ <html>                                 │              │
│      │   <head>                               │ Suggestions: │
│ src/ │     <title>Mon Portfolio</title>       │ • Ajouter    │
│ ├─📄 │   </head>                              │   dark mode  │
│ │ in │   <body>                               │ • Optimiser  │
│ ├─📁 │     <h1>Bienvenue</h1>                 │   images     │
│ │ cs │   </body>                              │              │
│ ├─📁 │ </html>                                │ [Demander]   │
│ │ js │                                        │              │
│ └─📁 │                                        │              │
│   as │                                        │              │
│      │                                        │              │
│ [+]  │ Terminal ▼                             │              │
│      │ $ npm run dev                          │              │
│      │ Server running on port 3000            │              │
└──────┴────────────────────────────────────────┴──────────────┘
```

### Colonne 1 : Explorateur de Fichiers
- Arborescence complète
- Icônes par type de fichier
- Contexte menu (clic droit) :
  - Nouveau fichier/dossier
  - Renommer
  - Supprimer
  - Copier/Coller
  - Télécharger
- Recherche de fichiers (Ctrl+P)
- Filtres (modifiés, non trackés)

### Colonne 2 : Éditeur
- Onglets pour plusieurs fichiers
- Coloration syntaxique
- Numéros de lignes
- Minimap
- Auto-complétion
- Linting en temps réel
- Rechercher/Remplacer (Ctrl+F)
- Multi-curseurs (Alt+Click)
- Formatage (Shift+Alt+F)
- Terminal intégré (en bas)

### Colonne 3 : Assistant IA
- Suggestions contextuelles
- Chat avec l'IA
- Actions rapides :
  - Expliquer le code sélectionné
  - Refactorer
  - Générer tests
  - Corriger bugs
  - Optimiser
  - Documenter

---

## 3. Vue Git (`/projects/{id}/git`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ Git - Portfolio                [Branch: main ▼]         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 📝 Changes (3)                                          │
│ ┌─────────────────────────────────────────────────────┐│
│ │ ☑ index.html          +12 -5                        ││
│ │ ☑ styles.css          +45 -0                        ││
│ │ ☐ script.js           +8 -2                         ││
│ └─────────────────────────────────────────────────────┘│
│                                                         │
│ 💬 Commit message:                                      │
│ ┌─────────────────────────────────────────────────────┐│
│ │ Ajout du dark mode et optimisation CSS              ││
│ └─────────────────────────────────────────────────────┘│
│ [🤖 Générer message] [Commit] [Commit & Push]          │
│                                                         │
│ 📜 History                                              │
│ ┌─────────────────────────────────────────────────────┐│
│ │ abc123 - Ajout page contact (il y a 2h)            ││
│ │ def456 - Fix responsive header (hier)              ││
│ │ ghi789 - Initial commit (il y a 3 jours)           ││
│ └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Fonctionnalités
- Liste des fichiers modifiés
- Diff visuel (avant/après)
- Staging (sélection des fichiers)
- Message de commit (manuel ou généré par IA)
- Historique des commits
- Gestion des branches
- Pull/Push
- Résolution de conflits

---

## 4. Déploiement (`/projects/{id}/deploy`)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│ Déploiement - Portfolio                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🌍 Environnements                                       │
│ ┌─────────────────────────────────────────────────────┐│
│ │ 🟢 Production                                        ││
│ │ URL: https://portfolio.com                          ││
│ │ Dernier déploiement: il y a 2h                      ││
│ │ [Voir] [Redéployer] [Rollback]                      ││
│ ├─────────────────────────────────────────────────────┤│
│ │ 🟡 Staging                                           ││
│ │ URL: https://staging.portfolio.com                  ││
│ │ [Déployer]                                          ││
│ └─────────────────────────────────────────────────────┘│
│                                                         │
│ 📊 Historique des déploiements                          │
│ ┌─────────────────────────────────────────────────────┐│
│ │ ✅ #42 - Production (il y a 2h) - 1m 23s           ││
│ │ ✅ #41 - Staging (il y a 5h) - 58s                 ││
│ │ ❌ #40 - Production (hier) - Failed                 ││
│ └─────────────────────────────────────────────────────┘│
│                                                         │
│ ⚙️ Configuration                                        │
│ Provider: [Vercel ▼]                                    │
│ Auto-deploy: [✓] Activer                               │
│ Branch: [main ▼]                                        │
└─────────────────────────────────────────────────────────┘
```

---

# 🔌 API ENDPOINTS

## Projets

```python
# Liste des projets
GET /api/projects
Response: {
    "projects": [
        {
            "id": 1,
            "name": "Portfolio",
            "slug": "portfolio",
            "type": "nextjs",
            "status": "active",
            "prod_url": "https://portfolio.com",
            "updated_at": "2025-11-22T15:30:00Z"
        }
    ]
}

# Créer un projet
POST /api/projects
Body: {
    "name": "Mon Site",
    "type": "react",
    "template_id": 5  # optionnel
}
Response: {
    "project": {...},
    "message": "Projet créé avec succès"
}

# Détails d'un projet
GET /api/projects/{id}
Response: {
    "project": {...},
    "stats": {
        "total_files": 45,
        "total_lines": 2340,
        "last_commit": "abc123"
    }
}

# Mettre à jour un projet
PUT /api/projects/{id}
Body: {
    "name": "Nouveau nom",
    "description": "..."
}

# Supprimer un projet
DELETE /api/projects/{id}
```

## Fichiers

```python
# Liste des fichiers
GET /api/projects/{id}/files
Response: {
    "files": [
        {
            "path": "src/index.html",
            "name": "index.html",
            "size": 1024,
            "updated_at": "..."
        }
    ]
}

# Contenu d'un fichier
GET /api/projects/{id}/files/{path}
Response: {
    "content": "<html>...</html>",
    "encoding": "utf-8"
}

# Créer/Modifier un fichier
PUT /api/projects/{id}/files/{path}
Body: {
    "content": "...",
    "message": "Update header"  # optionnel pour commit
}

# Supprimer un fichier
DELETE /api/projects/{id}/files/{path}
```

## Git

```python
# Statut Git
GET /api/projects/{id}/git/status
Response: {
    "branch": "main",
    "modified": ["index.html", "styles.css"],
    "untracked": ["new-file.js"],
    "ahead": 2,
    "behind": 0
}

# Commit
POST /api/projects/{id}/git/commit
Body: {
    "message": "Add dark mode",
    "files": ["index.html", "styles.css"]
}

# Push
POST /api/projects/{id}/git/push

# Pull
POST /api/projects/{id}/git/pull

# Branches
GET /api/projects/{id}/git/branches
POST /api/projects/{id}/git/branches
Body: {
    "name": "feature/new-page",
    "from": "main"
}

# Historique
GET /api/projects/{id}/git/commits?limit=20
```

## Déploiement

```python
# Déployer
POST /api/projects/{id}/deploy
Body: {
    "environment": "production",  # ou staging, dev
    "branch": "main"
}
Response: {
    "deployment_id": "dep_123",
    "status": "building",
    "url": "https://..."
}

# Statut déploiement
GET /api/projects/{id}/deployments/{deployment_id}

# Historique
GET /api/projects/{id}/deployments?limit=10

# Rollback
POST /api/projects/{id}/deployments/{deployment_id}/rollback
```

## Actions IA

```python
# Demander à l'IA
POST /api/projects/{id}/ai/ask
Body: {
    "prompt": "Ajoute une page Contact avec formulaire",
    "context": {
        "current_file": "src/index.html",
        "selected_code": "..."
    }
}
Response: {
    "plan": {
        "steps": [
            "Créer contact.html",
            "Ajouter formulaire avec validation",
            "Créer contact.css",
            "Ajouter lien dans navigation"
        ],
        "files_to_create": ["contact.html", "contact.css"],
        "files_to_modify": ["index.html"]
    },
    "requires_confirmation": true
}

# Exécuter le plan IA
POST /api/projects/{id}/ai/execute
Body: {
    "plan_id": "plan_123",
    "confirmed": true
}
```

---

# 🛠️ TECHNOLOGIES

## Backend
- **FastAPI** (API REST)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (base de données)
- **GitPython** (gestion Git)
- **Paramiko** (SSH pour VPS)

## Frontend
- **Monaco Editor** (éditeur de code, même que VS Code)
- **Xterm.js** (terminal)
- **React** ou **Vue.js** (interface)
- **TailwindCSS** (styles)

## IA
- **OpenAI GPT-4** (génération de code)
- **Claude** (refactoring)
- **Codex** (auto-complétion)

## Déploiement
- **Vercel SDK**
- **Netlify API**
- **Paramiko** (SSH pour VPS)
- **AWS SDK** (S3, EC2, Lambda)

---

# 📋 CHECKLIST PHASE 1

## Semaine 1-2 : Setup
- [ ] Créer les modèles de données
- [ ] Migrations base de données
- [ ] Routes API de base (CRUD projets)
- [ ] Interface liste projets

## Semaine 3-4 : Import/Création
- [ ] Import depuis Git
- [ ] Import depuis ZIP
- [ ] Création from scratch
- [ ] Templates de base (5 templates)

## Semaine 5-6 : Éditeur
- [ ] Intégration Monaco Editor
- [ ] Vue fichiers/dossiers
- [ ] Lecture/écriture fichiers
- [ ] Recherche dans fichiers

## Semaine 7-8 : Terminal
- [ ] Intégration Xterm.js
- [ ] Exécution commandes
- [ ] Logs en temps réel

## Semaine 9-10 : Git
- [ ] Statut Git
- [ ] Diff visuel
- [ ] Commits
- [ ] Push/Pull
- [ ] Branches

## Semaine 11-12 : Déploiement
- [ ] Intégration Vercel
- [ ] Intégration Netlify
- [ ] Déploiement manuel
- [ ] Historique déploiements

## Semaine 13-14 : IA
- [ ] Chat IA dans l'éditeur
- [ ] Suggestions contextuelles
- [ ] Génération de code
- [ ] Refactoring

## Semaine 15-16 : Polish
- [ ] Tests
- [ ] Optimisations
- [ ] Documentation
- [ ] Déploiement

---

**Prêt à commencer le développement ? 🚀**
