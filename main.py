"""
WeBox Multi-IA - Application FastAPI avec Architecture MVC
Point d'entrée principal de l'application
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.middleware.auth import get_current_user_from_cookie
from pathlib import Path

# Importer les modules existants
from modules.core.landing_page.model import LandingPageData

# Créer l'application FastAPI
app = FastAPI(
    title="WeBox Multi-IA",
    description="L'Interface IA la Plus Complète du Marché",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer le dossier uploads s'il n'existe pas
Path("uploads").mkdir(exist_ok=True)

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configurer les templates Jinja2
templates = Jinja2Templates(directory="templates")

# Ajouter un context processor pour le cache busting
import time
def add_cache_buster(request: Request):
    return {"cache_version": int(time.time())}

templates.env.globals['cache_version'] = int(time.time())

# Charger les données de la landing page
landing_data = LandingPageData()

# Importer les routes
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.chat_routes import router as chat_router
from app.routes.stats_routes import router as stats_router
from app.routes.assistants_routes import router as assistants_router
from app.routes.prompts_routes import router as prompts_router
from app.routes.generation_routes import router as generation_router

# Importer et inclure les routes podcast
from app.routes.podcast_routes import router as podcast_router

# Importer et inclure les routes avatar
from app.routes.avatar_routes import router as avatar_router

# Importer et inclure les routes AI Agent
from app.routes.ai_agent_routes import router as ai_agent_router

# Importer et inclure les routes Series
from app.routes.series_routes import router as series_router

# Importer et inclure les routes PWA
from app.routes.pwa_routes import router as pwa_router

# Importer et inclure les routes React Native
from app.routes.react_native_routes import router as react_native_router

# Importer et inclure les routes Analytics
from app.routes.analytics_routes import router as analytics_router

# Importer et inclure les routes Documents
from app.routes.document_routes import router as document_router

# Inclure les routes
app.include_router(auth_router, tags=["Authentication"])
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(chat_router, tags=["Chat"])
app.include_router(stats_router, tags=["Statistics"])
app.include_router(assistants_router, tags=["Assistants"])
app.include_router(prompts_router, tags=["Prompts"])
app.include_router(generation_router, tags=["Generation"])
app.include_router(podcast_router, tags=["Podcasts"])
app.include_router(avatar_router, tags=["Avatars"])
app.include_router(ai_agent_router, tags=["AI Agent"])
app.include_router(series_router, tags=["Series"])
app.include_router(pwa_router, tags=["PWA"])
app.include_router(react_native_router, tags=["React Native"])
app.include_router(analytics_router, tags=["Analytics"])
app.include_router(document_router, tags=["Documents"])

# Importer et inclure les routes profil
from app.routes.profile_routes import router as profile_router
app.include_router(profile_router, tags=["Profile"])

# Importer et inclure les routes admin
from app.routes.admin_routes import router as admin_router
app.include_router(admin_router, tags=["Admin"])

# Route page admin principale
@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    """Page d'administration principale"""
    user = get_current_user_from_cookie(request)
    
    # Rediriger vers login si non connecté
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Vérifier si admin
    if not user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    return templates.TemplateResponse("dashboard/admin_analytics.html", {
        "request": request,
        "user": user
    })

# Importer et inclure les routes blog
from app.routes.blog_routes import router as blog_router
app.include_router(blog_router, tags=["Blog"])

# Importer et inclure les routes media
from app.routes.media_routes import router as media_router
app.include_router(media_router, tags=["Media"])

# Importer et inclure les routes voice
from app.routes.voice_routes import router as voice_router
app.include_router(voice_router, tags=["Voice"])

# Importer et inclure les routes combinations
from app.routes.combinations_routes import router as combinations_router
app.include_router(combinations_router, tags=["Combinations"])

# Importer et inclure les routes documentation
from app.routes.documentation_routes import router as documentation_router
app.include_router(documentation_router, tags=["Documentation"])

# Importer et inclure les routes projets web (Studio Web IA)
from app.routes.web_projects_routes import router as web_projects_router
app.include_router(web_projects_router, tags=["Web Projects"])

# Importer et inclure les routes social
from app.routes.social_routes import router as social_router
app.include_router(social_router, tags=["Social"])

# Importer et inclure les routes influencers
from app.routes.influencer_routes import router as influencer_router
app.include_router(influencer_router, tags=["Influencers"])

# Importer et inclure les routes business (Logos, Présentations, Landing Pages)
from app.routes.business_routes import router as business_router
app.include_router(business_router, tags=["Business"])

# DEPRECATED : Anciennes routes funnels (remplacées par marketing_routes)
# from app.routes.funnel_routes import router as funnel_router
# app.include_router(funnel_router, tags=["Funnels"])

# Importer et inclure les routes website
from app.routes.website_routes import router as website_router
app.include_router(website_router, tags=["Website"])

# Importer et inclure les routes AI Chat
from app.routes.ai_chat_routes import router as ai_chat_router
app.include_router(ai_chat_router, tags=["AI Chat"])

