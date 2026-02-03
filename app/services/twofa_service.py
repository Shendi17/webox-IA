"""
Service 2FA (Authentification à deux facteurs)
Utilise TOTP (Time-based One-Time Password)
"""
import pyotp
import qrcode
import io
import base64
from datetime import datetime
from typing import Optional, Tuple


class TwoFAService:
    """Service de gestion 2FA"""
    
    def __init__(self):
        self.issuer_name = "WeBox"
    
    def generate_secret(self) -> str:
        """
        Générer un secret TOTP pour un utilisateur
        
        Returns:
            Secret encodé en base32
        """
        return pyotp.random_base32()
    
    def get_provisioning_uri(self, email: str, secret: str) -> str:
        """
        Générer l'URI de provisioning pour les apps d'authentification
        
        Args:
            email: Email de l'utilisateur
            secret: Secret TOTP
            
        Returns:
            URI de provisioning
        """
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=email,
            issuer_name=self.issuer_name
        )
    
    def generate_qr_code(self, email: str, secret: str) -> str:
        """
        Générer un QR code pour l'activation 2FA
        
        Args:
            email: Email de l'utilisateur
            secret: Secret TOTP
            
        Returns:
            QR code en base64
        """
        uri = self.get_provisioning_uri(email, secret)
        
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        # Convertir en image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir en base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    def verify_token(self, secret: str, token: str) -> bool:
        """
        Vérifier un code TOTP
        
        Args:
            secret: Secret TOTP de l'utilisateur
            token: Code à 6 chiffres fourni par l'utilisateur
            
        Returns:
            True si le code est valide
        """
        try:
            totp = pyotp.TOTP(secret)
            # Vérifier avec une fenêtre de tolérance de ±1 intervalle (30s)
            return totp.verify(token, valid_window=1)
        except Exception as e:
            print(f"Erreur vérification 2FA: {e}")
            return False
    
    def get_current_token(self, secret: str) -> str:
        """
        Obtenir le code actuel (pour tests)
        
        Args:
            secret: Secret TOTP
            
        Returns:
            Code à 6 chiffres actuel
        """
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    def generate_backup_codes(self, count: int = 10) -> list:
        """
        Générer des codes de secours
        
        Args:
            count: Nombre de codes à générer
            
        Returns:
            Liste de codes de secours
        """
        import secrets
        import string
        
        codes = []
        for _ in range(count):
            # Générer un code de 8 caractères
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                          for _ in range(8))
            # Formater: XXXX-XXXX
            formatted = f"{code[:4]}-{code[4:]}"
            codes.append(formatted)
        
        return codes


# Instance globale
twofa_service = TwoFAService()
