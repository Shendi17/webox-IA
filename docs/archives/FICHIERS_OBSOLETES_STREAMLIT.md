# 🗑️ Fichiers Obsolètes Streamlit à Supprimer

**Date :** 30 Octobre 2025
**Raison :** Migration vers FastAPI terminée
**Action :** Suppression des fichiers Streamlit obsolètes

---

## ⚠️ IMPORTANT - À LIRE AVANT SUPPRESSION

**NE PAS SUPPRIMER IMMÉDIATEMENT !**

Ces fichiers contiennent la logique métier complète de l'application. Avant de les supprimer :
1. ✅ Vérifier que toutes les fonctionnalités sont migrées vers FastAPI
2. ✅ Créer une sauvegarde complète du projet
3. ✅ Tester toutes les fonctionnalités sur FastAPI
4. ✅ Documenter les changements

**Référence :** Voir `FONCTIONNALITES_A_MIGRER_FASTAPI.md` pour la liste complète des fonctionnalités à migrer.

---

## 📋 FICHIERS À SUPPRIMER (APRÈS MIGRATION COMPLÈTE)

### 1. **Application Streamlit Principale**
**Fichier :** `app.py` (72 KB)
**Raison :** Application Streamlit complète, remplacée par FastAPI
**Contient :**
- Chat Multi-IA
- Assistants IA
- Bibliothèque de Prompts
- Catalogue IA
- Combinaisons
- Pipedream
- Toute la logique Streamlit

**⚠️ CRITIQUE - Ne supprimer qu'après migration complète de toutes les fonctionnalités**

---

### 2. **Pages Streamlit**
**Dossier :** `pages/`

#### `pages/agents_ia.py` (Agents IA)
- Interface Streamlit pour les 8 agents spécialisés
- Orchestration de tâches
- Collaboration multi-agents
- **À migrer avant suppression**

#### `pages/assistant_vocal.py` (Assistant Vocal)
- Interface Streamlit pour l'assistant vocal
- Gestion des appels Twilio
- Test de synthèse vocale
- **À migrer avant suppression**

#### `pages/blog.py` (Blog)
- Interface Streamlit pour le blog
- Gestion des articles
- **À migrer avant suppression**

#### `pages/generation_audio.py` (Génération Audio)
- Interface Streamlit pour génération audio
- ElevenLabs, OpenAI TTS
- Bibliothèque audio
- **À migrer avant suppression**

#### `pages/generation_images.py` (Génération Images)
- Interface Streamlit pour génération d'images
- DALL-E 3, Stable Diffusion
- Galerie d'images
- **À migrer avant suppression**

#### `pages/generation_video.py` (Génération Vidéo)
- Page "Bientôt disponible"
- **Peut être supprimé en priorité (peu de logique)**

---

### 3. **Modules Streamlit**
**Dossier :** `modules/`

#### `modules/core/auth.py`
- Authentification Streamlit (session_state)
- **Remplacé par :** `app/controllers/auth_controller.py` (FastAPI)
- **Statut :** Peut être supprimé après vérification

#### `modules/core/landing_page/`
- `controller.py` - Contrôleur Streamlit
- `model.py` - Modèle de données
- `styles.py` - Styles Streamlit
- **Remplacé par :** Templates FastAPI + CSS
- **Statut :** Peut être supprimé après migration landing page

#### `modules/core/session_manager.py`
- Gestion des sessions Streamlit
- **Remplacé par :** JWT tokens FastAPI
- **Statut :** Peut être supprimé

#### `modules/core/theme_config.py`
- Configuration du thème Streamlit
- **Remplacé par :** CSS dans `static/css/`
- **Statut :** Peut être supprimé

#### `modules/pages/` (Pages statiques Streamlit)
- `cgu.py` - CGU
- `contact.py` - Contact
- `documentation.py` - Documentation
- `privacy.py` - Politique de confidentialité
- **Remplacé par :** Templates HTML FastAPI
- **Statut :** Peut être supprimé après migration des pages

---

### 4. **Scripts de Lancement Streamlit**
**Dossier :** `scripts/`

#### Scripts à Supprimer
- `DEMARRER-WEBOX.bat` - Lance Streamlit
- `LANCER-WEBOX.bat` - Lance Streamlit
- `lancer-webox.ps1` - Lance Streamlit
- `start.ps1` - Lance Streamlit
- `restart_app.ps1` - Redémarre Streamlit

**Remplacé par :** `LANCER-WEBOX-FLASH.bat` (FastAPI)