# Importer et inclure les routes Git
from app.routes.git_routes import router as git_router
app.include_router(git_router, tags=["Git"])

# Importer et inclure les routes Deployment
from app.routes.deployment_routes import router as deployment_router
app.include_router(deployment_router, tags=["Deployment"])

# Importer et inclure les routes Templates
from app.routes.template_routes import router as template_router
app.include_router(template_router, tags=["Templates"])

# Importer et inclure les routes Voice Automation
from app.routes.voice_automation_routes import router as voice_automation_router
app.include_router(voice_automation_router, tags=["Voice Automation"])

# Importer et inclure les routes LMS
from app.routes.lms_routes import router as lms_router
app.include_router(lms_router, tags=["LMS"])

# Importer et inclure les routes Content Engine
from app.routes.content_routes import router as content_router
app.include_router(content_router, tags=["Content Engine"])

# Importer et inclure les routes Marketing
from app.routes.marketing_routes import router as marketing_router, router_pages as marketing_pages_router
app.include_router(marketing_router, tags=["Marketing"])
app.include_router(marketing_pages_router, tags=["Marketing Pages"])

# Importer et inclure les routes Agents IA
from app.routes.agent_routes import router as agent_router
app.include_router(agent_router, tags=["Agents"])

# Importer et inclure les routes Marketplace
from app.routes.marketplace_routes import router as marketplace_router
app.include_router(marketplace_router, tags=["Marketplace"])

# Importer et inclure les routes Notifications
from app.routes.notifications_routes import router as notifications_router
app.include_router(notifications_router, tags=["Notifications"])

# Importer et inclure les nouvelles routes Notification WebSocket
from app.routes.notification_routes import router as notification_ws_router
app.include_router(notification_ws_router, tags=["Notifications WebSocket"])

# Importer et inclure les routes Settings
from app.routes.settings_routes import router as settings_router
app.include_router(settings_router, tags=["Settings"])

# Importer et inclure les routes Support
from app.routes.support_routes import router as support_router
app.include_router(support_router, tags=["Support"])

# Importer et inclure les routes Account
from app.routes.account_routes import router as account_router
app.include_router(account_router, tags=["Account"])

# Importer et inclure les routes Activities
from app.routes.activities_routes import router as activities_router
app.include_router(activities_router, tags=["Activities"])

# Importer et inclure les routes Payment
from app.routes.payment_routes import router as payment_router
app.include_router(payment_router, tags=["Payment"])

# Importer et inclure les routes Orders
from app.routes.orders_routes import router as orders_router
app.include_router(orders_router, tags=["Orders"])

# Importer et inclure les routes Cart
from app.routes.cart_routes import router as cart_router
app.include_router(cart_router, prefix="/api", tags=["Cart"])

# Importer et inclure les routes Search
from app.routes.search_routes import router as search_router
app.include_router(search_router, tags=["Search"])

# Importer et inclure les routes Promo Codes
from app.routes.promo_routes import router as promo_router
app.include_router(promo_router, tags=["Promo Codes"])

# Importer et inclure les routes Invoices
from app.routes.invoice_routes import router as invoice_router
app.include_router(invoice_router, tags=["Invoices"])

# Importer et inclure les routes Tickets
from app.routes.ticket_routes import router as ticket_router
app.include_router(ticket_router, tags=["Support Tickets"])

# Importer et inclure les routes Security
from app.routes.security_routes import router as security_router
app.include_router(security_router, tags=["Security"])

# Importer et inclure les routes Monitoring
from app.routes.monitoring_routes import router as monitoring_router
app.include_router(monitoring_router, tags=["Monitoring"])

# Importer et inclure les routes 2FA
from app.routes.twofa_routes import router as twofa_router
app.include_router(twofa_router, tags=["2FA"])

# Importer et inclure les routes Cache
from app.routes.cache_routes import router as cache_router
app.include_router(cache_router, tags=["Cache"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil / Landing page"""
    user = get_current_user_from_cookie(request)
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": user,
        "title_emoji": landing_data.TITLE_EMOJI,
        "title_webox": landing_data.TITLE_WEBOX,
        "title_multi_ia": landing_data.TITLE_MULTI_IA,
        "subtitle": landing_data.SUBTITLE,
        "hero_features": landing_data.HERO_FEATURES,
        "hero_description": landing_data.HERO_DESCRIPTION,
        "stats": landing_data.STATS,
        "features_col1": landing_data.FEATURES_COL1,
        "features_col2": landing_data.FEATURES_COL2,
        "features_col3": landing_data.FEATURES_COL3,
        "testimonials": landing_data.TESTIMONIALS,
        "why_choose": landing_data.WHY_CHOOSE,
        "version": landing_data.VERSION,
        "footer_tagline": landing_data.FOOTER_TAGLINE,
        "footer_features": landing_data.FOOTER_FEATURES,
        "copyright": landing_data.COPYRIGHT,
    })


@app.get("/health")
async def health():
    """Endpoint de santé"""
    return {"status": "ok", "app": "WeBox Multi-IA", "version": "2.0.0"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
