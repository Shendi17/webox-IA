"""
Routes API pour les tickets de support
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user_from_token, require_admin
from app.services.ticket_service import ticket_service

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


class TicketCreate(BaseModel):
    subject: str
    message: str
    category: str = "general"  # general, technical, billing, feature
    priority: str = "normal"  # low, normal, high, urgent


class TicketMessage(BaseModel):
    message: str


class TicketStatusUpdate(BaseModel):
    status: str  # open, in_progress, waiting, resolved, closed


class TicketAssign(BaseModel):
    assigned_to: str


@router.post("/create")
async def create_ticket(
    request: TicketCreate,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Créer un nouveau ticket de support
    """
    result = ticket_service.create_ticket(
        user_id=current_user["id"],
        user_email=current_user.get("email", ""),
        user_name=current_user.get("name", "Utilisateur"),
        subject=request.subject,
        message=request.message,
        category=request.category,
        priority=request.priority
    )
    
    return result


@router.get("/list")
async def list_tickets(
    status: Optional[str] = None,
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Lister les tickets de l'utilisateur
    """
    tickets = ticket_service.list_tickets(
        user_id=current_user["id"],
        status=status,
        category=category
    )
    
    return {"tickets": tickets, "total": len(tickets)}


@router.get("/admin/list")
async def list_all_tickets(
    status: Optional[str] = None,
    category: Optional[str] = None,
    current_user: dict = Depends(require_admin)
):
    """
    Lister tous les tickets (admin uniquement)
    """
    tickets = ticket_service.list_tickets(
        status=status,
        category=category
    )
    
    return {"tickets": tickets, "total": len(tickets)}


@router.get("/{ticket_id}")
async def get_ticket(
    ticket_id: int,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Récupérer un ticket spécifique
    """
    ticket = ticket_service.get_ticket(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    
    # Vérifier que l'utilisateur a accès au ticket
    if ticket["user_id"] != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    
    return ticket


@router.post("/{ticket_id}/message")
async def add_ticket_message(
    ticket_id: int,
    request: TicketMessage,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Ajouter un message à un ticket
    """
    ticket = ticket_service.get_ticket(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    
    # Vérifier que l'utilisateur a accès au ticket
    if ticket["user_id"] != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    
    # Déterminer le type d'auteur
    author_type = "support" if current_user.get("role") == "admin" else "user"
    
    success = ticket_service.add_message(
        ticket_id=ticket_id,
        author=current_user.get("name", "Utilisateur"),
        author_type=author_type,
        message=request.message
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout du message")
    
    return {"success": True, "message": "Message ajouté avec succès"}


@router.patch("/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: int,
    request: TicketStatusUpdate,
    current_user: dict = Depends(require_admin)
):
    """
    Mettre à jour le statut d'un ticket (admin uniquement)
    """
    success = ticket_service.update_status(ticket_id, request.status)
    
    if not success:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    
    return {"success": True, "message": "Statut mis à jour avec succès"}


@router.patch("/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: int,
    request: TicketAssign,
    current_user: dict = Depends(require_admin)
):
    """
    Assigner un ticket à un membre du support (admin uniquement)
    """
    success = ticket_service.assign_ticket(ticket_id, request.assigned_to)
    
    if not success:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    
    return {"success": True, "message": "Ticket assigné avec succès"}


@router.get("/admin/stats")
async def get_ticket_stats(
    current_user: dict = Depends(require_admin)
):
    """
    Obtenir des statistiques sur les tickets (admin uniquement)
    """
    stats = ticket_service.get_stats()
    return stats
