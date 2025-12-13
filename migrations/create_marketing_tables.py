"""
Migration : Créer toutes les tables Marketing
Date : 23 Novembre 2025
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import engine, Base
from app.models.marketing_db import (
    Funnel, FunnelPage, EmailCampaign, Lead, LeadInteraction, AdCampaign
)

def create_tables():
    """Crée toutes les tables Marketing dans la base de données"""
    
    print("🔄 Création des tables Marketing...")
    print("=" * 60)
    
    try:
        # Créer toutes les tables définies dans Base
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables créées avec succès !")
        print("\nTables créées :")
        print("  ✅ funnels")
        print("  ✅ funnel_pages")
        print("  ✅ email_campaigns")
        print("  ✅ leads")
        print("  ✅ lead_interactions")
        print("  ✅ ad_campaigns")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        return False

if __name__ == "__main__":
    print("🚀 Migration : Création des tables Marketing")
    print("=" * 60)
    
    success = create_tables()
    
    print("=" * 60)
    if success:
        print("✅ Migration terminée avec succès !")
    else:
        print("❌ Migration échouée")
