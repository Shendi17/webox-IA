"""
Modèles SQLAlchemy pour la Génération Multi-Média
Date : 10 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
from app.database import Base


class GeneratedImageDB(Base):
    """
    Modèle pour les images générées
    Table: generated_images
    """
    __tablename__ = "generated_images"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Paramètres de génération
    prompt = Column(Text, nullable=False)
    negative_prompt = Column(Text, nullable=True)
    model = Column(String(50), nullable=False)  # dall-e-3, midjourney, stable-diffusion
    size = Column(String(20), nullable=True)  # 1024x1024, 1792x1024, etc.
    style = Column(String(50), nullable=True)  # natural, vivid, artistic
    quality = Column(String(20), nullable=True)  # standard, hd
    
    # Résultat
    image_url = Column(String(500), nullable=True)
    local_path = Column(String(500), nullable=True)
    
    # Métadonnées
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)  # en bytes
    
    # Coût et statut
    cost = Column(Float, nullable=True)  # Coût en USD
    status = Column(String(50), default='generating')  # generating, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<GeneratedImage(id={self.id}, model='{self.model}', status='{self.status}')>"
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "prompt": self.prompt,
            "model": self.model,
            "size": self.size,
            "style": self.style,
            "image_url": self.image_url,
            "width": self.width,
            "height": self.height,
            "cost": self.cost,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class GeneratedVideoDB(Base):
    """
    Modèle pour les vidéos générées
    Table: generated_videos
    """
    __tablename__ = "generated_videos"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Paramètres de génération
    prompt = Column(Text, nullable=False)
    model = Column(String(50), nullable=False)  # runway, pika, luma
    duration = Column(Integer, nullable=True)  # en secondes
    resolution = Column(String(20), nullable=True)  # 1080p, 4k, etc.
    fps = Column(Integer, nullable=True)  # frames per second
    
    # Résultat
    video_url = Column(String(500), nullable=True)
    local_path = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    
    # Métadonnées
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)  # en bytes
    actual_duration = Column(Float, nullable=True)  # durée réelle en secondes
    
    # Coût et statut
    cost = Column(Float, nullable=True)
    status = Column(String(50), default='generating')
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<GeneratedVideo(id={self.id}, model='{self.model}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "prompt": self.prompt,
            "model": self.model,
            "duration": self.duration,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "cost": self.cost,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class GeneratedAudioDB(Base):
    """
    Modèle pour l'audio généré
    Table: generated_audio
    """
    __tablename__ = "generated_audio"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Paramètres de génération
    prompt = Column(Text, nullable=False)
    model = Column(String(50), nullable=False)  # suno, udio, elevenlabs
    audio_type = Column(String(50), nullable=True)  # music, speech, sound_effect
    voice_id = Column(String(100), nullable=True)  # Pour TTS
    language = Column(String(10), nullable=True)
    duration = Column(Integer, nullable=True)  # en secondes
    
    # Résultat
    audio_url = Column(String(500), nullable=True)
    local_path = Column(String(500), nullable=True)
    
    # Métadonnées
    file_size = Column(Integer, nullable=True)
    actual_duration = Column(Float, nullable=True)
    format = Column(String(20), nullable=True)  # mp3, wav, etc.
    
    # Coût et statut
    cost = Column(Float, nullable=True)
    status = Column(String(50), default='generating')
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<GeneratedAudio(id={self.id}, model='{self.model}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "prompt": self.prompt,
            "model": self.model,
            "audio_type": self.audio_type,
            "duration": self.duration,
            "audio_url": self.audio_url,
            "cost": self.cost,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class EBookDB(Base):
    """
    Modèle pour les eBooks générés
    Table: ebooks
    """
    __tablename__ = "ebooks"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Paramètres de génération
    title = Column(String(255), nullable=False)
    subject = Column(Text, nullable=False)
    chapters = Column(Integer, nullable=False)
    tone = Column(String(50), nullable=True)  # professionnel, decontracte, etc.
    audience = Column(String(50), nullable=True)  # debutants, experts, etc.
    language = Column(String(10), nullable=True)
    
    # Options
    has_cover = Column(Boolean, default=True)
    has_toc = Column(Boolean, default=True)  # Table of contents
    has_illustrations = Column(Boolean, default=False)
    has_summaries = Column(Boolean, default=True)
    
    # Résultat
    cover_url = Column(String(500), nullable=True)
    pdf_url = Column(String(500), nullable=True)
    epub_url = Column(String(500), nullable=True)
    mobi_url = Column(String(500), nullable=True)
    
    # Métadonnées
    total_pages = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    
    # Contenu (JSON)
    table_of_contents = Column(JSON, nullable=True)  # Liste des chapitres
    
    # Coût et statut
    cost = Column(Float, nullable=True)
    status = Column(String(50), default='generating')  # generating, completed, failed
    progress = Column(Integer, default=0)  # 0-100%
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<EBook(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "subject": self.subject,
            "chapters": self.chapters,
            "tone": self.tone,
            "audience": self.audience,
            "cover_url": self.cover_url,
            "pdf_url": self.pdf_url,
            "epub_url": self.epub_url,
            "total_pages": self.total_pages,
            "word_count": self.word_count,
            "cost": self.cost,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class VideoShortDB(Base):
    """
    Modèle pour les vidéos short générées
    Table: video_shorts
    """
    __tablename__ = "video_shorts"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Paramètres de génération
    subject = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)  # 15, 30, 60, 90 secondes
    format = Column(String(20), nullable=False)  # 9:16, 1:1, 16:9
    style = Column(String(50), nullable=True)  # moderne, minimaliste, etc.
    voice = Column(String(50), nullable=True)  # femme-fr, homme-en, etc.
    
    # Options
    has_music = Column(Boolean, default=True)
    has_subtitles = Column(Boolean, default=True)
    has_logo = Column(Boolean, default=False)
    has_hook = Column(Boolean, default=True)
    has_cta = Column(Boolean, default=True)
    
    # Résultat
    video_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    script = Column(Text, nullable=True)  # Script généré
    
    # Métadonnées
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    actual_duration = Column(Float, nullable=True)
    
    # Assets utilisés (JSON)
    visuals = Column(JSON, nullable=True)  # URLs des visuels générés
    audio_url = Column(String(500), nullable=True)  # Voix-off
    music_url = Column(String(500), nullable=True)
    
    # Coût et statut
    cost = Column(Float, nullable=True)
    status = Column(String(50), default='generating')
    progress = Column(Integer, default=0)  # 0-100%
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<VideoShort(id={self.id}, subject='{self.subject[:30]}...', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subject": self.subject,
            "duration": self.duration,
            "format": self.format,
            "style": self.style,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "script": self.script,
            "cost": self.cost,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class WorkflowDB(Base):
    """
    Modèle pour les workflows de combinaisons IA
    Table: workflows
    """
    __tablename__ = "workflows"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Informations du workflow
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)  # content, video, marketing, etc.
    
    # Configuration (JSON)
    steps = Column(JSON, nullable=False)  # Liste des étapes du workflow
    # Format: [{"ai": "gpt-4", "prompt": "...", "params": {...}}, ...]
    
    # Métadonnées
    is_template = Column(Boolean, default=False)  # Template prédéfini ou custom
    is_public = Column(Boolean, default=False)
    times_used = Column(Integer, default=0)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "steps": self.steps,
            "is_template": self.is_template,
            "is_public": self.is_public,
            "times_used": self.times_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None
        }


class WorkflowExecutionDB(Base):
    """
    Modèle pour les exécutions de workflows
    Table: workflow_executions
    """
    __tablename__ = "workflow_executions"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Inputs
    input_data = Column(JSON, nullable=True)  # Variables d'entrée
    
    # Résultats (JSON)
    results = Column(JSON, nullable=True)  # Résultats de chaque étape
    # Format: [{"step": 1, "ai": "gpt-4", "output": "...", "cost": 0.05}, ...]
    
    # Métadonnées
    total_cost = Column(Float, nullable=True)
    total_duration = Column(Float, nullable=True)  # en secondes
    
    # Statut
    status = Column(String(50), default='running')  # running, completed, failed
    current_step = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<WorkflowExecution(id={self.id}, workflow_id={self.workflow_id}, status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "user_id": self.user_id,
            "input_data": self.input_data,
            "results": self.results,
            "total_cost": self.total_cost,
            "total_duration": self.total_duration,
            "status": self.status,
            "current_step": self.current_step,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class CatalogFavoriteDB(Base):
    """
    Modèle pour les favoris du catalogue IA
    Table: catalog_favorites
    """
    __tablename__ = "catalog_favorites"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    tool_id = Column(String(100), nullable=False)  # ID de l'outil IA
    tool_name = Column(String(255), nullable=True)
    tool_category = Column(String(50), nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CatalogFavorite(user_id={self.user_id}, tool_id='{self.tool_id}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "tool_category": self.tool_category,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class GeneratedAdDB(Base):
    """
    Modèle pour les publicités vidéo générées
    Table: generated_ads
    """
    __tablename__ = "generated_ads"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    user_email = Column(String(255), nullable=True)
    
    # Informations produit
    product_name = Column(String(255), nullable=False)
    product_description = Column(Text, nullable=False)
    product_image_url = Column(String(500), nullable=False)
    
    # Paramètres de génération
    ad_type = Column(String(50), nullable=False)  # product-showcase, lifestyle, testimonial, promo, comparison
    duration = Column(Integer, nullable=False)  # 15, 30, 60 secondes
    style = Column(String(50), nullable=False)  # modern, elegant, dynamic, minimal, luxury
    voice = Column(String(50), nullable=False)  # professional-male, professional-female, etc.
    cta = Column(String(255), nullable=True)  # Call-to-action
    options = Column(JSON, nullable=True)  # Options supplémentaires (music, effects, etc.)
    
    # Résultats
    script = Column(Text, nullable=True)  # Script généré
    audio_url = Column(String(500), nullable=True)  # Voix-off
    video_url = Column(String(500), nullable=True)  # Vidéo finale
    local_path = Column(String(500), nullable=True)
    
    # Métadonnées
    file_size = Column(Integer, nullable=True)  # en bytes
    
    # Coût et statut
    cost = Column(Float, nullable=True)  # Coût en USD
    status = Column(String(50), default='generating')  # generating, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<GeneratedAd(id={self.id}, product='{self.product_name}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "product_image_url": self.product_image_url,
            "ad_type": self.ad_type,
            "duration": self.duration,
            "style": self.style,
            "voice": self.voice,
            "cta": self.cta,
            "options": self.options,
            "script": self.script,
            "audio_url": self.audio_url,
            "video_url": self.video_url,
            "local_path": self.local_path,
            "file_size": self.file_size,
            "cost": self.cost,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
