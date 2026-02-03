"""
Script de test pour vérifier l'API agents
"""
import sys
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.ai_agent import AIAgent

def test_query():
    """Tester la requête des agents"""
    db = next(get_db())
    
    try:
        # Test 1: Compter les agents
        count = db.query(AIAgent).count()
        print(f"✅ Nombre total d'agents: {count}")
        
        # Test 2: Récupérer les agents marketplace
        marketplace_agents = db.query(AIAgent).filter(AIAgent.is_marketplace == True).all()
        print(f"✅ Agents marketplace: {len(marketplace_agents)}")
        
        # Test 3: Afficher un agent
        if marketplace_agents:
            agent = marketplace_agents[0]
            print(f"\n📊 Premier agent marketplace:")
            print(f"  ID: {agent.id}")
            print(f"  Nom: {agent.name}")
            print(f"  Catégorie: {agent.category}")
            print(f"  Description: {agent.description}")
            
            # Test 4: Tester to_dict()
            try:
                agent_dict = agent.to_dict()
                print(f"\n✅ to_dict() fonctionne:")
                print(f"  Keys: {list(agent_dict.keys())}")
            except Exception as e:
                print(f"\n❌ Erreur to_dict(): {e}")
                import traceback
                traceback.print_exc()
        
        # Test 5: Simuler la requête de l'API
        print("\n🔍 Test requête API (agents utilisateur):")
        user_agents = db.query(AIAgent).filter(
            AIAgent.user_id == 1,  # ID utilisateur test
            AIAgent.is_marketplace == False
        ).all()
        print(f"  Agents utilisateur (user_id=1): {len(user_agents)}")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_query()
