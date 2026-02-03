"""
Routes pour la page des commandes
Affichage et gestion des commandes utilisateur
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, current_user: UserDB = Depends(get_current_user)):
    """Page des commandes de l'utilisateur"""
    
    # Données exemple des commandes
    # En production, ces données viendraient de la base de données
    orders = [
        {
            "id": "WB-2026-001234",
            "date": "23 janvier 2026 - 23:45",
            "status": "completed",
            "items": [
                {
                    "name": "Générateur de Contenu IA Pro",
                    "description": "Licence perpétuelle",
                    "quantity": 1,
                    "price": 49.99
                },
                {
                    "name": "Pack Templates Premium",
                    "description": "50+ templates professionnels",
                    "quantity": 2,
                    "price": 59.98
                }
            ],
            "payment_method": "card",
            "payment_status": "paid",
            "total": 95.96
        },
        {
            "id": "WB-2026-001235",
            "date": "24 janvier 2026 - 10:30",
            "status": "pending",
            "items": [
                {
                    "name": "Assistant IA Personnalisé",
                    "description": "Configuration sur mesure",
                    "quantity": 1,
                    "price": 199.99
                }
            ],
            "payment_method": "bank_transfer",
            "payment_status": "pending",
            "total": 199.99
        },
        {
            "id": "WB-2026-001220",
            "date": "20 janvier 2026 - 15:20",
            "status": "completed",
            "items": [
                {
                    "name": "Formation Marketing IA",
                    "description": "Masterclass complète",
                    "quantity": 1,
                    "price": 69.99
                }
            ],
            "payment_method": "paypal",
            "payment_status": "paid",
            "total": 69.99
        },
        {
            "id": "WB-2026-001215",
            "date": "18 janvier 2026 - 09:15",
            "status": "completed",
            "items": [
                {
                    "name": "Website Builder Pro",
                    "description": "Créateur de sites web avec IA",
                    "quantity": 1,
                    "price": 79.99
                }
            ],
            "payment_method": "card",
            "payment_status": "paid",
            "total": 79.99
        },
        {
            "id": "WB-2026-001210",
            "date": "15 janvier 2026 - 14:00",
            "status": "cancelled",
            "items": [
                {
                    "name": "Analytics Dashboard",
                    "description": "Tableau de bord analytics avancé",
                    "quantity": 1,
                    "price": 59.99
                }
            ],
            "payment_method": "card",
            "payment_status": "cancelled",
            "total": 59.99
        }
    ]
    
    return templates.TemplateResponse(
        "pages/orders.html",
        {
            "request": request,
            "user": current_user,
            "orders": orders,
            "cache_version": "1.0"
        }
    )


@router.get("/api/orders/list")
async def get_orders_list(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """API pour récupérer la liste des commandes de l'utilisateur"""
    
    # Pour l'instant, retourner des données exemple
    # En production, récupérer depuis la base de données
    orders = [
        {
            "id": "WB-2026-001234",
            "date": "2026-01-23T23:45:00",
            "status": "completed",
            "total": 95.96,
            "items_count": 2,
            "payment_method": "card"
        },
        {
            "id": "WB-2026-001235",
            "date": "2026-01-24T10:30:00",
            "status": "pending",
            "total": 199.99,
            "items_count": 1,
            "payment_method": "bank_transfer"
        }
    ]
    
    return orders
