@echo off
echo ========================================
echo DEMARRAGE SERVEUR ET TESTS WEBOX
echo ========================================
echo.
echo 1. Demarrage du serveur en arriere-plan...
start "WeBox Server" cmd /k "python main.py"
echo.
echo ⏳ Attente 10 secondes pour le demarrage du serveur...
timeout /t 10 /nobreak
echo.
echo 2. Creation utilisateur test via API...
python -c "import httpx; import asyncio; async def create(): async with httpx.AsyncClient() as c: r = await c.post('http://localhost:8000/api/auth/register', json={'email':'test@webox.com','username':'testuser','password':'test123456','name':'Test User'}); print(r.status_code, r.text); asyncio.run(create())"
echo.
echo 3. Test du panier...
python TEST_PANIER_API.py
echo.
echo ========================================
echo TESTS TERMINES
echo ========================================
pause
