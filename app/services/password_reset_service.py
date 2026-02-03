"""
Service de réinitialisation de mot de passe
Gère les tokens de réinitialisation et l'envoi d'emails
"""
import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.database import SessionLocal
from app.models.user_db import UserDB


class PasswordResetService:
    """Service pour gérer la réinitialisation de mot de passe"""
    
    def __init__(self):
        self.token_expiry_hours = 24
        self.tokens_storage = {}  # En production, utiliser Redis ou DB
    
    def generate_reset_token(self, email: str) -> Optional[str]:
        """
        Génère un token de réinitialisation pour un email
        
        Returns:
            Token de réinitialisation ou None si l'email n'existe pas
        """
        db = SessionLocal()
        
        try:
            user = db.query(UserDB).filter(UserDB.email == email).first()
            
            if not user:
                return None
            
            # Générer un token sécurisé
            token = secrets.token_urlsafe(32)
            
            # Stocker le token avec expiration
            self.tokens_storage[token] = {
                "email": email,
                "user_id": user.id,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
            }
            
            return token
            
        except Exception as e:
            print(f"Erreur génération token: {e}")
            return None
        finally:
            db.close()
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valide un token de réinitialisation
        
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
    
    def reset_password(self, token: str, new_password: str) -> Dict[str, Any]:
        """
        Réinitialise le mot de passe avec un token valide
        
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
            
            # Hasher le nouveau mot de passe
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            user.password = hashed_password
            
            db.commit()
            
            # Supprimer le token utilisé
            del self.tokens_storage[token]
            
            return {
                "success": True,
                "message": "Mot de passe réinitialisé avec succès"
            }
            
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": f"Erreur lors de la réinitialisation: {str(e)}"
            }
        finally:
            db.close()
    
    def send_reset_email(self, email: str, token: str) -> bool:
        """
        Envoie l'email de réinitialisation
        
        Returns:
            True si envoyé, False sinon
        """
        try:
            from app.services.email_service import email_service
            
            reset_url = f"http://localhost:8000/reset-password?token={token}"
            
            subject = "Réinitialisation de votre mot de passe - WeBox"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #3498db;">Réinitialisation de mot de passe</h2>
                    
                    <p>Bonjour,</p>
                    
                    <p>Vous avez demandé la réinitialisation de votre mot de passe sur WeBox Multi-IA.</p>
                    
                    <p>Cliquez sur le bouton ci-dessous pour réinitialiser votre mot de passe :</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background-color: #3498db; color: white; padding: 12px 30px; 
                                  text-decoration: none; border-radius: 5px; display: inline-block;">
                            Réinitialiser mon mot de passe
                        </a>
                    </div>
                    
                    <p>Ou copiez ce lien dans votre navigateur :</p>
                    <p style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; 
                              word-break: break-all;">
                        {reset_url}
                    </p>
                    
                    <p><strong>Ce lien est valide pendant {self.token_expiry_hours} heures.</strong></p>
                    
                    <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.</p>
                    
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
            Réinitialisation de mot de passe - WeBox Multi-IA
            
            Bonjour,
            
            Vous avez demandé la réinitialisation de votre mot de passe.
            
            Cliquez sur ce lien pour réinitialiser votre mot de passe :
            {reset_url}
            
            Ce lien est valide pendant {self.token_expiry_hours} heures.
            
            Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
            
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
    
    def request_password_reset(self, email: str) -> Dict[str, Any]:
        """
        Demande complète de réinitialisation de mot de passe
        
        Returns:
            Dict avec success et message
        """
        # Générer le token
        token = self.generate_reset_token(email)
        
        if not token:
            # Ne pas révéler si l'email existe ou non (sécurité)
            return {
                "success": True,
                "message": "Si cet email existe, un lien de réinitialisation a été envoyé"
            }
        
        # Envoyer l'email
        email_sent = self.send_reset_email(email, token)
        
        if not email_sent:
            return {
                "success": False,
                "error": "Erreur lors de l'envoi de l'email"
            }
        
        return {
            "success": True,
            "message": "Un email de réinitialisation a été envoyé"
        }


# Instance globale
password_reset_service = PasswordResetService()
