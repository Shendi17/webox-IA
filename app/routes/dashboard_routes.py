"""
Routes du dashboard utilisateur
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.middleware.auth import get_current_user_from_cookie
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/test-modal", response_class=HTMLResponse)
async def test_modal(request: Request):
    """Page de test pour les modals"""
    return templates.TemplateResponse("test_modal_page.html", {
        "request": request
    })


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/index.html", {
        "request": request,
        "user": user
    })


@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    """Page de chat Multi-IA"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/chat.html", {
        "request": request,
        "user": user
    })


@router.get("/generation", response_class=HTMLResponse)
async def generation(request: Request):
    """Page de génération (images, audio, vidéo)"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/generation.html", {
        "request": request,
        "user": user
    })


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """Page de profil utilisateur"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/profile.html", {
        "request": request,
        "user": user
    })


@router.get("/agents", response_class=HTMLResponse)
async def agents(request: Request):
    """Page des agents IA spécialisés"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/agents.html", {
        "request": request,
        "user": user
    })


@router.get("/agent-chat/{agent_id}", response_class=HTMLResponse)
async def agent_chat(agent_id: int, request: Request):
    """Page de conversation avec un agent spécifique"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/agent_chat.html", {
        "request": request,
        "user": user,
        "agent_id": agent_id
    })


@router.get("/agent-config/{agent_id}", response_class=HTMLResponse)
async def agent_config(agent_id: int, request: Request):
    """Page de configuration d'un agent"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/agent_config.html", {
        "request": request,
        "user": user,
        "agent_id": agent_id
    })


@router.get("/prompts", response_class=HTMLResponse)
async def prompts(request: Request):
    """Page de la bibliothèque de prompts"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/prompts.html", {
        "request": request,
        "user": user
    })


@router.get("/lms", response_class=HTMLResponse)
async def lms(request: Request):
    """Page LMS - Formations"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/lms.html", {
        "request": request,
        "user": user
    })


@router.get("/content", response_class=HTMLResponse)
async def content(request: Request):
    """Page Content Engine"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/content.html", {
        "request": request,
        "user": user
    })


@router.get("/voice", response_class=HTMLResponse)
async def voice(request: Request):
    """Page de l'assistant vocal"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/voice.html", {
        "request": request,
        "user": user
    })


@router.get("/catalog", response_class=HTMLResponse)
async def catalog(request: Request):
    """Page du catalogue d'outils IA"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/catalog.html", {
        "request": request,
        "user": user
    })


@router.get("/automation", response_class=HTMLResponse)
async def automation(request: Request):
    """Page d'automatisation Pipedream"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/automation.html", {
        "request": request,
        "user": user
    })


@router.get("/collaboration", response_class=HTMLResponse)
async def collaboration(request: Request):
    """Page de collaboration"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/collaboration.html", {
        "request": request,
        "user": user
    })


@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    """Page Analytics"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/analytics.html", {
        "request": request,
        "user": user
    })


@router.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    """Page du blog IA - Accessible sans authentification"""
    user = get_current_user_from_cookie(request)
    
    return templates.TemplateResponse("dashboard/blog.html", {
        "request": request,
        "user": user
    })


@router.get("/media", response_class=HTMLResponse)
async def media(request: Request):
    """Page du gestionnaire de médias"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/media.html", {
        "request": request,
        "user": user
    })


@router.get("/test-inline", response_class=HTMLResponse)
async def test_inline(request: Request):
    """Page de test avec CSS inline"""
    return templates.TemplateResponse("dashboard/test_inline.html", {
        "request": request
    })

