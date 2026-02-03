"""
Script pour ajouter plus d'agents marketplace (toutes les catégories)
Date: 13 Décembre 2024
"""
import sys
sys.path.append('.')

from app.database import engine
from app.models.ai_agent import AIAgent
from sqlalchemy.orm import Session

def add_marketplace_agents():
    """Ajouter des agents marketplace pour toutes les catégories"""
    
    db = Session(bind=engine)
    
    try:
        print("📦 Ajout d'agents marketplace supplémentaires...")
        
        new_agents = [
            # SALES (Ventes)
            {
                "name": "Expert Ventes B2B",
                "icon": "💼",
                "category": "sales",
                "status": "active",
                "description": "Spécialiste en ventes B2B et négociation commerciale",
                "features": ["Prospection B2B", "Négociation", "Closing", "Account management"],
                "is_marketplace": True,
                "downloads": 987,
                "rating": 4.8,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.7,
                "instructions": "Tu es un expert en ventes B2B. Tu aides à prospecter, négocier et conclure des ventes."
            },
            
            # SUPPORT
            {
                "name": "Assistant Support Client",
                "icon": "🎧",
                "category": "support",
                "status": "active",
                "description": "Support client 24/7 et gestion des tickets",
                "features": ["Réponses automatiques", "Gestion tickets", "FAQ dynamique", "Escalade intelligente"],
                "is_marketplace": True,
                "downloads": 2456,
                "rating": 4.9,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.6,
                "instructions": "Tu es un assistant support client expert. Tu aides à résoudre les problèmes clients rapidement."
            },
            
            # FINANCE
            {
                "name": "Analyste Financier",
                "icon": "💹",
                "category": "finance",
                "status": "active",
                "description": "Analyse financière et gestion de trésorerie",
                "features": ["Analyse financière", "Prévisions", "Budgets", "Reporting"],
                "is_marketplace": True,
                "downloads": 1234,
                "rating": 4.7,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.4,
                "instructions": "Tu es un analyste financier expert. Tu aides à analyser les données financières et créer des rapports."
            },
            
            # OPERATIONS
            {
                "name": "Manager Opérations",
                "icon": "⚙️",
                "category": "operations",
                "status": "active",
                "description": "Optimisation des processus et gestion de projet",
                "features": ["Process mapping", "Optimisation", "Gestion projet", "KPIs"],
                "is_marketplace": True,
                "downloads": 876,
                "rating": 4.6,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.6,
                "instructions": "Tu es un expert en opérations. Tu aides à optimiser les processus et gérer les projets."
            },
            
            # STRATEGY (Stratégie)
            {
                "name": "Consultant Stratégie",
                "icon": "🎯",
                "category": "strategy",
                "status": "active",
                "description": "Conseil stratégique et développement business",
                "features": ["Analyse marché", "Business plan", "Roadmap", "Positionnement"],
                "is_marketplace": True,
                "downloads": 1543,
                "rating": 4.8,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.7,
                "instructions": "Tu es un consultant en stratégie. Tu aides à définir la stratégie et le développement business."
            },
            
            # HR (Ressources Humaines)
            {
                "name": "Expert RH & Recrutement",
                "icon": "👥",
                "category": "hr",
                "status": "active",
                "description": "Gestion RH et processus de recrutement",
                "features": ["Recrutement", "Onboarding", "Formation", "Évaluation"],
                "is_marketplace": True,
                "downloads": 1098,
                "rating": 4.7,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.6,
                "instructions": "Tu es un expert RH. Tu aides au recrutement, onboarding et gestion des talents."
            },
            
            # PRODUCT (Produit)
            {
                "name": "Product Manager",
                "icon": "📱",
                "category": "product",
                "status": "active",
                "description": "Gestion produit et roadmap",
                "features": ["Product vision", "Roadmap", "User stories", "Priorisation"],
                "is_marketplace": True,
                "downloads": 1345,
                "rating": 4.8,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.7,
                "instructions": "Tu es un Product Manager expert. Tu aides à définir la vision produit et la roadmap."
            },
            
            # Agents supplémentaires pour catégories existantes
            {
                "name": "Growth Hacker",
                "icon": "🚀",
                "category": "marketing",
                "status": "active",
                "description": "Stratégies de croissance et acquisition",
                "features": ["Growth hacking", "Acquisition", "Viral loops", "Metrics"],
                "is_marketplace": True,
                "downloads": 1876,
                "rating": 4.9,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.8,
                "instructions": "Tu es un growth hacker expert. Tu aides à développer des stratégies de croissance rapide."
            },
            
            {
                "name": "DevOps Engineer",
                "icon": "🔧",
                "category": "dev",
                "status": "active",
                "description": "Infrastructure et automatisation DevOps",
                "features": ["CI/CD", "Docker", "Kubernetes", "Monitoring"],
                "is_marketplace": True,
                "downloads": 1456,
                "rating": 4.7,
                "price": "Gratuit",
                "model": "gpt-4",
                "temperature": 0.5,
                "instructions": "Tu es un DevOps engineer expert. Tu aides à automatiser l'infrastructure et les déploiements."
            }
        ]
        
        for agent_data in new_agents:
            # Vérifier si l'agent existe déjà
            existing = db.query(AIAgent).filter(
                AIAgent.name == agent_data["name"],
                AIAgent.is_marketplace == True
            ).first()
            
            if not existing:
                agent = AIAgent(**agent_data)
                db.add(agent)
                print(f"  ✅ {agent_data['name']} ({agent_data['category']})")
        
        db.commit()
        print(f"\n✅ Agents marketplace ajoutés avec succès!")
        
        # Afficher le résumé par catégorie
        print("\n📊 Résumé par catégorie:")
        categories = db.query(AIAgent.category).filter(AIAgent.is_marketplace == True).distinct().all()
        for (cat,) in categories:
            count = db.query(AIAgent).filter(
                AIAgent.category == cat,
                AIAgent.is_marketplace == True
            ).count()
            print(f"  {cat}: {count} agents")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_marketplace_agents()
