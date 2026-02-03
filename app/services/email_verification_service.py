"""
Service de vérification d'email
Gère l'envoi et la validation des emails de vérification
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.database import SessionLocal
from app.models.user_db import UserDB


class EmailVerificationService:
    """Service pour gérer la vérification d'email"""
    
    def __init__(self):
        self.token_expiry_hours = 48
        self.tokens_storage = {}  # En production, utiliser Redis ou DB
    
    def generate_verification_token(self, user_id: int, email: str) -> str:
        """
        Génère un token de vérification pour un utilisateur
        
        Returns:
            Token de vérification
        """
        token = secrets.token_urlsafe(32)
        
        self.tokens_storage[token] = {
            "user_id": user_id,
            "email": email,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        
        return token
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valide un token de vérification
        
        Returns:
            Informations du token si valide, None sinon
        """
        if token not in self.tokens_storage:
            return None
        
        token_data = self.tokens_storage[token]
        
        # Vérifier l'expiration
        if datetime.utcnow() > token_data["expires_at"]:
            del self.tokens_storage[token]
            return None
        
        return token_data
    
    def verify_email(self, token: str) -> Dict[str, Any]:
        """
        Vérifie l'email avec un token valide
        
        Returns:
            Dict avec success et message
        """
        token_data = self.validate_token(token)
        
        if not token_data:
            return {
                "success": False,
                "error": "Token invalide ou expiré"
            }
        
        db = SessionLocal()
        
        try:
            user = db.query(UserDB).filter(UserDB.id == token_data["user_id"]).first()
            
            if not user:
                return {
                    "success": False,
                    "error": "Utilisateur non trouvé"
                }
            
            # Marquer l'email comme vérifié
            user.email_verified = True
            user.email_verified_at = datetime.utcnow()
            
            db.commit()
            
            # Supprimer le token utilisé
            del self.tokens_storage[token]
            
            return {
                "success": True,
                "message": "Email vérifié avec succès"
            }
            
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la vérification: {str(e)}"
            }
        finally:
            db.close()
    
    def send_verification_email(self, user_id: int, email: str) -> bool:
        """
        Envoie l'email de vérification
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            from app.services.email_service import email_service
            
            # Générer le token
            token = self.generate_verification_token(user_id, email)
            
            verification_url = f"http://localhost:8000/verify-email?token={token}"
            
            subject = "Vérifiez votre adresse email - WeBox"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #3498db;">Bienvenue sur WeBox Multi-IA ! 🎉</h2>
                    
                    <p>Bonjour,</p>
                    
                    <p>Merci de vous être inscrit sur WeBox Multi-IA, votre plateforme de génération IA.</p>
                    
                    <p>Pour activer votre compte, veuillez vérifier votre adresse email en cliquant sur le bouton ci-dessous :</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" 
                           style="background-color: #27ae60; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Vérifier mon email
                        </a>
                    </div>
                    
                    <p>Ou copiez ce lien dans votre navigateur :</p>
                    <p style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; 
                              word-break: break-all;">
                        {verification_url}
                    </p>
                    
                    <p><strong>Ce lien est valide pendant {self.token_expiry_hours} heures.</strong></p>
                    
                    <p>Une fois votre email vérifié, vous pourrez profiter de toutes les fonctionnalités :</p>
                    <ul>
                        <li>🎨 Génération d'images avec DALL-E et Stable Diffusion</li>
                        <li>📚 Création d'eBooks personnalisés</li>
                        <li>🎬 Génération de vidéos et publicités</li>
                        <li>🤖 Chat avec plusieurs IA (GPT-4, Claude, Gemini)</li>
                        <li>🛍️ Marketplace de contenus IA</li>
                    </ul>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                    
                    <p style="color: #777; font-size: 12px;">
                        WeBox Multi-IA - Plateforme de génération IA<br>
                        Cet email a été envoyé automatiquement, merci de ne pas y répondre.
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Bienvenue sur WeBox Multi-IA !
            
            Merci de vous être inscrit sur notre plateforme.
            
            Pour activer votre compte, veuillez vérifier votre adresse email en cliquant sur ce lien :
            {verification_url}
            
            Ce lien est valide pendant {self.token_expiry_hours} heures.
            
            WeBox Multi-IA
            """
            
            result = email_service.send_email(
                to_email=email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
            return result
            
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
    
    def resend_verification_email(self, user_id: int) -> Dict[str, Any]:
        """
        Renvoie l'email de vérification
        
        Returns:
            Dict avec success et message
        """
        db = SessionLocal()
        
        try:
            user = db.query(UserDB).filter(UserDB.id == user_id).first()
            
            if not user:
                return {
                    "success": False,
                    "error": "Utilisateur non trouvé"
                }
            
            if user.email_verified:
                return {
                    "success": False,
                    "error": "Email déjà vérifié"
                }
            
            # Envoyer l'email
            email_sent = self.send_verification_email(user.id, user.email)
            
            if not email_sent:
                return {
                    "success": False,
                    "error": "Erreur lors de l'envoi de l'email"
                }
            
            return {
                "success": True,
                "message": "Email de vérification renvoyé"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            db.close()


# Instance globale
email_verification_service = EmailVerificationService()
