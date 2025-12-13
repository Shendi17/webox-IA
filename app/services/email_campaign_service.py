"""
Service pour la gestion des campagnes email
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.marketing_db import EmailCampaign, CampaignStatus
from app.services.ai_providers import AIProviderFactory


class EmailCampaignService:
    """Service pour gérer les campagnes email"""
    
    @staticmethod
    def create_campaign(db: Session, campaign_data: Dict, author_id: int) -> Dict:
        """
        Créer une campagne email
        
        Args:
            db: Session de base de données
            campaign_data: Données de la campagne
            author_id: ID de l'auteur
        
        Returns:
            Dict avec la campagne créée
        """
        try:
            campaign = EmailCampaign(
                name=campaign_data.get("name"),
                subject=campaign_data.get("subject"),
                preheader=campaign_data.get("preheader"),
                html_content=campaign_data.get("html_content"),
                text_content=campaign_data.get("text_content"),
                from_name=campaign_data.get("from_name"),
                from_email=campaign_data.get("from_email"),
                reply_to=campaign_data.get("reply_to"),
                segment_rules=campaign_data.get("segment_rules"),
                author_id=author_id
            )
            
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            
            return {
                "success": True,
                "campaign": campaign.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la création de la campagne: {str(e)}"
            }
    
    @staticmethod
    def get_campaign(db: Session, campaign_id: int, author_id: int) -> Optional[EmailCampaign]:
        """Récupérer une campagne"""
        return db.query(EmailCampaign).filter(
            EmailCampaign.id == campaign_id,
            EmailCampaign.author_id == author_id
        ).first()
    
    @staticmethod
    def list_campaigns(
        db: Session,
        author_id: int,
        status: str = None
    ) -> List[EmailCampaign]:
        """Lister les campagnes"""
        query = db.query(EmailCampaign).filter(EmailCampaign.author_id == author_id)
        
        if status:
            query = query.filter(EmailCampaign.status == CampaignStatus[status.upper()])
        
        return query.order_by(EmailCampaign.created_at.desc()).all()
    
    @staticmethod
    def update_campaign(
        db: Session,
        campaign_id: int,
        author_id: int,
        update_data: Dict
    ) -> Dict:
        """Mettre à jour une campagne"""
        try:
            campaign = EmailCampaignService.get_campaign(db, campaign_id, author_id)
            
            if not campaign:
                return {
                    "success": False,
                    "error": "Campagne non trouvée"
                }
            
            for key, value in update_data.items():
                if hasattr(campaign, key):
                    if key == "status":
                        value = CampaignStatus[value.upper()]
                    setattr(campaign, key, value)
            
            campaign.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(campaign)
            
            return {
                "success": True,
                "campaign": campaign.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la mise à jour: {str(e)}"
            }
    
    @staticmethod
    def delete_campaign(db: Session, campaign_id: int, author_id: int) -> Dict:
        """Supprimer une campagne"""
        try:
            campaign = EmailCampaignService.get_campaign(db, campaign_id, author_id)
            
            if not campaign:
                return {
                    "success": False,
                    "error": "Campagne non trouvée"
                }
            
            db.delete(campaign)
            db.commit()
            
            return {
                "success": True,
                "message": "Campagne supprimée"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la suppression: {str(e)}"
            }
    
    @staticmethod
    def schedule_campaign(
        db: Session,
        campaign_id: int,
        author_id: int,
        scheduled_at: datetime
    ) -> Dict:
        """Planifier l'envoi d'une campagne"""
        try:
            campaign = EmailCampaignService.get_campaign(db, campaign_id, author_id)
            
            if not campaign:
                return {
                    "success": False,
                    "error": "Campagne non trouvée"
                }
            
            campaign.scheduled_at = scheduled_at
            campaign.status = CampaignStatus.SCHEDULED
            
            db.commit()
            db.refresh(campaign)
            
            return {
                "success": True,
                "campaign": campaign.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la planification: {str(e)}"
            }
    
    @staticmethod
    def send_campaign(db: Session, campaign_id: int, author_id: int) -> Dict:
        """
        Envoyer une campagne
        (Cette méthode devrait intégrer un service d'envoi d'emails comme SendGrid)
        """
        try:
            campaign = EmailCampaignService.get_campaign(db, campaign_id, author_id)
            
            if not campaign:
                return {
                    "success": False,
                    "error": "Campagne non trouvée"
                }
            
            # TODO: Intégrer SendGrid, Mailchimp, etc.
            # Pour l'instant, on simule l'envoi
            
            campaign.status = CampaignStatus.ACTIVE
            campaign.sent_at = datetime.utcnow()
            
            # Simuler des statistiques
            campaign.total_sent = campaign.total_recipients
            campaign.total_delivered = int(campaign.total_recipients * 0.98)
            campaign.total_opened = int(campaign.total_recipients * 0.25)
            campaign.total_clicked = int(campaign.total_recipients * 0.05)
            
            campaign.open_rate = (campaign.total_opened / campaign.total_sent * 100) if campaign.total_sent > 0 else 0
            campaign.click_rate = (campaign.total_clicked / campaign.total_sent * 100) if campaign.total_sent > 0 else 0
            
            db.commit()
            db.refresh(campaign)
            
            return {
                "success": True,
                "campaign": campaign.to_dict(),
                "message": "Campagne envoyée avec succès"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de l'envoi: {str(e)}"
            }
    
    @staticmethod
    def generate_campaign_with_ai(
        db: Session,
        campaign_type: str,
        topic: str,
        target_audience: str,
        tone: str,
        author_id: int
    ) -> Dict:
        """
        Générer une campagne email avec IA
        
        Args:
            db: Session de base de données
            campaign_type: Type de campagne (newsletter, promo, etc.)
            topic: Sujet de la campagne
            target_audience: Audience cible
            tone: Ton du contenu
            author_id: ID de l'auteur
        
        Returns:
            Dict avec la campagne générée
        """
        try:
            ai_provider = AIProviderFactory.get_provider("gpt-4")
            
            prompt = f"""Tu es un expert en email marketing.