@router.get("/test-agent", response_class=HTMLResponse)
async def test_agent_page(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("dashboard/test_agent.html", {
        "request": request,
        "user": current_user
    })

@router.get("/agents-standalone", response_class=HTMLResponse)
async def agents_standalone_page(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("dashboard/agents_standalone.html", {
        "request": request,
        "user": current_user
    })

@router.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    """Page de gestion des projets web"""
    return templates.TemplateResponse("dashboard/projects.html", {
        "request": request,
        "user": current_user
    })

@router.get("/projects/create", response_class=HTMLResponse)
async def project_create_page(request: Request, current_user: dict = Depends(get_current_user_from_cookie)):
    """Page de création de projet"""
    return templates.TemplateResponse("dashboard/project_create.html", {
        "request": request,
        "user": current_user
    })

@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_details_page(request: Request, project_id: int, current_user: dict = Depends(get_current_user_from_cookie)):
    """Page de détails d'un projet"""
    return templates.TemplateResponse("dashboard/project_details.html", {
        "request": request,
        "user": current_user,
        "project_id": project_id
    })

@router.get("/projects/{project_id}/editor", response_class=HTMLResponse)
async def project_editor_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    """Page de l'éditeur de code"""
    from app.models.web_project_db import WebProject
    
    # Récupérer le projet
    project = db.query(WebProject).filter(WebProject.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    return templates.TemplateResponse("dashboard/project_editor_v3.html", {
        "request": request,
        "user": None,
        "project_id": project_id,
        "project": project
    })


# API Routes pour le dashboard
@router.get("/api/dashboard/stats")
async def get_dashboard_stats(user: dict = Depends(get_current_user_from_cookie)):
    """Récupère les statistiques du dashboard"""
    if not user:
        return {"error": "Non authentifié"}
    
    # Statistiques simulées (à remplacer par vraies données)
    return {
        "websites": 12,
        "funnels": 8,
        "conversations": 156,
        "generations": 342,
        "storage_used": "2.4 GB",
        "storage_total": "10 GB"
    }


@router.get("/api/dashboard/recent-projects")
async def get_recent_projects(user: dict = Depends(get_current_user_from_cookie)):
    """Récupère les projets récents"""
    if not user:
        return {"error": "Non authentifié"}
    
    # Projets simulés (à remplacer par vraies données)
    return {
        "projects": [
            {
                "id": 1,
                "type": "website",
                "icon": "🌐",
                "name": "Mon Portfolio",
                "status": "published",
                "updated": "Il y a 2h",
                "url": "/website-builder"
            },
            {
                "id": 2,
                "type": "funnel",
                "icon": "🎯",
                "name": "Tunnel E-commerce",
                "status": "draft",
                "updated": "Il y a 5h",
                "url": "/funnels"
            },
            {
                "id": 3,
                "type": "website",
                "icon": "🌐",
                "name": "Site Entreprise",
                "status": "published",
                "updated": "Hier",
                "url": "/website-builder"
            },
            {
                "id": 4,
                "type": "generation",
                "icon": "🎨",
                "name": "Logo Moderne",
                "status": "completed",
                "updated": "Il y a 3 jours",
                "url": "/generation"
            }
        ]
    }


@router.get("/api/dashboard/notifications")
async def get_notifications(user: dict = Depends(get_current_user_from_cookie)):
    """Récupère les notifications"""
    if not user:
        return {"error": "Non authentifié"}
    
    # Notifications simulées (à remplacer par vraies données)
    return {
        "notifications": [
            {
                "id": 1,
                "type": "success",
                "icon": "✅",
                "message": "Site 'Mon Portfolio' publié avec succès",
                "time": "Il y a 10 min",
                "read": False
            },
            {
                "id": 2,
                "type": "info",
                "icon": "ℹ️",
                "message": "Nouvelle fonctionnalité disponible : Assistant Vocal",
                "time": "Il y a 1h",
                "read": False
            },
            {
                "id": 3,
                "type": "warning",
                "icon": "⚠️",
                "message": "Votre stockage atteint 80%",
                "time": "Il y a 2h",
                "read": True
            }
        ],
        "unread_count": 2
    }


@router.get("/api/dashboard/recent-activity")
async def get_recent_activity(user: dict = Depends(get_current_user_from_cookie)):
    """Récupère l'activité récente de l'utilisateur"""
    if not user:
        return {"error": "Non authentifié"}
    
    # Activités simulées (à remplacer par vraies données depuis la DB)
    return {
        "activities": [
            {
                "icon": "🌐",
                "title": "Site web créé",
                "description": "Nouveau site 'Portfolio Moderne' créé avec succès",
                "time": "Il y a 5 minutes"
            },
            {
                "icon": "💬",
                "title": "Conversation IA",
                "description": "Discussion avec GPT-4 sur le marketing digital",
                "time": "Il y a 15 minutes"
            },
            {
                "icon": "🎨",
                "title": "Image générée",
                "description": "Logo créé avec DALL-E pour le projet E-commerce",
                "time": "Il y a 1 heure"
            },
            {
                "icon": "📧",
                "title": "Campagne email",
                "description": "Campagne 'Promo Automne' envoyée à 1,234 contacts",
                "time": "Il y a 2 heures"
            },
            {
                "icon": "🎯",
                "title": "Tunnel modifié",
                "description": "Tunnel de vente 'Formation IA' mis à jour",
                "time": "Il y a 3 heures"
            },
            {
                "icon": "📱",
                "title": "Post publié",
                "description": "Publication sur LinkedIn et Twitter",
                "time": "Il y a 4 heures"
            },
            {
                "icon": "🤖",
                "title": "Agent IA créé",
                "description": "Nouvel agent 'Support Client' configuré",
                "time": "Il y a 5 heures"
            },
            {
                "icon": "📊",
                "title": "Rapport généré",
                "description": "Analyse des performances du mois d'octobre",
                "time": "Hier"
            }
        ]
    }


@router.get("/podcasts", response_class=HTMLResponse)
async def podcasts_list(request: Request):
    """Page de liste des podcasts"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/podcasts.html", {
        "request": request,
        "user": user
    })


@router.get("/podcast/create", response_class=HTMLResponse)
async def podcast_create(request: Request):
    """Page de création de podcast"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/podcast_creator.html", {
        "request": request,
        "user": user
    })


@router.get("/avatars", response_class=HTMLResponse)
async def avatars_list(request: Request):
    """Page de liste des avatars"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/avatars.html", {
        "request": request,
        "user": user
    })


@router.get("/avatar/create", response_class=HTMLResponse)
async def avatar_create(request: Request):
    """Page de création d'avatar"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/avatar_creator.html", {
        "request": request,
        "user": user
    })


