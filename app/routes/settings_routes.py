"""
Routes pour les paramètres utilisateur
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    current_user: UserDB = Depends(get_current_user)
):
    """Page Paramètres - Gérer les paramètres du compte"""
    return templates.TemplateResponse(
        "pages/settings.html",
        {
            "request": request,
            "user": current_user,
            "title": "Paramètres - WeBox Multi-IA",
            "page": "settings"
        }
    )
