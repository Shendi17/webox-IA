"""
Script pour créer les tables des projets web
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import engine
from app.models.web_project_db import (
    WebProject,
    ProjectFile,
    Deployment,
    ProjectCommit,
    ProjectAIAction,
    ProjectTemplate
)

# Créer les tables
WebProject.__table__.create(bind=engine, checkfirst=True)
ProjectFile.__table__.create(bind=engine, checkfirst=True)
Deployment.__table__.create(bind=engine, checkfirst=True)
ProjectCommit.__table__.create(bind=engine, checkfirst=True)
ProjectAIAction.__table__.create(bind=engine, checkfirst=True)
ProjectTemplate.__table__.create(bind=engine, checkfirst=True)

print("✅ Tables des projets web créées avec succès !")
