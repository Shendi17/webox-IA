"""
Routes API pour le chat IA
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import json
import os

from app.database import get_db
from app.models.ai_chat_db import AIConversation, AIMessage, AIAction
from app.models.web_project_db import WebProject

router = APIRouter(prefix="/api/chat", tags=["AI Chat"])


# ==================== SCHEMAS ====================

class MessageCreate(BaseModel):
    conversation_id: Optional[int] = None
    project_id: int
    content: str
    model: Optional[str] = "gpt-4-turbo"
    context: Optional[dict] = None


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    actions: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    project_id: int
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    project_id: int
    title: Optional[str]
    created_at: datetime
    message_count: int
    
    class Config:
        from_attributes = True


# ==================== HELPER FUNCTIONS ====================

def get_project_context(project_id: int, db: Session, user_query: str = "") -> dict:
    """Récupère le contexte enrichi du projet"""
    project = db.query(WebProject).filter(WebProject.id == project_id).first()
    
    if not project:
        return {}
    
    # Contexte de base
    context = {
        "project_id": project.id,
        "project_name": project.name,
        "project_type": project.project_type,
        "description": project.description,
        "technologies": project.technologies or [],
        "local_path": project.local_path
    }
    
    # Analyser le projet pour enrichir le contexte
    try:
        from app.services.project_context import ProjectAnalyzer
        
        analyzer = ProjectAnalyzer(project.local_path)
        analysis = analyzer.analyze()
        
        # Ajouter l'analyse au contexte
        context.update({
            "structure": analysis.get("structure", {}),
            "detected_technologies": analysis.get("technologies", []),
            "file_tree": analysis.get("file_tree", {}),
            "statistics": analysis.get("statistics", {}),
            "dependencies": analysis.get("dependencies", {}),
            "important_files": analysis.get("important_files", {})
        })
        
        # Si une requête est fournie, trouver les fichiers pertinents
        if user_query:
            relevant_files = analyzer.get_relevant_files(user_query, max_files=3)
            context["relevant_files"] = relevant_files
    
    except Exception as e:
        context["analysis_error"] = str(e)
    
    return context


async def call_ai_api(messages: List[dict], project_context: dict, model: str = "gpt-4-turbo") -> str:
    """Appelle l'API IA appropriée selon le modèle"""
    try:
        from app.services.ai_providers import call_ai
        from app.services.project_context import build_context_prompt
        
        # Construire le contexte enrichi
        context_info = build_context_prompt(project_context)
        
        # Construire le prompt système
        system_prompt = f"""Tu es un assistant IA intégré à WeBox Studio, un éditeur de code web.

{context_info}

📊 **Statistiques** :
- Fichiers : {project_context.get('statistics', {}).get('total_files', 0)}
- Lignes de code : {project_context.get('statistics', {}).get('total_lines', 0)}

🔧 **Technologies détectées** : {', '.join(project_context.get('detected_technologies', []))}

Capacités :
- Créer/modifier/supprimer des fichiers
- Expliquer du code
- Corriger des erreurs
- Suggérer des améliorations
- Générer du code

Format de réponse :
- Texte explicatif clair et concis
- Code avec ```language
- Si tu dois effectuer une action, indique-le clairement avec [ACTION:type:data]

Sois concis, précis et professionnel."""
        
        # Préparer les messages
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages)
        
        # Appeler l'IA appropriée
        response = await call_ai(api_messages, model=model, temperature=0.7, max_tokens=2000)
        
        return response
        
    except Exception as e:
        return f"❌ Erreur lors de l'appel à l'IA : {str(e)}"


# ==================== ROUTES ====================

