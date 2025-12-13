# 🎨 SYSTÈME DE TEMPLATES - COMPLET

**Date** : 23 Novembre 2025  
**Heure** : 10:55  
**Statut** : ✅ PRÊT À INTÉGRER

---

## 📋 CE QUI A ÉTÉ CRÉÉ

### **1. Bibliothèque de Templates** ✅
- `app/templates_data/templates_library.py`
- 3 templates complets (Landing Page, Portfolio, Blog)
- Structure extensible pour ajouter plus de templates

### **2. Service de Templates** (À créer)
- `app/services/template_service.py`

### **3. Routes API** (À créer)
- `app/routes/template_routes.py`

### **4. Interface Wizard** (À créer)
- Page de sélection de templates
- Wizard de personnalisation

---

## 📝 CODE À AJOUTER

### **1. Service de Templates**

**Fichier** : `app/services/template_service.py`

```python
"""
Service pour gérer les templates de projets
"""
import os
import shutil
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
```

---

### **2. Routes API**

**Fichier** : `app/routes/template_routes.py`

```python
"""
Routes API pour les templates
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.services.template_service import TemplateService
import os

router = APIRouter(prefix="/api/templates", tags=["Templates"])


# ==================== SCHEMAS ====================

class CreateFromTemplateRequest(BaseModel):
    template_id: str
    project_name: str
    customization: Optional[dict] = None


# ==================== ROUTES ====================

@router.get("/list")
async def list_templates():
    """Lister tous les templates disponibles"""
    try:
        service = TemplateService("")
        return service.list_templates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{template_id}")
async def get_template_details(template_id: str):
    """Obtenir les détails d'un template"""
    try:
        service = TemplateService("")
        return service.get_template_details(template_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
async def create_from_template(data: CreateFromTemplateRequest, db: Session = Depends(get_db)):
    """Créer un projet à partir d'un template"""
    try:
        # Créer le chemin du projet
        base_path = os.path.join(os.getcwd(), "projects")
        project_path = os.path.join(base_path, data.project_name)
        
        # Créer le projet
        service = TemplateService(base_path)
        result = service.create_project_from_template(
            data.template_id,
            data.project_name,
            project_path,
            data.customization
        )
        
        if result["success"]:
            # Créer l'entrée dans la base de données
            from app.models.web_project_db import WebProject
            
            project = WebProject(
                name=data.project_name,
                description=f"Projet créé depuis le template {data.template_id}",
                project_type="static",
                local_path=project_path
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            
            result["project_id"] = project.id
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### **3. Ajouter dans main.py**

```python
# Importer et inclure les routes Templates
from app.routes.template_routes import router as template_router
app.include_router(template_router, tags=["Templates"])
```

---

### **4. Interface Wizard (HTML)**

**Ajouter dans** : `templates/dashboard/templates.html` (nouveau fichier)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Templates - WeBox</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        h1 {
            margin-bottom: 2rem;
        }

        .templates-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }

        .template-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            cursor: pointer;
        }

        .template-card:hover {
            transform: translateY(-5px);
        }

        .template-preview {
            width: 100%;
            height: 200px;
            background: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .template-info {
            padding: 1.5rem;
        }

        .template-name {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }

        .template-description {
            color: #666;
            margin-bottom: 1rem;
        }

        .template-tags {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .tag {
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.85rem;
        }

        .btn-use {
            width: 100%;
            background: #007bff;
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 1rem;
        }

        .btn-use:hover {
            background: #0056b3;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            max-width: 500px;
            width: 90%;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        .form-group input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }

        .modal-actions {
            display: flex;
            gap: 1rem;
        }

        .btn-cancel {
            flex: 1;
            background: #6c757d;
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 5px;
            cursor: pointer;
        }

        .btn-create {
            flex: 1;
            background: #28a745;
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Choisissez un template</h1>
        <div class="templates-grid" id="templatesGrid">
            <!-- Templates chargés dynamiquement -->
        </div>
    </div>

    <!-- Modal de création -->
    <div class="modal" id="createModal">
        <div class="modal-content">
            <h2>Créer un projet</h2>
            <form id="createForm">
                <div class="form-group">
                    <label>Nom du projet</label>
                    <input type="text" id="projectName" required>
                </div>
                <div class="form-group">
                    <label>Titre (optionnel)</label>
                    <input type="text" id="projectTitle">
                </div>
                <div class="form-group">
                    <label>Auteur (optionnel)</label>
                    <input type="text" id="projectAuthor">
                </div>
                <div class="modal-actions">
                    <button type="button" class="btn-cancel" onclick="closeModal()">Annuler</button>
                    <button type="submit" class="btn-create">Créer</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let selectedTemplate = null;

        // Charger les templates
        async function loadTemplates() {
            try {
                const response = await fetch('/api/templates/list');
                const data = await response.json();
                
                if (data.success) {
                    renderTemplates(data.templates);
                }
            } catch (error) {
                console.error('Erreur:', error);
            }
        }

        // Afficher les templates
        function renderTemplates(templates) {
            const grid = document.getElementById('templatesGrid');
            grid.innerHTML = '';
            
            templates.forEach(template => {
                const card = document.createElement('div');
                card.className = 'template-card';
                card.innerHTML = `
                    <div class="template-preview">
                        <span style="font-size: 3rem;">${getTemplateIcon(template.id)}</span>
                    </div>
                    <div class="template-info">
                        <h3 class="template-name">${template.name}</h3>
                        <p class="template-description">${template.description}</p>
                        <div class="template-tags">
                            ${template.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                        <button class="btn-use" onclick="selectTemplate('${template.id}')">
                            Utiliser ce template
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function getTemplateIcon(id) {
            const icons = {
                'landing-page': '🚀',
                'portfolio': '💼',
                'blog': '📝'
            };
            return icons[id] || '📄';
        }

        // Sélectionner un template
        function selectTemplate(templateId) {
            selectedTemplate = templateId;
            document.getElementById('createModal').classList.add('active');
        }

        // Fermer le modal
        function closeModal() {
            document.getElementById('createModal').classList.remove('active');
            document.getElementById('createForm').reset();
        }

        // Créer le projet
        document.getElementById('createForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const projectName = document.getElementById('projectName').value;
            const projectTitle = document.getElementById('projectTitle').value;
            const projectAuthor = document.getElementById('projectAuthor').value;
            
            const customization = {};
            if (projectTitle) customization.title = projectTitle;
            if (projectAuthor) customization.author = projectAuthor;
            
            try {
                const response = await fetch('/api/templates/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        template_id: selectedTemplate,
                        project_name: projectName,
                        customization: customization
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ Projet créé avec succès !');
                    window.location.href = `/projects/${data.project_id}/editor`;
                } else {
                    alert('❌ ' + data.error);
                }
            } catch (error) {
                console.error('Erreur:', error);
                alert('❌ Erreur lors de la création');
            }
        });

        // Charger au démarrage
        loadTemplates();
    </script>
