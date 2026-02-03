"""
Routes pour les paiements
Gestion des paiements Stripe, PayPal et virement bancaire
"""
import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional
from app.services.payment_service import PaymentService
from app.routes.auth_routes import get_current_user
from app.models.user_db import UserDB

router = APIRouter(prefix="/api/payment", tags=["Payment"])

# Modèles de données
class StripePaymentRequest(BaseModel):
    amount: float
    currency: str = "eur"
    metadata: Optional[dict] = None

class PayPalOrderRequest(BaseModel):
    amount: float
    currency: str = "EUR"
    description: str = ""

class BankTransferRequest(BaseModel):
    order_id: str

class PaymentConfirmation(BaseModel):
    payment_intent_id: str

# Routes Stripe
@router.post("/stripe/create-intent")
async def create_stripe_intent(
    request: StripePaymentRequest,
    current_user: UserDB = Depends(get_current_user)
):
    """Créer une intention de paiement Stripe"""
    try:
        result = PaymentService.create_stripe_payment_intent(
            amount=request.amount,
            currency=request.currency,
            metadata={
                **(request.metadata or {}),
                "user_id": str(current_user.id),
                "user_email": current_user.email
            }
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stripe/confirm")
async def confirm_stripe_payment(
    request: PaymentConfirmation,
    current_user: UserDB = Depends(get_current_user)
):
    """Confirmer un paiement Stripe"""
    try:
        result = PaymentService.confirm_stripe_payment(request.payment_intent_id)
        
        # Enregistrer le paiement
        PaymentService.create_payment_record(
            user_id=str(current_user.id),
            amount=result["amount"],
            payment_method="stripe",
            payment_id=request.payment_intent_id,
            status=result["status"]
        )
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Routes PayPal
@router.post("/paypal/create-order")
async def create_paypal_order(
    request: PayPalOrderRequest,
    current_user: UserDB = Depends(get_current_user)
):
    """Créer une commande PayPal"""
    try:
        result = PaymentService.create_paypal_order(
            amount=request.amount,
            currency=request.currency,
            description=request.description or f"Commande WeBox - {current_user.email}"
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/paypal/success")
async def paypal_success(
    paymentId: str,
    PayerID: str,
    current_user: UserDB = Depends(get_current_user)
):
    """Callback de succès PayPal"""
    try:
        result = PaymentService.execute_paypal_payment(paymentId, PayerID)
        
        # Enregistrer le paiement
        PaymentService.create_payment_record(
            user_id=str(current_user.id),
            amount=float(result["amount"]),
            payment_method="paypal",
            payment_id=paymentId,
            status="completed"
        )
        
        # Rediriger vers la page de confirmation
        return RedirectResponse(url="/checkout?step=3&status=success")
    except Exception as e:
        return RedirectResponse(url="/checkout?step=2&error=payment_failed")

@router.get("/paypal/cancel")
async def paypal_cancel():
    """Callback d'annulation PayPal"""
    return RedirectResponse(url="/checkout?step=2&error=payment_cancelled")

# Routes virement bancaire
@router.post("/bank-transfer/generate")
async def generate_bank_transfer(
    request: BankTransferRequest,
    current_user: UserDB = Depends(get_current_user)
):
    """Générer les informations de virement bancaire"""
    try:
        result = PaymentService.generate_bank_transfer_reference(
            order_id=request.order_id,
            user_id=str(current_user.id)
        )
        
        # Enregistrer le paiement en attente
        PaymentService.create_payment_record(
            user_id=str(current_user.id),
            amount=0,  # Montant sera mis à jour lors de la vérification
            payment_method="bank_transfer",
            payment_id=result["reference"],
            status="pending",
            metadata=result
        )
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bank-transfer/verify/{reference}")
async def verify_bank_transfer(
    reference: str,
    current_user: UserDB = Depends(get_current_user)
):
    """Vérifier le statut d'un virement bancaire"""
    try:
        result = PaymentService.verify_bank_transfer(reference)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Webhook Stripe
@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """Webhook pour les événements Stripe"""
    import stripe
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET", "")
        )
        
        # Traiter l'événement
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            # Mettre à jour le statut du paiement dans la base de données
            print(f"Paiement réussi: {payment_intent['id']}")
        
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            # Mettre à jour le statut du paiement dans la base de données
            print(f"Paiement échoué: {payment_intent['id']}")
        
        return JSONResponse(content={"status": "success"})
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
