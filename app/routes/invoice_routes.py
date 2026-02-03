"""
Routes API pour les factures
"""
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from app.middleware.auth import get_current_user_from_token
from app.services.invoice_service import invoice_service
import os

router = APIRouter(prefix="/api/invoice", tags=["invoice"])


class InvoiceItem(BaseModel):
    name: str
    quantity: int
    price: float


class InvoiceGenerate(BaseModel):
    order_id: int
    items: List[InvoiceItem]
    discount: float = 0.0
    shipping: float = 0.0
    payment_method: str = "Carte bancaire"


@router.post("/generate")
async def generate_invoice(
    request: InvoiceGenerate,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Générer une facture PDF pour une commande
    """
    try:
        # Préparer les données de commande
        order_data = {
            "items": [item.dict() for item in request.items],
            "discount": request.discount,
            "shipping": request.shipping,
            "payment_method": request.payment_method,
            "total": sum(item.quantity * item.price for item in request.items) - request.discount + request.shipping
        }
        
        # Préparer les données utilisateur
        user_data = {
            "name": current_user.get("name", "Client"),
            "email": current_user.get("email", ""),
            "address": current_user.get("address", "Adresse non renseignée")
        }
        
        # Générer la facture
        filepath = invoice_service.generate_invoice(
            order_id=request.order_id,
            order_data=order_data,
            user_data=user_data
        )
        
        if not filepath:
            raise HTTPException(status_code=500, detail="Erreur lors de la génération de la facture")
        
        return {
            "success": True,
            "invoice_number": f"INV-{request.order_id:06d}",
            "filepath": filepath,
            "message": "Facture générée avec succès"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@router.get("/download/{order_id}")
async def download_invoice(
    order_id: int,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Télécharger une facture PDF
    """
    invoice_number = f"INV-{order_id:06d}"
    filename = f"facture_{invoice_number}.pdf"
    filepath = os.path.join("generated/invoices", filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename
    )


@router.get("/list")
async def list_invoices(
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Lister toutes les factures de l'utilisateur
    """
    invoices_dir = "generated/invoices"
    
    if not os.path.exists(invoices_dir):
        return {"invoices": []}
    
    invoices = []
    for filename in os.listdir(invoices_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(invoices_dir, filename)
            stat = os.stat(filepath)
            
            invoices.append({
                "filename": filename,
                "size": stat.st_size,
                "created_at": stat.st_ctime
            })
    
    return {"invoices": invoices, "total": len(invoices)}
