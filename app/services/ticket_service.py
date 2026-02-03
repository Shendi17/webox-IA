"""
Service de gestion des tickets de support
Système de tickets pour le support client
"""
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List


class TicketService:
    """Service de gestion des tickets de support"""
    
    def __init__(self):
        self.tickets_file = "data/support_tickets.json"
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Créer le fichier de tickets s'il n'existe pas"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.tickets_file):
            with open(self.tickets_file, "w", encoding="utf-8") as f:
                json.dump({"tickets": [], "next_id": 1}, f)
    
    def _load_data(self) -> Dict:
        """Charger tous les tickets"""
        try:
            with open(self.tickets_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"tickets": [], "next_id": 1}
    
    def _save_data(self, data: Dict):
        """Sauvegarder les tickets"""
        with open(self.tickets_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_ticket(
        self,
        user_id: int,
        user_email: str,
        user_name: str,
        subject: str,
        message: str,
        category: str = "general",
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Créer un nouveau ticket de support
        
        Args:
            user_id: ID de l'utilisateur
            user_email: Email de l'utilisateur
            user_name: Nom de l'utilisateur
            subject: Sujet du ticket
            message: Message initial
            category: Catégorie (general, technical, billing, feature)
            priority: Priorité (low, normal, high, urgent)
        """
        data = self._load_data()
        
        ticket_id = data["next_id"]
        ticket = {
            "id": ticket_id,
            "user_id": user_id,
            "user_email": user_email,
            "user_name": user_name,
            "subject": subject,
            "category": category,
            "priority": priority,
            "status": "open",  # open, in_progress, waiting, resolved, closed
            "messages": [
                {
                    "id": 1,
                    "author": user_name,
                    "author_type": "user",
                    "message": message,
                    "created_at": datetime.utcnow().isoformat()
                }
            ],
            "assigned_to": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "resolved_at": None
        }
        
        data["tickets"].append(ticket)
        data["next_id"] += 1
        
        self._save_data(data)
        
        return {
            "success": True,
            "ticket": ticket
        }
    
    def get_ticket(self, ticket_id: int) -> Optional[Dict]:
        """Récupérer un ticket par son ID"""
        data = self._load_data()
        
        for ticket in data["tickets"]:
            if ticket["id"] == ticket_id:
                return ticket
        
        return None
    
    def list_tickets(
        self,
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """Lister les tickets avec filtres optionnels"""
        data = self._load_data()
        tickets = data["tickets"]
        
        # Filtrer par utilisateur
        if user_id is not None:
            tickets = [t for t in tickets if t["user_id"] == user_id]
        
        # Filtrer par statut
        if status:
            tickets = [t for t in tickets if t["status"] == status]
        
        # Filtrer par catégorie
        if category:
            tickets = [t for t in tickets if t["category"] == category]
        
        # Trier par date de mise à jour (plus récent en premier)
        tickets.sort(key=lambda t: t["updated_at"], reverse=True)
        
        return tickets
    
    def add_message(
        self,
        ticket_id: int,
        author: str,
        author_type: str,  # "user" ou "support"
        message: str
    ) -> bool:
        """Ajouter un message à un ticket"""
        data = self._load_data()
        
        for ticket in data["tickets"]:
            if ticket["id"] == ticket_id:
                message_id = len(ticket["messages"]) + 1
                
                ticket["messages"].append({
                    "id": message_id,
                    "author": author,
                    "author_type": author_type,
                    "message": message,
                    "created_at": datetime.utcnow().isoformat()
                })
                
                ticket["updated_at"] = datetime.utcnow().isoformat()
                
                # Si c'est une réponse du support, passer en "in_progress"
                if author_type == "support" and ticket["status"] == "open":
                    ticket["status"] = "in_progress"
                
                self._save_data(data)
                return True
        
        return False
    
    def update_status(
        self,
        ticket_id: int,
        status: str
    ) -> bool:
        """Mettre à jour le statut d'un ticket"""
        data = self._load_data()
        
        for ticket in data["tickets"]:
            if ticket["id"] == ticket_id:
                ticket["status"] = status
                ticket["updated_at"] = datetime.utcnow().isoformat()
                
                if status == "resolved":
                    ticket["resolved_at"] = datetime.utcnow().isoformat()
                
                self._save_data(data)
                return True
        
        return False
    
    def assign_ticket(
        self,
        ticket_id: int,
        assigned_to: str
    ) -> bool:
        """Assigner un ticket à un membre du support"""
        data = self._load_data()
        
        for ticket in data["tickets"]:
            if ticket["id"] == ticket_id:
                ticket["assigned_to"] = assigned_to
                ticket["updated_at"] = datetime.utcnow().isoformat()
                
                if ticket["status"] == "open":
                    ticket["status"] = "in_progress"
                
                self._save_data(data)
                return True
        
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtenir des statistiques sur les tickets"""
        data = self._load_data()
        tickets = data["tickets"]
        
        stats = {
            "total": len(tickets),
            "by_status": {},
            "by_category": {},
            "by_priority": {},
            "avg_resolution_time": None
        }
        
        # Compter par statut
        for ticket in tickets:
            status = ticket["status"]
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            category = ticket["category"]
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            priority = ticket["priority"]
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
        
        # Calculer temps moyen de résolution
        resolved_tickets = [t for t in tickets if t["resolved_at"]]
        if resolved_tickets:
            total_time = 0
            for ticket in resolved_tickets:
                created = datetime.fromisoformat(ticket["created_at"])
                resolved = datetime.fromisoformat(ticket["resolved_at"])
                total_time += (resolved - created).total_seconds()
            
            avg_seconds = total_time / len(resolved_tickets)
            stats["avg_resolution_time"] = f"{avg_seconds / 3600:.1f} heures"
        
        return stats


# Instance globale
ticket_service = TicketService()
