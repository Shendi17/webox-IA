"""
Routes API pour le Website Builder (Phase 6)
Date : 15 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import re

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from app.models.website_db import WebsiteDB, WebsitePageDB, BlogPostDB, WebsiteAnalyticsDB
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


# ============================================================================
# PYDANTIC SCHEMAS
# ============================================================================

class WebsiteCreate(BaseModel):
    name: str
    site_type: str  # business, portfolio, blog, ecommerce, landing
    industry: str
    template: Optional[str] = "modern"
    has_blog: Optional[bool] = False
    has_ecommerce: Optional[bool] = False

class PageCreate(BaseModel):
    title: str
    slug: str
    sections: Optional[List[Dict]] = []

class BlogPostCreate(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []


# ============================================================================
# PAGE HTML
# ============================================================================

@router.get("/website-builder", response_class=HTMLResponse)
async def website_builder_page(request: Request, user: dict = Depends(get_current_user_from_token)):
    """Page du Website Builder"""
    return templates.TemplateResponse("dashboard/website_builder.html", {
        "request": request,
        "user": user
    })


# ============================================================================
# WEBSITES - CRUD
# ============================================================================

@router.post("/api/websites/create")
async def create_website(
    website: WebsiteCreate,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Créer un nouveau site web avec IA"""
    try:
        # Générer subdomain unique
        subdomain = re.sub(r'[^a-z0-9]+', '-', website.name.lower()).strip('-')
        
        # Vérifier unicité
        existing = db.query(WebsiteDB).filter(WebsiteDB.subdomain == subdomain).first()
        if existing:
            subdomain = f"{subdomain}-{int(datetime.now().timestamp())}"
        
        # Créer le site
        new_website = WebsiteDB(
            user_id=user["id"],
            name=website.name,
            subdomain=subdomain,
            site_type=website.site_type,
            industry=website.industry,
            template=website.template,
            has_blog=website.has_blog,
            has_ecommerce=website.has_ecommerce,
            colors={"primary": "#667eea", "secondary": "#764ba2", "accent": "#ffd700"},
            fonts={"heading": "Montserrat", "body": "Open Sans"}
        )
        
        db.add(new_website)
        db.commit()
        db.refresh(new_website)
        
        # Générer contenu en arrière-plan
        background_tasks.add_task(generate_website_content, new_website.id, website, db)
        
        return {
            "success": True,
            "message": "Site web en cours de création !",
            "website_id": new_website.id,
            "subdomain": subdomain,
            "estimated_time": "30-60 secondes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/websites/list")
