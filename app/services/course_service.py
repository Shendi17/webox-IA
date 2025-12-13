"""
Service de gestion des cours LMS
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import re

from app.models.lms_db import Course, Module, Lesson, Quiz, Enrollment, Progress


class CourseService:
    """Service pour gérer les cours"""
    
    @staticmethod
    def create_slug(title: str) -> str:
        """Créer un slug à partir du titre"""
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    @staticmethod
    def create_course(db: Session, course_data: Dict, author_id: int) -> Dict:
        """
        Créer un nouveau cours
        
        Args:
            db: Session de base de données
            course_data: Données du cours
            author_id: ID de l'auteur
        
        Returns:
            Dict avec success et course
        """
        try:
            # Créer le slug
            slug = CourseService.create_slug(course_data["title"])
            
            # Vérifier si le slug existe déjà
            existing = db.query(Course).filter(Course.slug == slug).first()
            if existing:
                slug = f"{slug}-{datetime.now().timestamp()}"
            
            # Créer le cours
            course = Course(
                title=course_data["title"],
                slug=slug,
                description=course_data.get("description"),
                short_description=course_data.get("short_description"),
                category=course_data.get("category"),
                level=course_data.get("level", "beginner"),
                price=course_data.get("price", 0.0),
                is_free=course_data.get("is_free", True),
                language=course_data.get("language", "fr"),
                author_id=author_id,
                author_name=course_data.get("author_name")
            )
            
            db.add(course)
            db.commit()
            db.refresh(course)
            
            return {
                "success": True,
                "course": course.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de création: {str(e)}"
            }
    
    @staticmethod
    def get_course(db: Session, course_id: int) -> Optional[Course]:
        """Récupérer un cours par ID"""
        return db.query(Course).filter(Course.id == course_id).first()
    
    @staticmethod
    def get_course_by_slug(db: Session, slug: str) -> Optional[Course]:
        """Récupérer un cours par slug"""
        return db.query(Course).filter(Course.slug == slug).first()
    
    @staticmethod
    def list_courses(
        db: Session,
        author_id: Optional[int] = None,
        category: Optional[str] = None,
        is_published: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Course]:
        """
        Lister les cours avec filtres
        
        Args:
            db: Session de base de données
            author_id: Filtrer par auteur
            category: Filtrer par catégorie
            is_published: Filtrer par statut de publication
            limit: Nombre maximum de résultats
            offset: Décalage pour la pagination
        
        Returns:
            Liste de cours
        """
        query = db.query(Course)
        
        if author_id is not None:
            query = query.filter(Course.author_id == author_id)
        
        if category is not None:
            query = query.filter(Course.category == category)
        
        if is_published is not None:
            query = query.filter(Course.is_published == is_published)
        
        query = query.order_by(Course.created_at.desc())
        query = query.limit(limit).offset(offset)
        
        return query.all()
    
    @staticmethod
    def update_course(db: Session, course_id: int, update_data: Dict) -> Dict:
        """
        Mettre à jour un cours
        
        Args:
            db: Session de base de données
            course_id: ID du cours
            update_data: Données à mettre à jour
        
        Returns:
            Dict avec success et course
        """
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            
            if not course:
                return {
                    "success": False,
                    "error": "Cours non trouvé"
                }
            
            # Mettre à jour les champs
            for key, value in update_data.items():
                if hasattr(course, key) and key not in ["id", "slug", "created_at"]:
                    setattr(course, key, value)
            
            course.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(course)
            
            return {
                "success": True,
                "course": course.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de mise à jour: {str(e)}"
            }
    
    @staticmethod
    def delete_course(db: Session, course_id: int) -> Dict:
        """
        Supprimer un cours
        
        Args:
            db: Session de base de données
            course_id: ID du cours
        
        Returns:
            Dict avec success
        """
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            
            if not course:
                return {
                    "success": False,
                    "error": "Cours non trouvé"
                }
            
            db.delete(course)
            db.commit()
            
            return {
                "success": True,
                "message": "Cours supprimé"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de suppression: {str(e)}"
            }
    
    @staticmethod
    def publish_course(db: Session, course_id: int) -> Dict:
        """
        Publier un cours
        
        Args:
            db: Session de base de données
            course_id: ID du cours
        
        Returns:
            Dict avec success
        """
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            
            if not course:
                return {
                    "success": False,
                    "error": "Cours non trouvé"
                }
            
            course.is_published = True
            course.published_at = datetime.utcnow()
            
            db.commit()
            
            return {
                "success": True,
                "message": "Cours publié"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de publication: {str(e)}"
            }
    
    @staticmethod
    def get_course_stats(db: Session, course_id: int) -> Dict:
        """
        Obtenir les statistiques d'un cours
        
        Args:
            db: Session de base de données
            course_id: ID du cours
        
        Returns:
            Dict avec les statistiques
        """
        try:
            course = db.query(Course).filter(Course.id == course_id).first()
            
            if not course:
                return {
                    "success": False,
                    "error": "Cours non trouvé"
                }
            
            # Compter les modules
            total_modules = db.query(func.count(Module.id)).filter(
                Module.course_id == course_id
            ).scalar()
            
            # Compter les leçons
            total_lessons = db.query(func.count(Lesson.id)).join(Module).filter(
                Module.course_id == course_id
            ).scalar()
            
            # Compter les étudiants
            total_students = db.query(func.count(Enrollment.id)).filter(
                Enrollment.course_id == course_id
            ).scalar()
            
            # Calculer la durée totale
            total_duration = db.query(func.sum(Lesson.duration)).join(Module).filter(
                Module.course_id == course_id
            ).scalar() or 0
            
            return {
                "success": True,
                "stats": {
                    "total_modules": total_modules,
                    "total_lessons": total_lessons,
                    "total_students": total_students,
                    "total_duration": total_duration
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de statistiques: {str(e)}"
            }
