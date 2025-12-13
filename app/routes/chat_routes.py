"""
Routes API pour le Chat Multi-IA
Date : 30 Octobre 2025
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.middleware.auth import get_current_user_from_token
from app.models.user_db import UserDB
from app.models.conversation_db import ConversationDB, MessageDB
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithMessages,
    MessageResponse
)
from modules.core.ai_providers import ai_manager

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Envoyer un message et obtenir les réponses des IA
    """
    try:
        # Récupérer ou créer la conversation
        if request.conversation_id:
            conversation = db.query(ConversationDB).filter(
                ConversationDB.id == request.conversation_id,
                ConversationDB.user_id == current_user["id"]
            ).first()
            
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Créer une nouvelle conversation
            conversation = ConversationDB(
                user_id=current_user["id"],
                title=request.message[:50] + "..." if len(request.message) > 50 else request.message,
                folder="Général"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Sauvegarder le message utilisateur
        user_message = MessageDB(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.commit()
        
        # Générer les réponses des IA
        start_time = datetime.now()
        
        messages = [{"role": "user", "content": request.message}]
        
        ai_responses = await ai_manager.generate_multi_response(
            messages=messages,
            selected_providers=request.selected_providers,
            models=request.selected_models,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        end_time = datetime.now()
        response_time = int((end_time - start_time).total_seconds() * 1000)  # en ms
        
        # Sauvegarder les réponses
        assistant_message = MessageDB(
            conversation_id=conversation.id,
            role="assistant",
            content="",  # Vide car on a plusieurs réponses
            ai_responses=ai_responses,
            ai_provider=",".join(request.selected_providers),
            response_time=response_time
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # Mettre à jour la date de la conversation
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        return ChatResponse(
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            user_message=request.message,
            ai_responses=ai_responses,
            response_time=response_time,
            created_at=assistant_message.created_at
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    folder: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer toutes les conversations de l'utilisateur
    """
    query = db.query(ConversationDB).filter(
        ConversationDB.user_id == current_user["id"]
    )
    
    if folder:
        query = query.filter(ConversationDB.folder == folder)
    
    conversations = query.order_by(ConversationDB.updated_at.desc()).all()
    
    # Ajouter le nombre de messages et l'aperçu
    result = []
    for conv in conversations:
        conv_dict = conv.to_dict()
        conv_dict["message_count"] = len(conv.messages)
        
        # Ajouter un aperçu du premier message
        if conv.messages and len(conv.messages) > 0:
            first_msg = conv.messages[0]
            preview = first_msg.content[:100] + "..." if len(first_msg.content) > 100 else first_msg.content
            conv_dict["preview"] = preview
        else:
            conv_dict["preview"] = "Aucun message"
        
        result.append(ConversationResponse(**conv_dict))
    
    return result


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer une conversation avec tous ses messages
    """
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageDB).filter(
        MessageDB.conversation_id == conversation_id
    ).order_by(MessageDB.created_at).all()
    
    conv_dict = conversation.to_dict()
    conv_dict["message_count"] = len(messages)
    conv_dict["messages"] = [MessageResponse(**msg.to_dict()) for msg in messages]
    
    return ConversationWithMessages(**conv_dict)


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Créer une nouvelle conversation
    """
    new_conversation = ConversationDB(
        user_id=current_user["id"],
        title=conversation.title,
        folder=conversation.folder
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    
    conv_dict = new_conversation.to_dict()
    conv_dict["message_count"] = 0
    
    return ConversationResponse(**conv_dict)


@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    update: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Mettre à jour une conversation
    """
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if update.title:
        conversation.title = update.title
    if update.folder:
        conversation.folder = update.folder
    
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    
    conv_dict = conversation.to_dict()
    conv_dict["message_count"] = len(conversation.messages)
    
    return ConversationResponse(**conv_dict)


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Supprimer une conversation
    """
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    
    return {"message": "Conversation deleted successfully"}


@router.websocket("/ws/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    WebSocket pour le streaming en temps réel
    """
    await websocket.accept()
    
    try:
        while True:
            # Recevoir le message
            data = await websocket.receive_json()
            
            # Générer les réponses en streaming
            for provider in data.get("providers", ["GPT-4"]):
                async for chunk in ai_manager.stream_response(
                    provider=provider,
                    message=data.get("message", ""),
                    model=data.get("models", {}).get(provider)
                ):
                    await websocket.send_json({
                        "provider": provider,
                        "chunk": chunk,
                        "done": False
                    })
            
            # Envoyer la fin du streaming
            await websocket.send_json({
                "status": "complete",
                "done": True
            })
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for conversation {conversation_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


@router.post("/conversations/{conversation_id}/favorite")
async def toggle_favorite(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Basculer le statut favori d'une conversation
    """
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Toggle favori
    conversation.is_favorite = not conversation.is_favorite
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)
    
    return {"is_favorite": conversation.is_favorite}


@router.get("/conversations/{conversation_id}/export")
async def export_conversation(
    conversation_id: int,
    format: str = "pdf",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Exporter une conversation en PDF, Markdown ou TXT
    """
    from fastapi.responses import StreamingResponse
    import io
    
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(MessageDB).filter(
        MessageDB.conversation_id == conversation_id
    ).order_by(MessageDB.created_at).all()
    
    if format == "txt":
        # Export TXT
        content = f"Conversation: {conversation.title}\n"
        content += f"Date: {conversation.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        content += "=" * 50 + "\n\n"
        
        for msg in messages:
            role = "Vous" if msg.role == "user" else "IA"
            content += f"{role}: {msg.content}\n\n"
        
        return StreamingResponse(
            io.BytesIO(content.encode()),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename=conversation_{conversation_id}.txt"}
        )
    
    elif format == "md":
        # Export Markdown
        content = f"# {conversation.title}\n\n"
        content += f"**Date**: {conversation.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        content += "---\n\n"
        
        for msg in messages:
            role = "**Vous**" if msg.role == "user" else "**IA**"
            content += f"{role}:\n\n{msg.content}\n\n---\n\n"
        
        return StreamingResponse(
            io.BytesIO(content.encode()),
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=conversation_{conversation_id}.md"}
        )
    
    elif format == "pdf":
        # Export PDF (nécessite reportlab)
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Titre
            story.append(Paragraph(f"<b>{conversation.title}</b>", styles['Title']))
            story.append(Spacer(1, 12))
            
            # Messages
            for msg in messages:
                role = "Vous" if msg.role == "user" else "IA"
                story.append(Paragraph(f"<b>{role}:</b>", styles['Heading2']))
                story.append(Paragraph(msg.content, styles['Normal']))
                story.append(Spacer(1, 12))
            
            doc.build(story)
            buffer.seek(0)
            
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=conversation_{conversation_id}.pdf"}
            )
        except ImportError:
            raise HTTPException(status_code=501, detail="PDF export requires reportlab library")
    
    else:
        raise HTTPException(status_code=400, detail="Format must be pdf, md, or txt")


@router.get("/search")
async def search_conversations(
    q: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Rechercher dans les conversations et messages
    """
    if len(q) < 2:
        return {"results": []}
    
    # Recherche dans les titres et contenus des messages
    conversations = db.query(ConversationDB).filter(
        ConversationDB.user_id == current_user["id"],
        ConversationDB.title.ilike(f"%{q}%")
    ).all()
    
    messages = db.query(MessageDB).join(ConversationDB).filter(
        ConversationDB.user_id == current_user["id"],
        MessageDB.content.ilike(f"%{q}%")
    ).all()
    
    results = []
    
    # Résultats des titres
    for conv in conversations:
        results.append({
            "conversation_id": conv.id,
            "title": conv.title,
            "snippet": conv.title,
            "date": conv.updated_at.strftime("%d/%m/%Y %H:%M")
        })
    
    # Résultats des messages
    for msg in messages:
        conversation = db.query(ConversationDB).filter(
            ConversationDB.id == msg.conversation_id
        ).first()
        
        # Créer un snippet avec le contexte
        content = msg.content
        index = content.lower().find(q.lower())
        start = max(0, index - 50)
        end = min(len(content), index + len(q) + 50)
        snippet = "..." + content[start:end] + "..."
        
        results.append({
            "conversation_id": conversation.id,
            "title": conversation.title,
            "snippet": snippet,
            "date": msg.created_at.strftime("%d/%m/%Y %H:%M")
        })
    
    # Limiter à 10 résultats
    return {"results": results[:10]}


@router.post("/conversations/{conversation_id}/tags")
async def add_tag(
    conversation_id: int,
    tag_data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Ajouter un tag à une conversation
    """
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    tag = tag_data.get("tag", "").strip()
    if not tag:
        raise HTTPException(status_code=400, detail="Tag cannot be empty")
    
    # Ajouter le tag (en supposant que tags est une liste JSON)
    if not conversation.tags:
        conversation.tags = []
    
    if tag not in conversation.tags:
        conversation.tags.append(tag)
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(conversation)
    
    return {"tags": conversation.tags}


@router.delete("/conversations/{conversation_id}/tags/{tag}")
async def remove_tag(
    conversation_id: int,
    tag: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Supprimer un tag d'une conversation
    """
    conversation = db.query(ConversationDB).filter(
        ConversationDB.id == conversation_id,
        ConversationDB.user_id == current_user["id"]
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.tags and tag in conversation.tags:
        conversation.tags.remove(tag)
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(conversation)
    
    return {"tags": conversation.tags if conversation.tags else []}
