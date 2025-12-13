from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from app.database import get_db
from app.models.document import DocumentAnalysis
from app.services.document_service import DocumentService

router = APIRouter(prefix="/api/documents", tags=["documents"])
document_service = DocumentService()

# Modèles Pydantic
class QuestionRequest(BaseModel):
    question: str

# Routes
@router.get("/formats")
async def get_supported_formats():
    """Obtenir les formats supportés"""
    try:
        formats = document_service.get_supported_formats()
        return {"success": True, "formats": formats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Upload et analyse d'un document"""
    try:
        # Vérifier le type de fichier
        file_extension = Path(file.filename).suffix.lower()
        allowed_extensions = [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".jpg", ".jpeg", ".png", ".gif", ".bmp"]
        
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Type de fichier non supporté : {file_extension}")
        
        # Créer le dossier uploads
        upload_dir = Path("uploads/documents")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder le fichier
        file_path = upload_dir / f"{hash(file.filename)}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Déterminer le type
        file_type = "pdf" if file_extension == ".pdf" else \
                   "docx" if file_extension in [".docx", ".doc"] else \
                   "xlsx" if file_extension in [".xlsx", ".xls"] else \
                   "image"
        
        # Créer l'entrée en BDD
        document = DocumentAnalysis(
            user_id=1,  # À remplacer par l'utilisateur connecté
            filename=file.filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_type=file_type,
            file_size=file_path.stat().st_size,
            status="processing"
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Lancer l'analyse en arrière-plan
        background_tasks.add_task(
            analyze_document_task,
            document.id,
            str(file_path),
            file_type,
            file.filename
        )
        
        return {
            "success": True,
            "document": document.to_dict(),
            "message": "Document en cours d'analyse..."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lister les documents analysés"""
    try:
        total = db.query(DocumentAnalysis).count()
        documents = db.query(DocumentAnalysis).order_by(
            DocumentAnalysis.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "documents": [d.to_dict() for d in documents],
            "total": total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Obtenir un document spécifique"""
    try:
        document = db.query(DocumentAnalysis).filter(
            DocumentAnalysis.id == document_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document non trouvé")
        
        # Incrémenter les vues
        document.views_count += 1
        db.commit()
        
        return {
            "success": True,
            "document": document.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{document_id}/question")
async def ask_question(
    document_id: int,
    question_data: QuestionRequest,
    db: Session = Depends(get_db)
):
    """Poser une question sur le document"""
    try:
        document = db.query(DocumentAnalysis).filter(
            DocumentAnalysis.id == document_id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document non trouvé")
        
        if not document.extracted_text:
            raise HTTPException(status_code=400, detail="Document non encore analysé")
        
        # Répondre à la question
        result = await document_service.answer_question(
            document.extracted_text,
            question_data.question
        )
        
        if result["success"]:
            # Sauvegarder la Q&A
            qa_pairs = document.qa_pairs or []
            qa_pairs.append({
                "question": question_data.question,
                "answer": result["answer"]
            })
            document.qa_pairs = qa_pairs
            db.commit()
            
            return {
                "success": True,
                "question": question_data.question,
                "answer": result["answer"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Supprimer un document"""
    try:
        document = db.query(DocumentAnalysis).filter(
            DocumentAnalysis.id == document_id
        ).first()
        
        if document:
            # Supprimer le fichier
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
            
            db.delete(document)
            db.commit()
        
        return {"success": True, "message": "Document supprimé"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_stats(db: Session = Depends(get_db)):
    """Obtenir les statistiques globales"""
    try:
        total_documents = db.query(DocumentAnalysis).count()
        total_views = db.query(DocumentAnalysis).with_entities(
            db.func.sum(DocumentAnalysis.views_count)
        ).scalar() or 0
        
        by_type = {}
        for file_type in ["pdf", "docx", "xlsx", "image"]:
            count = db.query(DocumentAnalysis).filter(
                DocumentAnalysis.file_type == file_type
            ).count()
            by_type[file_type] = count
        
        return {
            "success": True,
            "stats": {
                "total_documents": total_documents,
                "total_views": total_views,
                "by_type": by_type
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tâche en arrière-plan
async def analyze_document_task(document_id: int, file_path: str, 
                               file_type: str, filename: str):
    """Tâche d'analyse de document"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        document = db.query(DocumentAnalysis).filter(
            DocumentAnalysis.id == document_id
        ).first()
        if not document:
            return
        
        # Extraire le texte
        extract_result = await document_service.extract_text(file_path, file_type)
        
        if extract_result["success"]:
            document.extracted_text = extract_result["text"]
            document.page_count = extract_result.get("page_count", 0)
            db.commit()
            
            # Analyser avec IA
            analysis_result = await document_service.analyze_document_with_ai(
                extract_result["text"],
                filename
            )
            
            if analysis_result["success"]:
                analysis = analysis_result["analysis"]
                
                document.summary = analysis.get("summary")
                document.key_points = analysis.get("key_points")
                document.entities = analysis.get("entities")
                document.categories = analysis.get("categories")
                document.sentiment = analysis.get("sentiment")
                document.language = analysis.get("language")
                document.document_metadata = {
                    "document_type": analysis.get("document_type")
                }
                document.status = "completed"
                db.commit()
            else:
                document.status = "error"
                document.error_message = analysis_result.get("error")
                db.commit()
        else:
            document.status = "error"
            document.error_message = extract_result.get("error")
            db.commit()
            
    except Exception as e:
        print(f"Erreur analyse document: {e}")
        document.status = "error"
        document.error_message = str(e)
        db.commit()
    finally:
        db.close()
