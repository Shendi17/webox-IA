"""
Service d'envoi d'emails automatiques
"""
import os
from typing import List, Optional
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@webox.com")
        self.from_name = os.getenv("FROM_NAME", "WeBox Multi-IA")
        
    def _create_message(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> MIMEMultipart:
        """Créer un message email"""
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email
        
        # Ajouter version texte
        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)
        
        # Ajouter version HTML
        part2 = MIMEText(html_content, "html")
        message.attach(part2)
        
        return message
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Envoyer un email"""
        try:
            # Si pas de configuration SMTP, enregistrer dans un fichier
            if not self.smtp_user or not self.smtp_password:
                return await self._save_to_file(to_email, subject, html_content)
            
            message = self._create_message(to_email, subject, html_content, text_content)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
    
    async def _save_to_file(self, to_email: str, subject: str, content: str) -> bool:
        """Enregistrer l'email dans un fichier (mode développement)"""
        try:
            log_dir = "logs/emails"
            os.makedirs(log_dir, exist_ok=True)
            
            filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{to_email.replace('@', '_')}.html"
            filepath = os.path.join(log_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"<!-- Email pour: {to_email} -->\n")
                f.write(f"<!-- Sujet: {subject} -->\n")
                f.write(f"<!-- Date: {datetime.utcnow().isoformat()} -->\n\n")
                f.write(content)
            
            print(f"Email enregistré: {filepath}")
            return True
            
        except Exception as e:
            print(f"Erreur sauvegarde email: {e}")
            return False
    
    async def send_order_confirmation(
        self,
        to_email: str,
        order_id: str,
        items: List[dict],
        total: float
    ) -> bool:
        """Envoyer email de confirmation de commande"""
        subject = f"Confirmation de commande #{order_id}"
        
        items_html = ""
        for item in items:
            items_html += f"""
            <tr>
                <td>{item['name']}</td>
                <td>{item['quantity']}</td>
                <td>{item['price']:.2f} €</td>
            </tr>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                .total {{ font-size: 1.2em; font-weight: bold; text-align: right; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>WeBox Multi-IA</h1>
                    <p>Confirmation de commande</p>
                </div>
                <div class="content">
                    <h2>Merci pour votre commande !</h2>
                    <p>Votre commande <strong>#{order_id}</strong> a été confirmée.</p>
                    
                    <h3>Détails de la commande:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Produit</th>
                                <th>Quantité</th>
                                <th>Prix</th>
                            </tr>
                        </thead>
                        <tbody>
                            {items_html}
                        </tbody>
                    </table>
                    
                    <p class="total">Total: {total:.2f} €</p>
                    
                    <p>Vous recevrez un email de confirmation dès que votre commande sera expédiée.</p>
                </div>
                <div class="footer">
                    <p>© 2026 WeBox Multi-IA - Tous droits réservés</p>
                    <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        """Envoyer email de bienvenue"""
        subject = "Bienvenue sur WeBox Multi-IA !"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>WeBox Multi-IA</h1>
                </div>
                <div class="content">
                    <h2>Bienvenue {username} !</h2>
                    <p>Merci de vous être inscrit sur WeBox Multi-IA, votre plateforme de génération de contenu par intelligence artificielle.</p>
                    
                    <p>Vous pouvez maintenant:</p>
                    <ul>
                        <li>Générer des images avec DALL-E</li>
                        <li>Créer des eBooks complets</li>
                        <li>Produire des vidéos shorts</li>
                        <li>Et bien plus encore...</li>
                    </ul>
                    
                    <a href="http://localhost:8000/dashboard" class="button">Accéder au Dashboard</a>
                    
                    <p>Si vous avez des questions, n'hésitez pas à contacter notre support.</p>
                </div>
                <div class="footer">
                    <p>© 2026 WeBox Multi-IA - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_password_reset(self, to_email: str, reset_token: str) -> bool:
        """Envoyer email de réinitialisation de mot de passe"""
        subject = "Réinitialisation de votre mot de passe"
        
        reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>WeBox Multi-IA</h1>
                </div>
                <div class="content">
                    <h2>Réinitialisation de mot de passe</h2>
                    <p>Vous avez demandé à réinitialiser votre mot de passe.</p>
                    
                    <p>Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe:</p>
                    
                    <a href="{reset_link}" class="button">Réinitialiser mon mot de passe</a>
                    
                    <div class="warning">
                        <strong>⚠️ Important:</strong> Ce lien est valable pendant 1 heure.
                    </div>
                    
                    <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.</p>
                </div>
                <div class="footer">
                    <p>© 2026 WeBox Multi-IA - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)


# Instance globale du service
email_service = EmailService()
