"""
Routes API pour la gestion du panier
Date : 24 Janvier 2026
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models.product_db import ProductDB, CartItemDB
from app.models.user_db import UserDB
from app.routes.auth_routes import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


# ========== MODÈLES PYDANTIC ==========

class CartAddRequest(BaseModel):
    """Modèle pour ajouter un produit au panier"""
    product_id: int
    quantity: int = 1


class CartUpdateRequest(BaseModel):
    """Modèle pour mettre à jour la quantité"""
    quantity: int


# ========== ROUTES API ==========

@router.get("")
async def get_cart(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupérer le panier de l'utilisateur connecté
    """
    try:
        # Récupérer tous les articles du panier
        cart_items = db.query(CartItemDB).filter(
            CartItemDB.user_id == current_user.id
        ).all()
        
        # Calculer les totaux
        subtotal = sum(item.price_at_addition * item.quantity for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        
        return {
            "success": True,
            "cart": {
                "items": [item.to_dict() for item in cart_items],
                "total_items": total_items,
                "subtotal": round(subtotal, 2),
                "tax": round(subtotal * 0.20, 2),  # TVA 20%
                "total": round(subtotal * 1.20, 2)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du panier: {str(e)}"
        )


@router.post("/add")
async def add_to_cart(
    request: CartAddRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ajouter un produit au panier
    """
    try:
        # Vérifier que le produit existe
        product = db.query(ProductDB).filter(ProductDB.id == request.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produit non trouvé"
            )
        
        # Vérifier la disponibilité
        if not product.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce produit n'est plus disponible"
            )
        
        # Vérifier le stock (si produit physique)
        if not product.is_digital and product.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuffisant. Disponible: {product.stock}"
            )
        
        # Vérifier si le produit est déjà dans le panier
        existing_item = db.query(CartItemDB).filter(
            CartItemDB.user_id == current_user.id,
            CartItemDB.product_id == request.product_id
        ).first()
        
        if existing_item:
            # Mettre à jour la quantité
            new_quantity = existing_item.quantity + request.quantity
            
            # Vérifier le stock pour la nouvelle quantité
            if not product.is_digital and product.stock < new_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuffisant. Disponible: {product.stock}"
                )
            
            existing_item.quantity = new_quantity
            db.commit()
            db.refresh(existing_item)
            
            return {
                "success": True,
                "message": "Quantité mise à jour",
                "item": existing_item.to_dict()
            }
        else:
            # Créer un nouvel article dans le panier
            cart_item = CartItemDB(
                user_id=current_user.id,
                product_id=request.product_id,
                quantity=request.quantity,
                price_at_addition=product.price
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            
            return {
                "success": True,
                "message": "Produit ajouté au panier",
                "item": cart_item.to_dict()
            }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'ajout au panier: {str(e)}"
        )


@router.put("/{item_id}")
async def update_cart_item(
    item_id: int,
    request: CartUpdateRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mettre à jour la quantité d'un article du panier
    """
    try:
        # Vérifier que la quantité est valide
        if request.quantity < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La quantité doit être au moins 1"
            )
        
        # Récupérer l'article du panier
        cart_item = db.query(CartItemDB).filter(
            CartItemDB.id == item_id,
            CartItemDB.user_id == current_user.id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article non trouvé dans le panier"
            )
        
        # Vérifier le stock si produit physique
        product = cart_item.product
        if not product.is_digital and product.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuffisant. Disponible: {product.stock}"
            )
        
        # Mettre à jour la quantité
        cart_item.quantity = request.quantity
        db.commit()
        db.refresh(cart_item)
        
        return {
            "success": True,
            "message": "Quantité mise à jour",
            "item": cart_item.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )


@router.delete("/{item_id}")
async def remove_from_cart(
    item_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprimer un article du panier
    """
    try:
        # Récupérer l'article du panier
        cart_item = db.query(CartItemDB).filter(
            CartItemDB.id == item_id,
            CartItemDB.user_id == current_user.id
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article non trouvé dans le panier"
            )
        
        # Supprimer l'article
        db.delete(cart_item)
        db.commit()
        
        return {
            "success": True,
            "message": "Article supprimé du panier"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )


@router.delete("")
async def clear_cart(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Vider complètement le panier
    """
    try:
        # Supprimer tous les articles du panier
        deleted_count = db.query(CartItemDB).filter(
            CartItemDB.user_id == current_user.id
        ).delete()
        
        db.commit()
        
        return {
            "success": True,
            "message": f"{deleted_count} article(s) supprimé(s)",
            "deleted_count": deleted_count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du vidage du panier: {str(e)}"
        )


@router.get("/count")
async def get_cart_count(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupérer le nombre d'articles dans le panier
    """
    try:
        cart_items = db.query(CartItemDB).filter(
            CartItemDB.user_id == current_user.id
        ).all()
        
        total_items = sum(item.quantity for item in cart_items)
        
        return {
            "success": True,
            "count": total_items
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur: {str(e)}"
        )
