"""
Routes pour les notifications temps réel avec WebSocket
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from datetime import datetime
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Gestionnaire de connexions WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                self.disconnect(user_id)

    async def broadcast(self, message: dict):
        disconnected = []
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except:
                disconnected.append(user_id)
        
        for user_id in disconnected:
            self.disconnect(user_id)

manager = ConnectionManager()


@router.get("/notifications", response_class=HTMLResponse)
async def notifications_page(
    request: Request,
    current_user: UserDB = Depends(get_current_user)
):
    """Page des notifications"""
    return templates.TemplateResponse(
        "pages/notifications.html",
        {
            "request": request,
            "user": current_user,
            "title": "Notifications - WeBox Multi-IA",
            "page": "notifications"
        }
    )


@router.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(websocket: WebSocket, user_id: str):
    """
    WebSocket pour les notifications en temps réel
    """
    await manager.connect(websocket, user_id)
    
    try:
        # Envoyer message de bienvenue
        await manager.send_personal_message({
            "type": "connection",
            "message": "Connecté aux notifications en temps réel",
            "timestamp": datetime.utcnow().isoformat()
        }, user_id)
        
        while True:
            # Recevoir messages du client
            data = await websocket.receive_json()
            
            # Traiter selon le type de message
            if data.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id)
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"Erreur WebSocket: {e}")
        manager.disconnect(user_id)


@router.post("/api/notifications/send")
async def send_notification(
    user_id: str,
    notification_type: str,
    title: str,
    message: str,
    current_user: UserDB = Depends(get_current_user)
):
    """
    API pour envoyer une notification à un utilisateur
    """
    notification = {
        "type": notification_type,
        "title": title,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "read": False
    }
    
    await manager.send_personal_message(notification, user_id)
    
    return {
        "success": True,
        "message": "Notification envoyée"
    }


@router.post("/api/notifications/broadcast")
async def broadcast_notification(
    notification_type: str,
    title: str,
    message: str,
    current_user: UserDB = Depends(get_current_user)
):
    """
    API pour diffuser une notification à tous les utilisateurs connectés
    Réservé aux administrateurs
    """
    if not current_user.is_admin:
        return {"success": False, "message": "Accès refusé"}
    
    notification = {
        "type": notification_type,
        "title": title,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "read": False
    }
    
    await manager.broadcast(notification)
    
    return {
        "success": True,
        "message": f"Notification diffusée à {len(manager.active_connections)} utilisateur(s)"
    }
