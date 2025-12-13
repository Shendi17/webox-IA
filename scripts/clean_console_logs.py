"""
Script pour nettoyer les console.log() des templates HTML
Date : 23 Novembre 2025
"""

import os
import re

def clean_console_logs(file_path):
    """Supprime les console.log() d'un fichier HTML"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Patterns à supprimer
    patterns = [
        # console.log simple
        r'\s*console\.log\([^)]*\);\s*\n',
        # console.log avec template literals
        r'\s*console\.log\(`[^`]*`\);\s*\n',
        # console.log avec quotes
        r'\s*console\.log\("[^"]*"\);\s*\n',
        r"\s*console\.log\('[^']*'\);\s*\n",
        # console.log avec variables
        r'\s*console\.log\([^;]+\);\s*\n',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content)
    
    # Garder console.error et console.warn
    # (ils sont déjà préservés car on ne les supprime pas)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Nettoie tous les templates HTML"""
    
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    
    print("🧹 Nettoyage des console.log() dans les templates...")
    print("=" * 60)
    
    cleaned_files = []
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, templates_dir)
                
                if clean_console_logs(file_path):
                    cleaned_files.append(rel_path)
                    print(f"✅ {rel_path}")
    
    print("=" * 60)
    print(f"\n✅ {len(cleaned_files)} fichiers nettoyés")
    
    if cleaned_files:
        print("\nFichiers modifiés :")
        for file in cleaned_files:
            print(f"  - {file}")

if __name__ == "__main__":
    main()
