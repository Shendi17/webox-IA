"""
Modèles de base de données pour les produits et le panier
Date : 24 Janvier 2026
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_db import UserDB


class ProductDB(Base):
    """Modèle pour les produits de la marketplace"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    long_description = Column(Text)
    category = Column(String(100), index=True)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    discount_percentage = Column(Integer, default=0)
    currency = Column(String(3), default="EUR")
    
    # Images et médias
    image_url = Column(String(500))
    images = Column(JSON)  # Liste d'URLs d'images
    
    # Stock et disponibilité
    stock = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    is_digital = Column(Boolean, default=True)
    
    # Métadonnées
    badge = Column(String(50))  # "Populaire", "Nouveau", "Promo"
    reviews_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    sales_count = Column(Integer, default=0)
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(Text)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    cart_items = relationship("CartItemDB", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItemDB", back_populates="product")
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "long_description": self.long_description,
            "category": self.category,
            "price": self.price,
            "original_price": self.original_price,
            "discount_percentage": self.discount_percentage,
            "currency": self.currency,
            "image_url": self.image_url,
            "images": self.images,
            "stock": self.stock,
            "is_available": self.is_available,
            "is_digital": self.is_digital,
            "badge": self.badge,
            "reviews_count": self.reviews_count,
            "rating": self.rating,
            "sales_count": self.sales_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class CartItemDB(Base):
    """Modèle pour les articles du panier"""
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    
    # Prix au moment de l'ajout (pour garder l'historique)
    price_at_addition = Column(Float, nullable=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    # user = relationship("UserDB", back_populates="cart_items")  # Commenté temporairement
    product = relationship("ProductDB", back_populates="cart_items")
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price_at_addition": self.price_at_addition,
            "subtotal": self.price_at_addition * self.quantity,
            "product": self.product.to_dict() if self.product else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class OrderDB(Base):
    """Modèle pour les commandes"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Montants
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    shipping = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    currency = Column(String(3), default="EUR")
    
    # Statut
    status = Column(String(50), default="pending", index=True)
    # pending, processing, completed, cancelled, refunded
    
    # Paiement
    payment_method = Column(String(50))  # stripe, paypal, bank_transfer
    payment_id = Column(String(255))
    payment_status = Column(String(50), default="pending")
    
    # Informations de facturation
    billing_name = Column(String(255))
    billing_email = Column(String(255))
    billing_address = Column(Text)
    billing_city = Column(String(100))
    billing_postal_code = Column(String(20))
    billing_country = Column(String(100))
    
    # Informations de livraison (si différent)
    shipping_name = Column(String(255))
    shipping_address = Column(Text)
    shipping_city = Column(String(100))
    shipping_postal_code = Column(String(20))
    shipping_country = Column(String(100))
    
    # Notes
    customer_notes = Column(Text)
    admin_notes = Column(Text)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relations
    # user = relationship("UserDB", back_populates="orders")  # Commenté temporairement
    items = relationship("OrderItemDB", back_populates="order", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "user_id": self.user_id,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "shipping": self.shipping,
            "discount": self.discount,
            "total": self.total,
            "currency": self.currency,
            "status": self.status,
            "payment_method": self.payment_method,
            "payment_id": self.payment_id,
            "payment_status": self.payment_status,
            "billing_name": self.billing_name,
            "billing_email": self.billing_email,
            "billing_address": self.billing_address,
            "billing_city": self.billing_city,
            "billing_postal_code": self.billing_postal_code,
            "billing_country": self.billing_country,
            "customer_notes": self.customer_notes,
            "items": [item.to_dict() for item in self.items] if self.items else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class OrderItemDB(Base):
    """Modèle pour les articles d'une commande"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Informations du produit au moment de la commande
    product_name = Column(String(255), nullable=False)
    product_description = Column(Text)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    order = relationship("OrderDB", back_populates="items")
    product = relationship("ProductDB", back_populates="order_items")
    
    def to_dict(self):
        """Convertir en dictionnaire"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
