"""
Script pour organiser les fichiers MD dans docs/
Date : 23 Novembre 2025
"""

import os
import shutil

def organize_docs():
    """Organise les fichiers MD dans des sous-dossiers"""
    
    root_dir = os.path.dirname(os.path.dirname(__file__))
    docs_dir = os.path.join(root_dir, 'docs')
    
    # Créer la structure
    subdirs = {
        'sessions': os.path.join(docs_dir, 'sessions'),
        'phases': os.path.join(docs_dir, 'phases'),
        'corrections': os.path.join(docs_dir, 'corrections'),
        'guides': os.path.join(docs_dir, 'guides'),
        'architecture': os.path.join(docs_dir, 'architecture'),
        'implementation': os.path.join(docs_dir, 'implementation'),
    }
    
    for subdir in subdirs.values():
        os.makedirs(subdir, exist_ok=True)
    
    # Règles de catégorisation
    rules = {
        'sessions': ['SESSION_', 'SYNTHESE_', 'RESUME_SESSION'],
        'phases': ['PHASE_', 'PHASE1_', 'PHASE2_', 'PHASE3_', 'PHASE4_', 'PHASE5_'],
        'corrections': ['FIX_', 'CORRECTION_', 'CORRECTIONS_', 'SOLUTION_', 'MIGRATION_'],
        'guides': ['GUIDE_', 'QUICK_', 'INSTRUCTIONS_', 'CHECKLIST_', 'VIDER_'],
        'architecture': ['ROADMAP_', 'SIDEBAR_', 'PLAN_', 'AUDIT_', 'ANALYSE_', 'DIFFERENCE_', 'CLARIFICATION_'],
        'implementation': ['IMPLEMENTATION_', 'COMPLETE', 'INTERFACE_', 'SYSTEME_', 'TEMPLATES_', 'UNIFORMISATION_', 'ENRICHISSEMENT_', 'NOUVELLES_FONCTIONNALITES', 'FONCTIONNALITES_'],
    }
    
    # Fichiers à garder à la racine
    keep_at_root = ['README.md', 'LICENSE', '.gitignore', 'QUICK_START.md', 'INDEX_DOCUMENTATION.md']
    
    print("📁 Organisation des fichiers MD...")
    print("=" * 60)
    
    moved_files = []
    
    # Parcourir les fichiers MD à la racine
    for file in os.listdir(root_dir):
        if file.endswith('.md') and file not in keep_at_root:
            file_path = os.path.join(root_dir, file)
            
            if os.path.isfile(file_path):
                # Déterminer la catégorie
                category = None
                for cat, keywords in rules.items():
                    if any(keyword in file.upper() for keyword in keywords):
                        category = cat
                        break
                
                # Si pas de catégorie, mettre dans implementation
                if not category:
                    category = 'implementation'
                
                # Déplacer le fichier
                dest_path = os.path.join(subdirs[category], file)
                
                try:
                    shutil.move(file_path, dest_path)
                    moved_files.append((file, category))
                    print(f"✅ {file} → {category}/")
                except Exception as e:
                    print(f"❌ Erreur avec {file}: {e}")
    
    print("=" * 60)
    print(f"\n✅ {len(moved_files)} fichiers déplacés")
    
    # Statistiques par catégorie
    print("\n📊 Répartition :")
    for cat in subdirs.keys():
        count = sum(1 for _, c in moved_files if c == cat)
        print(f"  {cat:15} : {count} fichiers")

if __name__ == "__main__":
    organize_docs()
