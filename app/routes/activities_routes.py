from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/activities", response_class=HTMLResponse)
async def activities_page(request: Request, current_user: UserDB = Depends(get_current_user)):
    """Page des activités de l'utilisateur"""
    return templates.TemplateResponse(
        "pages/activities.html",
        {
            "request": request,
            "user": current_user,
            "cache_version": "1.0"
        }
    )
