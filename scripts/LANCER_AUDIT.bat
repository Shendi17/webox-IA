@echo off
echo ========================================
echo AUDIT COMPLET WEBOX - LANCEMENT
echo ========================================
echo.
echo Verification du serveur...
echo.

REM Vérifier si le serveur est lancé
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Le serveur n'est pas lance sur http://localhost:8000
    echo.
    echo Veuillez d'abord lancer le serveur avec:
    echo   python main.py
    echo ou
    echo   uvicorn main:app --reload
    echo.
    pause
    exit /b 1
)

echo [OK] Serveur detecte
echo.
echo Lancement de l'audit...
echo.

python AUDIT_COMPLET_FONCTIONNALITES.py

echo.
echo ========================================
echo AUDIT TERMINE
echo ========================================
echo.
echo Consultez le rapport dans:
echo - RAPPORT_AUDIT_FONCTIONNALITES.md
echo - audit_results_*.json
echo.
pause
