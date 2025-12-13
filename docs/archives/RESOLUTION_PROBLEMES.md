# 🔧 Résolution des Problèmes - WeBox Multi-IA

## ✅ Problèmes Résolus

### **1. Erreur: ModuleNotFoundError: No module named 'session_manager'**

**Cause:** Imports non mis à jour après la réorganisation

**Solution:** ✅ CORRIGÉ
- Fichier `modules/core/auth.py` mis à jour
- Imports corrigés vers `modules.core.session_manager`

---

### **2. Fichier `.env` obsolète**

**Cause:** Ancien format de configuration

**Solution:** Mettre à jour avec le nouveau template

```bash
# Sauvegarder vos clés actuelles
# Puis copier le nouveau template
copy .env.example .env
```

**Remplir au minimum:**
```env
OPENAI_API_KEY=sk-votre-clé-ici
```

---

## 🚀 Vérifications Post-Réorganisation

### **Checklist de Démarrage**

- [x] Structure réorganisée
- [x] Imports mis à jour
- [x] Chemins des fichiers JSON corrigés
- [x] Compilation vérifiée
- [ ] Fichier `.env` mis à jour (À FAIRE PAR VOUS)
- [ ] Application testée

---

## 📝 Actions Requises

### **1. Mettre à Jour `.env`**

**Étape 1:** Sauvegarder vos clés actuelles
```
OPENAI_API_KEY=sk-xxxxxxxx
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
GOOGLE_APPLICATION_CREDENTIALS=C:/chemin/vers/credentials.json
```

**Étape 2:** Copier le nouveau template
```bash
copy .env.example .env
```

**Étape 3:** Remplir avec vos clés
Ouvrir `.env` et ajouter vos clés dans les sections appropriées :

```env
# ============================================
# 1. IA CONVERSATIONNELLES
# ============================================

# OpenAI [REQUIS]
OPENAI_API_KEY=sk-votre-vraie-clé-ici

# Anthropic Claude [RECOMMANDÉ]
ANTHROPIC_API_KEY=

# Google AI [RECOMMANDÉ]
GOOGLE_API_KEY=

# ============================================
# 5. ASSISTANT VOCAL IA
# ============================================

# Twilio [REQUIS pour assistant vocal]
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
TWILIO_PHONE_NUMBER=+33123456789

# Google Cloud [REQUIS pour assistant vocal]
GOOGLE_APPLICATION_CREDENTIALS=C:/chemin/vers/credentials.json

# ============================================
# 10. CONFIGURATION DE L'APPLICATION
# ============================================

APP_NAME=WeBox Multi-IA
APP_VERSION=2.0.0
DEBUG=True
```

---

### **2. Vérifier les Fichiers de Données**

Les fichiers JSON sont maintenant dans le dossier `data/` :

```bash
# Vérifier que le dossier existe
dir data

# Si le dossier n'existe pas, le créer
mkdir data
```

**Fichiers attendus dans `data/`:**
- `users.json` (créé automatiquement au premier lancement)
- `sessions.json` (créé automatiquement)
- `blog_articles.json` (déplacé depuis la racine)
- `agent_knowledge_base.json` (déplacé depuis la racine)

---

## 🧪 Test de l'Application

### **1. Vérifier la Compilation**

```bash
python -m py_compile app.py
```

**Résultat attendu:** Aucune erreur ✅

---

### **2. Lancer l'Application**

```bash
streamlit run app.py
```

**Ou utiliser le script:**
```bash
scripts\LANCER-WEBOX.bat
```

---

### **3. Tester la Connexion**

1. Ouvrir http://localhost:8501
2. Se connecter avec:
   - Email: `admin@webox.com`
   - Mot de passe: `admin123`

---

## ❌ Problèmes Possibles

### **Erreur: FileNotFoundError: users.json**

**Cause:** Fichier dans l'ancien emplacement

**Solution:**
```bash
# Déplacer le fichier vers data/
move users.json data\users.json
move sessions.json data\sessions.json
```

---

### **Erreur: No module named 'modules.core.xxx'**

**Cause:** Import incorrect

**Solution:** Vérifier que tous les imports utilisent `modules.core.` ou `modules.agents.` ou `modules.voice.`

**Exemple correct:**
```python
from modules.core.ai_providers import ai_manager
from modules.agents.ai_agent_framework import agent_orchestrator
from modules.voice.voice_telephony import twilio_manager
```

---

### **Erreur: Invalid API key**

**Cause:** Clé API incorrecte ou manquante dans `.env`

**Solution:**
1. Vérifier que `.env` existe
2. Vérifier que la clé est correctement copiée (pas d'espaces)
3. Vérifier que la clé est valide sur la plateforme

---

### **Erreur: Port already in use**

**Cause:** Port 8501 déjà utilisé

**Solution:**
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502
```

---

## 📊 État Actuel du Projet

### **✅ Fonctionnel**
- Structure réorganisée
- Imports corrigés
- Chemins JSON corrigés
- Compilation réussie

### **⚠️ À Faire par Vous**
- Mettre à jour le fichier `.env`
- Déplacer les fichiers JSON vers `data/` (si nécessaire)
- Tester l'application

---

## 🔍 Diagnostic Rapide

### **Commandes de Vérification**

```bash
# 1. Vérifier la structure
dir modules
dir modules\core
dir modules\agents
dir modules\voice

# 2. Vérifier les données
dir data

# 3. Vérifier la compilation
python -m py_compile app.py
python -m py_compile modules\core\auth.py
python -m py_compile modules\core\session_manager.py

# 4. Vérifier .env
type .env
```

---

## 📞 Support

### **Documentation**
- `README.md` - Documentation principale
- `DEMARRAGE_RAPIDE.md` - Démarrage en 3 étapes
- `CONFIGURATION_API.md` - Configuration des APIs
- `STRUCTURE_PROJET.md` - Structure du projet

### **Guides**
- `docs/GUIDE_OBTENTION_CLES_API.md` - Obtenir les clés API
- `MISE_A_JOUR_CONFIGURATION.md` - Configuration complète

---

## ✅ Résumé des Corrections

| Problème | Fichier | Correction |
|----------|---------|------------|
| Import session_manager | `modules/core/auth.py` | ✅ Corrigé |
| Chemin users.json | `modules/core/auth.py` | ✅ Corrigé |
| Chemin sessions.json | `modules/core/session_manager.py` | ✅ Corrigé |
| Chemin blog_articles.json | `modules/core/blog_manager.py` | ✅ Corrigé |
| Compilation | `app.py` | ✅ Vérifiée |

---

**🔧 Problèmes résolus ! Il ne reste plus qu'à mettre à jour votre fichier `.env` ! 🚀**
