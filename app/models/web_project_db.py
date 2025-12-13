"""
Modèles de base de données pour le Studio Web IA
Gestion complète de projets web avec Git, déploiement et IA
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class WebProject(Base):
    """
    Projet web complet géré par WeBox IA
    Supporte : Static, React, Vue, Next.js, Django, FastAPI, WordPress, etc.
    """
    __tablename__ = "web_projects"
    
    # Identité
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    cover_image = Column(String(500))  # URL de l'image de preview
    
    # Type & Stack
    project_type = Column(String(50))  # static, react, vue, nextjs, django, fastapi, wordpress
    framework = Column(String(50))
    framework_version = Column(String(20))
    languages = Column(JSON)  # ["python", "javascript", "html", "css"]
    dependencies = Column(JSON)  # package.json ou requirements.txt parsé
    
    # Stockage
    storage_type = Column(String(20), default="local")  # local, git
    local_path = Column(String(500))  # chemin absolu si local
    
    # Git
    git_provider = Column(String(20))  # github, gitlab, bitbucket
    git_repo_url = Column(String(500))
    git_branch = Column(String(100), default="main")
    git_token = Column(String(500))  # chiffré - TODO: utiliser encryption
    git_username = Column(String(200))
    git_email = Column(String(200))
    
    # Déploiement
    deployment_provider = Column(String(50))  # vercel, netlify, vps, aws, github_pages
    deployment_config = Column(JSON)  # config spécifique au provider
    prod_url = Column(String(500))
    staging_url = Column(String(500))
    dev_url = Column(String(500))
    auto_deploy = Column(Boolean, default=False)
    auto_deploy_branch = Column(String(100), default="main")
    
    # Environnement
    environment_vars = Column(JSON)  # variables d'environnement {key: value}
    build_command = Column(String(500))  # ex: "npm run build"
    start_command = Column(String(500))  # ex: "npm start"
    install_command = Column(String(500))  # ex: "npm install"
    output_directory = Column(String(200))  # ex: "dist", "build", "out"
    
    # Métadonnées
    owner_id = Column(Integer, nullable=False, index=True)  # ID de l'utilisateur propriétaire
    team_members = Column(JSON)  # [user_ids] pour collaboration future
    status = Column(String(20), default="active")  # active, archived, maintenance, deleted
    visibility = Column(String(20), default="private")  # private, public, team
    
    # Statistiques
    total_files = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    total_size = Column(Integer, default=0)  # en bytes
    last_build_at = Column(DateTime)
    last_deploy_at = Column(DateTime)
    last_commit_at = Column(DateTime)
    deploy_count = Column(Integer, default=0)
    
    # SEO & Analytics (optionnel)
    domain_custom = Column(String(200))  # domaine personnalisé
    analytics_enabled = Column(Boolean, default=False)
    seo_title = Column(String(200))
    seo_description = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    archived_at = Column(DateTime)
    
    # Relations
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")
    deployments = relationship("Deployment", back_populates="project", cascade="all, delete-orphan")
    commits = relationship("ProjectCommit", back_populates="project", cascade="all, delete-orphan")
    ai_actions = relationship("ProjectAIAction", back_populates="project", cascade="all, delete-orphan")


class ProjectFile(Base):
    """
    Fichier d'un projet web
    Stocke le contenu et les métadonnées de chaque fichier
    """
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"), nullable=False, index=True)
    
    # Chemin
    path = Column(String(1000), nullable=False)  # chemin relatif depuis la racine (ex: "src/index.html")
    name = Column(String(255), nullable=False)
    extension = Column(String(20))
    directory = Column(String(1000))  # dossier parent
    
    # Contenu
    content = Column(Text)  # contenu du fichier (NULL si binaire)
    content_hash = Column(String(64))  # SHA256 pour détecter les changements
    size = Column(Integer)  # taille en bytes
    lines = Column(Integer)  # nombre de lignes (si texte)
    
    # Métadonnées
    is_binary = Column(Boolean, default=False)
    is_directory = Column(Boolean, default=False)
    mime_type = Column(String(100))
    encoding = Column(String(20), default="utf-8")
    language = Column(String(50))  # python, javascript, html, css, etc.
    
    # Git
    git_status = Column(String(20))  # untracked, modified, staged, committed
    last_commit_hash = Column(String(40))
    last_commit_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_accessed_at = Column(DateTime)
    
    # Relations
    project = relationship("WebProject", back_populates="files")


class Deployment(Base):
    """
    Déploiement d'un projet web
    Historique de tous les déploiements (dev, staging, prod)
    """
    __tablename__ = "deployments"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"), nullable=False, index=True)
    
    # Déploiement
    environment = Column(String(20), nullable=False)  # dev, staging, prod
    provider = Column(String(50), nullable=False)  # vercel, netlify, vps, etc.
    deployment_id = Column(String(200))  # ID chez le provider
    deployment_url = Column(String(500))
    
    # Build
    commit_hash = Column(String(40))
    commit_message = Column(Text)
    branch = Column(String(100))
    build_status = Column(String(20), default="pending")  # pending, building, success, failed, cancelled
    build_logs = Column(Text)  # logs du build
    build_duration = Column(Integer)  # durée en secondes
    build_error = Column(Text)  # message d'erreur si échec
    
    # Métadonnées
    triggered_by = Column(String(20))  # manual, auto, webhook, voice
    user_id = Column(Integer, index=True)
    is_rollback = Column(Boolean, default=False)
    rollback_from_id = Column(Integer)  # si c'est un rollback (ID du déploiement)
    
    # Configuration
    environment_vars = Column(JSON)  # variables d'env utilisées
    build_command = Column(String(500))
    
    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    project = relationship("WebProject", back_populates="deployments")


class ProjectCommit(Base):
    """
    Commit Git d'un projet
    Historique de tous les commits
    """
    __tablename__ = "project_commits"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"), nullable=False, index=True)
    
    # Git
    commit_hash = Column(String(40), unique=True, nullable=False, index=True)
    branch = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    author_name = Column(String(200))
    author_email = Column(String(200))
    
    # Changements
    files_changed = Column(Integer, default=0)
    insertions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    changed_files = Column(JSON)  # liste des fichiers modifiés avec stats
    
    # Métadonnées
    is_merge = Column(Boolean, default=False)
    is_ai_generated = Column(Boolean, default=False)  # commit généré par l'IA
    parent_hashes = Column(JSON)  # commits parents
    tags = Column(JSON)  # tags Git associés
    
    # Timestamps
    committed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    project = relationship("WebProject", back_populates="commits")


class ProjectAIAction(Base):
    """
    Action IA effectuée sur un projet
    Historique de toutes les modifications par IA
    """
    __tablename__ = "project_ai_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("web_projects.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Action
    action_type = Column(String(50), nullable=False)  # create_file, modify_file, refactor, add_feature, etc.
    prompt = Column(Text, nullable=False)  # demande de l'utilisateur
    context = Column(JSON)  # contexte (fichier actif, code sélectionné, etc.)
    
    # Plan d'exécution
    plan = Column(JSON)  # plan généré par l'IA
    plan_approved = Column(Boolean, default=False)
    
    # Résultat
    status = Column(String(20), default="pending")  # pending, executing, completed, failed, cancelled
    result = Column(JSON)  # résultat de l'action
    files_created = Column(JSON)  # fichiers créés
    files_modified = Column(JSON)  # fichiers modifiés
    files_deleted = Column(JSON)  # fichiers supprimés
    commit_hash = Column(String(40))  # commit créé par cette action
    
    # Métadonnées
    ai_model = Column(String(50))  # gpt-4, claude, etc.
    tokens_used = Column(Integer)
    execution_time = Column(Integer)  # en secondes
    error_message = Column(Text)
    
    # Feedback
    user_rating = Column(Integer)  # 1-5 étoiles
    user_feedback = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relations
    project = relationship("WebProject", back_populates="ai_actions")


class ProjectTemplate(Base):
    """
    Template de projet web
    Templates prédéfinis pour démarrer rapidement
    """
    __tablename__ = "project_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identité
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    cover_image = Column(String(500))
    preview_url = Column(String(500))  # URL de démo
    
    # Catégorie
    category = Column(String(50))  # landing, portfolio, blog, ecommerce, saas, etc.
    tags = Column(JSON)  # ["responsive", "dark-mode", "animations"]
    
    # Stack
    project_type = Column(String(50))
    framework = Column(String(50))
    languages = Column(JSON)
    features = Column(JSON)  # ["auth", "payment", "blog", "admin"]
    
    # Contenu
    git_repo_url = Column(String(500))  # repo du template
    zip_url = Column(String(500))  # ou ZIP téléchargeable
    files_structure = Column(JSON)  # structure des fichiers
    
    # Métadonnées
    author_id = Column(Integer, index=True)  # ID de l'auteur du template
    is_official = Column(Boolean, default=False)  # template officiel WeBox
    is_premium = Column(Boolean, default=False)
    price = Column(Integer, default=0)  # en centimes
    
    # Statistiques
    usage_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)  # moyenne * 100
    reviews_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published_at = Column(DateTime)
