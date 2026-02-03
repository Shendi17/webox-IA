"""
Routes API pour les Agents IA
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_db import UserDB
from app.models.ai_agent import AIAgent
from app.middleware.auth import get_current_user_from_token, get_current_user_from_cookie
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter()

@router.get("/api/agents/stats")
async def get_agent_stats(
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Récupérer les statistiques globales des agents
    """
    # TODO: Récupérer les vraies données de la base
    # Pour l'instant, données simulées
    
    return {
        "total_conversations": 633,
        "total_tasks": 1691,
        "time_saved": 73,
        "avg_satisfaction": 94
    }


@router.get("/api/agents/conversations/recent")
async def get_recent_conversations(
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Récupérer l'historique des conversations récentes
    """
    # TODO: Récupérer les vraies données de la base
    # Pour l'instant, données simulées
    
    agents_data = [
        {
            "icon": "💰",
            "agent_name": "Agent Ventes",
            "first_message": "Comment améliorer mon taux de conversion sur les landing pages ?",
            "time_ago": "Il y a 2h",
            "message_count": 12,
            "rating": 4.8
        },
        {
            "icon": "📢",
            "agent_name": "Agent Marketing",
            "first_message": "Créer une stratégie de contenu pour LinkedIn",
            "time_ago": "Hier",
            "message_count": 8,
            "rating": 5.0
        },
        {
            "icon": "💵",
            "agent_name": "Agent Finance",
            "first_message": "Analyse de trésorerie et prévisions Q4",
            "time_ago": "Il y a 2 jours",
            "message_count": 15,
            "rating": 4.9
        },
        {
            "icon": "⚙️",
            "agent_name": "Agent Opérations",
            "first_message": "Optimiser le workflow de production",
            "time_ago": "Il y a 3 jours",
            "message_count": 10,
            "rating": 4.7
        },
        {
            "icon": "💬",
            "agent_name": "Agent Service Client",
            "first_message": "Automatiser les réponses FAQ",
            "time_ago": "Il y a 4 jours",
            "message_count": 18,
            "rating": 4.9
        }
    ]
    
    return {
        "conversations": agents_data
    }


@router.get("/api/agents/performance")
async def get_agent_performance(
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Récupérer les performances détaillées par agent
    """
    # TODO: Récupérer les vraies données de la base
    # Pour l'instant, données simulées
    
    performances = [
        {
            "agent_type": "ventes",
            "agent_name": "Agent Ventes",
            "icon": "💰",
            "conversations": 156,
            "tasks": 423,
            "time_saved": 18,
            "satisfaction": 4.8,
            "trend": "+15%"
        },
        {
            "agent_type": "marketing",
            "agent_name": "Agent Marketing",
            "icon": "📢",
            "conversations": 134,
            "tasks": 389,
            "time_saved": 15,
            "satisfaction": 4.9,
            "trend": "+22%"
        },
        {
            "agent_type": "finance",
            "agent_name": "Agent Finance",
            "icon": "💵",
            "conversations": 98,
            "tasks": 267,
            "time_saved": 12,
            "satisfaction": 4.7,
            "trend": "+8%"
        },
        {
            "agent_type": "operations",
            "agent_name": "Agent Opérations",
            "icon": "⚙️",
            "conversations": 112,
            "tasks": 345,
            "time_saved": 14,
            "satisfaction": 4.6,
            "trend": "+12%"
        },
        {
            "agent_type": "service-client",
            "agent_name": "Agent Service Client",
            "icon": "💬",
            "conversations": 245,
            "tasks": 612,
            "time_saved": 28,
            "satisfaction": 4.9,
            "trend": "+31%"
        },
        {
            "agent_type": "rh",
            "agent_name": "Agent RH",
            "icon": "👤",
            "conversations": 87,
            "tasks": 234,
            "time_saved": 10,
            "satisfaction": 4.5,
            "trend": "+5%"
        },
        {
            "agent_type": "produit",
            "agent_name": "Agent Produit",
            "icon": "🎯",
            "conversations": 76,
            "tasks": 198,
            "time_saved": 9,
            "satisfaction": 4.8,
            "trend": "+18%"
        },
        {
            "agent_type": "strategie",
            "agent_name": "Agent Stratégie",
            "icon": "🎯",
            "conversations": 65,
            "tasks": 156,
            "time_saved": 8,
            "satisfaction": 4.7,
            "trend": "+10%"
        }
    ]
    
    return {
        "performances": performances
    }


class AgentCreate(BaseModel):
    name: str
    category: str
    description: str
    instructions: str
    model: str = "gpt-4"
    temperature: float = 0.7


@router.get("/api/agents/my-agents")
async def get_my_agents(
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Récupérer les agents de l'utilisateur
    """
    agents = db.query(AIAgent).filter(
        AIAgent.user_id == current_user["user_id"],
        AIAgent.is_marketplace == False
    ).all()
    
    return {"agents": [agent.to_dict() for agent in agents]}


@router.get("/api/agents/marketplace")
async def get_marketplace_agents(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupérer les agents de la marketplace
    """
    query = db.query(AIAgent).filter(AIAgent.is_marketplace == True)
    
    if category:
        query = query.filter(AIAgent.category == category)
    
    agents = query.order_by(AIAgent.downloads.desc()).all()
    return {"agents": [agent.to_dict() for agent in agents]}


@router.post("/api/agents/create")
async def create_agent(
    request: Request,
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Créer un nouvel agent
    """
    new_agent = AIAgent(
        user_id=current_user["user_id"],
        name=agent_data.name,
        category=agent_data.category,
        description=agent_data.description,
        instructions=agent_data.instructions,
        model=agent_data.model,
        temperature=agent_data.temperature,
        icon="🤖",
        status="active",
        features=[]
    )
    
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    
    return {"success": True, "agent": new_agent.to_dict()}


@router.post("/api/agents/install/{agent_id}")
async def install_marketplace_agent(
    agent_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Installer un agent depuis la marketplace
    """
    marketplace_agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id,
        AIAgent.is_marketplace == True
    ).first()
    
    if not marketplace_agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    # Créer une copie pour l'utilisateur
    user_agent = AIAgent(
        user_id=current_user["user_id"],
        name=marketplace_agent.name,
        icon=marketplace_agent.icon,
        category=marketplace_agent.category,
        description=marketplace_agent.description,
        features=marketplace_agent.features,
        model=marketplace_agent.model,
        temperature=marketplace_agent.temperature,
        instructions=marketplace_agent.instructions,
        status="active"
    )
    
    db.add(user_agent)
    
    # Incrémenter les téléchargements
    marketplace_agent.downloads += 1
    
    db.commit()
    db.refresh(user_agent)
    
    return {"success": True, "agent": user_agent.to_dict()}


@router.put("/api/agents/{agent_id}")
async def update_agent(
    agent_id: int,
    request: Request,
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Mettre à jour un agent
    """
    agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id,
        AIAgent.user_id == current_user["user_id"]
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    # Mettre à jour les champs
    agent.name = agent_data.name
    agent.category = agent_data.category
    agent.description = agent_data.description
    agent.instructions = agent_data.instructions
    agent.model = agent_data.model
    agent.temperature = agent_data.temperature
    
    db.commit()
    db.refresh(agent)
    
    return {"success": True, "agent": agent.to_dict()}


@router.delete("/api/agents/{agent_id}")
async def delete_agent(
    agent_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    current_user = get_current_user_from_cookie(request)
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    """
    Supprimer un agent
    """
    agent = db.query(AIAgent).filter(
        AIAgent.id == agent_id,
        AIAgent.user_id == current_user["user_id"]
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")
    
    db.delete(agent)
    db.commit()
    
    return {"success": True, "message": "Agent supprimé"}
