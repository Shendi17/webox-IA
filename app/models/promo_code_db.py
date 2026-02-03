"""
Modèle de base de données pour les codes promo
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.database import Base


class PromoCodeDB(Base):
    """Modèle pour les codes promo"""
    __tablename__ = "promo_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    discount_type = Column(String(20), nullable=False)
    discount_value = Column(Float, nullable=False)
    min_amount = Column(Float, default=0.0)
    max_uses = Column(Integer, nullable=True)
    current_uses = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    description = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