@router.post("/conversations")
async def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle conversation"""
    try:
        # Vérifier que le projet existe
        project = db.query(WebProject).filter(WebProject.id == data.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        # Créer la conversation
        conversation = AIConversation(
            project_id=data.project_id,
            title=data.title or f"Conversation - {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}",
            context=get_project_context(data.project_id, db)
        )
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return {
            "success": True,
            "conversation_id": conversation.id,
            "title": conversation.title
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{project_id}")
async def list_conversations(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Liste les conversations d'un projet"""
    try:
        conversations = db.query(AIConversation).filter(
            AIConversation.project_id == project_id
        ).order_by(AIConversation.updated_at.desc()).all()
        
        result = []
        for conv in conversations:
            result.append({
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "message_count": len(conv.messages)
            })
        
        return {"conversations": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Récupère les messages d'une conversation"""
    try:
        conversation = db.query(AIConversation).filter(
            AIConversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
        
        messages = db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation_id
        ).order_by(AIMessage.created_at).all()
        
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "actions": msg.actions,
                "created_at": msg.created_at.isoformat()
            })
        
        return {"messages": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/chat")
async def ai_chat_simple(
    request: Request,
    db: Session = Depends(get_db)
):
    """Endpoint simple pour le chat IA dans l'éditeur"""
    try:
        from app.services.ai_providers import call_ai
        
        body = await request.json()
        message = body.get("message", "")
        context = body.get("context", {})
        project_id = body.get("project_id")
        model = body.get("model", "gpt-4o")
        
        if not message:
            return {"response": "Message vide"}
        
        # Mapper les noms de modèles pour l'affichage
        model_names = {
            "gpt-4o": "GPT-4o (Omni)",
            "gpt-4-turbo": "GPT-4 Turbo",
            "gpt-4": "GPT-4",
            "gpt-3.5-turbo": "GPT-3.5 Turbo",
            "claude-3.5-sonnet": "Claude 3.5 Sonnet",
            "claude-3-opus": "Claude 3 Opus",
            "claude-3-sonnet": "Claude 3 Sonnet",
            "claude-3-haiku": "Claude 3 Haiku",
            "gemini-pro": "Gemini Pro",
            "mistral-large": "Mistral Large",
            "mistral-medium": "Mistral Medium"
        }
        
        model_display = model_names.get(model, model)
        
        # Construire le prompt avec le contexte
        system_message = "Tu es un assistant IA expert en développement web. Tu aides les développeurs à écrire, corriger et optimiser leur code."
        
        user_prompt = message
        
        if context.get("file"):
            user_prompt += f"\n\n📄 Fichier actuel : {context['file']}"
        
        if context.get("language"):
            user_prompt += f"\n💻 Langage : {context['language']}"
        
        if context.get("code"):
            user_prompt += f"\n\n```{context.get('language', '')}\n{context['code']}\n```"
        
        # Préparer les messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        # Appeler l'IA réelle
        ai_response = await call_ai(messages, model=model, temperature=0.7, max_tokens=2000)
        
        # Vérifier si c'est un message d'erreur (commence par ⚠️ ou ❌)
        if ai_response.startswith("⚠️") or ai_response.startswith("❌"):
            return {"response": ai_response}
        
        # Formater la réponse
        response = f"🤖 **{model_display}** répond :\n\n{ai_response}"
        
        return {"response": response}
        
    except Exception as e:
        print(f"Erreur ai_chat_simple: {e}")
        import traceback
        traceback.print_exc()
        return {"response": f"❌ Erreur lors du traitement : {str(e)}"}


@router.post("/message")
async def send_message(
    data: MessageCreate,
    db: Session = Depends(get_db)
):
    """Envoyer un message et recevoir une réponse de l'IA"""
    try:
        # Créer ou récupérer la conversation
        if data.conversation_id:
            conversation = db.query(AIConversation).filter(
                AIConversation.id == data.conversation_id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation non trouvée")
        else:
            # Créer une nouvelle conversation
            conversation = AIConversation(
                project_id=data.project_id,
                title=f"Conversation - {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}",
                context=get_project_context(data.project_id, db)
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Sauvegarder le message utilisateur
        user_message = AIMessage(
            conversation_id=conversation.id,
            role="user",
            content=data.content
        )
        db.add(user_message)
        db.commit()
        
        # Récupérer l'historique des messages
        messages_history = db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation.id
        ).order_by(AIMessage.created_at).all()
        
        # Préparer les messages pour l'API
        api_messages = []
        for msg in messages_history:
            api_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Appeler l'API IA appropriée
        ai_response = await call_ai_api(api_messages, conversation.context or {}, model=data.model)
        
        # Parser et exécuter les actions sur les fichiers
        from app.services.file_actions import process_ai_response
        
        project = db.query(WebProject).filter(WebProject.id == data.project_id).first()
        cleaned_response, action_results = process_ai_response(ai_response, project.local_path)
        
        # Préparer les actions pour la BDD
        actions_data = None
        if action_results:
            actions_data = {
                "actions": action_results,
                "count": len(action_results),
                "success_count": sum(1 for r in action_results if r.get("success"))
            }
        
        # Sauvegarder la réponse de l'IA
        assistant_message = AIMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=cleaned_response,
            actions=actions_data
        )
        db.add(assistant_message)
        
        # Mettre à jour la conversation
        conversation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(assistant_message)
        
        return {
            "success": True,
            "conversation_id": conversation.id,
            "message": {
                "id": assistant_message.id,
                "role": "assistant",
                "content": ai_response,
                "created_at": assistant_message.created_at.isoformat()
            }
        }
        
    except Exception as e:
        db.rollback()
        print(f"Erreur send_message: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Supprimer une conversation"""
    try:
        conversation = db.query(AIConversation).filter(
            AIConversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
        
        db.delete(conversation)
        db.commit()
        
        return {"success": True, "message": "Conversation supprimée"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/stream")
async def send_message_stream(
    data: MessageCreate,
    db: Session = Depends(get_db)
):
    """Envoyer un message et recevoir une réponse en streaming"""
    
    async def generate():
        try:
            # Créer ou récupérer la conversation
            if data.conversation_id:
                conversation = db.query(AIConversation).filter(
                    AIConversation.id == data.conversation_id
                ).first()
                if not conversation:
                    yield f"data: {json.dumps({'error': 'Conversation non trouvée'})}\n\n"
                    return
            else:
                # Créer une nouvelle conversation
                conversation = AIConversation(
                    project_id=data.project_id,
                    title=f"Conversation - {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}",
                    context=get_project_context(data.project_id, db, data.content)
                )
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
                
                # Envoyer l'ID de conversation
                yield f"data: {json.dumps({'type': 'conversation_id', 'conversation_id': conversation.id})}\n\n"
            
            # Sauvegarder le message utilisateur
            user_message = AIMessage(
                conversation_id=conversation.id,
                role="user",
                content=data.content
            )
            db.add(user_message)
            db.commit()
            
            # Récupérer l'historique des messages
            messages_history = db.query(AIMessage).filter(
                AIMessage.conversation_id == conversation.id
            ).order_by(AIMessage.created_at).all()
            
            # Préparer les messages pour l'API
            api_messages = []
            for msg in messages_history:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Appeler l'IA avec streaming
            from app.services.ai_providers import AIProviderFactory
            
            provider, actual_model = AIProviderFactory.get_provider(data.model)
            
            # Pour le streaming, on simule pour l'instant
            # TODO: Implémenter le vrai streaming avec OpenAI/Claude
            ai_response = await provider.chat(api_messages, actual_model, temperature=0.7, max_tokens=2000)
            
            # Envoyer la réponse par morceaux
            chunk_size = 50
            for i in range(0, len(ai_response), chunk_size):
                chunk = ai_response[i:i+chunk_size]
                yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
            
            # Parser et exécuter les actions
            from app.services.file_actions import process_ai_response
            
            project = db.query(WebProject).filter(WebProject.id == data.project_id).first()
            cleaned_response, action_results = process_ai_response(ai_response, project.local_path)
            
            # Envoyer les actions
            if action_results:
                yield f"data: {json.dumps({'type': 'actions', 'actions': action_results})}\n\n"
            
            # Sauvegarder la réponse
            actions_data = None
            if action_results:
                actions_data = {
                    "actions": action_results,
                    "count": len(action_results),
                    "success_count": sum(1 for r in action_results if r.get("success"))
                }
            
            assistant_message = AIMessage(
                conversation_id=conversation.id,
                role="assistant",
                content=cleaned_response,
                actions=actions_data
            )
            db.add(assistant_message)
            conversation.updated_at = datetime.utcnow()
            db.commit()
            
            # Envoyer la fin
            yield f"data: {json.dumps({'type': 'done', 'message_id': assistant_message.id})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
