@echo off
title Restauration Automatique du Fichier Hosts
color 0E

echo.
echo ========================================================
echo      RESTAURATION AUTOMATIQUE DU FICHIER HOSTS
echo ========================================================
echo.
echo Ce script va :
echo   1. Rechercher la derniere sauvegarde
echo   2. Restaurer vos projets
echo   3. Ajouter webox.local sans toucher aux autres
echo.
echo IMPORTANT: Droits administrateur requis
echo.
pause

powershell.exe -ExecutionPolicy Bypass -File "%~dp0RESTAURATION-AUTO.ps1"
