# 🔍 DIAGNOSTIC STUDIO WEB IA

**Date** : 24 Novembre 2025  
**Problème** : Interface vide, éditeur ne charge pas  

---

## 🐛 SYMPTÔMES

1. ✅ Page charge (URL correcte)
2. ❌ Interface vide (écran noir)
3. ❌ Éditeur Monaco ne s'affiche pas
4. ❌ Arborescence fichiers vide
5. ❌ Terminal ne s'affiche pas

---

## 🔍 CAUSES POSSIBLES

### **1. Monaco Editor ne charge pas**
- CDN bloqué ou lent
- Erreur JavaScript
- `require.js` non chargé

### **2. Projet inexistant**
- ID projet invalide
- Projet supprimé
- Pas de fichiers dans le projet

### **3. Erreur API**
- Route `/api/projects/{id}/files` en erreur
- Authentification échouée
- Timeout

### **4. Erreur JavaScript**
- Console du navigateur avec erreurs
- Scripts non chargés
- Conflit de bibliothèques

---

## ✅ CORRECTIONS APPLIQUÉES

### **1. Initialisation Monaco améliorée**

**Avant** :
```javascript
require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(...);
});
```

**Après** :
```javascript
function initMonaco() {
    if (typeof monaco === 'undefined') {
        console.log('Monaco pas encore chargé, attente...');
        setTimeout(initMonaco, 100);
        return;
    }
    
    try {
        editor = monaco.editor.create(...);
        console.log('Monaco Editor initialisé');
    } catch (error) {
        console.error('Erreur initialisation Monaco:', error);
    }
}

// Avec fallback
if (typeof require !== 'undefined') {
    require.config({ paths: { vs: '...' }});
    require(['vs/editor/editor.main'], initMonaco);
} else {
    setTimeout(initMonaco, 1000);
}
```

**Bénéfices** :
- ✅ Retry automatique
- ✅ Logs détaillés
- ✅ Fallback si require absent
- ✅ Gestion d'erreur

---

### **2. Chargement arborescence amélioré**

**Avant** :
```javascript
async function loadFileTree() {
    const response = await fetch(`/api/projects/${projectId}/files`);
    const data = await response.json();
    renderFileTree(data.files);
}
```

**Après** :
```javascript
async function loadFileTree() {
    console.log('Chargement arborescence pour projet:', projectId);
    
    try {
        const response = await fetch(`/api/projects/${projectId}/files`);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Fichiers reçus:', data);
        
        if (data.files && data.files.length > 0) {
            renderFileTree(data.files);
        } else {
            // Afficher message "Aucun fichier"
        }
    } catch (error) {
        console.error('Erreur:', error);
        // Afficher message d'erreur
    }
}
```

**Bénéfices** :
- ✅ Logs à chaque étape
- ✅ Vérification HTTP status
- ✅ Gestion cas vide
- ✅ Messages d'erreur clairs

---

### **3. Initialisation séquencée**

**Avant** :
```javascript
document.addEventListener('DOMContentLoaded', () => {
    loadFileTree();
    initTerminal();
});
```

**Après** :
```javascript
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM chargé, initialisation...');
    console.log('Project ID:', projectId);
    
    // Terminal d'abord (500ms)
    setTimeout(() => {
        initTerminal();
    }, 500);
    
    // Arborescence ensuite (1000ms)
    setTimeout(() => {
        loadFileTree();
    }, 1000);
    
    // Fichier par défaut (2000ms)
    setTimeout(() => {
        openFile('index.html');
    }, 2000);
});
```

**Bénéfices** :
- ✅ Chargement progressif
- ✅ Évite les conflits
- ✅ Logs de debug
- ✅ Temps pour Monaco de charger

---

## 🧪 TESTS À EFFECTUER

### **Test 1 : Console navigateur**

**Ouvrir la console** (F12) et vérifier :

```
✅ "DOM chargé, initialisation..."
✅ "Project ID: X"
✅ "Monaco pas encore chargé, attente..." (peut apparaître plusieurs fois)
✅ "Monaco Editor initialisé"
✅ "Chargement arborescence pour projet: X"
✅ "Response status: 200"
✅ "Fichiers reçus: {...}"
```

**Si erreurs** :
```
❌ "Erreur initialisation Monaco: ..."
❌ "Erreur chargement arborescence: ..."
❌ "HTTP 404" ou "HTTP 500"
```

---

### **Test 2 : Vérifier le projet existe**

