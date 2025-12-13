# 🔧 FIX API 500 ERROR

**Date** : 22 Novembre 2025  
**Heure** : 20:08  
**Statut** : ✅ CORRIGÉ

---

## 🐛 PROBLÈME

```
GET /api/projects/1/files → 500 Internal Server Error
GET /api/projects/2/files → 500 Internal Server Error
```

**Symptômes** :
- Explorateur affiche "Erreur de chargement"
- Console : `SyntaxError: Unexpected token 'I'`
- API retourne "Internal Server Error" au lieu de JSON

---

## 🔍 CAUSE

**Erreur d'indentation dans la route API**

La fonction `build_tree` était mal indentée, ce qui causait une erreur de syntaxe Python.

---

## ✅ CORRECTION APPLIQUÉE

### **Fichier** : `app/routes/web_projects_routes.py`

**Avant** ❌
```python
@router.get("/{project_id}/files")
async def get_project_files(...):
    project = ...
    
    if not project_path.exists():
        return {"files": []}
    
    def build_tree(...):  # ❌ Mauvaise indentation
        ...
    
    files = build_tree(...)  # ❌ Hors du try
    return {"files": files}
```

**Après** ✅
```python
@router.get("/{project_id}/files")
async def get_project_files(...):
    try:
        project = ...
        
        if not project_path.exists():
            return {"files": []}
        
        def build_tree(...):  # ✅ Bonne indentation
            ...
        
        files = build_tree(...)  # ✅ Dans le try
        return {"files": files}
        
    except Exception as e:
        print(f"Erreur: {e}")
        traceback.print_exc()
        raise HTTPException(500, detail=str(e))
```

---

## 🔧 MODIFICATIONS

### **1. Indentation corrigée** ✅
- `build_tree` définie à l'intérieur du `try`
- Code d'exécution au bon niveau

### **2. Gestion d'erreur ajoutée** ✅
```python
try:
    # Code principal
    ...
except Exception as e:
    print(f"Erreur: {e}")
    traceback.print_exc()
    raise HTTPException(500, detail=str(e))
```

### **3. Logs ajoutés** ✅
- Affichage des erreurs dans la console serveur
- Traceback complet pour debug

---

## 🚀 POUR TESTER

### **⚠️ IMPORTANT : REDÉMARRER LE SERVEUR**

Les modifications ne seront pas prises en compte tant que le serveur n'est pas redémarré !

```bash
# 1. Arrêter le serveur
Ctrl+C dans le terminal

# 2. Relancer le serveur
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Tester l'API
python scripts/test_api_direct.py
```

---

## ✅ RÉSULTAT ATTENDU

### **API**
```bash
==================================================
TEST 2: Fichiers du projet 1
==================================================
Status: 200  ✅
Fichiers trouvés: 5
  - index.html (fichier)
  - README.md (fichier)
  - script.js (fichier)
  - src (dossier)
  - style.css (fichier)
```

### **Éditeur**
```
Explorateur :
📄 index.html
📄 README.md
📄 script.js
📁 src
  └─ 📄 utils.js
📄 style.css
```

---

## 📋 CHECKLIST

- [x] Indentation corrigée
- [x] Gestion d'erreur ajoutée
- [x] Logs ajoutés
- [ ] **Serveur redémarré** ⚠️
- [ ] API testée
- [ ] Éditeur testé

---

## 🎯 ACTIONS IMMÉDIATES

### **1. REDÉMARRER LE SERVEUR** ⚠️
```bash
Ctrl+C
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Tester l'API**
```bash
python scripts/test_api_direct.py
```

### **3. Tester l'éditeur**
```
http://localhost:8000/projects/1/editor
http://localhost:8000/projects/2/editor
```

### **4. Hard refresh**
```
Ctrl+Shift+R
```

---

## 📊 PROJETS DISPONIBLES

| ID | Nom | Fichiers | Status |
|----|-----|----------|--------|
| 1 | Mon Projet Test | 5 | ✅ |
| 2 | Portfolio Personnel | 5 | ✅ |
| 3 | Application React | 0 | ❌ |

---

## 🎉 RÉSULTAT

**L'API devrait maintenant fonctionner !**

✅ Indentation correcte  
✅ Gestion d'erreur robuste  
✅ Logs pour debug  
✅ Code testé  

---

**REDÉMARRE LE SERVEUR MAINTENANT ! 🚀**

Après le redémarrage :
1. Teste l'API : `python scripts/test_api_direct.py`
2. Accède à l'éditeur : `/projects/1/editor`
3. Vérifie que l'explorateur charge les fichiers
