"""
Service pour la gestion CRM (Leads)
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.marketing_db import Lead, LeadInteraction, LeadStatus


class CRMService:
    """Service pour gérer les leads CRM"""
    
    @staticmethod
    def create_lead(db: Session, lead_data: Dict, author_id: int) -> Dict:
        """
        Créer un lead
        
        Args:
            db: Session de base de données
            lead_data: Données du lead
            author_id: ID de l'auteur
        
        Returns:
            Dict avec le lead créé
        """
        try:
            lead = Lead(
                first_name=lead_data.get("first_name"),
                last_name=lead_data.get("last_name"),
                email=lead_data.get("email"),
                phone=lead_data.get("phone"),
                company=lead_data.get("company"),
                job_title=lead_data.get("job_title"),
                status=LeadStatus[lead_data.get("status", "NEW").upper()],
                score=lead_data.get("score", 0),
                source=lead_data.get("source"),
                source_url=lead_data.get("source_url"),
                estimated_value=lead_data.get("estimated_value", 0.0),
                tags=lead_data.get("tags", []),
                notes=lead_data.get("notes"),
                custom_fields=lead_data.get("custom_fields"),
                owner_id=lead_data.get("owner_id"),
                author_id=author_id
            )
            
            db.add(lead)
            db.commit()
            db.refresh(lead)
            
            return {
                "success": True,
                "lead": lead.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la création du lead: {str(e)}"
            }
    
    @staticmethod
    def get_lead(db: Session, lead_id: int, author_id: int) -> Optional[Lead]:
        """Récupérer un lead"""
        return db.query(Lead).filter(
            Lead.id == lead_id,
            Lead.author_id == author_id
        ).first()
    
    @staticmethod
    def list_leads(
        db: Session,
        author_id: int,
        status: str = None,
        owner_id: int = None,
        search: str = None
    ) -> List[Lead]:
        """Lister les leads avec filtres"""
        query = db.query(Lead).filter(Lead.author_id == author_id)
        
        if status:
            query = query.filter(Lead.status == LeadStatus[status.upper()])
        
        if owner_id:
            query = query.filter(Lead.owner_id == owner_id)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Lead.first_name.ilike(search_filter)) |
                (Lead.last_name.ilike(search_filter)) |
                (Lead.email.ilike(search_filter)) |
                (Lead.company.ilike(search_filter))
            )
        
        return query.order_by(Lead.created_at.desc()).all()
    
    @staticmethod
    def update_lead(db: Session, lead_id: int, author_id: int, update_data: Dict) -> Dict:
        """Mettre à jour un lead"""
        try:
            lead = CRMService.get_lead(db, lead_id, author_id)
            
            if not lead:
                return {
                    "success": False,
                    "error": "Lead non trouvé"
                }
            
            for key, value in update_data.items():
                if hasattr(lead, key):
                    if key == "status":
                        value = LeadStatus[value.upper()]
                    setattr(lead, key, value)
            
            lead.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(lead)
            
            return {
                "success": True,
                "lead": lead.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la mise à jour: {str(e)}"
            }
    
    @staticmethod
    def delete_lead(db: Session, lead_id: int, author_id: int) -> Dict:
        """Supprimer un lead"""
        try:
            lead = CRMService.get_lead(db, lead_id, author_id)
            
            if not lead:
                return {
                    "success": False,
                    "error": "Lead non trouvé"
                }
            
            db.delete(lead)
            db.commit()
            
            return {
                "success": True,
                "message": "Lead supprimé"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la suppression: {str(e)}"
            }
    
    @staticmethod
    def add_interaction(
        db: Session,
        lead_id: int,
        author_id: int,
        interaction_data: Dict
    ) -> Dict:
        """Ajouter une interaction à un lead"""
        try:
            lead = CRMService.get_lead(db, lead_id, author_id)
            
            if not lead:
                return {
                    "success": False,
                    "error": "Lead non trouvé"
                }
            
            interaction = LeadInteraction(
                lead_id=lead_id,
                interaction_type=interaction_data.get("interaction_type"),
                subject=interaction_data.get("subject"),
                content=interaction_data.get("content"),
                interaction_metadata=interaction_data.get("metadata"),
                author_id=author_id
            )
            
            db.add(interaction)
            
            # Mettre à jour la date de dernier contact
            lead.last_contact_at = datetime.utcnow()
            
            db.commit()
            db.refresh(interaction)
            
            return {
                "success": True,
                "interaction": interaction.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de l'ajout de l'interaction: {str(e)}"
            }
    
    @staticmethod
    def get_lead_interactions(db: Session, lead_id: int, author_id: int) -> List[LeadInteraction]:
        """Récupérer les interactions d'un lead"""
        lead = CRMService.get_lead(db, lead_id, author_id)
        
        if not lead:
            return []
        
        return db.query(LeadInteraction).filter(
            LeadInteraction.lead_id == lead_id
        ).order_by(LeadInteraction.created_at.desc()).all()
    
    @staticmethod
    def get_pipeline_stats(db: Session, author_id: int) -> Dict:
        """Obtenir les statistiques du pipeline"""
        try:
            leads = db.query(Lead).filter(Lead.author_id == author_id).all()
            
            stats_by_status = {}
            total_value = 0
            
            for status in LeadStatus:
                status_leads = [l for l in leads if l.status == status]
                status_value = sum(l.estimated_value for l in status_leads)
                
                stats_by_status[status.value] = {
                    "count": len(status_leads),
                    "value": status_value
                }
                
                total_value += status_value
            
            return {
                "success": True,
                "stats": {
                    "total_leads": len(leads),
                    "total_value": total_value,
                    "by_status": stats_by_status,
                    "conversion_rate": (
                        len([l for l in leads if l.status == LeadStatus.WON]) / len(leads) * 100
                    ) if len(leads) > 0 else 0
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération des stats: {str(e)}"
            }
    
    @staticmethod
    def update_lead_score(db: Session, lead_id: int, author_id: int) -> Dict:
        """
        Mettre à jour automatiquement le score d'un lead
        basé sur ses interactions et caractéristiques
        """
        try:
            lead = CRMService.get_lead(db, lead_id, author_id)
            
            if not lead:
                return {
                    "success": False,
                    "error": "Lead non trouvé"
                }
            
            score = 0
            
            # Points pour les informations complètes
            if lead.first_name and lead.last_name:
                score += 10
            if lead.phone:
                score += 10
            if lead.company:
                score += 15
            if lead.job_title:
                score += 10
            
            # Points pour les interactions
            interactions = db.query(LeadInteraction).filter(
                LeadInteraction.lead_id == lead_id
            ).all()
            
            score += min(len(interactions) * 5, 30)  # Max 30 points
            
            # Points pour la valeur estimée
            if lead.estimated_value > 0:
                score += 20
            
            # Points pour le dernier contact récent
            if lead.last_contact_at:
                days_since_contact = (datetime.utcnow() - lead.last_contact_at).days
                if days_since_contact < 7:
                    score += 15
                elif days_since_contact < 30:
                    score += 10
            
            lead.score = min(score, 100)  # Score max 100
            
            db.commit()
            db.refresh(lead)
            
            return {
                "success": True,
                "lead": lead.to_dict(),
                "score": lead.score
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors du calcul du score: {str(e)}"
            }
