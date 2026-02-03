@echo off
chcp 65001 >nul
title WeBox - Redémarrage Backend

echo.
echo 🔄 Arrêt du backend actuel...
echo.

REM Tuer le processus sur le port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul

timeout /t 2 /nobreak >nul

echo.
echo 🚀 Démarrage du nouveau backend...
echo.

REM Lancer le backend
start "WeBox Backend" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo ✅ Backend redémarré !
echo.
echo 📊 Accès :
echo   - Interface : http://webox.local:8000
echo   - API Docs  : http://webox.local:8000/docs
echo.
pause
