"""
Script pour créer les tables du Studio Créatif
"""

from app.database import Base, engine
from app.models.podcast import Podcast
from app.models.avatar import Avatar
from app.models.ai_agent import AgentConversation, AgentMessage
from app.models.series import Series, Episode, Scene
from app.models.pwa import PWAProject
from app.models.react_native import ReactNativeProject
from app.models.document import DocumentAnalysis

def create_tables():
    """Créer toutes les tables du Studio Créatif"""
    print("🔧 Création des tables du Studio Créatif...")
    
    try:
        # Créer les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès !")
        print("   - podcasts")
        print("   - avatars")
        print("   - agent_conversations")
        print("   - agent_messages")
        print("   - series")
        print("   - episodes")
        print("   - scenes")
        print("   - pwa_projects")
        print("   - react_native_projects")
        print("   - document_analyses")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")

if __name__ == "__main__":
    create_tables()