#### Scripts à Conserver (Setup)
- `SETUP-COMPLET.ps1` - Setup général (peut être adapté)
- `SETUP-COMPLET-V2.ps1` - Setup général (peut être adapté)
- `SETUP-FINAL.ps1` - Setup général (peut être adapté)

---

### 5. **Configuration Streamlit**
**Dossier :** `.streamlit/`

#### Fichiers
- `.streamlit/config.toml` - Configuration Streamlit
- **Statut :** Peut être supprimé (dossier vide actuellement)

---

### 6. **Fichiers de Test Streamlit**
**Racine du projet**

#### Fichiers à Supprimer
- `test_dashboard.py` - Tests Streamlit
- `test_links.py` - Tests Streamlit
- `test_login.py` - Tests Streamlit

**Remplacé par :** Tests FastAPI (pytest)

---

### 7. **Documentation Obsolète**
**Racine du projet**

#### Fichiers à Archiver (pas supprimer)
Ces fichiers contiennent de la documentation utile, à déplacer dans `docs/archives/` :

- `BOUTONS_FONCTIONNELS.md`
- `CLARIFICATION_LIENS.md`
- `COMPLETION_FINALE.md`
- `CONFIGURATION_API.md`
- `CONFIGURATION_WEBOX_LOCAL.md`
- `CONFIRMATION_LIENS.md`
- `DEBUG_BOUTONS.md`
- `DIAGNOSTIC_COMPLET.md`
- `DIAGNOSTIC_UI.md`
- `ENRICHISSEMENT_COMPLET.md`
- `ETAPES_FINALES.md`
- `FIX_CHAT_ERROR.md`
- `FIX_CONSOLE_ERRORS.md`
- `FONCTIONNALITES_COMPLETES.md`
- `GUIDE_CONNEXION.md`
- `GUIDE_COULEURS_SIDEBAR.md`
- `INTERFACE_COMPLETE.md`
- `LIENS_COMPLETS.md`
- `MIGRATION_COMPLETE.md`
- `PLAN_ENRICHISSEMENT.md`
- `SOLUTION_FINALE.md`
- `SOLUTION_LIENS.md`
- `STRUCTURE_PROJET.md`
- `STRUCTURE_PROJET_PROPRE.md`
- `SYSTEME_UI_COMPLET.md`
- `TEST_CONNEXION.md`
- `TEST_DIRECT.md`
- `TEST_LIENS_DASHBOARD.md`
- `TOUS_BOUTONS_FONCTIONNELS.md`
- `TOUTES_FONCTIONNALITES_COMPLETES.md`
- `TOUTES_FONCTIONS_ENRICHIES.md`

---

## 📊 RÉSUMÉ DES SUPPRESSIONS

### Fichiers Critiques (Ne PAS supprimer avant migration)
- ❌ `app.py` - Application principale
- ❌ `pages/agents_ia.py` - Agents IA
- ❌ `pages/assistant_vocal.py` - Assistant vocal
- ❌ `pages/generation_audio.py` - Génération audio
- ❌ `pages/generation_images.py` - Génération images
- ❌ `pages/blog.py` - Blog

### Fichiers à Supprimer en Priorité (Peu de logique)
- ✅ `pages/generation_video.py` - Page "Bientôt disponible"
- ✅ `.streamlit/config.toml` - Configuration Streamlit
- ✅ Scripts de lancement Streamlit (5 fichiers)
- ✅ Tests Streamlit (3 fichiers)

### Fichiers à Supprimer Après Vérification
- ⚠️ `modules/core/auth.py` - Après vérification auth FastAPI
- ⚠️ `modules/core/session_manager.py` - Après vérification sessions
- ⚠️ `modules/core/theme_config.py` - Après vérification CSS
- ⚠️ `modules/core/landing_page/` - Après migration landing page
- ⚠️ `modules/pages/` - Après migration pages statiques

### Documentation à Archiver (PAS supprimer)
- 📁 Déplacer 29 fichiers MD vers `docs/archives/`

---

## 🔄 PLAN DE SUPPRESSION PROGRESSIF

### Phase 1 : Suppression Immédiate (Sans Risque)
**Fichiers sans logique métier importante**

