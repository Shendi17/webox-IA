"""
Script pour créer un projet de test
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import WebProject
from datetime import datetime


def create_test_project():
    db = SessionLocal()
    
    # Vérifier si un projet de test existe déjà
    existing = db.query(WebProject).filter(WebProject.slug == "mon-projet-test").first()
    
    if existing:
        print("⏭️  Un projet de test existe déjà")
        return
    
    # Créer un projet de test
    project = WebProject(
        name="Mon Projet Test",
        slug="mon-projet-test",
        description="Ceci est un projet de test pour vérifier l'affichage",
        project_type="static",
        framework="html",
        owner_id=1,  # ID de l'utilisateur (à adapter)
        status="active",
        total_files=3,
        total_lines=150,
        total_size=5120,  # 5 KB
        local_path="projects/1/mon-projet-test",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    print(f"✅ Projet de test créé : {project.name} (ID: {project.id})")
    
    db.close()


if __name__ == "__main__":
    create_test_project()
