"""
Script pour créer plusieurs projets de test
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import WebProject
from datetime import datetime, timedelta


def seed_test_projects():
    db = SessionLocal()
    
    projects = [
        {
            "name": "Portfolio Personnel",
            "slug": "portfolio-personnel",
            "description": "Mon portfolio professionnel avec mes projets",
            "project_type": "static",
            "framework": "html",
            "total_files": 12,
            "total_lines": 450,
            "total_size": 25600,
            "prod_url": "https://portfolio.example.com"
        },
        {
            "name": "Application React",
            "slug": "app-react",
            "description": "Application web moderne avec React",
            "project_type": "react",
            "framework": "react",
            "total_files": 45,
            "total_lines": 2300,
            "total_size": 156000
        },
        {
            "name": "Blog Next.js",
            "slug": "blog-nextjs",
            "description": "Blog personnel avec Next.js et Markdown",
            "project_type": "nextjs",
            "framework": "nextjs",
            "total_files": 28,
            "total_lines": 1200,
            "total_size": 89000,
            "prod_url": "https://blog.example.com"
        },
        {
            "name": "API FastAPI",
            "slug": "api-fastapi",
            "description": "API REST avec FastAPI et PostgreSQL",
            "project_type": "fastapi",
            "framework": "fastapi",
            "total_files": 18,
            "total_lines": 890,
            "total_size": 45000
        },
        {
            "name": "Site E-commerce",
            "slug": "ecommerce",
            "description": "Boutique en ligne avec panier et paiement",
            "project_type": "vue",
            "framework": "vue",
            "total_files": 67,
            "total_lines": 3400,
            "total_size": 234000,
            "status": "maintenance"
        }
    ]
    
    for i, project_data in enumerate(projects):
        # Vérifier si le projet existe déjà
        existing = db.query(WebProject).filter(
            WebProject.slug == project_data["slug"]
        ).first()
        
        if existing:
            print(f"⏭️  Projet existe déjà : {project_data['name']}")
            continue
        
        # Extraire le status avant de passer les données
        status = project_data.pop("status", "active")
        
        project = WebProject(
            **project_data,
            owner_id=1,
            status=status,
            local_path=f"projects/1/{project_data['slug']}",
            created_at=datetime.now() - timedelta(days=30-i*5),
            updated_at=datetime.now() - timedelta(days=i)
        )
        
        db.add(project)
        print(f"✅ Projet créé : {project_data['name']}")
    
    db.commit()
    db.close()
    print("\n🎉 Seed des projets de test terminé !")


if __name__ == "__main__":
    seed_test_projects()