```powershell
# Supprimer les scripts Streamlit obsolètes
Remove-Item "scripts\DEMARRER-WEBOX.bat"
Remove-Item "scripts\LANCER-WEBOX.bat"
Remove-Item "scripts\lancer-webox.ps1"
Remove-Item "scripts\start.ps1"
Remove-Item "restart_app.ps1"

# Supprimer les tests Streamlit
Remove-Item "test_dashboard.py"
Remove-Item "test_links.py"
Remove-Item "test_login.py"

# Supprimer la page vidéo (placeholder)
Remove-Item "pages\generation_video.py"

# Supprimer le dossier .streamlit
Remove-Item ".streamlit" -Recurse -Force
```

### Phase 2 : Archivage Documentation
**Déplacer vers docs/archives/**

```powershell
# Créer le dossier archives si nécessaire
New-Item -ItemType Directory -Force -Path "docs\archives\migration_fastapi"

# Déplacer les fichiers MD obsolètes
Move-Item "BOUTONS_FONCTIONNELS.md" "docs\archives\migration_fastapi\"
Move-Item "CLARIFICATION_LIENS.md" "docs\archives\migration_fastapi\"
# ... (répéter pour tous les fichiers MD listés)
```

### Phase 3 : Suppression Modules Streamlit
**Après vérification que FastAPI fonctionne**

```powershell
# Supprimer les modules Streamlit
Remove-Item "modules\core\auth.py"
Remove-Item "modules\core\session_manager.py"
Remove-Item "modules\core\theme_config.py"
Remove-Item "modules\core\landing_page" -Recurse -Force
Remove-Item "modules\pages" -Recurse -Force
```

### Phase 4 : Suppression Pages Streamlit
**Après migration complète des fonctionnalités**

```powershell
# Supprimer les pages Streamlit
Remove-Item "pages\agents_ia.py"
Remove-Item "pages\assistant_vocal.py"
Remove-Item "pages\blog.py"
Remove-Item "pages\generation_audio.py"
Remove-Item "pages\generation_images.py"
```

### Phase 5 : Suppression Application Principale
**DERNIÈRE ÉTAPE - Après migration 100% complète**

```powershell
# Créer une sauvegarde finale
Copy-Item "app.py" "docs\archives\migration_fastapi\app_streamlit_backup.py"

# Supprimer l'application Streamlit
Remove-Item "app.py"
```

---

## ✅ CHECKLIST AVANT SUPPRESSION

### Avant Phase 1
- [ ] Vérifier que FastAPI fonctionne sur http://webox.local:8000
- [ ] Tester l'authentification FastAPI
- [ ] Créer une sauvegarde complète du projet

### Avant Phase 2
- [ ] Vérifier que la documentation est accessible
- [ ] Créer le dossier archives

### Avant Phase 3
- [ ] Vérifier l'authentification FastAPI
- [ ] Vérifier les sessions utilisateur
- [ ] Vérifier le CSS/styling

### Avant Phase 4
- [ ] Migrer toutes les fonctionnalités vers FastAPI
- [ ] Tester chaque fonctionnalité
- [ ] Documenter les changements

### Avant Phase 5
- [ ] Migration 100% complète
- [ ] Tests complets réussis
- [ ] Sauvegarde finale créée
- [ ] Équipe informée

---

## 📦 SAUVEGARDE RECOMMANDÉE

Avant toute suppression, créer une archive complète :

```powershell
# Créer une archive de sauvegarde
$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupName = "webox_streamlit_backup_$date.zip"

# Compresser le projet
Compress-Archive -Path "C:\Users\Anthony\CascadeProjects\webox\*" `
                 -DestinationPath "C:\Users\Anthony\CascadeProjects\$backupName"

Write-Host "Sauvegarde créée : $backupName"
```

---

## 🎯 OBJECTIF FINAL

Après suppression complète :
- ✅ Application 100% FastAPI
- ✅ Pas de dépendances Streamlit
- ✅ Code plus propre et maintenable
- ✅ Performance améliorée
- ✅ Architecture moderne (REST API + Frontend)

---

## 📊 STATISTIQUES

### Fichiers à Supprimer
- **Fichiers Python :** 15 fichiers
- **Scripts :** 5 fichiers
- **Documentation :** 29 fichiers (à archiver)
- **Total :** 49 fichiers

### Espace Disque Libéré (Estimé)
- **app.py :** 72 KB
- **Pages Streamlit :** ~150 KB
- **Modules Streamlit :** ~50 KB
- **Scripts :** ~20 KB
- **Total :** ~300 KB

---

**⚠️ RAPPEL IMPORTANT :** Ne supprimer les fichiers qu'après avoir migré toutes les fonctionnalités vers FastAPI et créé une sauvegarde complète !

**📅 Date de création :** 30 Octobre 2025
**👤 Créé par :** Cascade AI
