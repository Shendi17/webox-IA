"""
Routes API pour les statistiques utilisateur
Date : 1er Novembre 2025
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from app.models.conversation_db import ConversationDB, MessageDB

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get("/overview")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
) -> Dict:
    """
    Récupérer les statistiques globales de l'utilisateur
    """
    user_id = current_user["id"]
    
    # Nombre total de conversations
    total_conversations = db.query(func.count(ConversationDB.id)).filter(
        ConversationDB.user_id == user_id
    ).scalar()
    
    # Nombre total de messages
    total_messages = db.query(func.count(MessageDB.id)).join(
        ConversationDB
    ).filter(
        ConversationDB.user_id == user_id
    ).scalar()
    
    # Messages utilisateur vs IA
    user_messages = db.query(func.count(MessageDB.id)).join(
        ConversationDB
    ).filter(
        ConversationDB.user_id == user_id,
        MessageDB.role == "user"
    ).scalar()
    
    ai_messages = db.query(func.count(MessageDB.id)).join(
        ConversationDB
    ).filter(
        ConversationDB.user_id == user_id,
        MessageDB.role == "assistant"
    ).scalar()
    
    # Temps de réponse moyen
    avg_response_time = db.query(func.avg(MessageDB.response_time)).join(
        ConversationDB
    ).filter(
        ConversationDB.user_id == user_id,
        MessageDB.response_time.isnot(None)
    ).scalar()
    
    # Conversations cette semaine
    week_ago = datetime.utcnow() - timedelta(days=7)
    conversations_this_week = db.query(func.count(ConversationDB.id)).filter(
        ConversationDB.user_id == user_id,
        ConversationDB.created_at >= week_ago
    ).scalar()
    
    # IA les plus utilisées
    ai_usage = db.query(
        MessageDB.ai_provider,
        func.count(MessageDB.id).label('count')
    ).join(
        ConversationDB
    ).filter(
        ConversationDB.user_id == user_id,
        MessageDB.ai_provider.isnot(None)
    ).group_by(
        MessageDB.ai_provider
    ).order_by(
        func.count(MessageDB.id).desc()
    ).limit(5).all()
    
    # Formater les résultats
    ai_usage_dict = {}
    for provider, count in ai_usage:
        # Séparer les providers multiples
        providers = provider.split(',') if provider else []
        for p in providers:
            p = p.strip()
            if p:
                ai_usage_dict[p] = ai_usage_dict.get(p, 0) + count
    
    # Trier par utilisation
    top_ai = sorted(ai_usage_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total_conversations": total_conversations or 0,
        "total_messages": total_messages or 0,
        "user_messages": user_messages or 0,
        "ai_messages": ai_messages or 0,
        "avg_response_time": round(avg_response_time) if avg_response_time else 0,
        "conversations_this_week": conversations_this_week or 0,
        "top_ai_providers": [{"name": name, "count": count} for name, count in top_ai]
    }


@router.get("/activity")
async def get_activity_stats(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
) -> List[Dict]:
    """
    Récupérer l'activité quotidienne de l'utilisateur
    """
    user_id = current_user["id"]
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Activité par jour
    daily_activity = db.query(
        func.date(ConversationDB.created_at).label('date'),
        func.count(ConversationDB.id).label('conversations'),
        func.count(MessageDB.id).label('messages')
    ).join(
        MessageDB, ConversationDB.id == MessageDB.conversation_id, isouter=True
    ).filter(
        ConversationDB.user_id == user_id,
        ConversationDB.created_at >= start_date
    ).group_by(
        func.date(ConversationDB.created_at)
    ).order_by(
        func.date(ConversationDB.created_at)
    ).all()
    
    # Formater les résultats
    result = []
    for date, conversations, messages in daily_activity:
        result.append({
            "date": date.isoformat() if date else None,
            "conversations": conversations or 0,
            "messages": messages or 0
        })
    
    return result


@router.get("/folders")
async def get_folder_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
) -> List[Dict]:
    """
    Récupérer les statistiques par dossier
    """
    user_id = current_user["id"]
    
    folder_stats = db.query(
        ConversationDB.folder,
        func.count(ConversationDB.id).label('count')
    ).filter(
        ConversationDB.user_id == user_id
    ).group_by(
        ConversationDB.folder
    ).order_by(
        func.count(ConversationDB.id).desc()
    ).all()
    
    return [
        {
            "folder": folder or "Sans dossier",
            "count": count
        }
        for folder, count in folder_stats
    ]


@router.get("/recent-conversations")
async def get_recent_conversations(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
) -> List[Dict]:
    """
    Récupérer les conversations récentes
    """
    user_id = current_user["id"]
    
    recent = db.query(ConversationDB).filter(
        ConversationDB.user_id == user_id
    ).order_by(
        ConversationDB.updated_at.desc()
    ).limit(limit).all()
    
    result = []
    for conv in recent:
        message_count = len(conv.messages)
        result.append({
            "id": conv.id,
            "title": conv.title,
            "folder": conv.folder,
            "message_count": message_count,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat()
        })
    
    return result
