"""
Migration pour créer les tables agents IA et CRM
Date : 3 Février 2026
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.models.ai_agent import AIAgent
from app.models.marketing_db import Lead, LeadInteraction, EmailCampaign, Funnel, FunnelPage

print("🔧 Création des tables agents IA et CRM...")
print("")

try:
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables créées avec succès !")
    print("")
    print("Tables créées :")
    print("  - ai_agents (Agents IA)")
    print("  - leads (Leads CRM)")
    print("  - lead_interactions (Interactions avec les leads)")
    print("  - email_campaigns (Campagnes email)")
    print("  - funnels (Tunnels de vente)")
    print("  - funnel_pages (Pages de tunnels)")
    print("")
    print("🎉 Migration terminée avec succès !")
    
except Exception as e:
    print(f"❌ Erreur lors de la création des tables : {e}")
    print("")
    import traceback
    traceback.print_exc()
