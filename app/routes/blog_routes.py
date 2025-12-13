"""
Routes API pour le blog
Date : 2 Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.models.article_db import ArticleDB
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/api/blog", tags=["Blog"])


# ========== MODÈLES PYDANTIC ==========

class ArticleCreate(BaseModel):
    """Modèle pour créer un article"""
    title: str
    excerpt: Optional[str] = None
    content: str
    category: str = "Nouveautés"
    image_url: Optional[str] = None
    is_featured: bool = False


class ArticleUpdate(BaseModel):
    """Modèle pour mettre à jour un article"""
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = None


class NewsletterSubscribe(BaseModel):
    """Modèle pour s'abonner à la newsletter"""
    email: str


# ========== FONCTIONS UTILITAIRES ==========

def create_slug(title: str) -> str:
    """Crée un slug à partir d'un titre"""
    import re
    slug = title.lower()
    slug = re.sub(r'[àáâãäå]', 'a', slug)
    slug = re.sub(r'[èéêë]', 'e', slug)
    slug = re.sub(r'[ìíîï]', 'i', slug)
    slug = re.sub(r'[òóôõö]', 'o', slug)
    slug = re.sub(r'[ùúûü]', 'u', slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def calculate_reading_time(content: str) -> int:
    """Calcule le temps de lecture en minutes (250 mots/min)"""
    words = len(content.split())
    return max(1, round(words / 250))


# ========== ROUTES API ==========

@router.get("/articles")
async def get_articles(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des articles
    """
    query = db.query(ArticleDB).filter(ArticleDB.is_published == True)
    
    # Filtrer par catégorie
    if category and category != "Tous":
        query = query.filter(ArticleDB.category == category)
    
    # Recherche
    if search:
        query = query.filter(
            or_(
                ArticleDB.title.ilike(f"%{search}%"),
                ArticleDB.excerpt.ilike(f"%{search}%"),
                ArticleDB.content.ilike(f"%{search}%")
            )
        )
    
    # Trier par date
    query = query.order_by(ArticleDB.published_at.desc())
    
    # Pagination
    total = query.count()
    articles = query.offset(offset).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "articles": [article.to_dict() for article in articles]
    }


@router.get("/articles/featured")
async def get_featured_article(db: Session = Depends(get_db)):
    """
    Récupère l'article à la une
    """
    article = db.query(ArticleDB).filter(
        ArticleDB.is_published == True,
        ArticleDB.is_featured == True
    ).order_by(ArticleDB.published_at.desc()).first()
    
    if not article:
        # Si pas d'article featured, prendre le plus récent
        article = db.query(ArticleDB).filter(
            ArticleDB.is_published == True
        ).order_by(ArticleDB.published_at.desc()).first()
    
    if not article:
        return {
            "success": False,
            "message": "Aucun article disponible"
        }
    
    return {
        "success": True,
        "article": article.to_dict()
    }


@router.get("/articles/{slug}")
async def get_article(slug: str, db: Session = Depends(get_db)):
    """
    Récupère un article par son slug
    """
    article = db.query(ArticleDB).filter(ArticleDB.slug == slug).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article non trouvé"
        )
    
    # Incrémenter les vues
    article.views += 1
    db.commit()
    
    return {
        "success": True,
        "article": article.to_dict()
    }


@router.post("/articles")
async def create_article(
    article_data: ArticleCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel article (admin seulement)
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs"
        )
    
    try:
        # Créer le slug
        slug = create_slug(article_data.title)
        
        # Vérifier que le slug n'existe pas déjà
        existing = db.query(ArticleDB).filter(ArticleDB.slug == slug).first()
        if existing:
            slug = f"{slug}-{datetime.now().timestamp()}"
        
        # Calculer le temps de lecture
        reading_time = calculate_reading_time(article_data.content)
        
        # Créer l'article
        article = ArticleDB(
            title=article_data.title,
            slug=slug,
            excerpt=article_data.excerpt,
            content=article_data.content,
            category=article_data.category,
            image_url=article_data.image_url,
            is_featured=article_data.is_featured,
            author_id=current_user.id,
            author_name=current_user.name,
            reading_time=reading_time
        )
        
        db.add(article)
        db.commit()
        db.refresh(article)
        
        return {
            "success": True,
            "message": "Article créé avec succès",
            "article": article.to_dict()
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création: {str(e)}"
        )


@router.post("/newsletter/subscribe")
async def subscribe_newsletter(
    data: NewsletterSubscribe,
    db: Session = Depends(get_db)
):
    """
    S'abonner à la newsletter
    """
    # TODO: Implémenter le système de newsletter
    # Pour l'instant, juste retourner un succès
    
    return {
        "success": True,
        "message": f"Merci ! Vous êtes maintenant abonné à notre newsletter avec l'adresse {data.email}"
    }


@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """
    Récupère la liste des catégories avec le nombre d'articles
    """
    from sqlalchemy import func
    
    categories = db.query(
        ArticleDB.category,
        func.count(ArticleDB.id).label('count')
    ).filter(
        ArticleDB.is_published == True
    ).group_by(ArticleDB.category).all()
    
    return {
        "success": True,
        "categories": [
            {"name": cat[0], "count": cat[1]}
            for cat in categories
        ]
    }
