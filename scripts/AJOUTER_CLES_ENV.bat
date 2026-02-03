@echo off
echo ========================================
echo AJOUT CLES MANQUANTES DANS .env
echo ========================================
echo.
echo Ce script va ajouter les cles manquantes dans votre fichier .env
echo.

REM Generer une cle secrete aleatoire
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env

echo.
echo ✅ Cles JWT_SECRET_KEY et SECRET_KEY ajoutees
echo.
echo ⚠️ N'oubliez pas d'ajouter manuellement:
echo    STRIPE_PUBLISHABLE_KEY=pk_test_...
echo.
pause
