"""
Modèles SQLAlchemy pour le Marketing & Business
Date : 23 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class FunnelType(str, enum.Enum):
    """Types de tunnels de vente"""
    WEBINAR = "webinar"
    PRODUCT = "product"
    SERVICE = "service"
    LEAD_MAGNET = "lead_magnet"
    MEMBERSHIP = "membership"
    OTHER = "other"


class FunnelPageType(str, enum.Enum):
    """Types de pages de tunnel"""
    OPTIN = "optin"
    VSL = "vsl"
    SALES = "sales"
    UPSELL = "upsell"
    DOWNSELL = "downsell"
    THANK_YOU = "thank_you"
    WEBINAR = "webinar"


class CampaignStatus(str, enum.Enum):
    """Statuts de campagne"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class LeadStatus(str, enum.Enum):
    """Statuts de lead"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class Funnel(Base):
    """
    Modèle pour les tunnels de vente
    Table: funnels
    """
    __tablename__ = "funnels"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations de base
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    funnel_type = Column(Enum(FunnelType), nullable=False)
    
    # Configuration
    is_active = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    
    # Statistiques
    total_visitors = Column(Integer, default=0)
    total_leads = Column(Integer, default=0)
    total_sales = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    # Auteur
    author_id = Column(Integer, nullable=False, index=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    pages = relationship("FunnelPage", back_populates="funnel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Funnel(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "funnel_type": self.funnel_type.value if self.funnel_type else None,
            "is_active": self.is_active,
            "total_visitors": self.total_visitors,
            "total_leads": self.total_leads,
            "total_sales": self.total_sales,
            "total_revenue": self.total_revenue,
            "conversion_rate": self.conversion_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class FunnelPage(Base):
    """
    Modèle pour les pages de tunnel
    Table: funnel_pages
    """
    __tablename__ = "funnel_pages"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec le tunnel
    funnel_id = Column(Integer, ForeignKey("funnels.id"), nullable=False, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    page_type = Column(Enum(FunnelPageType), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    
    # Contenu
    html_content = Column(Text, nullable=True)
    css_content = Column(Text, nullable=True)
    js_content = Column(Text, nullable=True)
    
    # Configuration
    order = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    
    # SEO
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(500), nullable=True)
    
    # Statistiques
    visitors = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    funnel = relationship("Funnel", back_populates="pages")
    
    def __repr__(self):
        return f"<FunnelPage(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "funnel_id": self.funnel_id,
            "name": self.name,
            "page_type": self.page_type.value if self.page_type else None,
            "slug": self.slug,
            "is_published": self.is_published,
            "visitors": self.visitors,
            "conversions": self.conversions,
            "conversion_rate": self.conversion_rate
        }


class EmailCampaign(Base):
    """
    Modèle pour les campagnes email
    Table: email_campaigns
    """
    __tablename__ = "email_campaigns"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    preheader = Column(String(500), nullable=True)
    
    # Contenu
    html_content = Column(Text, nullable=False)
    text_content = Column(Text, nullable=True)
    
    # Configuration
    from_name = Column(String(255), nullable=True)
    from_email = Column(String(255), nullable=True)
    reply_to = Column(String(255), nullable=True)
    
    # Statut
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Planification
    scheduled_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    
    # Statistiques
    total_recipients = Column(Integer, default=0)
    total_sent = Column(Integer, default=0)
    total_delivered = Column(Integer, default=0)
    total_opened = Column(Integer, default=0)
    total_clicked = Column(Integer, default=0)
    total_bounced = Column(Integer, default=0)
    total_unsubscribed = Column(Integer, default=0)
    
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    
    # Segmentation
    segment_rules = Column(JSON, nullable=True)
    
    # Auteur
    author_id = Column(Integer, nullable=False, index=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<EmailCampaign(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "subject": self.subject,
            "status": self.status.value if self.status else None,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "total_recipients": self.total_recipients,
            "total_sent": self.total_sent,
            "total_opened": self.total_opened,
            "total_clicked": self.total_clicked,
            "open_rate": self.open_rate,
            "click_rate": self.click_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Lead(Base):
    """
    Modèle pour les leads CRM
    Table: leads
    """
    __tablename__ = "leads"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations personnelles
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    
    # Statut
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, index=True)
    
    # Scoring
    score = Column(Integer, default=0)
    
    # Source
    source = Column(String(255), nullable=True)  # Formulaire, publicité, etc.
    source_url = Column(String(500), nullable=True)
    
    # Valeur
    estimated_value = Column(Float, default=0.0)
    
    # Tags et notes
    tags = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Données personnalisées
    custom_fields = Column(JSON, nullable=True)
    
    # Propriétaire
    owner_id = Column(Integer, nullable=True, index=True)
    
    # Auteur (qui a créé le lead)
    author_id = Column(Integer, nullable=False, index=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact_at = Column(DateTime, nullable=True)
    
    # Relations
    interactions = relationship("LeadInteraction", back_populates="lead", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lead(id={self.id}, email='{self.email}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "job_title": self.job_title,
            "status": self.status.value if self.status else None,
            "score": self.score,
            "source": self.source,
            "estimated_value": self.estimated_value,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_contact_at": self.last_contact_at.isoformat() if self.last_contact_at else None
        }


class LeadInteraction(Base):
    """
    Modèle pour les interactions avec les leads
    Table: lead_interactions
    """
    __tablename__ = "lead_interactions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec le lead
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    
    # Type d'interaction
    interaction_type = Column(String(100), nullable=False)  # email, call, meeting, note
    
    # Contenu
    subject = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    
    # Métadonnées (renommé car 'metadata' est réservé)
    interaction_metadata = Column(JSON, nullable=True)
    
    # Auteur
    author_id = Column(Integer, nullable=False)
    
    # Date
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    lead = relationship("Lead", back_populates="interactions")
    
    def __repr__(self):
        return f"<LeadInteraction(id={self.id}, type='{self.interaction_type}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "interaction_type": self.interaction_type,
            "subject": self.subject,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class AdCampaign(Base):
    """
    Modèle pour les campagnes publicitaires
    Table: ad_campaigns
    """
    __tablename__ = "ad_campaigns"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Plateforme
    platform = Column(String(100), nullable=False)  # facebook, google, linkedin, etc.
    
    # Créatifs
    ad_copy = Column(Text, nullable=True)
    headline = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    
    # Ciblage
    target_audience = Column(JSON, nullable=True)
    
    # Budget
    daily_budget = Column(Float, default=0.0)
    total_budget = Column(Float, default=0.0)
    
    # Statut
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Statistiques
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    spent = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)  # Click-through rate
    cpc = Column(Float, default=0.0)  # Cost per click
    cpa = Column(Float, default=0.0)  # Cost per acquisition
    
    # Auteur
    author_id = Column(Integer, nullable=False, index=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<AdCampaign(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "platform": self.platform,
            "status": self.status.value if self.status else None,
            "daily_budget": self.daily_budget,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "conversions": self.conversions,
            "spent": self.spent,
            "ctr": self.ctr,
            "cpc": self.cpc,
            "cpa": self.cpa,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
