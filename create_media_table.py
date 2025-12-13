"""
Script pour créer la table media
"""
from app.database import engine, Base
from app.models.media_db import MediaDB

# Créer la table
Base.metadata.create_all(bind=engine)
print('✅ Table media créée avec succès !')
