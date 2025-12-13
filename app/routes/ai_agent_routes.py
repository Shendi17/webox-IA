from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import json
from app.database import get_db
from app.models.ai_agent import AgentConversation, AgentMessage
from app.services.ai_agent_service import AIAgentService

router = APIRouter(prefix="/api/agent", tags=["ai-agent"])
agent_service = AIAgentService()

# Modèles Pydantic
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    model: str = "gemini-2.0-flash"

class ConversationCreate(BaseModel):
    title: Optional[str] = None
    context: Optional[str] = None
    model: str = "gemini-2.0-flash"

# Routes HTTP
@router.get("/models")
async def get_models():
    """Obtenir la liste des modèles disponibles"""
    try:
        models = agent_service.get_available_models()
        return {
            "success": True,
            "models": models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quick-actions")
async def get_quick_actions():
    """Obtenir les actions rapides"""
    try:
        actions = agent_service.get_quick_actions()
        return {
            "success": True,
            "actions": actions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat(chat_data: ChatMessage, db: Session = Depends(get_db)):
    """Envoyer un message à l'agent IA"""
    try:
        # Générer ou récupérer la session
        session_id = chat_data.session_id or agent_service.generate_session_id()
        
        # Récupérer ou créer la conversation
        conversation = db.query(AgentConversation).filter(
            AgentConversation.session_id == session_id
        ).first()
        
        if not conversation:
            # Créer une nouvelle conversation
            title = agent_service.generate_title(chat_data.message)
            conversation = AgentConversation(
                user_id=1,  # TODO: Récupérer l'utilisateur authentifié
                session_id=session_id,
                title=title,
                model=chat_data.model
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Récupérer l'historique
        history_messages = db.query(AgentMessage).filter(
            AgentMessage.session_id == session_id
        ).order_by(AgentMessage.created_at).all()
        
        history = [{"role": msg.role, "content": msg.content} for msg in history_messages]
        
        # Sauvegarder le message utilisateur
        user_message = AgentMessage(
            conversation_id=conversation.id,
            session_id=session_id,
            role="user",
            content=chat_data.message
        )
        db.add(user_message)
        
        # Envoyer à l'IA
        response = await agent_service.chat(chat_data.message, history, chat_data.model)
        
        if not response.get("success"):
            return {
                "success": False,
                "error": response.get("error")
            }
        
        # Sauvegarder la réponse de l'IA
        assistant_message = AgentMessage(
            conversation_id=conversation.id,
            session_id=session_id,
            role="assistant",
            content=response["content"],
            model=response.get("model"),
            tokens=response.get("tokens"),
            response_time=response.get("response_time")
        )
        db.add(assistant_message)
        
        # Mettre à jour les statistiques de la conversation
        conversation.messages_count += 2
        conversation.tokens_used += response.get("tokens", 0)
        
        db.commit()
        db.refresh(assistant_message)
        
        return {
            "success": True,
            "message": assistant_message.to_dict(),
            "session_id": session_id,
            "conversation_id": conversation.id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
async def list_conversations(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lister les conversations"""
    try:
        total = db.query(AgentConversation).count()
        conversations = db.query(AgentConversation).order_by(
            AgentConversation.updated_at.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "conversations": [c.to_dict() for c in conversations],
            "total": total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Obtenir les messages d'une conversation"""
    try:
        messages = db.query(AgentMessage).filter(
            AgentMessage.conversation_id == conversation_id
        ).order_by(AgentMessage.created_at).all()
        
        return {
            "success": True,
            "messages": [m.to_dict() for m in messages]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer une conversation"""
    try:
        # Supprimer les messages
        db.query(AgentMessage).filter(
            AgentMessage.conversation_id == conversation_id
        ).delete()
        
        # Supprimer la conversation
        conversation = db.query(AgentConversation).filter(
            AgentConversation.id == conversation_id
        ).first()
        
        if conversation:
            db.delete(conversation)
            db.commit()
        
        return {
            "success": True,
            "message": "Conversation supprimée"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_conversations = db.query(AgentConversation).count()
        total_messages = db.query(AgentMessage).count()
        total_tokens = db.query(AgentConversation).with_entities(
            db.func.sum(AgentConversation.tokens_used)
        ).scalar() or 0
        
        return {
            "success": True,
            "stats": {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "total_tokens": total_tokens
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket pour chat en temps réel
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, db: Session = Depends(get_db)):
    """WebSocket pour chat en temps réel"""
    await websocket.accept()
    
    try:
        while True:
            # Recevoir le message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message = message_data.get("message")
            model = message_data.get("model", "gemini-2.0-flash")
            
            if not message:
                continue
            
            # Récupérer la conversation
            conversation = db.query(AgentConversation).filter(
                AgentConversation.session_id == session_id
            ).first()
            
            if not conversation:
                # Créer une nouvelle conversation
                title = agent_service.generate_title(message)
                conversation = AgentConversation(
                    user_id=1,
                    session_id=session_id,
                    title=title,
                    model=model
                )
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
            
            # Récupérer l'historique
            history_messages = db.query(AgentMessage).filter(
                AgentMessage.session_id == session_id
            ).order_by(AgentMessage.created_at).all()
            
            history = [{"role": msg.role, "content": msg.content} for msg in history_messages]
            
            # Sauvegarder le message utilisateur
            user_message = AgentMessage(
                conversation_id=conversation.id,
                session_id=session_id,
                role="user",
                content=message
            )
            db.add(user_message)
            db.commit()
            
            # Envoyer à l'IA
            response = await agent_service.chat(message, history, model)
            
            if response.get("success"):
                # Sauvegarder la réponse
                assistant_message = AgentMessage(
                    conversation_id=conversation.id,
                    session_id=session_id,
                    role="assistant",
                    content=response["content"],
                    model=response.get("model"),
                    tokens=response.get("tokens"),
                    response_time=response.get("response_time")
                )
                db.add(assistant_message)
                
                # Mettre à jour les stats
                conversation.messages_count += 2
                conversation.tokens_used += response.get("tokens", 0)
                db.commit()
                
                # Envoyer la réponse
                await websocket.send_json({
                    "success": True,
                    "message": assistant_message.to_dict()
                })
            else:
                await websocket.send_json({
                    "success": False,
                    "error": response.get("error")
                })
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
