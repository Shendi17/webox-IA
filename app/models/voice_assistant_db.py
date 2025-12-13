"""
Modèles SQLAlchemy pour les assistants vocaux
Date : 2 Novembre 2025
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from datetime import datetime
from app.database import Base


class VoiceAssistantDB(Base):
    """
    Modèle pour les assistants vocaux configurés
    Table: voice_assistants
    """
    __tablename__ = "voice_assistants"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informations client
    client_name = Column(String(255), nullable=False)  # Nom de l'entreprise cliente
    client_email = Column(String(255), nullable=True)
    
    # Configuration Twilio
    twilio_phone_number = Column(String(50), unique=True, nullable=False)
    twilio_account_sid = Column(String(255), nullable=True)
    twilio_auth_token = Column(String(255), nullable=True)
    
    # Configuration IA
    ai_model = Column(String(50), default="gpt-4")  # gpt-4, claude-3, etc.
    ai_context = Column(Text, nullable=False)  # Instructions/contexte pour l'IA
    ai_personality = Column(String(100), default="professional")  # professional, friendly, casual
    
    # Configuration voix
    voice_provider = Column(String(50), default="elevenlabs")  # elevenlabs, google, azure
    voice_id = Column(String(255), default="default")  # ID de la voix
    voice_language = Column(String(10), default="fr-FR")
    
    # Paramètres
    max_call_duration = Column(Integer, default=600)  # En secondes (10 min par défaut)
    enable_recording = Column(Boolean, default=True)
    enable_transcription = Column(Boolean, default=True)
    fallback_to_human = Column(Boolean, default=True)
    
    # Statistiques
    total_calls = Column(Integer, default=0)
    total_duration = Column(Integer, default=0)  # En secondes
    average_satisfaction = Column(Float, default=0.0)
    
    # Statut
    is_active = Column(Boolean, default=True)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Propriétaire
    owner_id = Column(Integer, nullable=True)
    owner_email = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<VoiceAssistant(id={self.id}, client='{self.client_name}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "client_name": self.client_name,
            "client_email": self.client_email,
            "twilio_phone_number": self.twilio_phone_number,
            "ai_model": self.ai_model,
            "ai_personality": self.ai_personality,
            "voice_provider": self.voice_provider,
            "voice_language": self.voice_language,
            "total_calls": self.total_calls,
            "total_duration": self.total_duration,
            "average_satisfaction": self.average_satisfaction,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class VoiceCallDB(Base):
    """
    Modèle pour l'historique des appels
    Table: voice_calls
    """
    __tablename__ = "voice_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Lien avec l'assistant
    assistant_id = Column(Integer, nullable=False)
    
    # Informations Twilio
    call_sid = Column(String(255), unique=True, nullable=False)
    from_number = Column(String(50), nullable=False)
    to_number = Column(String(50), nullable=False)
    
    # Détails de l'appel
    duration = Column(Integer, default=0)  # En secondes
    status = Column(String(50), default="initiated")  # initiated, in-progress, completed, failed
    
    # Transcription
    transcription = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    
    # Enregistrement
    recording_url = Column(String(500), nullable=True)
    
    # Satisfaction
    satisfaction_score = Column(Float, nullable=True)  # 0-5
    
    # Métadonnées
    call_metadata = Column(JSON, nullable=True)
    
    # Dates
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<VoiceCall(id={self.id}, call_sid='{self.call_sid}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "assistant_id": self.assistant_id,
            "call_sid": self.call_sid,
            "from_number": self.from_number,
            "to_number": self.to_number,
            "duration": self.duration,
            "status": self.status,
            "transcription": self.transcription,
            "ai_response": self.ai_response,
            "recording_url": self.recording_url,
            "satisfaction_score": self.satisfaction_score,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None
        }
