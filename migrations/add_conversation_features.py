"""
Migration : Ajouter les champs is_favorite et tags à la table conversations
Date : 24 Novembre 2025
"""

import sqlite3
import json

def migrate():
    """Ajouter les colonnes is_favorite et tags"""
    
    conn = sqlite3.connect('webox.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 Migration : Ajout des champs is_favorite et tags...")
        
        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Ajouter is_favorite si elle n'existe pas
        if 'is_favorite' not in columns:
            print("  ➕ Ajout de la colonne is_favorite...")
            cursor.execute("""
                ALTER TABLE conversations 
                ADD COLUMN is_favorite INTEGER DEFAULT 0
            """)
            print("  ✅ Colonne is_favorite ajoutée")
        else:
            print("  ℹ️  Colonne is_favorite existe déjà")
        
        # Ajouter tags si elle n'existe pas
        if 'tags' not in columns:
            print("  ➕ Ajout de la colonne tags...")
            cursor.execute("""
                ALTER TABLE conversations 
                ADD COLUMN tags TEXT DEFAULT '[]'
            """)
            print("  ✅ Colonne tags ajoutée")
        else:
            print("  ℹ️  Colonne tags existe déjà")
        
        conn.commit()
        print("✅ Migration terminée avec succès !")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erreur lors de la migration : {e}")
        raise
    
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
