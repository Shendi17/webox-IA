"""
Routes API pour les Agents IA
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_db import UserDB
from app.middleware.auth import get_current_user_from_token
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/api/agents/stats")
async def get_agent_stats(
    current_user: UserDB = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
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
    current_user: UserDB = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
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
    current_user: UserDB = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
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