async def list_websites(
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des sites web"""
    try:
        websites = db.query(WebsiteDB).filter(
            WebsiteDB.user_id == user["id"]
        ).order_by(WebsiteDB.created_at.desc()).all()
        
        return {
            "success": True,
            "websites": [w.to_dict() for w in websites]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/websites/{website_id}")
async def get_website(
    website_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Détails d'un site"""
    try:
        website = db.query(WebsiteDB).filter(
            WebsiteDB.id == website_id,
            WebsiteDB.user_id == user["id"]
        ).first()
        
        if not website:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        # Récupérer les pages
        pages = db.query(WebsitePageDB).filter(
            WebsitePageDB.website_id == website_id
        ).order_by(WebsitePageDB.order).all()
        
        return {
            "success": True,
            "website": website.to_dict(),
            "pages": [p.to_dict() for p in pages]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/websites/{website_id}/publish")
async def publish_website(
    website_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Publier un site"""
    try:
        website = db.query(WebsiteDB).filter(
            WebsiteDB.id == website_id,
            WebsiteDB.user_id == user["id"]
        ).first()
        
        if not website:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        website.is_published = True
        website.published_url = f"https://{website.subdomain}.webox.app"
        website.last_published_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "message": "Site publié avec succès !",
            "url": website.published_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/websites/{website_id}")
async def delete_website(
    website_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Supprimer un site"""
    try:
        website = db.query(WebsiteDB).filter(
            WebsiteDB.id == website_id,
            WebsiteDB.user_id == user["id"]
        ).first()
        
        if not website:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        # Supprimer pages et posts associés
        db.query(WebsitePageDB).filter(WebsitePageDB.website_id == website_id).delete()
        db.query(BlogPostDB).filter(BlogPostDB.website_id == website_id).delete()
        db.query(WebsiteAnalyticsDB).filter(WebsiteAnalyticsDB.website_id == website_id).delete()
        
        db.delete(website)
        db.commit()
        
        return {
            "success": True,
            "message": "Site supprimé"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PAGES
# ============================================================================

@router.post("/api/websites/{website_id}/pages")
async def create_page(
    website_id: int,
    page: PageCreate,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Ajouter une page"""
    try:
        website = db.query(WebsiteDB).filter(
            WebsiteDB.id == website_id,
            WebsiteDB.user_id == user["id"]
        ).first()
        
        if not website:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        new_page = WebsitePageDB(
            website_id=website_id,
            title=page.title,
            slug=page.slug,
            sections=page.sections
        )
        
        db.add(new_page)
        db.commit()
        
        return {
            "success": True,
            "message": "Page créée"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/websites/{website_id}/pages")
async def get_pages(
    website_id: int,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des pages"""
    try:
        pages = db.query(WebsitePageDB).filter(
            WebsitePageDB.website_id == website_id
        ).order_by(WebsitePageDB.order).all()
        
        return {
            "success": True,
            "pages": [p.to_dict() for p in pages]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BLOG
# ============================================================================

@router.post("/api/websites/{website_id}/blog/posts")
async def create_blog_post(
    website_id: int,
    post: BlogPostCreate,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Créer un article de blog"""
    try:
        website = db.query(WebsiteDB).filter(
            WebsiteDB.id == website_id,
            WebsiteDB.user_id == user["id"]
        ).first()
        
        if not website:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        # Générer slug
        slug = re.sub(r'[^a-z0-9]+', '-', post.title.lower()).strip('-')
        
        new_post = BlogPostDB(
            website_id=website_id,
            title=post.title,
            slug=slug,
            content=post.content,
            excerpt=post.excerpt,
            category=post.category,
            tags=post.tags,
            author_name=user.get("name", "Admin")
        )
        
        db.add(new_post)
        db.commit()
        
        return {
            "success": True,
            "message": "Article créé"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/websites/{website_id}/blog/posts")
async def get_blog_posts(
    website_id: int,
    limit: int = 20,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Liste des articles"""
    try:
        posts = db.query(BlogPostDB).filter(
            BlogPostDB.website_id == website_id
        ).order_by(BlogPostDB.created_at.desc()).limit(limit).all()
        
        return {
            "success": True,
            "posts": [p.to_dict() for p in posts]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TEMPLATES
# ============================================================================

@router.get("/api/websites/templates/list")
async def get_website_templates():
    """Liste des templates de sites"""
    templates_list = [
        {
            "id": "modern-business",
            "name": "Business Moderne",
            "description": "Site professionnel pour entreprises",
            "icon": "💼",
            "pages": ["Accueil", "Services", "À propos", "Contact"],
            "preview": "https://placeholder.com/modern-business.jpg"
        },
        {
            "id": "creative-portfolio",
            "name": "Portfolio Créatif",
            "description": "Showcase pour créatifs et artistes",
            "icon": "🎨",
            "pages": ["Accueil", "Portfolio", "À propos", "Contact"],
            "preview": "https://placeholder.com/portfolio.jpg"
        },
        {
            "id": "blog-magazine",
            "name": "Blog Magazine",
            "description": "Blog professionnel avec articles",
            "icon": "📝",
            "pages": ["Accueil", "Blog", "À propos", "Contact"],
            "preview": "https://placeholder.com/blog.jpg"
        },
        {
            "id": "ecommerce-shop",
            "name": "Boutique E-commerce",
            "description": "Site de vente en ligne",
            "icon": "🛍️",
            "pages": ["Accueil", "Produits", "Panier", "Contact"],
            "preview": "https://placeholder.com/ecommerce.jpg"
        },
        {
            "id": "one-page",
            "name": "One Page",
            "description": "Site simple et efficace sur une seule page",
            "icon": "🎯",
            "pages": ["Accueil avec toutes les sections"],
            "preview": "https://placeholder.com/onepage.jpg"
        }
    ]
    
    return {
        "success": True,
        "templates": templates_list
    }


# ============================================================================
# ANALYTICS
# ============================================================================

@router.get("/api/websites/{website_id}/analytics")
async def get_website_analytics(
    website_id: int,
    days: int = 30,
    user: dict = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Analytics du site"""
    try:
        website = db.query(WebsiteDB).filter(
            WebsiteDB.id == website_id,
            WebsiteDB.user_id == user["id"]
        ).first()
        
        if not website:
            raise HTTPException(status_code=404, detail="Site non trouvé")
        
        # Analytics récentes
        analytics = db.query(WebsiteAnalyticsDB).filter(
            WebsiteAnalyticsDB.website_id == website_id
        ).order_by(WebsiteAnalyticsDB.date.desc()).limit(days).all()
        
        return {
            "success": True,
            "website": website.to_dict(),
            "analytics": [a.to_dict() for a in analytics]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BACKGROUND TASKS
# ============================================================================

def generate_website_content(website_id: int, website_data: WebsiteCreate, db: Session):
    """Générer le contenu du site avec IA"""
    import time
    time.sleep(5)  # Simuler génération IA
    
    website = db.query(WebsiteDB).filter(WebsiteDB.id == website_id).first()
    if not website:
        return
    
    # Générer pages par défaut selon le type
    default_pages = {
        "business": [
            {"title": "Accueil", "slug": "/", "order": 0},
            {"title": "Services", "slug": "/services", "order": 1},
            {"title": "À propos", "slug": "/about", "order": 2},
            {"title": "Contact", "slug": "/contact", "order": 3}
        ],
        "portfolio": [
            {"title": "Accueil", "slug": "/", "order": 0},
            {"title": "Portfolio", "slug": "/portfolio", "order": 1},
            {"title": "À propos", "slug": "/about", "order": 2},
            {"title": "Contact", "slug": "/contact", "order": 3}
        ],
        "blog": [
            {"title": "Accueil", "slug": "/", "order": 0},
            {"title": "Blog", "slug": "/blog", "order": 1},
            {"title": "À propos", "slug": "/about", "order": 2},
            {"title": "Contact", "slug": "/contact", "order": 3}
        ],
        "ecommerce": [
            {"title": "Accueil", "slug": "/", "order": 0},
            {"title": "Produits", "slug": "/products", "order": 1},
            {"title": "Panier", "slug": "/cart", "order": 2},
            {"title": "Contact", "slug": "/contact", "order": 3}
        ],
        "landing": [
            {"title": "Accueil", "slug": "/", "order": 0}
        ]
    }
    
    pages_to_create = default_pages.get(website_data.site_type, default_pages["business"])
    
    for page_data in pages_to_create:
        page = WebsitePageDB(
            website_id=website_id,
            title=page_data["title"],
            slug=page_data["slug"],
            order=page_data["order"],
            sections=[
                {"type": "hero", "content": {"title": f"Bienvenue sur {website.name}", "subtitle": "Contenu généré par IA"}},
                {"type": "features", "content": {"title": "Nos Services", "items": []}}
            ]
        )
        db.add(page)
    
    # Mettre à jour le site
    website.pages = [p["title"] for p in pages_to_create]
    db.commit()
