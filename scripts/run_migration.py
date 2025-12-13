"""
Script pour exécuter les migrations de base de données
Date : 10 Novembre 2025
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from app.database import DATABASE_URL, Base
from app.models import *  # Importer tous les modèles

def run_migration():
    """
    Créer toutes les tables définies dans les modèles SQLAlchemy
    """
    print("🚀 Démarrage de la migration...")
    print(f"📊 Base de données : {DATABASE_URL}")
    
    try:
        # Créer l'engine
        engine = create_engine(DATABASE_URL)
        
        # Créer toutes les tables
        print("\n📝 Création des tables...")
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Migration terminée avec succès !")
        print("\n📋 Tables créées :")
        
        # Lister les tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        for table in sorted(tables):
            print(f"  ✓ {table}")
        
        print(f"\n📊 Total : {len(tables)} tables")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la migration : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def check_tables():
    """
    Vérifier que toutes les tables existent
    """
    print("\n🔍 Vérification des tables...")
    
    try:
        engine = create_engine(DATABASE_URL)
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'users',
            'generated_images',
            'generated_videos',
            'generated_audio',
            'ebooks',
            'video_shorts',
            'workflows',
            'workflow_executions',
            'catalog_favorites',
            'generated_ads',
            'social_accounts',
            'scheduled_posts',
            'post_analytics',
            'ai_influencers',
            'influencer_content',
            'generated_logos',
            'presentations',
            'email_campaigns',
            'landing_pages',
            'funnels',
            'funnel_analytics',
            'funnel_contacts',
            'websites',
            'website_pages',
            'blog_posts',
            'website_analytics'
        ]
        
        missing_tables = []
        for table in required_tables:
            if table in tables:
                print(f"  ✓ {table}")
            else:
                print(f"  ✗ {table} (manquante)")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n⚠️ {len(missing_tables)} table(s) manquante(s)")
            return False
        else:
            print("\n✅ Toutes les tables sont présentes !")
            return True
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification : {e}")
        return False


def show_table_info(table_name):
    """
    Afficher les informations d'une table
    """
    try:
        engine = create_engine(DATABASE_URL)
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        print(f"\n📋 Table : {table_name}")
        print("=" * 60)
        
        # Colonnes
        columns = inspector.get_columns(table_name)
        print("\n🔹 Colonnes :")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"  - {col['name']:<30} {str(col['type']):<20} {nullable}")
        
        # Index
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\n🔹 Index :")
            for idx in indexes:
                cols = ", ".join(idx['column_names'])
                unique = "UNIQUE" if idx['unique'] else ""
                print(f"  - {idx['name']:<30} ({cols}) {unique}")
        
        # Foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            print("\n🔹 Foreign Keys :")
            for fk in fks:
                print(f"  - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestion des migrations de base de données")
    parser.add_argument('action', choices=['migrate', 'check', 'info'], 
                       help='Action à effectuer')
    parser.add_argument('--table', help='Nom de la table (pour info)')
    
    args = parser.parse_args()
    
    if args.action == 'migrate':
        run_migration()
    elif args.action == 'check':
        check_tables()
    elif args.action == 'info':
        if not args.table:
            print("❌ Veuillez spécifier une table avec --table")
            sys.exit(1)
        show_table_info(args.table)
