"""
Script de migration pour créer toutes les tables de la base de données
Date: 25 Janvier 2026
"""

from app.database import engine, Base
from app.models.user_db import UserDB
from app.models.generation_db import (
    GeneratedImageDB,
    GeneratedVideoDB,
    GeneratedAudioDB,
    EBookDB,
    VideoShortDB,
    WorkflowDB,
    WorkflowExecutionDB,
    CatalogFavoriteDB,
    GeneratedAdDB
)
from app.models.promo_code_db import PromoCodeDB

def create_all_tables():
    """Créer toutes les tables dans la base de données"""
    print("🔧 Création des tables de la base de données...")
    print("-" * 60)
    
    try:
        # Créer toutes les tables définies dans les modèles
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables créées avec succès:")
        print("   - users")
        print("   - generated_images")
        print("   - generated_videos")
        print("   - generated_audios")
        print("   - ebooks")
        print("   - video_shorts")
        print("   - workflows")
        print("   - workflow_executions")
        print("   - catalog_favorites")
        print("   - generated_ads")
        print("   - promo_codes")
        print("-" * 60)
        print("✅ Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        raise

if __name__ == "__main__":
    create_all_tables()
