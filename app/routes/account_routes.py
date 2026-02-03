from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/account", response_class=HTMLResponse)
async def account_page(request: Request, current_user: UserDB = Depends(get_current_user)):
    """Page de gestion du compte et des abonnements"""
    return templates.TemplateResponse(
        "pages/account.html",
        {
            "request": request,
            "user": current_user,
            "cache_version": "1.0"
        }
    )
