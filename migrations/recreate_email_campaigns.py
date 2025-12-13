"""
Migration : Recréer la table email_campaigns avec toutes les colonnes
Date : 23 Novembre 2025
"""

import sqlite3
import os

def recreate_email_campaigns():
    """Recrée la table email_campaigns avec le bon schéma"""
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webox.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='email_campaigns'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            print("📝 Suppression de l'ancienne table email_campaigns...")
            cursor.execute("DROP TABLE IF EXISTS email_campaigns")
        
        # Créer la nouvelle table avec toutes les colonnes
        print("📝 Création de la nouvelle table email_campaigns...")
        cursor.execute("""
            CREATE TABLE email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                subject VARCHAR(500) NOT NULL,
                preheader VARCHAR(500),
                html_content TEXT NOT NULL,
                text_content TEXT,
                from_name VARCHAR(255),
                from_email VARCHAR(255),
                reply_to VARCHAR(255),
                status VARCHAR(50) DEFAULT 'draft',
                scheduled_at DATETIME,
                sent_at DATETIME,
                total_recipients INTEGER DEFAULT 0,
                total_sent INTEGER DEFAULT 0,
                total_delivered INTEGER DEFAULT 0,
                total_opened INTEGER DEFAULT 0,
                total_clicked INTEGER DEFAULT 0,
                total_bounced INTEGER DEFAULT 0,
                total_unsubscribed INTEGER DEFAULT 0,
                open_rate FLOAT DEFAULT 0.0,
                click_rate FLOAT DEFAULT 0.0,
                segment_rules TEXT,
                author_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Table email_campaigns recréée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    print("🔄 Recréation de la table email_campaigns...")
    print("=" * 60)
    
    success = recreate_email_campaigns()
    
    print("=" * 60)
    if success:
        print("✅ Migration terminée avec succès !")
    else:
        print("❌ Migration échouée")
