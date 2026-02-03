@echo off
echo ========================================
echo MIGRATION E-COMMERCE - CREATION TABLES
echo ========================================
echo.
echo Creation des tables:
echo - products
echo - cart_items
echo - orders
echo - order_items
echo.
echo Ajout de 6 produits d'exemple
echo.
pause

python migrations\create_ecommerce_tables.py

echo.
echo ========================================
echo MIGRATION TERMINEE
echo ========================================
echo.
pause
