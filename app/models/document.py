from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base

class DocumentAnalysis(Base):
    __tablename__ = "document_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Informations du fichier
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx, xlsx, pptx, image
    file_size = Column(Integer)  # en bytes
    
    # Extraction
    extracted_text = Column(Text)
    page_count = Column(Integer)
    
    # Analyse IA
    summary = Column(Text)  # Résumé du document
    key_points = Column(JSON)  # Points clés extraits
    entities = Column(JSON)  # Entités (noms, dates, montants, etc.)
    categories = Column(JSON)  # Catégories détectées
    sentiment = Column(String(50))  # positive, negative, neutral
    language = Column(String(10))  # fr, en, etc.
    
    # Métadonnées extraites
    document_metadata = Column(JSON)  # Auteur, date création, etc.
    
    # Questions/Réponses
    qa_pairs = Column(JSON)  # Questions posées et réponses
    
    # Statut
    status = Column(String(50), default="processing")  # processing, completed, error
    error_message = Column(Text)
    
    # Statistiques
    views_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "extracted_text": self.extracted_text,
            "page_count": self.page_count,
            "summary": self.summary,
            "key_points": self.key_points,
            "entities": self.entities,
            "categories": self.categories,
            "sentiment": self.sentiment,
            "language": self.language,
            "document_metadata": self.document_metadata,
            "qa_pairs": self.qa_pairs,
            "status": self.status,
            "error_message": self.error_message,
            "views_count": self.views_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
