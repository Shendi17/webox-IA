@echo off
chcp 65001 >nul
title WeBox Multi-IA - Lancement Complet

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║           WEBOX MULTI-IA - LANCEMENT COMPLET                 ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Démarrage de WeBox Multi-IA...
echo.

REM Vérifier si .env existe
if not exist ".env" (
    echo ⚠️  Fichier .env non trouvé
    echo.
    echo Création depuis .env.example...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ Fichier .env créé
    ) else (
        echo ❌ Fichier .env.example non trouvé
        echo.
        pause
        exit /b 1
    )
)

echo.
echo 📦 Lancement du backend FastAPI (port 8000)...
echo.

REM Lancer le backend en arrière-plan
start "WeBox Backend" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Attendre 3 secondes
timeout /t 3 /nobreak >nul

echo.
echo 🎨 Lancement du frontend React (port 3000)...
echo.

REM Lancer le frontend en arrière-plan
start "WeBox Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ WeBox Multi-IA démarré avec succès !
echo.
echo 📊 Services disponibles :
echo   - Backend API : http://localhost:8000
echo   - Frontend    : http://localhost:3000
echo   - API Docs    : http://localhost:8000/docs
echo.
echo 💡 Ouvrez http://localhost:3000 dans votre navigateur
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul
