"""
Script pour supprimer l'utilisateur test via SQL direct
Date: 25 Janvier 2026
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def supprimer_utilisateur_test():
    """Supprimer l'utilisateur test@webox.com via SQL direct"""
    
    print("\n" + "="*70)
    print("SUPPRESSION UTILISATEUR TEST")
    print("="*70 + "\n")
    
    # Connexion PostgreSQL
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL non configuré")
        return
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe
        cursor.execute("SELECT id, email, name, username FROM users WHERE email = %s", ("test@webox.com",))
        user = cursor.fetchone()
        
        if user:
            print(f"Utilisateur trouvé:")
            print(f"  ID: {user[0]}")
            print(f"  Email: {user[1]}")
            print(f"  Nom: {user[2]}")
            print(f"  Username: {user[3]}")
            print()
            
            # Supprimer les données liées (cascade)
            print("Suppression des données liées...")
            cursor.execute("DELETE FROM cart_items WHERE user_id = %s", (user[0],))
            print(f"  - {cursor.rowcount} items panier supprimés")
            
            cursor.execute("DELETE FROM orders WHERE user_id = %s", (user[0],))
            print(f"  - {cursor.rowcount} commandes supprimées")
            
            cursor.execute("DELETE FROM conversations WHERE user_id = %s", (user[0],))
            print(f"  - {cursor.rowcount} conversations supprimées")
            
            cursor.execute("DELETE FROM prompts WHERE user_id = %s", (user[0],))
            print(f"  - {cursor.rowcount} prompts supprimés")
            
            # Supprimer l'utilisateur
            cursor.execute("DELETE FROM users WHERE email = %s", ("test@webox.com",))
            conn.commit()
            
            print()
            print("✅ Utilisateur test supprimé avec succès!")
            print()
            
        else:
            print("ℹ️ Aucun utilisateur test@webox.com trouvé")
            print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if 'conn' in locals():
            conn.rollback()
    
    print("="*70)
    print()


if __name__ == "__main__":
    supprimer_utilisateur_test()
