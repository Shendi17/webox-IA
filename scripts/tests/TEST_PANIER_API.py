"""
Script de test pour l'API Panier
Date: 24 Janvier 2026
"""

import httpx
import asyncio
import json

BASE_URL = "http://localhost:8000"

async def test_cart_api():
    """Tester toutes les fonctionnalités du panier"""
    
    print("\n" + "="*60)
    print("🛒 TEST API PANIER")
    print("="*60 + "\n")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        
        # 1. Connexion
        print("1️⃣ Connexion utilisateur...")
        login_response = await client.post("/api/auth/login", json={
            "email": "test@webox.com",
            "password": "test123456"
        })
        
        if login_response.status_code != 200:
            print("❌ Échec de la connexion")
            print(f"   Status: {login_response.status_code}")
            return
        
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Connexion réussie\n")
        
        # 2. Récupérer le panier (vide au départ)
        print("2️⃣ Récupération du panier...")
        cart_response = await client.get("/api/cart", headers=headers)
        
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            print(f"✅ Panier récupéré: {cart_data['cart']['total_items']} article(s)")
            print(f"   Sous-total: {cart_data['cart']['subtotal']}€\n")
        else:
            print(f"❌ Erreur: {cart_response.status_code}\n")
        
        # 3. Ajouter un produit au panier
        print("3️⃣ Ajout d'un produit au panier...")
        add_response = await client.post("/api/cart/add", 
            headers=headers,
            json={"product_id": 1, "quantity": 2}
        )
        
        if add_response.status_code == 200:
            add_data = add_response.json()
            print(f"✅ Produit ajouté: {add_data['item']['product']['name']}")
            print(f"   Quantité: {add_data['item']['quantity']}")
            print(f"   Prix unitaire: {add_data['item']['price_at_addition']}€\n")
        else:
            print(f"❌ Erreur: {add_response.status_code}")
            print(f"   {add_response.text}\n")
        
        # 4. Ajouter un autre produit
        print("4️⃣ Ajout d'un deuxième produit...")
        add_response2 = await client.post("/api/cart/add",
            headers=headers,
            json={"product_id": 2, "quantity": 1}
        )
        
        if add_response2.status_code == 200:
            print("✅ Deuxième produit ajouté\n")
        else:
            print(f"❌ Erreur: {add_response2.status_code}\n")
        
        # 5. Récupérer le panier mis à jour
        print("5️⃣ Récupération du panier mis à jour...")
        cart_response2 = await client.get("/api/cart", headers=headers)
        
        if cart_response2.status_code == 200:
            cart_data2 = cart_response2.json()
            print(f"✅ Panier: {cart_data2['cart']['total_items']} article(s)")
            print(f"   Sous-total: {cart_data2['cart']['subtotal']}€")
            print(f"   TVA (20%): {cart_data2['cart']['tax']}€")
            print(f"   Total: {cart_data2['cart']['total']}€")
            print(f"\n   Articles:")
            for item in cart_data2['cart']['items']:
                print(f"   - {item['product']['name']} x{item['quantity']} = {item['subtotal']}€")
            print()
        
        # 6. Modifier la quantité d'un article
        if cart_response2.status_code == 200:
            first_item_id = cart_data2['cart']['items'][0]['id']
            print(f"6️⃣ Modification de la quantité (article #{first_item_id})...")
            
            update_response = await client.put(f"/api/cart/{first_item_id}",
                headers=headers,
                json={"quantity": 5}
            )
            
            if update_response.status_code == 200:
                print("✅ Quantité mise à jour à 5\n")
            else:
                print(f"❌ Erreur: {update_response.status_code}\n")
        
        # 7. Supprimer un article
        if cart_response2.status_code == 200 and len(cart_data2['cart']['items']) > 1:
            second_item_id = cart_data2['cart']['items'][1]['id']
            print(f"7️⃣ Suppression d'un article (#{second_item_id})...")
            
            delete_response = await client.delete(f"/api/cart/{second_item_id}",
                headers=headers
            )
            
            if delete_response.status_code == 200:
                print("✅ Article supprimé\n")
            else:
                print(f"❌ Erreur: {delete_response.status_code}\n")
        
        # 8. Récupérer le nombre d'articles
        print("8️⃣ Récupération du nombre d'articles...")
        count_response = await client.get("/api/cart/count", headers=headers)
        
        if count_response.status_code == 200:
            count_data = count_response.json()
            print(f"✅ Nombre d'articles: {count_data['count']}\n")
        
        # 9. Vider le panier
        print("9️⃣ Vidage du panier...")
        clear_response = await client.delete("/api/cart", headers=headers)
        
        if clear_response.status_code == 200:
            clear_data = clear_response.json()
            print(f"✅ Panier vidé: {clear_data['deleted_count']} article(s) supprimé(s)\n")
        
        # 10. Vérifier que le panier est vide
        print("🔟 Vérification finale...")
        final_response = await client.get("/api/cart", headers=headers)
        
        if final_response.status_code == 200:
            final_data = final_response.json()
            if final_data['cart']['total_items'] == 0:
                print("✅ Panier vide confirmé\n")
            else:
                print(f"⚠️ Le panier contient encore {final_data['cart']['total_items']} article(s)\n")
    
    print("="*60)
    print("✅ TESTS TERMINÉS")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("\n⚠️ Assurez-vous que:")
    print("  1. Le serveur est lancé (python main.py)")
    print("  2. Les tables e-commerce sont créées (migration)")
    print("  3. Un utilisateur test existe (test@webox.com)\n")
    
    try:
        asyncio.run(test_cart_api())
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
