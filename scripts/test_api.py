"""Test de l'API des fichiers"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import WebProject
from pathlib import Path

db = SessionLocal()

# Vérifier le projet
project = db.query(WebProject).filter(WebProject.id == 1).first()

if not project:
    print("❌ Projet 1 non trouvé")
    sys.exit(1)

print(f"✅ Projet trouvé: {project.name}")
print(f"   Slug: {project.slug}")
print(f"   Local path: {project.local_path}")

if project.local_path:
    path = Path(project.local_path)
    print(f"   Path existe: {path.exists()}")
    
    if path.exists():
        files = list(path.iterdir())
        print(f"   Nombre de fichiers: {len(files)}")
        for f in files[:5]:
            print(f"     - {f.name}")
else:
    print("❌ Pas de local_path défini")

db.close()
