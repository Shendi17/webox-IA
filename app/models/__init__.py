"""
Modèles de données SQLAlchemy
Date : 10 Novembre 2025
"""

# Importer les modèles pour Alembic
from app.models.user import User
from .user import User, UserCreate, UserLogin, UserInDB

# Modèles de génération
from .generation_db import (
    GeneratedImageDB,
    GeneratedVideoDB,
    GeneratedAudioDB,
    EBookDB,
    VideoShortDB,
    WorkflowDB,
    WorkflowExecutionDB,
    CatalogFavoriteDB,
    GeneratedAdDB
)

# Modèles de réseaux sociaux
from .social_db import (
    SocialAccountDB,
    ScheduledPostDB,
    PostAnalyticsDB
)

# Modèles d'influenceurs IA
from .influencer_db import (
    AIInfluencerDB,
    InfluencerContentDB
)

# Modèles d'outils business
from .business_db import (
    GeneratedLogoDB,
    PresentationDB,
    EmailCampaignDB,
    LandingPageDB
)

# Modèles de tunnels de vente
from .funnel_db import (
    FunnelDB,
    FunnelAnalyticsDB,
    FunnelContactDB
)

# Modèles de website builder
from .website_db import (
    WebsiteDB,
    WebsitePageDB,
    BlogPostDB,
    WebsiteAnalyticsDB
)

# Modèles de projets web (Studio Web IA)
from .web_project_db import (
    WebProject,
    ProjectFile,
    Deployment,
    ProjectCommit,
    ProjectAIAction,
    ProjectTemplate
)

__all__ = [
    "User", 
    "UserCreate", 
    "UserLogin", 
    "UserInDB",
    "GeneratedImageDB",
    "GeneratedVideoDB",
    "GeneratedAudioDB",
    "EBookDB",
    "VideoShortDB",
    "WorkflowDB",
    "WorkflowExecutionDB",
    "CatalogFavoriteDB",
    "GeneratedAdDB",
    "SocialAccountDB",
    "ScheduledPostDB",
    "PostAnalyticsDB",
    "AIInfluencerDB",
    "InfluencerContentDB",
    "GeneratedLogoDB",
    "PresentationDB",
    "EmailCampaignDB",
    "LandingPageDB",
    "FunnelDB",
    "FunnelAnalyticsDB",
    "FunnelContactDB",
    "WebsiteDB",
    "WebsitePageDB",
    "BlogPostDB",
    "WebsiteAnalyticsDB",
    "WebProject",
    "ProjectFile",
    "Deployment",
    "ProjectCommit",
    "ProjectAIAction",
    "ProjectTemplate"
]
