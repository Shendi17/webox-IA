"""
Script pour créer des fichiers de test dans un projet
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.web_project_db import WebProject
from pathlib import Path


def setup_project_files(project_id=1):
    db = SessionLocal()
    
    # Récupérer le projet
    project = db.query(WebProject).filter(WebProject.id == project_id).first()
    
    if not project:
        print(f"❌ Projet {project_id} non trouvé")
        return
    
    # Créer le dossier du projet
    base_path = Path(__file__).parent.parent / "projects" / str(project.owner_id)
    project_path = base_path / project.slug
    
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Mettre à jour le local_path
    project.local_path = str(project_path)
    db.commit()
    
    print(f"📁 Dossier créé : {project_path}")
    
    # Créer une structure de fichiers de test
    files = {
        "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Projet Test</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Bienvenue sur Mon Projet Test</h1>
        <p>Ceci est un projet de test pour WeBox Studio.</p>
        <button onclick="sayHello()">Cliquez-moi !</button>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
        
        "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 600px;
}

h1 {
    color: #1a1a2e;
    margin-bottom: 1rem;
    font-size: 2.5rem;
}

p {
    color: #666;
    margin-bottom: 2rem;
    font-size: 1.1rem;
}

button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s ease;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}""",
        
        "script.js": """// Script principal
console.log('🚀 Projet chargé avec succès !');

function sayHello() {
    alert('👋 Bonjour depuis WeBox Studio !');
    console.log('Bouton cliqué !');
}

// Animation au chargement
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ DOM chargé');
    
    const container = document.querySelector('.container');
    container.style.opacity = '0';
    container.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        container.style.transition = 'all 0.5s ease';
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }, 100);
});""",
        
        "README.md": """# Mon Projet Test

Ceci est un projet de test pour **WeBox Studio**.

## Fonctionnalités

- ✅ HTML5
- ✅ CSS3 avec animations
- ✅ JavaScript moderne
- ✅ Design responsive

## Structure

```
mon-projet-test/
├── index.html
├── style.css
├── script.js
└── README.md
```

## Utilisation

Ouvrez `index.html` dans votre navigateur.

---

**Créé avec WeBox Studio** 🚀
"""
    }
    
    # Créer les fichiers
    for filename, content in files.items():
        file_path = project_path / filename
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Fichier créé : {filename}")
    
    # Créer un sous-dossier avec des fichiers
    src_path = project_path / "src"
    src_path.mkdir(exist_ok=True)
    
    (src_path / "utils.js").write_text("""// Fonctions utilitaires
export function formatDate(date) {
    return new Date(date).toLocaleDateString('fr-FR');
}

export function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
""", encoding='utf-8')
    
    print(f"✅ Sous-dossier créé : src/")
    
    # Mettre à jour les statistiques du projet
    project.total_files = len(files) + 1
    project.total_lines = sum(content.count('\n') for content in files.values()) + 10
    project.total_size = sum(len(content.encode('utf-8')) for content in files.values())
    db.commit()
    
    print(f"\n🎉 Projet configuré avec succès !")
    print(f"📊 Statistiques :")
    print(f"   - Fichiers : {project.total_files}")
    print(f"   - Lignes : {project.total_lines}")
    print(f"   - Taille : {project.total_size} octets")
    print(f"\n📂 Chemin : {project.local_path}")
    
    db.close()


if __name__ == "__main__":
    import sys
    project_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    setup_project_files(project_id)
