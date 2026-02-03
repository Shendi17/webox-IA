# 🚀 QUICK START - WeBox Multi-IA

**Date** : 10 Novembre 2025  
**Statut** : ✅ Prêt à tester

---

## ✅ CE QUI EST OPÉRATIONNEL

### **1. Base de données** ✅
- 17 tables créées
- 8 nouvelles tables pour la génération
- Migration exécutée avec succès

### **2. Génération d'images** ✅
- API complète (`/api/generation/image`)
- Intégration DALL-E 3 & DALL-E 2
- Interface utilisateur fonctionnelle
- Sauvegarde automatique en DB

### **3. Agents IA** ✅
- 8 agents spécialisés avec contextes
- API fonctionnelle (`/api/assistants/chat`)

---

## 🚀 DÉMARRAGE RAPIDE

### **1. Configuration** (IMPORTANT)

Créer/modifier le fichier `.env` :

```env
# OpenAI (OBLIGATOIRE pour la génération d'images)
OPENAI_API_KEY=sk-proj-...

# Optionnel (pour les autres fonctionnalités)
STABILITY_API_KEY=...
ELEVENLABS_API_KEY=...
RUNWAY_API_KEY=...
```

### **2. Lancer le serveur**

```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **3. Accéder à l'application**

Ouvrir dans le navigateur :
```
http://localhost:8000
```

---

## 🎨 TESTER LA GÉNÉRATION D'IMAGES

### **Via l'interface web** :

1. **Se connecter** à l'application
2. **Aller sur** : http://localhost:8000/generation
3. **Cliquer** sur l'onglet "🖼️ Images"
4. **Entrer un prompt**, par exemple :
   ```
   A beautiful sunset over mountains with a lake in the foreground, 
   digital art, vibrant colors, 4k quality
   ```
5. **Sélectionner** le modèle : DALL-E 3
6. **Cliquer** sur "🎨 Générer l'image"
7. **Attendre** ~10-15 secondes
8. **Voir** le résultat dans une modal

### **Via l'API (Postman/curl)** :

```bash
curl -X POST http://localhost:8000/api/generation/image \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "prompt": "A beautiful sunset over mountains",
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "standard",
    "style": "natural"
  }'
```

**Réponse** :
```json
{
  "id": 1,
  "status": "generating",
  "message": "Génération d'image lancée",
  "prompt": "A beautiful sunset over mountains",
  "model": "dall-e-3"
}
```

**Vérifier le statut** :
```bash
curl http://localhost:8000/api/generation/image/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🤖 TESTER LES AGENTS IA

### **Via l'interface web** :

1. **Aller sur** : http://localhost:8000/agents
2. **Choisir un agent**, par exemple "Agent Marketing"
3. **Cliquer** sur "Lancer l'agent"
4. **Poser une question** :
   ```
   Comment créer une stratégie de contenu pour LinkedIn ?
   ```
5. **Recevoir** une réponse personnalisée

### **Via l'API** :

```bash
curl -X POST http://localhost:8000/api/assistants/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "assistant_type": "marketing",
    "message": "Comment créer une stratégie de contenu pour LinkedIn ?",
    "provider": "GPT-4",
    "model": "gpt-4-turbo"
  }'
```

---

## 📊 VÉRIFIER LES TABLES

```powershell
# Lister toutes les tables
python scripts/run_migration.py check

# Voir les détails d'une table
python scripts/run_migration.py info --table generated_images
```

---

## 🔍 DÉBOGUER

### **Vérifier les imports** :

```powershell
# Modèles
python -c "from app.models.generation_db import GeneratedImageDB; print('✅ OK')"

# Routes
python -c "from app.routes.generation_routes import router; print('✅ OK')"
```

### **Logs du serveur** :

Le serveur affiche les logs en temps réel. Chercher :
- ✅ `Application startup complete`
- ✅ `Uvicorn running on http://0.0.0.0:8000`

### **Erreurs communes** :

| Erreur | Solution |
|--------|----------|
| `OPENAI_API_KEY not found` | Ajouter la clé dans `.env` |
| `Table not found` | Exécuter `python scripts/run_migration.py migrate` |
| `Import error` | Vérifier que tous les fichiers sont créés |
| `401 Unauthorized` | Se connecter à l'application |

---

## 📁 FICHIERS GÉNÉRÉS

Les images générées sont sauvegardées dans :
```
generated/images/image_1.png
generated/images/image_2.png
...
```

---

## 💰 COÛTS DALL-E

| Modèle | Qualité | Taille | Coût |
|--------|---------|--------|------|
| DALL-E 3 | Standard | 1024x1024 | $0.040 |
| DALL-E 3 | Standard | 1792x1024 | $0.080 |
| DALL-E 3 | HD | 1024x1024 | $0.080 |
| DALL-E 3 | HD | 1792x1024 | $0.120 |
| DALL-E 2 | - | 1024x1024 | $0.020 |

**Les coûts sont calculés et sauvegardés automatiquement dans la DB.**

---

## 📋 CHECKLIST DE TEST

### **Génération d'images** :
- [ ] Serveur démarré
- [ ] Clé API OpenAI configurée
- [ ] Page /generation accessible
- [ ] Génération d'image lancée
- [ ] Image affichée dans la modal
- [ ] Image téléchargeable
- [ ] Coût affiché correctement
- [ ] Image sauvegardée en DB

### **Agents IA** :
- [ ] Page /agents accessible
- [ ] Modal d'agent s'ouvre
- [ ] Message envoyé
- [ ] Réponse reçue
- [ ] Contexte spécialisé appliqué

---

## 🎯 PROCHAINES ÉTAPES

Une fois les tests validés :

1. **Option B** : Implémenter les Combinaisons IA (Workflows)
2. **Option D** : Créer les prototypes (Vidéos, Audio, eBooks, Shorts)

---

## 📞 SUPPORT

En cas de problème :

1. **Vérifier les logs** du serveur
2. **Consulter** `IMPLEMENTATION_STATUS.md`
3. **Relancer** la migration si nécessaire
4. **Vérifier** que la clé API est valide

---

## 🎉 RÉSUMÉ

✅ **17 tables** créées  
✅ **Génération d'images** opérationnelle  
✅ **8 agents IA** avec contextes  
✅ **API complète** documentée  
✅ **Interface utilisateur** fonctionnelle  

**🚀 Prêt à générer des images avec l'IA !**
