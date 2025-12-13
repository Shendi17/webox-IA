@echo off
title Installation Assistant Vocal IA
color 0E

echo.
echo ========================================================
echo        INSTALLATION ASSISTANT VOCAL IA - WEBOX
echo ========================================================
echo.
echo Installation des dependances pour l'assistant vocal...
echo.

REM Installation des packages Python
pip install twilio>=8.10.0
pip install google-cloud-speech>=2.24.0
pip install google-cloud-texttospeech>=2.16.0
pip install google-auth>=2.27.0

echo.
echo ========================================================
echo           INSTALLATION TERMINEE !
echo ========================================================
echo.
echo Prochaines etapes :
echo.
echo 1. Configurez vos cles API dans le fichier .env :
echo    - TWILIO_ACCOUNT_SID
echo    - TWILIO_AUTH_TOKEN
echo    - TWILIO_PHONE_NUMBER
echo    - GOOGLE_APPLICATION_CREDENTIALS
echo    - OPENAI_API_KEY
echo.
echo 2. Lancez WeBox avec LANCER-WEBOX.bat
echo.
echo 3. Allez dans "Assistant Vocal" dans le menu
echo.
echo Documentation complete : ASSISTANT_VOCAL_IA.md
echo.
pause
