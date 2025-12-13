@echo off
chcp 65001 >nul
cls

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║              🤖 WEBOX MULTI-IA - LANCEMENT FLASH            ║
echo ║                  Framework FastAPI                           ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Vérification de la configuration...
echo.

REM Vérifier si le fichier .env existe
if not exist ".env" (
    echo ⚠️  Fichier .env non trouvé
    echo Création du fichier .env...
    copy ".env.example" ".env" >nul
    echo ✅ Fichier .env créé
    echo.
    echo ⚠️  IMPORTANT : Configurez vos clés API dans le fichier .env
    echo Ouverture du fichier .env...
    timeout /t 2 /nobreak >nul
    notepad .env
    echo.
    echo Appuyez sur une touche après avoir configuré vos clés API...
    pause >nul
)

echo.
echo 🚀 Lancement de WeBox Multi-IA avec FastAPI...
echo.
echo 📍 L'application sera accessible sur :
echo    → http://localhost:8000
echo    → http://webox.local:8000
echo.
echo 💡 Pour arrêter l'application : Ctrl+C
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM Lancer FastAPI avec Uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

REM Si l'application se ferme
echo.
echo Application arrêtée.
echo Appuyez sur une touche pour fermer...
pause >nul
