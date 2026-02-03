"""
Script pour créer la table settings
"""
from app.database import engine, Base
from app.models.settings_db import SettingsDB

# Créer la table
Base.metadata.create_all(bind=engine)
print('✅ Table settings créée avec succès !')
