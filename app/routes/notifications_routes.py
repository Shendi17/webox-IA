"""
Routes pour les notifications utilisateur
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/notifications", response_class=HTMLResponse)
async def notifications_page(
    request: Request,
    current_user: UserDB = Depends(get_current_user)
):
    """Page Notifications - Gérer les notifications utilisateur"""
    return templates.TemplateResponse(
        "pages/notifications.html",
        {
            "request": request,
            "user": current_user,
            "title": "Notifications - WeBox Multi-IA",
            "page": "notifications"
        }
    )
