"""
Routes pour la page Documentation
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.middleware.auth import get_current_user_from_cookie, require_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/documentation", response_class=HTMLResponse)
async def documentation_page(request: Request, user=Depends(require_auth)):
    """Page de documentation complète"""
    return templates.TemplateResponse("dashboard/documentation.html", {
        "request": request,
        "user": user
    })
