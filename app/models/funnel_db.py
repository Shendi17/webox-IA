"""
Modèles SQLAlchemy pour les Tunnels de Vente (Sales Funnels)
Date : 15 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
from app.database import Base


class FunnelDB(Base):
    """
    Modèle pour les tunnels de vente (DEPRECATED - Utiliser marketing_db.Funnel)
    Table: funnels_old
    """
    __tablename__ = "funnels_old"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    template = Column(String(100), nullable=True)  # lead-gen, product-sale, webinar, launch, ecommerce
    
    # Structure du tunnel
    steps = Column(JSON, nullable=True)  # Liste des étapes avec leur configuration
    # Format: [
    #   {
    #     "id": "step1",
    #     "type": "ad",  # ad, landing-page, email, presentation, etc.
    #     "name": "Publicité Facebook",
    #     "config": {...},
    #     "next_steps": ["step2"],
    #     "conditions": {...}
    #   }
    # ]
    
    # Automatisations
    automations = Column(JSON, nullable=True)  # Règles d'automatisation
    # Format: [
    #   {
    #     "trigger": "email_opened",
    #     "conditions": {...},
    #     "actions": [{"type": "send_email", "params": {...}}]
    #   }
    # ]
    
    # Analytics globales
    total_entries = Column(Integer, default=0)  # Nombre total d'entrées dans le tunnel
    total_conversions = Column(Integer, default=0)  # Nombre de conversions finales
    conversion_rate = Column(Float, default=0.0)  # Taux de conversion global
    total_revenue = Column(Float, default=0.0)  # Revenu total généré
    avg_time_to_convert = Column(Integer, default=0)  # Temps moyen de conversion (secondes)
    
    # Statut
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "template": self.template,
            "steps": self.steps,
            "automations": self.automations,
            "total_entries": self.total_entries,
            "total_conversions": self.total_conversions,
            "conversion_rate": self.conversion_rate,
            "total_revenue": self.total_revenue,
            "is_active": self.is_active,
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class FunnelAnalyticsDB(Base):
    """
    Modèle pour les analytics par étape de tunnel
    Table: funnel_analytics
    """
    __tablename__ = "funnel_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    funnel_id = Column(Integer, nullable=False, index=True)
    step_id = Column(String(100), nullable=False)  # ID de l'étape dans le tunnel
    
    # Métriques
    entries = Column(Integer, default=0)  # Nombre d'entrées dans cette étape
    exits = Column(Integer, default=0)  # Nombre de sorties (abandons)
    conversions = Column(Integer, default=0)  # Nombre de passages à l'étape suivante
    conversion_rate = Column(Float, default=0.0)  # Taux de conversion de cette étape
    avg_time_spent = Column(Integer, default=0)  # Temps moyen passé (secondes)
    
    # Revenue (si applicable)
    revenue = Column(Float, default=0.0)
    
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "funnel_id": self.funnel_id,
            "step_id": self.step_id,
            "entries": self.entries,
            "exits": self.exits,
            "conversions": self.conversions,
            "conversion_rate": self.conversion_rate,
            "avg_time_spent": self.avg_time_spent,
            "revenue": self.revenue,
            "date": self.date.isoformat() if self.date else None
        }


class FunnelContactDB(Base):
    """
    Modèle pour les contacts dans les tunnels
    Table: funnel_contacts
    """
    __tablename__ = "funnel_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    funnel_id = Column(Integer, nullable=False, index=True)
    
    # Informations contact
    email = Column(String(255), nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Parcours dans le tunnel
    current_step = Column(String(100), nullable=True)  # Étape actuelle
    completed_steps = Column(JSON, nullable=True)  # Liste des étapes complétées
    # Format: ["step1", "step2", "step3"]
    
    # Données personnalisées
    tags = Column(JSON, nullable=True)  # Tags pour segmentation
    custom_fields = Column(JSON, nullable=True)  # Champs personnalisés
    
    # Conversion
    has_converted = Column(Boolean, default=False)
    conversion_value = Column(Float, default=0.0)
    converted_at = Column(DateTime, nullable=True)
    
    # Tracking
    source = Column(String(100), nullable=True)  # Source d'acquisition
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    
    # Engagement
    last_activity_at = Column(DateTime, nullable=True)
    total_emails_opened = Column(Integer, default=0)
    total_emails_clicked = Column(Integer, default=0)
    total_pages_viewed = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "funnel_id": self.funnel_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "tags": self.tags,
            "has_converted": self.has_converted,
            "conversion_value": self.conversion_value,
            "source": self.source,
            "last_activity_at": self.last_activity_at.isoformat() if self.last_activity_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
