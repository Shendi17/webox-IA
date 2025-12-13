@echo off
echo.
echo ========================================================
echo    Configuration de webox.local
echo ========================================================
echo.
echo Ce script va configurer le fichier hosts pour que
echo webox.local pointe vers 127.0.0.1
echo.
echo IMPORTANT: Ce script necessite les droits administrateur
echo.
pause

powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0fix-webox-local.ps1\"'"
