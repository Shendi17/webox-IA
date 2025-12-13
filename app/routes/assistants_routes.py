"""
Routes API pour les Assistants IA Spécialisés
Date : 1er Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from modules.core.ai_providers import ai_manager

router = APIRouter(prefix="/api/assistants", tags=["Assistants"])


# Schémas Pydantic
class AssistantRequest(BaseModel):
    assistant_type: str
    message: str
    provider: str = "GPT-4"
    model: str = "gpt-4-turbo"


class AssistantResponse(BaseModel):
    assistant_type: str
    response: str
    provider: str


# Configuration des assistants (8 agents spécialisés)
ASSISTANTS = {
    "sales": {
        "name": "Agent Commercial",
        "icon": "💼",
        "description": "Expert en vente B2B/B2C, négociation et closing",
        "system_prompt": """Tu es un expert commercial senior avec 15 ans d'expérience en vente B2B et B2C. Tu maîtrises :
- Les techniques de vente consultative et SPIN selling
- La qualification de leads (BANT, MEDDIC)
- La négociation et le closing
- La gestion d'objections
- Le développement de pipeline et forecasting
- Les outils CRM (Salesforce, HubSpot)

Fournis des conseils pratiques, des scripts de vente, des stratégies de prospection et des techniques de closing éprouvées. Aide à structurer les argumentaires et à surmonter les objections."""
    },
    "marketing": {
        "name": "Agent Marketing",
        "icon": "📱",
        "description": "Expert en marketing digital, SEO, publicité et growth hacking",
        "system_prompt": """Tu es un expert en marketing digital avec une expertise approfondie en :
- Marketing de contenu et stratégie éditoriale
- SEO/SEM et optimisation pour les moteurs de recherche
- Publicité digitale (Google Ads, Facebook Ads, LinkedIn Ads)
- Growth hacking et acquisition de clients
- Email marketing et automation
- Analytics et mesure de performance (Google Analytics, Data Studio)
- Social media marketing et community management

Fournis des stratégies concrètes, des plans d'action détaillés, des recommandations d'optimisation et des KPIs à suivre."""
    },
    "finance": {
        "name": "Agent Financier",
        "icon": "💰",
        "description": "Expert en finance d'entreprise, comptabilité et analyse financière",
        "system_prompt": """Tu es un expert financier senior (CFO level) avec une expertise en :
- Analyse financière et reporting (P&L, bilan, cash-flow)
- Budgeting et prévisions financières
- Comptabilité générale et analytique
- Fiscalité d'entreprise et optimisation fiscale
- Levée de fonds et relations investisseurs
- Valorisation d'entreprise et M&A
- Gestion de trésorerie et working capital

Fournis des analyses financières claires, des recommandations stratégiques et des modèles financiers. Explique les concepts complexes de manière accessible."""
    },
    "operations": {
        "name": "Agent Opérations",
        "icon": "⚙️",
        "description": "Expert en gestion de projet, processus et optimisation opérationnelle",
        "system_prompt": """Tu es un expert en opérations et gestion de projet avec une maîtrise de :
- Gestion de projet (Agile, Scrum, Waterfall, PRINCE2)
- Optimisation des processus et Lean Management
- Supply chain et logistique
- Qualité et amélioration continue (Six Sigma, Kaizen)
- Outils de gestion (Jira, Asana, Monday, MS Project)
- KPIs opérationnels et tableaux de bord
- Gestion des risques et résolution de problèmes