**Dans la console Python** :
```python
from app.database import SessionLocal
from app.models.web_project_db import WebProject

db = SessionLocal()
project = db.query(WebProject).filter(WebProject.id == 1).first()

if project:
    print(f"✅ Projet trouvé: {project.name}")
    print(f"   Chemin: {project.local_path}")
else:
    print("❌ Projet non trouvé")
```

---

### **Test 3 : Vérifier les fichiers**

**Manuellement** :
```bash
# Aller dans le dossier du projet
cd projects/1/nom-du-projet

# Lister les fichiers
ls -la
```

**Via API** :
```bash
curl http://localhost:8000/api/projects/1/files
```

**Résultat attendu** :
```json
{
  "files": [
    {
      "name": "index.html",
      "path": "index.html",
      "is_directory": false,
      "size": 1234
    },
    ...
  ]
}
```

---

## 🔧 SOLUTIONS PAR PROBLÈME

### **Si Monaco ne charge pas**

**Solution 1** : Vérifier CDN
```javascript
// Tester dans la console
console.log(typeof monaco);
// Devrait afficher "object" après quelques secondes
```

**Solution 2** : Utiliser un autre CDN
```html
<!-- Remplacer dans project_editor_v2.html -->
<script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs/loader.js"></script>
```

**Solution 3** : Télécharger Monaco localement
```bash
npm install monaco-editor
# Copier dans static/monaco/
```

---

### **Si arborescence vide**

**Solution 1** : Créer des fichiers de test
```python
from pathlib import Path

project_path = Path("projects/1/test-project")
project_path.mkdir(parents=True, exist_ok=True)

(project_path / "index.html").write_text("""<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body><h1>Hello World</h1></body>
</html>""")

(project_path / "styles.css").write_text("body { margin: 0; }")
(project_path / "script.js").write_text("console.log('Hello');")
```

**Solution 2** : Vérifier les permissions
```bash
# Donner les droits en lecture
chmod -R 755 projects/
```

---

### **Si erreur 404 sur API**

**Solution** : Vérifier que la route est enregistrée

```python
# Dans main.py
from app.routes.web_projects_routes import router as web_projects_router
app.include_router(web_projects_router, tags=["Web Projects"])
```

**Tester** :
```bash
curl http://localhost:8000/api/projects
# Devrait retourner la liste des projets
```

---

### **Si erreur authentification**

**Solution** : Se reconnecter

1. Aller sur `http://localhost:8000/login`
2. Se connecter
3. Retourner sur Studio IA

---

## 📊 CHECKLIST COMPLÈTE

### **Backend**
- [ ] Serveur démarré (`python main.py`)
- [ ] Route `/api/projects/{id}/files` fonctionne
- [ ] Projet existe en base de données
- [ ] Fichiers existent sur le disque
- [ ] Permissions correctes

### **Frontend**
- [ ] Page charge (pas de 404)
- [ ] Console sans erreurs JavaScript
- [ ] Monaco Editor CDN accessible
- [ ] Xterm.js CDN accessible
- [ ] `project_id` défini correctement

### **Données**
- [ ] Projet créé
- [ ] Fichiers présents
- [ ] Chemin `local_path` correct
- [ ] Utilisateur authentifié

---

## 🚀 COMMANDES RAPIDES

### **Redémarrer le serveur**
```bash
# Arrêter (Ctrl+C)
# Relancer
python main.py
```

### **Créer un projet de test**
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "project_type": "static",
    "description": "Projet de test"
  }'
```

### **Vérifier les logs**
```bash
# Dans le terminal où tourne le serveur
# Chercher les erreurs
```

### **Ouvrir la console navigateur**
```
F12 (Windows/Linux)
Cmd+Option+I (Mac)
```

---

## 💡 PROCHAINES ÉTAPES

1. **Ouvrir la console navigateur** (F12)
2. **Recharger la page** (Ctrl+R)
3. **Lire les logs** dans la console
4. **Identifier l'erreur** exacte
5. **Appliquer la solution** correspondante

---

## 📞 SI ÇA NE FONCTIONNE TOUJOURS PAS

**Envoyer** :
1. Screenshot de la console (F12)
2. Logs du serveur
3. Résultat de `curl http://localhost:8000/api/projects/1/files`

**Je pourrai alors** :
- Identifier le problème exact
- Proposer une solution ciblée
- Corriger le code si nécessaire

---

**Les corrections ont été appliquées. Redémarre le serveur et teste avec la console ouverte ! 🚀**