@router.get("/series", response_class=HTMLResponse)
async def series_list(request: Request):
    """Page de liste des séries"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/series.html", {
        "request": request,
        "user": user
    })


@router.get("/series/create", response_class=HTMLResponse)
async def series_create(request: Request):
    """Page de création de série"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/series_creator.html", {
        "request": request,
        "user": user
    })


@router.get("/series/{series_id}", response_class=HTMLResponse)
async def series_detail(request: Request, series_id: int):
    """Page de détail d'une série"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/series_detail.html", {
        "request": request,
        "user": user,
        "series_id": series_id
    })


@router.get("/pwa", response_class=HTMLResponse)
async def pwa_list(request: Request):
    """Page de liste des PWA"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/pwa.html", {
        "request": request,
        "user": user
    })


@router.get("/pwa/create", response_class=HTMLResponse)
async def pwa_create(request: Request):
    """Page de création de PWA"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/pwa_creator.html", {
        "request": request,
        "user": user
    })


@router.get("/documents", response_class=HTMLResponse)
async def documents_list(request: Request):
    """Page analyseur de documents"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/document_analyzer.html", {
        "request": request,
        "user": user
    })


@router.get("/documents/{document_id}", response_class=HTMLResponse)
async def document_detail(request: Request, document_id: int):
    """Page détail d'un document"""
    user = get_current_user_from_cookie(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("dashboard/document_detail.html", {
        "request": request,
        "user": user,
        "document_id": document_id
    })
