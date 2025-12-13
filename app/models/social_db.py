"""
Modèles SQLAlchemy pour les Réseaux Sociaux
Date : 15 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from datetime import datetime
from app.database import Base


class SocialAccountDB(Base):
    """
    Modèle pour les comptes de réseaux sociaux connectés
    Table: social_accounts
    """
    __tablename__ = "social_accounts"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations de la plateforme
    platform = Column(String(50), nullable=False)  # instagram, facebook, twitter, linkedin, tiktok, youtube
    account_name = Column(String(255), nullable=True)
    account_id = Column(String(255), nullable=True)
    
    # Tokens OAuth (chiffrés)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Statut
    is_active = Column(Boolean, default=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SocialAccount(id={self.id}, platform='{self.platform}', account='{self.account_name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "platform": self.platform,
            "account_name": self.account_name,
            "account_id": self.account_id,
            "is_active": self.is_active,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ScheduledPostDB(Base):
    """
    Modèle pour les posts programmés
    Table: scheduled_posts
    """
    __tablename__ = "scheduled_posts"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Contenu du post
    content = Column(Text, nullable=False)
    media_urls = Column(JSON, nullable=True)  # ['url1', 'url2']
    platforms = Column(JSON, nullable=False)  # ['instagram', 'facebook']
    hashtags = Column(JSON, nullable=True)  # ['#tag1', '#tag2']
    
    # Programmation
    scheduled_time = Column(DateTime, nullable=False, index=True)
    
    # Statut
    status = Column(String(50), default='scheduled')  # scheduled, published, failed, cancelled
    published_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Métadonnées
    platform_post_ids = Column(JSON, nullable=True)  # {'instagram': 'id1', 'facebook': 'id2'}
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScheduledPost(id={self.id}, status='{self.status}', scheduled='{self.scheduled_time}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "media_urls": self.media_urls,
            "platforms": self.platforms,
            "hashtags": self.hashtags,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "status": self.status,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "error_message": self.error_message,
            "platform_post_ids": self.platform_post_ids,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class PostAnalyticsDB(Base):
    """
    Modèle pour les statistiques des posts
    Table: post_analytics
    """
    __tablename__ = "post_analytics"
    
    # Colonnes principales
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    platform_post_id = Column(String(255), nullable=True)
    
    # Métriques
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    
    # Calculs
    engagement_rate = Column(Float, default=0.0)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<PostAnalytics(id={self.id}, platform='{self.platform}', engagement={self.engagement_rate}%)>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "platform": self.platform,
            "platform_post_id": self.platform_post_id,
            "views": self.views,
            "likes": self.likes,
            "comments": self.comments,
            "shares": self.shares,
            "saves": self.saves,
            "clicks": self.clicks,
            "engagement_rate": self.engagement_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
