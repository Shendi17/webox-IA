# 🐛 DEBUG ÉDITEUR

**Date** : 22 Novembre 2025  
**Heure** : 19:19  
**Statut** : 🔍 EN COURS

---

## 🐛 PROBLÈME

L'éditeur s'affiche mais :
- ❌ Explorateur affiche "Erreur de chargement"
- ❌ Monaco Editor ne charge pas
- ❌ API retourne "Internal Server Error"

---

## ✅ VÉRIFICATIONS EFFECTUÉES

### **1. Projet en BDD** ✅
```
✅ Projet trouvé: Mon Projet Test
✅ Slug: mon-projet-test
✅ Local path défini
✅ Path existe
✅ 5 fichiers présents
```

### **2. Fonction build_tree** ✅
```json
{
  "files": [
    {"name": "index.html", "path": "index.html"},
    {"name": "README.md", "path": "README.md"},
    {"name": "script.js", "path": "script.js"},
    {"name": "src", "is_directory": true, "children": [...]},
    {"name": "style.css", "path": "style.css"}
  ]
}
```

### **3. API** ❌
```
GET /api/projects/1/files
→ Internal Server Error
```

---

## 🔍 CAUSES POSSIBLES

### **1. Serveur non redémarré**
Les modifications des routes n'ont peut-être pas été prises en compte.

### **2. Erreur dans la route**
Il peut y avoir une exception non gérée dans la route API.

### **3. CORS ou Headers**
Problème de configuration CORS.

---

## 🔧 SOLUTIONS

### **1. Redémarrer le serveur** ⚠️
```bash
# Arrêter le serveur (Ctrl+C)
# Puis relancer
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Vérifier les logs**
Regarder la console du serveur pour voir l'erreur exacte.

### **3. Tester l'API manuellement**
```bash
curl http://localhost:8000/api/projects/1/files
```

### **4. Vérifier la console navigateur**
Ouvrir F12 et regarder les erreurs JavaScript.

---

## 📋 CHECKLIST DE DEBUG

- [x] Projet existe en BDD
- [x] Local path défini
- [x] Fichiers existent
- [x] Fonction build_tree fonctionne
- [ ] Serveur redémarré
- [ ] API répond correctement
- [ ] Console navigateur sans erreurs
- [ ] Monaco Editor charge

---

## 🚀 ACTIONS IMMÉDIATES

### **1. Redémarrer le serveur**
```bash
# Dans le terminal où tourne le serveur
Ctrl+C
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Tester l'API**
```bash
curl http://localhost:8000/api/projects/1/files
```

### **3. Vérifier la console**
- Ouvrir F12 dans le navigateur
- Onglet Console
- Regarder les erreurs

### **4. Rafraîchir la page**
```
Ctrl+Shift+R (hard refresh)
```

---

## 📊 ÉTAT ACTUEL

### **Backend** ✅
- Routes définies
- Fonction build_tree OK
- Projet en BDD OK
- Fichiers présents OK

### **Frontend** ❌
- Template OK
- JavaScript OK
- Mais API ne répond pas
- Monaco ne charge pas

---

## 🎯 PROCHAINE ÉTAPE

**REDÉMARRER LE SERVEUR !**

Le serveur doit être redémarré pour prendre en compte les modifications des routes API.

---

**Instructions** :
1. Arrête le serveur (Ctrl+C dans le terminal)
2. Relance : `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`
3. Rafraîchis la page de l'éditeur
4. Vérifie la console (F12)
