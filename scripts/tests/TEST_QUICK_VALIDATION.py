"""
Test rapide de validation - Endpoints critiques
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000"

async def quick_test():
    print("\n🔍 VALIDATION RAPIDE - ENDPOINTS CRITIQUES\n")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        tests = [
            ("Health Check", "GET", "/api/monitoring/health", None),
            ("Page Forgot Password", "GET", "/forgot-password", None),
            ("Page Reset Password", "GET", "/reset-password?token=test", None),
        ]
        
        passed = 0
        total = len(tests)
        
        for name, method, endpoint, data in tests:
            try:
                if method == "GET":
                    response = await client.get(f"{BASE_URL}{endpoint}")
                else:
                    response = await client.post(f"{BASE_URL}{endpoint}", json=data)
                
                if response.status_code < 500:
                    print(f"✅ {name}: {response.status_code}")
                    passed += 1
                else:
                    print(f"❌ {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: {e}")
        
        print(f"\n📊 Résultat: {passed}/{total} ({passed/total*100:.0f}%)\n")

if __name__ == "__main__":
    asyncio.run(quick_test())
