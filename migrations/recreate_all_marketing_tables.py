"""
Migration : Recréer TOUTES les tables Marketing avec le bon schéma
Date : 23 Novembre 2025
"""

import sqlite3
import os

def recreate_all_marketing_tables():
    """Recrée toutes les tables Marketing avec le bon schéma"""
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webox.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Liste des tables à recréer
        tables = ['funnels', 'funnel_pages', 'email_campaigns', 'leads', 'lead_interactions', 'ad_campaigns']
        
        # Supprimer les anciennes tables
        print("📝 Suppression des anciennes tables...")
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"   ✅ {table} supprimée")
        
        print("\n📝 Création des nouvelles tables...")
        
        # 1. FUNNELS
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
        print("   ✅ funnels créée")
        
        # 2. FUNNEL_PAGES
        cursor.execute("""
            CREATE TABLE funnel_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funnel_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                page_type VARCHAR(50),
                slug VARCHAR(255) NOT NULL,
                html_content TEXT,
                css_content TEXT,
                js_content TEXT,
                is_published BOOLEAN DEFAULT 0,
                order_index INTEGER DEFAULT 0,
                visitors INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                conversion_rate FLOAT DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (funnel_id) REFERENCES funnels(id) ON DELETE CASCADE
            )
        """)
        print("   ✅ funnel_pages créée")
        
        # 3. EMAIL_CAMPAIGNS
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
        print("   ✅ email_campaigns créée")
        
        # 4. LEADS
        cursor.execute("""
            CREATE TABLE leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                phone VARCHAR(50),
                company VARCHAR(255),
                job_title VARCHAR(255),
                status VARCHAR(50) DEFAULT 'new',
                source VARCHAR(100),
                score INTEGER DEFAULT 0,
                estimated_value FLOAT DEFAULT 0.0,
                notes TEXT,
                tags TEXT,
                custom_fields TEXT,
                last_contact_date DATETIME,
                next_follow_up DATETIME,
                assigned_to INTEGER,
                author_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ leads créée")
        
        # 5. LEAD_INTERACTIONS
        cursor.execute("""
            CREATE TABLE lead_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER NOT NULL,
                interaction_type VARCHAR(50) NOT NULL,
                subject VARCHAR(500),
                notes TEXT,
                interaction_metadata TEXT,
                created_by INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
            )
        """)
        print("   ✅ lead_interactions créée")
        
        # 6. AD_CAMPAIGNS
        cursor.execute("""
            CREATE TABLE ad_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                platform VARCHAR(50) NOT NULL,
                campaign_type VARCHAR(50),
                status VARCHAR(50) DEFAULT 'draft',
                budget FLOAT DEFAULT 0.0,
                daily_budget FLOAT DEFAULT 0.0,
                start_date DATETIME,
                end_date DATETIME,
                target_audience TEXT,
                ad_creative TEXT,
                total_impressions INTEGER DEFAULT 0,
                total_clicks INTEGER DEFAULT 0,
                total_conversions INTEGER DEFAULT 0,
                total_spent FLOAT DEFAULT 0.0,
                ctr FLOAT DEFAULT 0.0,
                cpc FLOAT DEFAULT 0.0,
                cpa FLOAT DEFAULT 0.0,
                roas FLOAT DEFAULT 0.0,
                author_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ ad_campaigns créée")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Toutes les tables Marketing recréées avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

if __name__ == "__main__":
    print("🔄 Recréation de TOUTES les tables Marketing...")
    print("=" * 60)
    
    success = recreate_all_marketing_tables()
    
    print("=" * 60)
    if success:
        print("✅ Migration terminée avec succès !")
        print("\n📊 Tables créées :")
        print("   1. funnels")
        print("   2. funnel_pages")
        print("   3. email_campaigns")
        print("   4. leads")
        print("   5. lead_interactions")
        print("   6. ad_campaigns")
    else:
        print("❌ Migration échouée")