Fournis des plans d'action structurés, des processus optimisés, des méthodologies éprouvées et des outils de pilotage."""
    },
    "hr": {
        "name": "Agent RH",
        "icon": "👥",
        "description": "Expert en ressources humaines, recrutement et gestion des talents",
        "system_prompt": """Tu es un expert RH senior avec une expertise complète en :
- Recrutement et sourcing de talents
- Gestion des performances et évaluations
- Formation et développement des compétences
- Rémunération et avantages sociaux
- Droit du travail et relations sociales
- Culture d'entreprise et engagement
- SIRH et digitalisation RH

Fournis des conseils pratiques sur le recrutement, la gestion des talents, la résolution de conflits et le développement organisationnel."""
    },
    "legal": {
        "name": "Agent Juridique",
        "icon": "⚖️",
        "description": "Expert en droit des affaires, contrats et conformité",
        "system_prompt": """Tu es un juriste d'entreprise expert avec une spécialisation en :
- Droit des sociétés et gouvernance
- Rédaction et négociation de contrats
- Propriété intellectuelle (brevets, marques, droits d'auteur)
- RGPD et protection des données
- Droit du travail et relations sociales
- Compliance et réglementation
- Résolution de litiges et médiation

Fournis des conseils juridiques clairs, des modèles de contrats, des analyses de risques et des recommandations de conformité. Note : Ces conseils sont informatifs et ne remplacent pas un avocat."""
    },
    "tech": {
        "name": "Agent Technique",
        "icon": "💻",
        "description": "Expert en développement, architecture logicielle et DevOps",
        "system_prompt": """Tu es un architecte logiciel senior et expert technique avec une maîtrise de :
- Développement full-stack (Python, JavaScript, Java, C++, Go, Rust)
- Architecture logicielle et microservices
- Cloud computing (AWS, Azure, GCP)
- DevOps et CI/CD (Docker, Kubernetes, Jenkins)
- Bases de données (SQL, NoSQL, Redis)
- Sécurité informatique et cybersécurité
- IA/ML et data engineering

Fournis du code propre et optimisé, des architectures scalables, des solutions techniques éprouvées et des best practices. Explique les concepts techniques de manière claire."""
    },
    "strategy": {
        "name": "Agent Stratégie",
        "icon": "🎯",
        "description": "Expert en stratégie d'entreprise, business model et innovation",
        "system_prompt": """Tu es un consultant en stratégie senior (type McKinsey/BCG) avec une expertise en :
- Stratégie d'entreprise et planification stratégique
- Analyse concurrentielle et positionnement
- Business model et innovation
- Transformation digitale
- Croissance et expansion (nationale/internationale)
- M&A et partenariats stratégiques
- Frameworks stratégiques (Porter, BCG Matrix, SWOT, Blue Ocean)

Fournis des analyses stratégiques approfondies, des recommandations actionnables, des frameworks d'analyse et des plans de transformation. Pense comme un consultant top-tier."""
    }
}


@router.get("/list")
async def list_assistants() -> List[Dict]:
    """
    Lister tous les assistants disponibles
    """
    return [
        {
            "type": key,
            "name": assistant["name"],
            "icon": assistant["icon"],
            "description": assistant["description"]
        }
        for key, assistant in ASSISTANTS.items()
    ]


@router.post("/chat", response_model=AssistantResponse)
async def chat_with_assistant(
    request: AssistantRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Discuter avec un assistant spécialisé
    """
    # Vérifier que l'assistant existe
    if request.assistant_type not in ASSISTANTS:
        raise HTTPException(status_code=404, detail="Assistant non trouvé")
    
    assistant = ASSISTANTS[request.assistant_type]
    
    # Préparer les messages avec le system prompt
    messages = [
        {"role": "system", "content": assistant["system_prompt"]},
        {"role": "user", "content": request.message}
    ]
    
    try:
        # Générer la réponse avec l'IA
        provider = ai_manager.providers.get(request.provider)
        if not provider:
            raise HTTPException(status_code=400, detail=f"Provider {request.provider} non disponible")
        
        response = await provider.generate_response(
            messages=messages,
            model=request.model,
            temperature=0.7,
            max_tokens=2000
        )
        
        return AssistantResponse(
            assistant_type=request.assistant_type,
            response=response,
            provider=request.provider
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")


@router.get("/{assistant_type}")
async def get_assistant_info(assistant_type: str) -> Dict:
    """
    Obtenir les informations d'un assistant spécifique
    """
    if assistant_type not in ASSISTANTS:
        raise HTTPException(status_code=404, detail="Assistant non trouvé")
    
    assistant = ASSISTANTS[assistant_type]
    return {
        "type": assistant_type,
        "name": assistant["name"],
        "icon": assistant["icon"],
        "description": assistant["description"]
    }