Crée une campagne email de type "{campaign_type}" sur le sujet : "{topic}"
Audience cible : {target_audience}
Ton : {tone}

Génère :
1. Objet de l'email (accrocheur, 50 caractères max)
2. Pré-header (complément objet, 100 caractères max)
3. Contenu HTML (structure complète avec header, body, footer)
4. Contenu texte (version plain text)

Le contenu doit :
- Être engageant et pertinent
- Avoir un call-to-action clair
- Être optimisé pour la conversion
- Respecter les bonnes pratiques email marketing

Réponds en JSON avec ce format :
{{
    "name": "Nom de la campagne",
    "subject": "Objet",
    "preheader": "Pré-header",
    "html_content": "HTML complet",
    "text_content": "Version texte"
}}
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            # Parser la réponse JSON
            import json
            import re
            
            content = response["content"]
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                campaign_data = json.loads(json_match.group())
            else:
                campaign_data = json.loads(content)
            
            # Créer la campagne
            campaign = EmailCampaign(
                name=campaign_data.get("name"),
                subject=campaign_data.get("subject"),
                preheader=campaign_data.get("preheader"),
                html_content=campaign_data.get("html_content"),
                text_content=campaign_data.get("text_content"),
                author_id=author_id
            )
            
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            
            return {
                "success": True,
                "campaign": campaign.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    @staticmethod
    def get_campaign_stats(db: Session, author_id: int) -> Dict:
        """Obtenir les statistiques globales des campagnes"""
        try:
            campaigns = db.query(EmailCampaign).filter(
                EmailCampaign.author_id == author_id
            ).all()
            
            total_sent = sum(c.total_sent for c in campaigns)
            total_opened = sum(c.total_opened for c in campaigns)
            total_clicked = sum(c.total_clicked for c in campaigns)
            
            return {
                "success": True,
                "stats": {
                    "total_campaigns": len(campaigns),
                    "total_sent": total_sent,
                    "total_opened": total_opened,
                    "total_clicked": total_clicked,
                    "avg_open_rate": (total_opened / total_sent * 100) if total_sent > 0 else 0,
                    "avg_click_rate": (total_clicked / total_sent * 100) if total_sent > 0 else 0,
                    "by_status": {
                        status.value: len([c for c in campaigns if c.status == status])
                        for status in CampaignStatus
                    }
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération des stats: {str(e)}"
            }
