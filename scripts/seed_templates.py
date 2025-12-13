"""
Script pour ajouter des templates de projets web de base
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import ProjectTemplate
from datetime import datetime


def seed_templates():
    db = SessionLocal()
    
    templates = [
        {
            "name": "Site Statique Simple",
            "slug": "static-simple",
            "description": "Un site statique basique avec HTML, CSS et JavaScript",
            "category": "landing",
            "project_type": "static",
            "framework": "html",
            "languages": ["html", "css", "javascript"],
            "features": ["responsive", "seo"],
            "tags": ["simple", "débutant", "rapide"],
            "is_official": True,
            "is_premium": False,
            "price": 0
        },
        {
            "name": "Portfolio Moderne",
            "slug": "portfolio-modern",
            "description": "Portfolio professionnel avec animations et dark mode",
            "category": "portfolio",
            "project_type": "static",
            "framework": "html",
            "languages": ["html", "css", "javascript"],
            "features": ["responsive", "dark-mode", "animations", "seo"],
            "tags": ["portfolio", "moderne", "animations"],
            "is_official": True,
            "is_premium": False,
            "price": 0
        },
        {
            "name": "Application React",
            "slug": "react-app",
            "description": "Application React avec routing et state management",
            "category": "saas",
            "project_type": "react",
            "framework": "react",
            "languages": ["javascript", "jsx", "css"],
            "features": ["spa", "routing", "state-management"],
            "tags": ["react", "moderne", "spa"],
            "is_official": True,
            "is_premium": False,
            "price": 0
        },
        {
            "name": "Site Next.js",
            "slug": "nextjs-site",
            "description": "Site Next.js avec SSR et optimisations",
            "category": "saas",
            "project_type": "nextjs",
            "framework": "nextjs",
            "languages": ["javascript", "jsx", "css"],
            "features": ["ssr", "seo", "optimized", "api-routes"],
            "tags": ["nextjs", "ssr", "performance"],
            "is_official": True,
            "is_premium": False,
            "price": 0
        },
        {
            "name": "Blog Minimaliste",
            "slug": "blog-minimal",
            "description": "Blog simple et élégant avec système de posts",
            "category": "blog",
            "project_type": "static",
            "framework": "html",
            "languages": ["html", "css", "javascript"],
            "features": ["blog", "responsive", "seo"],
            "tags": ["blog", "minimaliste", "simple"],
            "is_official": True,
            "is_premium": False,
            "price": 0
        },
        {
            "name": "Landing Page Conversion",
            "slug": "landing-conversion",
            "description": "Landing page optimisée pour la conversion avec CTA",
            "category": "landing",
            "project_type": "static",
            "framework": "html",
            "languages": ["html", "css", "javascript"],
            "features": ["responsive", "cta", "forms", "analytics"],
            "tags": ["landing", "conversion", "marketing"],
            "is_official": True,
            "is_premium": False,
            "price": 0
        }
    ]
    
    for template_data in templates:
        # Vérifier si le template existe déjà
        existing = db.query(ProjectTemplate).filter(
            ProjectTemplate.slug == template_data["slug"]
        ).first()
        
        if not existing:
            template = ProjectTemplate(
                **template_data,
                published_at=datetime.utcnow()
            )
            db.add(template)
            print(f"✅ Template ajouté : {template_data['name']}")
        else:
            print(f"⏭️  Template existe déjà : {template_data['name']}")
    
    db.commit()
    db.close()
    print("\n🎉 Seed des templates terminé !")


if __name__ == "__main__":
    seed_templates()