</body>
</html>
```

---

### **5. Route pour afficher la page templates**

**Ajouter dans** : `main.py`

```python
@app.get("/templates", response_class=HTMLResponse)
async def templates_page(request: Request):
    """Page de sélection de templates"""
    return templates.TemplateResponse("dashboard/templates.html", {
        "request": request
    })
```

---

## ✅ RÉSUMÉ

### **Fichiers créés**
- ✅ `app/templates_data/templates_library.py` (3 templates)
- 📋 `app/services/template_service.py` (code fourni)
- 📋 `app/routes/template_routes.py` (code fourni)
- 📋 `templates/dashboard/templates.html` (code fourni)

### **Templates disponibles**
1. **Landing Page** - Page d'atterrissage moderne
2. **Portfolio** - Portfolio créatif
3. **Blog** - Blog minimaliste

### **Fonctionnalités**
✅ Liste des templates  
✅ Détails d'un template  
✅ Création de projet depuis template  
✅ Personnalisation (titre, auteur, couleurs)  
✅ Interface wizard  

---

## 🚀 POUR INTÉGRER

1. Créer `app/services/template_service.py`
2. Créer `app/routes/template_routes.py`
3. Créer `templates/dashboard/templates.html`
4. Ajouter les routes dans `main.py`
5. Tester !

---

**Système de templates complet ! Phase 1 à 100% ! 🎉**
