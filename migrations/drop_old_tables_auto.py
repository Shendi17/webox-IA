"""
Suppression automatique des tables anciennes après migration
Date: 3 Février 2026
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import SessionLocal


def drop_old_tables():
    """Supprimer les tables anciennes après migration"""
    print("=" * 60)
    print("SUPPRESSION AUTOMATIQUE DES TABLES ANCIENNES")
    print("=" * 60)
    
    tables_to_drop = [
        "email_campaigns_old",
        "funnels_old",
        "funnel_analytics",
        "funnel_contacts"
    ]
    
    db = SessionLocal()
    
    try:
        for table_name in tables_to_drop:
            print(f"\n🗑️  Suppression de la table '{table_name}'...")
            
            try:
                # Vérifier si la table existe
                result = db.execute(text(f"""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='{table_name}'
                """))
                
                if result.fetchone():
                    # Supprimer la table
                    db.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                    db.commit()
                    print(f"✅ Table '{table_name}' supprimée")
                else:
                    print(f"⏭️  Table '{table_name}' n'existe pas (déjà supprimée)")
                    
            except Exception as e:
                print(f"⚠️  Erreur lors de la suppression de '{table_name}': {str(e)}")
                db.rollback()
        
        print("\n" + "=" * 60)
        print("✅ NETTOYAGE TERMINÉ")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur fatale: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def verify_tables():
    """Vérifier les tables restantes"""
    print("\n🔍 Vérification des tables restantes...")
    
    db = SessionLocal()
    
    try:
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """))
        
        tables = [row[0] for row in result.fetchall()]
        
        print(f"\n📊 Tables présentes dans la base de données ({len(tables)}):")
        
        # Filtrer les tables marketing
        marketing_tables = [t for t in tables if 'email' in t or 'funnel' in t or 'lead' in t or 'campaign' in t]
        
        if marketing_tables:
            print("\n📧 Tables Marketing/CRM:")
            for table in marketing_tables:
                print(f"   - {table}")
        
        # Vérifier les tables anciennes
        old_tables = [t for t in tables if '_old' in t]
        
        if old_tables:
            print(f"\n⚠️  Tables anciennes encore présentes:")
            for table in old_tables:
                print(f"   - {table}")
            return False
        else:
            print("\n✅ Aucune table ancienne détectée")
            return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 Démarrage de la suppression automatique des tables anciennes...\n")
    
    success = drop_old_tables()
    
    if success:
        verify_tables()
        print("\n✅ Opération terminée avec succès!")
    else:
        print("\n❌ Opération échouée")
