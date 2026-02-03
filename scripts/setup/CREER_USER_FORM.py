"""
Créer un utilisateur test via formulaire
Date: 24 Janvier 2026
"""

import httpx
import asyncio

async def create_user():
    """Créer un utilisateur via formulaire"""
    
    print("\n" + "="*60)
    print("CREATION UTILISATEUR TEST")
    print("="*60 + "\n")
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
        try:
            # Créer l'utilisateur via formulaire
            response = await client.post(
                "http://localhost:8000/register",
                data={
                    "email": "test@webox.com",
                    "name": "Test User",
                    "password": "test123456"
                }
            )
            
            if response.status_code in [200, 302]:
                print("OK Utilisateur cree avec succes!")
                print("   Email: test@webox.com")
                print("   Password: test123456")
                print("   Name: Test User")
                
            elif response.status_code == 400:
                print("ATTENTION L'utilisateur existe probablement deja")
                print("   Vous pouvez l'utiliser pour les tests")
                
            else:
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                
        except httpx.ConnectError:
            print("ERREUR Impossible de se connecter au serveur")
        except Exception as e:
            print(f"ERREUR: {e}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(create_user())
