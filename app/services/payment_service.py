"""
Service de gestion des paiements
Intégration Stripe, PayPal et virement bancaire
"""
import os
from typing import Dict, Optional
import stripe
from fastapi import HTTPException

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")

class PaymentService:
    """Service de gestion des paiements"""
    
    @staticmethod
    def create_stripe_payment_intent(amount: float, currency: str = "eur", metadata: dict = None) -> Dict:
        """
        Créer une intention de paiement Stripe
        
        Args:
            amount: Montant en euros
            currency: Devise (par défaut EUR)
            metadata: Métadonnées additionnelles
            
        Returns:
            Dict contenant client_secret et payment_intent_id
        """
        try:
            # Convertir en centimes
            amount_cents = int(amount * 100)
            
            # Créer l'intention de paiement
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                }
            )
            
            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id,
                "status": intent.status
            }
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Erreur Stripe: {str(e)}")
    
    @staticmethod
    def confirm_stripe_payment(payment_intent_id: str) -> Dict:
        """
        Confirmer un paiement Stripe
        
        Args:
            payment_intent_id: ID de l'intention de paiement
            
        Returns:
            Dict avec le statut du paiement
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                "status": intent.status,
                "amount": intent.amount / 100,
                "currency": intent.currency,
                "payment_method": intent.payment_method
            }
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Erreur Stripe: {str(e)}")
    
    @staticmethod
    def create_paypal_order(amount: float, currency: str = "EUR", description: str = "") -> Dict:
        """
        Créer une commande PayPal
        
        Args:
            amount: Montant
            currency: Devise
            description: Description de la commande
            
        Returns:
            Dict contenant order_id et approval_url
        """
        # Note: Nécessite l'installation de paypalrestsdk
        # pip install paypalrestsdk
        
        try:
            import paypalrestsdk
            
            # Configuration PayPal
            paypalrestsdk.configure({
                "mode": os.getenv("PAYPAL_MODE", "sandbox"),
                "client_id": os.getenv("PAYPAL_CLIENT_ID", ""),
                "client_secret": os.getenv("PAYPAL_CLIENT_SECRET", "")
            })
            
            # Créer la commande
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": os.getenv("PAYPAL_RETURN_URL", "http://webox.local:8000/payment/success"),
                    "cancel_url": os.getenv("PAYPAL_CANCEL_URL", "http://webox.local:8000/payment/cancel")
                },
                "transactions": [{
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": description
                }]
            })
            
            if payment.create():
                # Récupérer l'URL d'approbation
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return {
                    "order_id": payment.id,
                    "approval_url": approval_url,
                    "status": payment.state
                }
            else:
                raise HTTPException(status_code=400, detail=f"Erreur PayPal: {payment.error}")
                
        except ImportError:
            raise HTTPException(status_code=500, detail="Module PayPal non installé")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur PayPal: {str(e)}")
    
    @staticmethod
    def execute_paypal_payment(payment_id: str, payer_id: str) -> Dict:
        """
        Exécuter un paiement PayPal
        
        Args:
            payment_id: ID du paiement
            payer_id: ID du payeur
            
        Returns:
            Dict avec le statut du paiement
        """
        try:
            import paypalrestsdk
            
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                return {
                    "status": "completed",
                    "payment_id": payment.id,
                    "amount": payment.transactions[0].amount.total,
                    "currency": payment.transactions[0].amount.currency
                }
            else:
                raise HTTPException(status_code=400, detail=f"Erreur PayPal: {payment.error}")
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur PayPal: {str(e)}")
    
    @staticmethod
    def generate_bank_transfer_reference(order_id: str, user_id: str) -> Dict:
        """
        Générer une référence de virement bancaire
        
        Args:
            order_id: ID de la commande
            user_id: ID de l'utilisateur
            
        Returns:
            Dict avec les informations de virement
        """
        # Générer une référence unique
        reference = f"WB-{order_id}-{user_id}"
        
        return {
            "reference": reference,
            "bank_name": "Banque WeBox",
            "iban": "FR76 XXXX XXXX XXXX XXXX XXXX XXX",
            "bic": "WBOXFRPP",
            "account_holder": "WeBox SAS",
            "instructions": f"Merci d'indiquer la référence suivante lors de votre virement : {reference}",
            "processing_time": "2-3 jours ouvrés"
        }
    
    @staticmethod
    def verify_bank_transfer(reference: str) -> Dict:
        """
        Vérifier un virement bancaire
        
        Args:
            reference: Référence du virement
            
        Returns:
            Dict avec le statut de vérification
        """
        # Cette fonction devrait vérifier dans la base de données
        # si le virement a été reçu
        
        return {
            "reference": reference,
            "status": "pending",  # pending, completed, failed
            "message": "Virement en cours de vérification"
        }
    
    @staticmethod
    def create_payment_record(
        user_id: str,
        amount: float,
        payment_method: str,
        payment_id: str,
        status: str = "pending",
        metadata: dict = None
    ) -> Dict:
        """
        Créer un enregistrement de paiement dans la base de données
        
        Args:
            user_id: ID de l'utilisateur
            amount: Montant
            payment_method: Méthode de paiement (stripe, paypal, bank_transfer)
            payment_id: ID du paiement
            status: Statut (pending, completed, failed)
            metadata: Métadonnées additionnelles
            
        Returns:
            Dict avec les informations du paiement
        """
        # Cette fonction devrait enregistrer dans la base de données
        
        return {
            "id": payment_id,
            "user_id": user_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": status,
            "metadata": metadata or {},
            "created_at": "2026-01-23T23:00:00Z"
        }
