"""
Service pour la gestion des tunnels de vente
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import re

from app.models.marketing_db import Funnel, FunnelPage, FunnelType, FunnelPageType
from app.services.ai_providers import AIProviderFactory


class FunnelService:
    """Service pour gérer les tunnels de vente"""
    
    @staticmethod
    def create_funnel(db: Session, funnel_data: Dict, author_id: int) -> Dict:
        """
        Créer un tunnel de vente
        
        Args:
            db: Session de base de données
            funnel_data: Données du tunnel
            author_id: ID de l'auteur
        
        Returns:
            Dict avec le tunnel créé
        """
        try:
            funnel = Funnel(
                name=funnel_data.get("name"),
                description=funnel_data.get("description"),
                funnel_type=FunnelType[funnel_data.get("funnel_type", "PRODUCT").upper()],
                is_template=funnel_data.get("is_template", False),
                author_id=author_id
            )
            
            db.add(funnel)
            db.commit()
            db.refresh(funnel)
            
            return {
                "success": True,
                "funnel": funnel.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la création du tunnel: {str(e)}"
            }
    
    @staticmethod
    def get_funnel(db: Session, funnel_id: int, author_id: int) -> Optional[Funnel]:
        """Récupérer un tunnel"""
        return db.query(Funnel).filter(
            Funnel.id == funnel_id,
            Funnel.author_id == author_id
        ).first()
    
    @staticmethod
    def list_funnels(db: Session, author_id: int, is_template: bool = None) -> List[Funnel]:
        """Lister les tunnels"""
        query = db.query(Funnel).filter(Funnel.author_id == author_id)
        
        if is_template is not None:
            query = query.filter(Funnel.is_template == is_template)
        
        return query.order_by(Funnel.created_at.desc()).all()
    
    @staticmethod
    def update_funnel(db: Session, funnel_id: int, author_id: int, update_data: Dict) -> Dict:
        """Mettre à jour un tunnel"""
        try:
            funnel = FunnelService.get_funnel(db, funnel_id, author_id)
            
            if not funnel:
                return {
                    "success": False,
                    "error": "Tunnel non trouvé"
                }
            
            for key, value in update_data.items():
                if hasattr(funnel, key):
                    setattr(funnel, key, value)
            
            funnel.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(funnel)
            
            return {
                "success": True,
                "funnel": funnel.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la mise à jour: {str(e)}"
            }
    
    @staticmethod
    def delete_funnel(db: Session, funnel_id: int, author_id: int) -> Dict:
        """Supprimer un tunnel"""
        try:
            funnel = FunnelService.get_funnel(db, funnel_id, author_id)
            
            if not funnel:
                return {
                    "success": False,
                    "error": "Tunnel non trouvé"
                }
            
            db.delete(funnel)
            db.commit()
            
            return {
                "success": True,
                "message": "Tunnel supprimé"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la suppression: {str(e)}"
            }
    
    @staticmethod
    def add_page(db: Session, funnel_id: int, author_id: int, page_data: Dict) -> Dict:
        """Ajouter une page au tunnel"""
        try:
            funnel = FunnelService.get_funnel(db, funnel_id, author_id)
            
            if not funnel:
                return {
                    "success": False,
                    "error": "Tunnel non trouvé"
                }
            
            # Générer un slug unique
            slug = re.sub(r'[^a-z0-9]+', '-', page_data.get("name", "").lower())
            slug = f"{slug}-{funnel_id}"
            
            page = FunnelPage(
                funnel_id=funnel_id,
                name=page_data.get("name"),
                page_type=FunnelPageType[page_data.get("page_type", "SALES").upper()],
                slug=slug,
                html_content=page_data.get("html_content", ""),
                css_content=page_data.get("css_content", ""),
                js_content=page_data.get("js_content", ""),
                order=page_data.get("order", 0),
                meta_title=page_data.get("meta_title"),
                meta_description=page_data.get("meta_description")
            )
            
            db.add(page)
            db.commit()
            db.refresh(page)
            
            return {
                "success": True,
                "page": page.to_dict()
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de l'ajout de la page: {str(e)}"
            }
    
    @staticmethod
    def get_funnel_stats(db: Session, funnel_id: int, author_id: int) -> Dict:
        """Obtenir les statistiques d'un tunnel"""
        try:
            funnel = FunnelService.get_funnel(db, funnel_id, author_id)
            
            if not funnel:
                return {
                    "success": False,
                    "error": "Tunnel non trouvé"
                }
            
            pages = db.query(FunnelPage).filter(FunnelPage.funnel_id == funnel_id).all()
            
            total_visitors = sum(page.visitors for page in pages)
            total_conversions = sum(page.conversions for page in pages)
            
            return {
                "success": True,
                "stats": {
                    "total_visitors": total_visitors,
                    "total_conversions": total_conversions,
                    "total_pages": len(pages),
                    "conversion_rate": (total_conversions / total_visitors * 100) if total_visitors > 0 else 0,
                    "pages": [
                        {
                            "name": page.name,
                            "type": page.page_type.value,
                            "visitors": page.visitors,
                            "conversions": page.conversions,
                            "conversion_rate": page.conversion_rate
                        }
                        for page in pages
                    ]
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération des stats: {str(e)}"
            }
    
    @staticmethod
    def generate_funnel_with_ai(
        db: Session,
        funnel_type: str,
        topic: str,
        target_audience: str,
        author_id: int
    ) -> Dict:
        """
        Générer un tunnel complet avec IA
        
        Args:
            db: Session de base de données
            funnel_type: Type de tunnel
            topic: Sujet du tunnel
            target_audience: Audience cible
            author_id: ID de l'auteur
        
        Returns:
            Dict avec le tunnel généré
        """
        try:
            ai_provider = AIProviderFactory.get_provider("gpt-4")
            
            prompt = f"""Tu es un expert en tunnels de vente et copywriting.

Crée un tunnel de vente complet de type "{funnel_type}" sur le sujet : "{topic}"
Audience cible : {target_audience}

Génère la structure complète avec :
1. Nom du tunnel
2. Description
3. Liste des pages (optin, vsl, sales, upsell, downsell, thank_you)

Pour chaque page, fournis :
- Nom de la page
- Type (optin, vsl, sales, etc.)
- Titre accrocheur
- Sous-titre
- Points clés (3-5 bullets)
- Call-to-action

Réponds en JSON avec ce format :
{{
    "name": "Nom du tunnel",
    "description": "Description",
    "pages": [
        {{
            "name": "Nom de la page",
            "type": "optin",
            "title": "Titre",
            "subtitle": "Sous-titre",
            "bullets": ["Point 1", "Point 2", ...],
            "cta": "Call-to-action"
        }}
    ]
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
            content = response["content"]
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                funnel_data = json.loads(json_match.group())
            else:
                funnel_data = json.loads(content)
            
            # Créer le tunnel
            funnel = Funnel(
                name=funnel_data.get("name"),
                description=funnel_data.get("description"),
                funnel_type=FunnelType[funnel_type.upper()],
                author_id=author_id
            )
            
            db.add(funnel)
            db.flush()
            
            # Créer les pages
            for i, page_data in enumerate(funnel_data.get("pages", [])):
                slug = re.sub(r'[^a-z0-9]+', '-', page_data.get("name", "").lower())
                slug = f"{slug}-{funnel.id}"
                
                # Générer le HTML de la page
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{page_data.get('title')}</title>
    <meta name="description" content="{page_data.get('subtitle')}">
</head>
<body>
    <h1>{page_data.get('title')}</h1>
    <h2>{page_data.get('subtitle')}</h2>
    <ul>
        {''.join(f'<li>{bullet}</li>' for bullet in page_data.get('bullets', []))}
    </ul>
    <button>{page_data.get('cta')}</button>
</body>
</html>
"""
                
                page = FunnelPage(
                    funnel_id=funnel.id,
                    name=page_data.get("name"),
                    page_type=FunnelPageType[page_data.get("type", "sales").upper()],
                    slug=slug,
                    html_content=html_content,
                    order=i,
                    meta_title=page_data.get("title"),
                    meta_description=page_data.get("subtitle")
                )
                
                db.add(page)
            
            db.commit()
            db.refresh(funnel)
            
            return {
                "success": True,
                "funnel": funnel.to_dict(),
                "pages_count": len(funnel_data.get("pages", []))
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
