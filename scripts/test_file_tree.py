"""Test de la fonction build_tree"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import WebProject
from pathlib import Path
import json

db = SessionLocal()
project = db.query(WebProject).filter(WebProject.id == 1).first()

if not project or not project.local_path:
    print("❌ Projet non trouvé ou sans local_path")
    sys.exit(1)

project_path = Path(project.local_path)

def build_tree(path: Path, base_path: Path):
    """Construit l'arborescence récursivement"""
    items = []
    
    try:
        for item in sorted(path.iterdir()):
            # Ignorer les fichiers cachés et node_modules
            if item.name.startswith('.') or item.name == 'node_modules':
                continue
            
            relative_path = str(item.relative_to(base_path))
            
            if item.is_dir():
                items.append({
                    "name": item.name,
                    "path": relative_path,
                    "is_directory": True,
                    "children": build_tree(item, base_path)
                })
            else:
                items.append({
                    "name": item.name,
                    "path": relative_path,
                    "is_directory": False,
                    "size": item.stat().st_size
                })
    except PermissionError as e:
        print(f"❌ Permission error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return items

try:
    files = build_tree(project_path, project_path)
    print("✅ Arborescence générée:")
    print(json.dumps({"files": files}, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

db.close()
