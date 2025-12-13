"""
Routes API pour le système LMS
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user
from app.services.course_service import CourseService
from app.services.course_generator_service import CourseGeneratorService
from app.models.lms_db import Course, Module, Lesson, Enrollment

router = APIRouter(prefix="/api/lms", tags=["LMS"])


# ==================== SCHEMAS ====================

class CourseCreate(BaseModel):
    """Schéma pour créer un cours"""
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: Optional[str] = None
    level: str = "beginner"
    price: float = 0.0
    is_free: bool = True
    language: str = "fr"


class CourseUpdate(BaseModel):
    """Schéma pour mettre à jour un cours"""
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    price: Optional[float] = None
    is_free: Optional[bool] = None
    is_published: Optional[bool] = None


class CourseGenerate(BaseModel):
    """Schéma pour générer un cours avec IA"""
    title: str
    description: str
    num_modules: int = 5
    generate_content: bool = True
    generate_quizzes: bool = True


class EnrollmentCreate(BaseModel):
    """Schéma pour inscrire un étudiant"""
    course_id: int


# ==================== ROUTES COURS ====================

@router.post("/courses")
async def create_course(
    data: CourseCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Créer un nouveau cours
    
    Args:
        data: Données du cours
    
    Returns:
        Cours créé
    """
    try:
        course_data = data.dict()
        course_data["author_name"] = current_user.name
        
        result = CourseService.create_course(db, course_data, current_user.id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/courses")
async def list_courses(
    category: Optional[str] = None,
    is_published: Optional[bool] = None,
    my_courses: bool = False,
    limit: int = 50,
    offset: int = 0,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lister les cours
    
    Args:
        category: Filtrer par catégorie
        is_published: Filtrer par statut de publication
        my_courses: Afficher uniquement mes cours
        limit: Nombre maximum de résultats
        offset: Décalage pour la pagination
    
    Returns:
        Liste de cours
    """
    try:
        author_id = current_user.id if my_courses else None
        
        courses = CourseService.list_courses(
            db,
            author_id=author_id,
            category=category,
            is_published=is_published,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "courses": [course.to_dict() for course in courses],
            "total": len(courses)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/courses/{course_id}")
async def get_course(
    course_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtenir les détails d'un cours
    
    Args:
        course_id: ID du cours
    
    Returns:
        Détails du cours avec modules et leçons
    """
    try:
        course = CourseService.get_course(db, course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Cours non trouvé")
        
        # Récupérer les modules avec leçons
        modules = db.query(Module).filter(Module.course_id == course_id).order_by(Module.order).all()
        
        modules_data = []
        for module in modules:
            lessons = db.query(Lesson).filter(Lesson.module_id == module.id).order_by(Lesson.order).all()
            
            module_dict = module.to_dict()
            module_dict["lessons"] = [lesson.to_dict() for lesson in lessons]
            modules_data.append(module_dict)
        
        course_dict = course.to_dict()
        course_dict["modules"] = modules_data
        
        return {
            "success": True,
            "course": course_dict
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/courses/{course_id}")
async def update_course(
    course_id: int,
    data: CourseUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un cours
    
    Args:
        course_id: ID du cours
        data: Données à mettre à jour
    
    Returns:
        Cours mis à jour
    """
    try:
        # Vérifier que l'utilisateur est l'auteur
        course = CourseService.get_course(db, course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Cours non trouvé")
        
        if course.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Non autorisé")
        
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        
        result = CourseService.update_course(db, course_id, update_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/courses/{course_id}")
async def delete_course(
    course_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprimer un cours
    
    Args:
        course_id: ID du cours
    
    Returns:
        Message de confirmation
    """
    try:
        # Vérifier que l'utilisateur est l'auteur
        course = CourseService.get_course(db, course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Cours non trouvé")
        
        if course.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Non autorisé")
        
        result = CourseService.delete_course(db, course_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/courses/{course_id}/publish")
async def publish_course(
    course_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Publier un cours
    
    Args:
        course_id: ID du cours
    
    Returns:
        Message de confirmation
    """
    try:
        # Vérifier que l'utilisateur est l'auteur
        course = CourseService.get_course(db, course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Cours non trouvé")
        
        if course.author_id != current_user.id:
            raise HTTPException(status_code=403, detail="Non autorisé")
        
        result = CourseService.publish_course(db, course_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/courses/{course_id}/stats")
async def get_course_stats(
    course_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtenir les statistiques d'un cours
    
    Args:
        course_id: ID du cours
    
    Returns:
        Statistiques du cours
    """
    try:
        result = CourseService.get_course_stats(db, course_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ROUTES GÉNÉRATION IA ====================

@router.post("/courses/generate")
async def generate_course(
    data: CourseGenerate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Générer un cours complet avec IA
    
    Args:
        data: Données de génération
    
    Returns:
        Cours généré
    """
    try:
        generator = CourseGeneratorService()
        
        result = generator.create_complete_course(
            db,
            title=data.title,
            description=data.description,
            author_id=current_user.id,
            num_modules=data.num_modules,
            generate_content=data.generate_content,
            generate_quizzes=data.generate_quizzes
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ROUTES INSCRIPTION ====================

@router.post("/enroll")
async def enroll_course(
    data: EnrollmentCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    S'inscrire à un cours
    
    Args:
        data: Données d'inscription
    
    Returns:
        Inscription créée
    """
    try:
        # Vérifier si déjà inscrit
        existing = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == data.course_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Déjà inscrit à ce cours")
        
        # Créer l'inscription
        enrollment = Enrollment(
            user_id=current_user.id,
            course_id=data.course_id
        )
        
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        
        # Mettre à jour le nombre d'étudiants
        course = db.query(Course).filter(Course.id == data.course_id).first()
        if course:
            course.total_students += 1
            db.commit()
        
        return {
            "success": True,
            "enrollment": enrollment.to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-courses")
async def get_my_enrolled_courses(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtenir les cours auxquels je suis inscrit
    
    Returns:
        Liste de cours
    """
    try:
        enrollments = db.query(Enrollment).filter(
            Enrollment.user_id == current_user.id
        ).all()
        
        courses = []
        for enrollment in enrollments:
            course = db.query(Course).filter(Course.id == enrollment.course_id).first()
            if course:
                course_dict = course.to_dict()
                course_dict["enrollment"] = enrollment.to_dict()
                courses.append(course_dict)
        
        return {
            "success": True,
            "courses": courses
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
