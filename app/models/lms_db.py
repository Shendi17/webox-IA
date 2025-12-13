"""
Modèles SQLAlchemy pour le système LMS (Learning Management System)
Date : 23 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Course(Base):
    """
    Modèle pour les formations/cours
    Table: courses
    """
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations de base
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    
    # Contenu
    thumbnail = Column(String(500), nullable=True)
    trailer_url = Column(String(500), nullable=True)
    
    # Catégorie et tags
    category = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)  # Liste de tags
    
    # Niveau et durée
    level = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    estimated_duration = Column(Integer, default=0)  # En minutes
    
    # Prix et monétisation
    price = Column(Float, default=0.0)
    currency = Column(String(10), default="EUR")
    is_free = Column(Boolean, default=True)
    
    # Statut
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Statistiques
    total_students = Column(Integer, default=0)
    total_modules = Column(Integer, default=0)
    total_lessons = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Métadonnées
    language = Column(String(10), default="fr")
    requirements = Column(JSON, nullable=True)  # Liste de prérequis
    what_you_learn = Column(JSON, nullable=True)  # Liste d'objectifs
    
    # Auteur
    author_id = Column(Integer, nullable=False)
    author_name = Column(String(255), nullable=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    
    # Relations
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "short_description": self.short_description,
            "thumbnail": self.thumbnail,
            "category": self.category,
            "tags": self.tags,
            "level": self.level,
            "estimated_duration": self.estimated_duration,
            "price": self.price,
            "currency": self.currency,
            "is_free": self.is_free,
            "is_published": self.is_published,
            "is_featured": self.is_featured,
            "total_students": self.total_students,
            "total_modules": self.total_modules,
            "total_lessons": self.total_lessons,
            "average_rating": self.average_rating,
            "language": self.language,
            "author_name": self.author_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None
        }


class Module(Base):
    """
    Modèle pour les modules d'une formation
    Table: modules
    """
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec le cours
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Informations
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    
    # Statistiques
    total_lessons = Column(Integer, default=0)
    estimated_duration = Column(Integer, default=0)  # En minutes
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Module(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "total_lessons": self.total_lessons,
            "estimated_duration": self.estimated_duration,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Lesson(Base):
    """
    Modèle pour les leçons d'un module
    Table: lessons
    """
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec le module
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    
    # Informations
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    
    # Contenu
    content_type = Column(String(50), default="text")  # text, video, quiz, file
    content = Column(Text, nullable=True)  # Contenu texte ou HTML
    video_url = Column(String(500), nullable=True)
    file_url = Column(String(500), nullable=True)
    
    # Durée
    duration = Column(Integer, default=0)  # En minutes
    
    # Options
    is_free_preview = Column(Boolean, default=False)
    is_downloadable = Column(Boolean, default=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    module = relationship("Module", back_populates="lessons")
    quiz = relationship("Quiz", back_populates="lesson", uselist=False, cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="lesson", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "module_id": self.module_id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "content_type": self.content_type,
            "content": self.content,
            "video_url": self.video_url,
            "duration": self.duration,
            "is_free_preview": self.is_free_preview,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Quiz(Base):
    """
    Modèle pour les quiz associés aux leçons
    Table: quizzes
    """
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec la leçon
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    # Informations
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Questions (stockées en JSON)
    questions = Column(JSON, nullable=False)
    # Format: [
    #   {
    #     "question": "Quelle est la capitale de la France ?",
    #     "type": "multiple_choice",
    #     "options": ["Paris", "Lyon", "Marseille"],
    #     "correct_answer": 0,
    #     "explanation": "Paris est la capitale..."
    #   }
    # ]
    
    # Configuration
    passing_score = Column(Integer, default=70)  # Pourcentage
    time_limit = Column(Integer, nullable=True)  # En minutes (null = illimité)
    max_attempts = Column(Integer, default=3)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    lesson = relationship("Lesson", back_populates="quiz")
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "lesson_id": self.lesson_id,
            "title": self.title,
            "description": self.description,
            "questions": self.questions,
            "passing_score": self.passing_score,
            "time_limit": self.time_limit,
            "max_attempts": self.max_attempts
        }


class Enrollment(Base):
    """
    Modèle pour les inscriptions des étudiants aux cours
    Table: enrollments
    """
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Liens
    user_id = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Statut
    status = Column(String(50), default="active")  # active, completed, suspended
    progress_percentage = Column(Float, default=0.0)
    
    # Dates
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, nullable=True)
    
    # Relations
    course = relationship("Course", back_populates="enrollments")
    
    def __repr__(self):
        return f"<Enrollment(id={self.id}, user_id={self.user_id}, course_id={self.course_id})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class Progress(Base):
    """
    Modèle pour suivre la progression des étudiants par leçon
    Table: progress
    """
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Liens
    user_id = Column(Integer, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    # Progression
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Float, default=0.0)
    
    # Quiz
    quiz_score = Column(Float, nullable=True)
    quiz_attempts = Column(Integer, default=0)
    quiz_passed = Column(Boolean, default=False)
    
    # Dates
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    lesson = relationship("Lesson", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress(id={self.id}, user_id={self.user_id}, lesson_id={self.lesson_id})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "lesson_id": self.lesson_id,
            "is_completed": self.is_completed,
            "completion_percentage": self.completion_percentage,
            "quiz_score": self.quiz_score,
            "quiz_passed": self.quiz_passed,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
