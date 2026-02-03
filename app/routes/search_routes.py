"""
Routes pour la recherche et les filtres e-commerce
"""
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional, List
from app.database import get_db
from app.models.product_db import ProductDB

router = APIRouter()


@router.get("/api/products/search")
async def search_products(
    q: Optional[str] = Query(None, description="Terme de recherche"),
    category: Optional[str] = Query(None, description="Catégorie"),
    min_price: Optional[float] = Query(None, description="Prix minimum"),
    max_price: Optional[float] = Query(None, description="Prix maximum"),
    sort_by: Optional[str] = Query("name", description="Tri: name, price_asc, price_desc, popularity"),
    limit: int = Query(20, le=100, description="Nombre de résultats"),
    offset: int = Query(0, description="Décalage pour pagination"),
    db: Session = Depends(get_db)
):
    """
    API de recherche et filtrage des produits
    
    Paramètres:
    - q: Terme de recherche (nom, description)
    - category: Filtrer par catégorie
    - min_price: Prix minimum
    - max_price: Prix maximum
    - sort_by: Tri (name, price_asc, price_desc, popularity)
    - limit: Nombre de résultats (max 100)
    - offset: Pagination
    """
    
    # Requête de base
    query = db.query(ProductDB).filter(ProductDB.is_available == True)
    
    # Filtre de recherche textuelle
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                ProductDB.name.ilike(search_term),
                ProductDB.description.ilike(search_term)
            )
        )
    
    # Filtre par catégorie
    if category:
        query = query.filter(ProductDB.category == category)
    
    # Filtre par prix
    if min_price is not None:
        query = query.filter(ProductDB.price >= min_price)
    
    if max_price is not None:
        query = query.filter(ProductDB.price <= max_price)
    
    # Tri
    if sort_by == "price_asc":
        query = query.order_by(ProductDB.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(ProductDB.price.desc())
    elif sort_by == "popularity":
        query = query.order_by(ProductDB.stock.desc())  # Simuler popularité par stock
    else:  # name par défaut
        query = query.order_by(ProductDB.name.asc())
    
    # Compter le total
    total = query.count()
    
    # Pagination
    products = query.offset(offset).limit(limit).all()
    
    # Formater les résultats
    results = []
    for product in products:
        results.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "category": product.category,
            "image_url": product.image_url,
            "stock": product.stock,
            "is_available": product.is_available
        })
    
    return {
        "success": True,
        "total": total,
        "count": len(results),
        "offset": offset,
        "limit": limit,
        "products": results
    }


@router.get("/api/products/categories")
async def get_categories(db: Session = Depends(get_db)):
    """
    Récupérer la liste des catégories disponibles
    """
    categories = db.query(ProductDB.category).distinct().all()
    
    category_list = [cat[0] for cat in categories if cat[0]]
    
    return {
        "success": True,
        "categories": category_list
    }


@router.get("/api/products/filters")
async def get_filter_options(db: Session = Depends(get_db)):
    """
    Récupérer les options de filtrage disponibles
    (catégories, plage de prix, etc.)
    """
    # Catégories
    categories = db.query(ProductDB.category).distinct().all()
    category_list = [cat[0] for cat in categories if cat[0]]
    
    # Plage de prix
    min_price_result = db.query(ProductDB.price).order_by(ProductDB.price.asc()).first()
    max_price_result = db.query(ProductDB.price).order_by(ProductDB.price.desc()).first()
    
    min_price = float(min_price_result[0]) if min_price_result else 0
    max_price = float(max_price_result[0]) if max_price_result else 1000
    
    return {
        "success": True,
        "filters": {
            "categories": category_list,
            "price_range": {
                "min": min_price,
                "max": max_price
            },
            "sort_options": [
                {"value": "name", "label": "Nom (A-Z)"},
                {"value": "price_asc", "label": "Prix croissant"},
                {"value": "price_desc", "label": "Prix décroissant"},
                {"value": "popularity", "label": "Popularité"}
            ]
        }
    }
