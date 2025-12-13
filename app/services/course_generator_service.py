"""
Service de génération de cours avec IA
"""
from typing import Dict, List
from sqlalchemy.orm import Session

from app.services.ai_providers import AIProviderFactory
from app.models.lms_db import Course, Module, Lesson, Quiz


class CourseGeneratorService:
    """Service pour générer des cours complets avec IA"""
    
    def __init__(self, ai_model: str = "gpt-4"):
        self.ai_model = ai_model
        self.ai_provider = AIProviderFactory.get_provider(ai_model)
    
    def generate_course_structure(self, title: str, description: str, num_modules: int = 5) -> Dict:
        """
        Générer la structure complète d'un cours
        
        Args:
            title: Titre du cours
            description: Description du cours
            num_modules: Nombre de modules à générer
        
        Returns:
            Dict avec la structure du cours
        """
        try:
            prompt = f"""Tu es un expert en création de formations en ligne.

Génère la structure complète d'une formation sur : "{title}"

Description : {description}

Crée {num_modules} modules avec 5 leçons chacun.

Réponds UNIQUEMENT en JSON avec ce format exact:
{{
    "modules": [
        {{
            "title": "Titre du module",
            "description": "Description du module",
            "order": 1,
            "lessons": [
                {{
                    "title": "Titre de la leçon",
                    "description": "Description de la leçon",
                    "order": 1,
                    "content_type": "text",
                    "duration": 15
                }}
            ]
        }}
    ]
}}

Assure-toi que:
- Les modules sont progressifs (du plus simple au plus avancé)
- Chaque module a exactement 5 leçons
- Les durées sont réalistes (10-30 minutes par leçon)
- Le contenu est structuré et pédagogique
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            # Parser la réponse JSON
            import json
            import re
            
            content = response["content"]
            
            # Extraire le JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                structure = json.loads(json_match.group())
            else:
                structure = json.loads(content)
            
            return {
                "success": True,
                "structure": structure
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def generate_lesson_content(self, lesson_title: str, module_title: str, course_title: str) -> Dict:
        """
        Générer le contenu d'une leçon
        
        Args:
            lesson_title: Titre de la leçon
            module_title: Titre du module
            course_title: Titre du cours
        
        Returns:
            Dict avec le contenu de la leçon
        """
        try:
            prompt = f"""Tu es un formateur expert.

Génère le contenu complet de cette leçon:

Formation: {course_title}
Module: {module_title}
Leçon: {lesson_title}

Crée un contenu pédagogique détaillé en HTML avec:
- Introduction claire
- Points clés (3-5 points)
- Exemples concrets
- Résumé
- Points à retenir

Format HTML simple (pas de <html>, <head>, <body>).
Utilise <h2>, <h3>, <p>, <ul>, <li>, <strong>, etc.
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            return {
                "success": True,
                "content": response["content"]
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def generate_quiz(self, lesson_title: str, lesson_content: str, num_questions: int = 5) -> Dict:
        """
        Générer un quiz pour une leçon
        
        Args:
            lesson_title: Titre de la leçon
            lesson_content: Contenu de la leçon
            num_questions: Nombre de questions
        
        Returns:
            Dict avec le quiz
        """
        try:
            prompt = f"""Tu es un créateur de quiz pédagogiques.

Génère un quiz de {num_questions} questions pour cette leçon:

Titre: {lesson_title}

Contenu: {lesson_content[:1000]}...

Réponds UNIQUEMENT en JSON avec ce format:
{{
    "title": "Quiz: {lesson_title}",
    "questions": [
        {{
            "question": "Question ici ?",
            "type": "multiple_choice",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "correct_answer": 0,
            "explanation": "Explication de la réponse correcte"
        }}
    ]
}}

Assure-toi que:
- Les questions testent la compréhension
- 4 options par question
- correct_answer est l'index (0-3)
- Les explications sont claires
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            # Parser la réponse JSON
            import json
            import re
            
            content = response["content"]
            
            # Extraire le JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                quiz_data = json.loads(json_match.group())
            else:
                quiz_data = json.loads(content)
            
            return {
                "success": True,
                "quiz": quiz_data
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def create_complete_course(
        self,
        db: Session,
        title: str,
        description: str,
        author_id: int,
        num_modules: int = 5,
        generate_content: bool = True,
        generate_quizzes: bool = True
    ) -> Dict:
        """
        Créer un cours complet avec IA
        
        Args:
            db: Session de base de données
            title: Titre du cours
            description: Description du cours
            author_id: ID de l'auteur
            num_modules: Nombre de modules
            generate_content: Générer le contenu des leçons
            generate_quizzes: Générer les quiz
        
        Returns:
            Dict avec success et course
        """
        try:
            # 1. Générer la structure
            structure_result = self.generate_course_structure(title, description, num_modules)
            
            if not structure_result.get("success"):
                return structure_result
            
            structure = structure_result["structure"]
            
            # 2. Créer le cours
            from app.services.course_service import CourseService
            
            course_data = {
                "title": title,
                "description": description,
                "short_description": description[:200] if len(description) > 200 else description
            }
            
            course_result = CourseService.create_course(db, course_data, author_id)
            
            if not course_result.get("success"):
                return course_result
            
            course_id = course_result["course"]["id"]
            
            # 3. Créer les modules et leçons
            for module_data in structure["modules"]:
                # Créer le module
                module = Module(
                    course_id=course_id,
                    title=module_data["title"],
                    description=module_data.get("description"),
                    order=module_data.get("order", 0)
                )
                db.add(module)
                db.flush()
                
                # Créer les leçons
                for lesson_data in module_data.get("lessons", []):
                    lesson = Lesson(
                        module_id=module.id,
                        title=lesson_data["title"],
                        description=lesson_data.get("description"),
                        order=lesson_data.get("order", 0),
                        content_type=lesson_data.get("content_type", "text"),
                        duration=lesson_data.get("duration", 15)
                    )
                    
                    # Générer le contenu si demandé
                    if generate_content:
                        content_result = self.generate_lesson_content(
                            lesson_data["title"],
                            module_data["title"],
                            title
                        )
                        if content_result.get("success"):
                            lesson.content = content_result["content"]
                    
                    db.add(lesson)
                    db.flush()
                    
                    # Générer le quiz si demandé
                    if generate_quizzes and lesson.content:
                        quiz_result = self.generate_quiz(
                            lesson.title,
                            lesson.content
                        )
                        if quiz_result.get("success"):
                            quiz_data = quiz_result["quiz"]
                            quiz = Quiz(
                                lesson_id=lesson.id,
                                title=quiz_data.get("title", f"Quiz: {lesson.title}"),
                                questions=quiz_data.get("questions", [])
                            )
                            db.add(quiz)
            
            db.commit()
            
            # 4. Mettre à jour les statistiques du cours
            course = db.query(Course).filter(Course.id == course_id).first()
            total_modules = db.query(Module).filter(Module.course_id == course_id).count()
            total_lessons = db.query(Lesson).join(Module).filter(Module.course_id == course_id).count()
            
            course.total_modules = total_modules
            course.total_lessons = total_lessons
            
            db.commit()
            db.refresh(course)
            
            return {
                "success": True,
                "course": course.to_dict(),
                "message": f"Cours créé avec {total_modules} modules et {total_lessons} leçons"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de création: {str(e)}"
            }
