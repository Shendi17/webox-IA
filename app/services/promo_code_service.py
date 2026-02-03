"""
Service de gestion des codes promo
"""
from datetime import datetime
from typing import Optional, List, Dict
from app.database import SessionLocal
from app.models.promo_code_db import PromoCodeDB


class PromoCodeService:
    """Service pour gérer les codes promo"""
    
    def validate_code(self, code: str, cart_total: float) -> Dict:
        """
        Valide un code promo et calcule la réduction
        """
        db = SessionLocal()
        
        try:
            promo = db.query(PromoCodeDB).filter(
                PromoCodeDB.code == code.upper()
            ).first()
            
            if not promo:
                return {"success": False, "error": "Code promo invalide"}
            
            if not promo.is_active:
                return {"success": False, "error": "Code promo désactivé"}
            
            if promo.expires_at and datetime.now() > promo.expires_at:
                return {"success": False, "error": "Code promo expiré"}
            
            if promo.max_uses and promo.current_uses >= promo.max_uses:
                return {"success": False, "error": "Code promo épuisé"}
            
            if cart_total < promo.min_amount:
                return {
                    "success": False, 
                    "error": f"Montant minimum requis: {promo.min_amount}€"
                }
            
            discount_amount = 0
            if promo.discount_type == "percentage":
                discount_amount = cart_total * (promo.discount_value / 100)
            else:
                discount_amount = promo.discount_value
            
            discount_amount = min(discount_amount, cart_total)
            
            promo.current_uses += 1
            db.commit()
            
            return {
                "success": True,
                "code": promo.code,
                "discount_type": promo.discount_type,
                "discount_value": promo.discount_value,
                "discount_amount": round(discount_amount, 2),
                "new_total": round(cart_total - discount_amount, 2)
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()
    
    def create_code(
        self, 
        code: str, 
        discount_type: str, 
        discount_value: float,
        min_amount: float = 0.0,
        max_uses: Optional[int] = None,
        expires_at: Optional[str] = None,
        description: str = ""
    ) -> Dict:
        """
        Crée un nouveau code promo
        """
        db = SessionLocal()
        
        try:
            existing = db.query(PromoCodeDB).filter(
                PromoCodeDB.code == code.upper()
            ).first()
            
            if existing:
                return {"success": False, "error": "Ce code promo existe déjà"}
            
            if discount_type not in ["percentage", "fixed"]:
                return {
                    "success": False, 
                    "error": "Type de réduction invalide (percentage ou fixed)"
                }
            
            expires_dt = None
            if expires_at:
                try:
                    expires_dt = datetime.fromisoformat(expires_at)
                except:
                    pass
            
            new_promo = PromoCodeDB(
                code=code.upper(),
                discount_type=discount_type,
                discount_value=discount_value,
                min_amount=min_amount,
                max_uses=max_uses,
                expires_at=expires_dt,
                description=description,
                is_active=True,
                current_uses=0
            )
            
            db.add(new_promo)
            db.commit()
            
            return {
                "success": True,
                "message": "Code promo créé avec succès",
                "code": code.upper()
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
        finally:
            db.close()
    
    def list_codes(self, active_only: bool = False) -> List[Dict]:
        """
        Liste tous les codes promo
        """
        db = SessionLocal()
        
        try:
            query = db.query(PromoCodeDB)
            
            if active_only:
                query = query.filter(PromoCodeDB.is_active == True)
            
            promos = query.order_by(PromoCodeDB.created_at.desc()).all()
            
            codes = []
            for promo in promos:
                codes.append({
                    "code": promo.code,
                    "discount_type": promo.discount_type,
                    "discount_value": promo.discount_value,
                    "min_amount": promo.min_amount,
                    "max_uses": promo.max_uses,
                    "current_uses": promo.current_uses,
                    "expires_at": promo.expires_at.isoformat() if promo.expires_at else None,
                    "is_active": promo.is_active,
                    "description": promo.description,
                    "created_at": promo.created_at.isoformat() if promo.created_at else None
                })
            
            return codes
            
        except Exception as e:
            return []
        finally:
            db.close()
    
    def get_code(self, code: str) -> Optional[Dict]:
        """
        Récupère les informations d'un code promo
        """
        db = SessionLocal()
        
        try:
            promo = db.query(PromoCodeDB).filter(
                PromoCodeDB.code == code.upper()
            ).first()
            
            if not promo:
                return None
            
            return {
                "code": promo.code,
                "discount_type": promo.discount_type,
                "discount_value": promo.discount_value,
                "min_amount": promo.min_amount,
                "max_uses": promo.max_uses,
                "current_uses": promo.current_uses,
                "expires_at": promo.expires_at.isoformat() if promo.expires_at else None,
                "is_active": promo.is_active,
                "description": promo.description,
                "created_at": promo.created_at.isoformat() if promo.created_at else None
            }
            
        except Exception as e:
            return None
        finally:
            db.close()
    
    def delete_code(self, code: str) -> bool:
        """
        Supprime un code promo
        """
        db = SessionLocal()
        
        try:
            promo = db.query(PromoCodeDB).filter(
                PromoCodeDB.code == code.upper()
            ).first()
            
            if not promo:
                return False
            
            db.delete(promo)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            return False
        finally:
            db.close()
    
    def deactivate_code(self, code: str) -> bool:
        """
        Désactive un code promo
        """
        db = SessionLocal()
        
        try:
            promo = db.query(PromoCodeDB).filter(
                PromoCodeDB.code == code.upper()
            ).first()
            
            if not promo:
                return False
            
            promo.is_active = False
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            return False
        finally:
            db.close()


promo_service = PromoCodeService()
