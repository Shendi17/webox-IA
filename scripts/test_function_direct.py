"""Test direct de la fonction sans FastAPI"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import WebProject
from pathlib import Path

db = SessionLocal()

def test_project(project_id):
    print(f"\n{'='*50}")
    print(f"TEST PROJET {project_id}")
    print('='*50)
    
    try:
        project = db.query(WebProject).filter(WebProject.id == project_id).first()
        
        if not project:
            print(f"❌ Projet {project_id} non trouvé")
            return
        
        print(f"✅ Projet trouvé: {project.name}")
        print(f"   Local path: {project.local_path}")
        
        if not project.local_path:
            print("❌ Pas de local_path")
            return
        
        project_path = Path(project.local_path)
        print(f"   Path existe: {project_path.exists()}")
        
        if not project_path.exists():
            print("❌ Le chemin n'existe pas")
            return
        
        # Fonction build_tree
        def build_tree(path: Path, base_path: Path):
            items = []
            
            try:
                for item in sorted(path.iterdir()):
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
                print(f"   ⚠️ Permission denied: {e}")
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
                import traceback
                traceback.print_exc()
            
            return items
        
        print("\n   Génération de l'arborescence...")
        files = build_tree(project_path, project_path)
        
        print(f"\n✅ Arborescence générée: {len(files)} éléments")
        for f in files:
            icon = "📁" if f.get("is_directory") else "📄"
            print(f"   {icon} {f['name']}")
            if f.get("children"):
                for child in f["children"]:
                    icon2 = "📁" if child.get("is_directory") else "📄"
                    print(f"      {icon2} {child['name']}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

# Test projets 1 et 2
test_project(1)
test_project(2)

db.close()
