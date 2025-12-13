"""
Migration : Ajouter la colonne preheader à email_campaigns
Date : 23 Novembre 2025
"""

import sqlite3
import os

def migrate():
    """Ajoute la colonne preheader à la table email_campaigns"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webox.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la colonne existe déjà
        cursor.execute("PRAGMA table_info(email_campaigns)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'preheader' in columns:
            print("✅ La colonne 'preheader' existe déjà")
            conn.close()
            return True
        
        # Ajouter la colonne preheader
        print("📝 Ajout de la colonne 'preheader' à email_campaigns...")
        cursor.execute("""
            ALTER TABLE email_campaigns 
            ADD COLUMN preheader VARCHAR(500)
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Migration réussie : colonne 'preheader' ajoutée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")
        return False

if __name__ == "__main__":
    print("🔄 Démarrage de la migration...")
    print("=" * 50)
    
    success = migrate()
    
    print("=" * 50)
    if success:
        print("✅ Migration terminée avec succès !")
    else:
        print("❌ Migration échouée")
