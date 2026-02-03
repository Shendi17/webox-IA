"""
Script de migration pour créer la table ai_agents
Date: 13 Décembre 2024
"""
import sys
sys.path.append('.')

from app.database import engine, Base
from app.models.ai_agent import AIAgent
from sqlalchemy import text

def create_ai_agents_table():
    """Créer la table ai_agents"""
    
    print("🔧 Création de la table ai_agents...")
    
    # Créer la table
    Base.metadata.create_all(bind=engine, tables=[AIAgent.__table__])
    
    print("✅ Table ai_agents créée avec succès!")
    
    # Insérer les agents marketplace par défaut
    from sqlalchemy.orm import Session
    db = Session(bind=engine)
    
    try:
        # Vérifier si des agents marketplace existent déjà
        existing = db.query(AIAgent).filter(AIAgent.is_marketplace == True).count()
        
        if existing > 0:
            print(f"ℹ️  {existing} agents marketplace déjà présents")
            return
        
        print("📦 Insertion des agents marketplace par défaut...")
        
        marketplace_agents = [
            {
                "name": "Rédacteur SEO",
                "icon": "📝",
                "category": "marketing",
                "status": "premium",
                "description": "Rédaction d'articles optimisés SEO avec recherche de mots-clés",
                "features": ["Recherche keywords", "Optimisation SEO", "Meta descriptions", "Structure H1-H6"],
                "is_marketplace": True,
                "downloads": 1234,
                "rating": 4.9,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.7,
                "instructions": "Tu es un expert en rédaction SEO. Tu aides à créer du contenu optimisé pour les moteurs de recherche."
            },
            {
                "name": "Analyste Data",
                "icon": "📊",
                "category": "dev",
                "status": "active",
                "description": "Analyse de données et création de rapports automatisés",
                "features": ["Analyse statistique", "Visualisations", "Rapports PDF", "Prédictions"],
                "is_marketplace": True,
                "downloads": 892,
                "rating": 4.8,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.5,
                "instructions": "Tu es un analyste de données expert. Tu aides à analyser et interpréter les données."
            },
            {
                "name": "Designer UI/UX",
                "icon": "🎨",
                "category": "marketing",
                "status": "active",
                "description": "Conseils design et création de maquettes",
                "features": ["Audit UX", "Wireframes", "Prototypes", "Design system"],
                "is_marketplace": True,
                "downloads": 756,
                "rating": 4.7,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.8,
                "instructions": "Tu es un designer UI/UX expert. Tu aides à créer des interfaces utilisateur intuitives."
            },
            {
                "name": "Email Marketing",
                "icon": "📧",
                "category": "marketing",
                "status": "active",
                "description": "Création de campagnes email et newsletters",
                "features": ["Templates email", "A/B testing", "Segmentation", "Analytics"],
                "is_marketplace": True,
                "downloads": 1567,
                "rating": 4.9,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.7,
                "instructions": "Tu es un expert en email marketing. Tu aides à créer des campagnes email efficaces."
            },
            {
                "name": "Social Media Manager",
                "icon": "📱",
                "category": "marketing",
                "status": "active",
                "description": "Gestion des réseaux sociaux et création de contenu",
                "features": ["Planification posts", "Hashtags", "Analytics", "Engagement"],
                "is_marketplace": True,
                "downloads": 2134,
                "rating": 4.8,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.8,
                "instructions": "Tu es un expert en réseaux sociaux. Tu aides à créer du contenu engageant."
            },
            {
                "name": "Code Assistant",
                "icon": "💻",
                "category": "dev",
                "status": "active",
                "description": "Assistant de développement et génération de code",
                "features": ["Génération code", "Refactoring", "Tests unitaires", "Documentation"],
                "is_marketplace": True,
                "downloads": 1823,
                "rating": 4.9,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.3,
                "instructions": "Tu es un développeur expert. Tu aides à écrire du code propre et efficace."
            }
        ]
        
        for agent_data in marketplace_agents:
            agent = AIAgent(**agent_data)
            db.add(agent)
        
        db.commit()
        print(f"✅ {len(marketplace_agents)} agents marketplace insérés!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_ai_agents_table()
