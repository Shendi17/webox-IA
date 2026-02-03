"""
Routes pour la Marketplace WeBox
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.middleware.auth import get_current_user_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/marketplace", response_class=HTMLResponse)
async def marketplace(request: Request):
    """Page Marketplace - Boutique d'outils et services IA"""
    user = get_current_user_from_cookie(request)
    
    return templates.TemplateResponse(
        "pages/marketplace.html",
        {
            "request": request,
            "user": user,
            "title": "Marketplace - WeBox Multi-IA",
            "page": "marketplace"
        }
    )

@router.get("/product/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    """Page détail d'un produit"""
    user = get_current_user_from_cookie(request)
    
    # Données exemple du produit
    product = {
        "id": product_id,
        "name": "Générateur de Contenu IA Pro",
        "category": "Outils IA",
        "price": "49,99 €",
        "original_price": "79,99 €",
        "discount": "37",
        "image": "/static/images/products/product1.jpg",
        "badge": "Populaire",
        "reviews": 245,
        "description": "Créez du contenu de qualité professionnelle en quelques secondes grâce à l'intelligence artificielle.",
        "long_description": "Notre générateur de contenu IA Pro utilise les dernières technologies d'intelligence artificielle pour vous aider à créer du contenu de qualité professionnelle en quelques secondes. Que ce soit pour vos articles de blog, vos posts sur les réseaux sociaux, ou vos descriptions de produits, cet outil vous fera gagner un temps précieux."
    }
    
    return templates.TemplateResponse(
        "pages/product_detail.html",
        {
            "request": request,
            "user": user,
            "product": product
        }
    )

@router.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    """Page panier dynamique avec API"""
    user = get_current_user_from_cookie(request)
    
    return templates.TemplateResponse(
        "pages/cart_dynamic.html",
        {
            "request": request,
            "user": user
        }
    )

@router.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    """Page des abonnements"""
    user = get_current_user_from_cookie(request)
    
    return templates.TemplateResponse(
        "pages/pricing.html",
        {
            "request": request,
            "user": user
        }
    )

@router.get("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    """Page de paiement"""
    user = get_current_user_from_cookie(request)
    
    return templates.TemplateResponse(
        "pages/checkout.html",
        {
            "request": request,
            "user": user
        }
    )
