"""
Service pour gérer les templates de projets
"""
import os
from pathlib import Path
from typing import Dict, Optional

from app.templates_data.templates_library import get_all_templates, get_template


class TemplateService:
    """Service de gestion des templates"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
    
    def list_templates(self) -> Dict:
        """Lister tous les templates disponibles"""
        try:
            templates = get_all_templates()
            return {
                "success": True,
                "templates": list(templates.values())
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_template_details(self, template_id: str) -> Dict:
        """Obtenir les détails d'un template"""
        try:
            template = get_template(template_id)
            if not template:
                return {"success": False, "error": "Template non trouvé"}
            
            return {
                "success": True,
                "template": template
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_project_from_template(
        self, 
        template_id: str, 
        project_name: str,
        project_path: str,
        customization: Optional[Dict] = None
    ) -> Dict:
        """Créer un projet à partir d'un template"""
        try:
            # Obtenir le template
            template = get_template(template_id)
            if not template:
                return {"success": False, "error": "Template non trouvé"}
            
            # Créer le dossier du projet
            project_dir = Path(project_path)
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Créer les fichiers
            for filename, content in template["files"].items():
                file_path = project_dir / filename
                
                # Appliquer la personnalisation si fournie
                if customization:
                    content = self._apply_customization(content, customization)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return {
                "success": True,
                "message": f"Projet créé à partir du template '{template['name']}'",
                "files_created": list(template["files"].keys())
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _apply_customization(self, content: str, customization: Dict) -> str:
        """Appliquer la personnalisation au contenu"""
        # Remplacer les placeholders
        if "title" in customization:
            content = content.replace("Mon Portfolio", customization["title"])
            content = content.replace("Mon Blog", customization["title"])
            content = content.replace("MonApp", customization["title"])
        
        if "description" in customization:
            content = content.replace(
                "La plateforme tout-en-un pour développer votre activité en ligne",
                customization["description"]
            )
        
        if "author" in customization:
            content = content.replace("John Doe", customization["author"])
        
        if "primary_color" in customization:
            content = content.replace("#007bff", customization["primary_color"])
            content = content.replace("#667eea", customization["primary_color"])
        
        return content
