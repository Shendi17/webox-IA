"""
Script pour créer les tables voice_assistants et voice_calls
"""
from app.database import engine, Base
from app.models.voice_assistant_db import VoiceAssistantDB, VoiceCallDB

# Créer les tables
Base.metadata.create_all(bind=engine)
print('✅ Tables voice_assistants et voice_calls créées avec succès !')
