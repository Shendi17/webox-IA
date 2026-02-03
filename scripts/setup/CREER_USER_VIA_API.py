"""
Créer un utilisateur test via l'API
Date: 24 Janvier 2026
"""

import httpx
import asyncio

async def create_user():
    """Créer un utilisateur via l'API"""
    
    print("\n" + "="*60)
    print("CREATION UTILISATEUR TEST VIA API")
    print("="*60 + "\n")
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Essayer de créer l'utilisateur
            response = await client.post(
                "http://localhost:8000/api/auth/register",
                json={
                    "email": "test@webox.com",
                    "username": "testuser",
                    "password": "test123456",
                    "name": "Test User"
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                print("OK Utilisateur cree avec succes!")
                print(f"   Email: test@webox.com")
                print(f"   Username: testuser")
                print(f"   Password: test123456")
                print(f"   ID: {data.get('user', {}).get('id')}")
                
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get("detail", "").lower():
                    print("ATTENTION L'utilisateur test@webox.com existe deja")
                    print("   Vous pouvez l'utiliser pour les tests")
                else:
                    print(f"ERREUR: {error.get('detail')}")
                    
            else:
                print(f"ERREUR {response.status_code}")
                print(f"   {response.text}")
                
        except httpx.ConnectError:
            print("ERREUR Impossible de se connecter au serveur")
            print("   Assurez-vous que le serveur est demarre:")
            print("   python main.py")
        except Exception as e:
            print(f"ERREUR: {e}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(create_user())
