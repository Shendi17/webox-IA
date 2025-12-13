"""
Migration : Recréer la table funnels avec toutes les colonnes
Date : 23 Novembre 2025
"""

import sqlite3
import os

def recreate_funnels():
    """Recrée la table funnels avec le bon schéma"""
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webox.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funnels'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            print("📝 Suppression de l'ancienne table funnels...")
            cursor.execute("DROP TABLE IF EXISTS funnels")
        
        # Créer la nouvelle table avec toutes les colonnes
        print("📝 Création de la nouvelle table funnels...")
        cursor.execute("""
            CREATE TABLE funnels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                funnel_type VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT 0,
                is_template BOOLEAN DEFAULT 0,
                total_visitors INTEGER DEFAULT 0,
                total_leads INTEGER DEFAULT 0,
                total_sales INTEGER DEFAULT 0,
                total_revenue FLOAT DEFAULT 0.0,
                conversion_rate FLOAT DEFAULT 0.0,
                author_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Table funnels recréée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    print("🔄 Recréation de la table funnels...")
    print("=" * 60)
    
    success = recreate_funnels()
    
    print("=" * 60)
    if success:
        print("✅ Migration terminée avec succès !")
    else:
        print("❌ Migration échouée")
