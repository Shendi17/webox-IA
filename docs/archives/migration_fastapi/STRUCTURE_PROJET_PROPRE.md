# 📁 STRUCTURE DU PROJET WEBOX (Nettoyée)

## 🎯 Organisation Générale

```
webox/
├── 📄 Fichiers de configuration
│   ├── .env                          # Variables d'environnement (API keys)
│   ├── .env.example                  # Exemple de configuration
│   ├── .gitignore                    # Fichiers à ignorer par Git
│   └── .streamlit/
│       └── config.toml               # Configuration Streamlit
│
├── 📄 Documentation principale
│   ├── README.md                     # Guide principal du projet
│   ├── DEMARRAGE_RAPIDE.md          # Guide de démarrage rapide
│   ├── CONFIGURATION_API.md          # Configuration des API
│   ├── STRUCTURE_PROJET.md           # Structure détaillée
│   ├── GUIDE_COULEURS_SIDEBAR.md    # Guide de personnalisation UI
│   └── LICENSE                       # Licence du projet
│
├── 📄 Fichiers principaux
│   ├── app.py                        # Application principale Streamlit
│   ├── restart_app.ps1               # Script de redémarrage
│   └── agent_knowledge_base.json     # Base de connaissances des agents
│
├── 📂 modules/                       # Code source organisé
│   ├── core/                         # Modules principaux
│   │   ├── __init__.py
│   │   ├── ai_providers.py           # Gestion des fournisseurs IA
│   │   ├── ai_tools_catalog.py       # Catalogue des outils IA
│   │   ├── auth.py                   # Authentification
│   │   ├── blog_manager.py           # Gestion du blog
│   │   ├── collaboration.py          # Collaboration multi-IA
│   │   ├── config.py                 # Configuration globale
│   │   ├── generation_providers.py   # Génération média (images, audio, vidéo)
│   │   ├── media_manager.py          # Gestion des médias
│   │   ├── pipedream_assistant.py    # Assistant Pipedream
│   │   ├── session_manager.py        # Gestion des sessions
│   │   ├── theme_config.py           # Configuration du thème UI
│   │   ├── utils.py                  # Utilitaires
│   │   └── landing_page/             # Landing page (architecture MVC)
│   │       ├── __init__.py
│   │       ├── controller.py         # Contrôleur
│   │       ├── model.py              # Modèle
│   │       └── styles.py             # Styles CSS
│   │
│   └── pages/                        # Pages supplémentaires
│       ├── __init__.py
│       ├── contact.py
│       ├── documentation.py
│       ├── cgu.py
│       └── privacy.py
│
├── 📂 pages/                         # Pages Streamlit multi-pages
│   ├── generation_audio.py
│   ├── generation_images.py
│   ├── generation_video.py
│   ├── assistant_vocal.py
│   ├── agents_ia.py
│   └── blog.py
│
├── 📂 data/                          # Données de l'application
│   ├── users/                        # Données utilisateurs
│   ├── conversations/                # Historique des conversations
│   └── prompts/                      # Prompts sauvegardés
│
├── 📂 exports/                       # Exports générés
│   └── conversations/                # Conversations exportées
│
├── 📂 media/                         # Médias générés
│   ├── images/                       # Images générées
│   ├── audio/                        # Audio généré
│   └── video/                        # Vidéos générées
│
├── 📂 scripts/                       # Scripts utilitaires
│   ├── setup/                        # Scripts d'installation
│   ├── maintenance/                  # Scripts de maintenance
│   └── utils/                        # Scripts utilitaires
│
└── 📂 docs/                          # Documentation complète
    ├── api/                          # Documentation API
    ├── guides/                       # Guides utilisateur
    ├── development/                  # Documentation développeur
    └── archives/                     # 🗄️ Anciennes documentations de sessions
        ├── AJUSTEMENT_ESPACEMENT_BOUTONS.md
        ├── AJUSTEMENT_MARGES_LANDING.md
        ├── AJUSTEMENT_MARGES_LATERALES.md
        ├── COMMENT_VOIR_LES_CHANGEMENTS.md
        ├── CORRECTION_MARGES_FINALE.md
        ├── DIAGNOSTIC_MARGES.md
        ├── MIGRATION_MVC.md
        ├── MISE_A_JOUR_CONFIGURATION.md
        ├── MISE_A_JOUR_LANDING_PAGE.md
        ├── NETTOYAGE_CODE_BOUTON_TOGGLE.md
        ├── RECAP_SESSION_LANDING_PAGE.md
        ├── REORGANISATION_COMPLETE.md
        ├── RESOLUTION_PROBLEMES.md
        └── RESUME_FINAL_COMPLET.md
```

---

## 🎨 Fichiers de Configuration UI

### **Thème et Couleurs**
- **`modules/core/theme_config.py`** - Configuration complète du thème
  - Couleurs de la sidebar (12 groupes d'éléments)
  - Couleurs de la page principale
  - Couleurs des cartes
  - Génération du CSS

- **`GUIDE_COULEURS_SIDEBAR.md`** - Guide de personnalisation
  - Liste de tous les éléments modifiables
  - Numéros de lignes exacts
  - Exemples de couleurs
  - Instructions de modification

---

## 🤖 Modules Principaux

### **1. Gestion des IA**
- `ai_providers.py` - Gestion des fournisseurs IA (OpenAI, Anthropic, Google, etc.)
- `ai_tools_catalog.py` - Catalogue des outils IA disponibles
- `collaboration.py` - Collaboration multi-IA

### **2. Génération de Contenu**
- `generation_providers.py` - Génération d'images, audio, vidéo
- `media_manager.py` - Gestion des médias générés

### **3. Système**
- `auth.py` - Authentification utilisateur
- `session_manager.py` - Gestion des sessions
- `config.py` - Configuration globale
- `utils.py` - Fonctions utilitaires

### **4. Fonctionnalités**
- `blog_manager.py` - Gestion du blog
- `pipedream_assistant.py` - Assistant Pipedream
- `landing_page/` - Landing page (architecture MVC)

---

## 📄 Documentation Principale (Racine)

### **À Conserver :**
1. **README.md** - Guide principal du projet
2. **DEMARRAGE_RAPIDE.md** - Guide de démarrage rapide
3. **CONFIGURATION_API.md** - Configuration des clés API
4. **STRUCTURE_PROJET.md** - Structure détaillée du projet
5. **GUIDE_COULEURS_SIDEBAR.md** - Guide de personnalisation UI
6. **LICENSE** - Licence du projet

### **Archivés (docs/archives/) :**
- Tous les fichiers de sessions de développement
- Documentation obsolète
- Guides de migration

---

## 🗂️ Organisation des Données

### **data/**
- `users/` - Profils et préférences utilisateurs
- `conversations/` - Historique des conversations
- `prompts/` - Bibliothèque de prompts

### **exports/**
- `conversations/` - Conversations exportées (JSON, MD, TXT)

### **media/**
- `images/` - Images générées par IA
- `audio/` - Audio généré par IA
- `video/` - Vidéos générées par IA

---

## 🔧 Scripts Utilitaires

### **scripts/**
- `setup/` - Scripts d'installation et configuration
- `maintenance/` - Scripts de maintenance et nettoyage
- `utils/` - Scripts utilitaires divers

---

## 🚀 Démarrage Rapide

### **1. Installation**
```powershell
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API
```

### **2. Lancement**
```powershell
# Démarrer l'application
streamlit run app.py

# Ou utiliser le script de redémarrage
.\restart_app.ps1
```

---

## 📝 Fichiers Importants

### **Configuration**
- `.env` - Clés API et configuration (NE PAS COMMIT)
- `.streamlit/config.toml` - Configuration Streamlit

### **Code Principal**
- `app.py` - Point d'entrée de l'application
- `modules/core/theme_config.py` - Configuration du thème

### **Documentation**
- `README.md` - Guide principal
- `GUIDE_COULEURS_SIDEBAR.md` - Personnalisation UI

---

## 🧹 Nettoyage Effectué

### **✅ Fichiers Supprimés**
- `test_mvc.py` - Fichier de test obsolète
- `test_mvc_import.py` - Fichier de test obsolète
- `INSTRUCTIONS_BOUTON_SIDEBAR.md` - Fichier vide
- `modules/core/landing_page_backup.py` - Backup obsolète
- `modules/core/landing_page_old.py` - Ancienne version

### **📦 Fichiers Archivés (docs/archives/)**
- 15 fichiers de documentation de sessions
- Guides de migration et ajustements
- Résolutions de problèmes passés

---

## 🎯 Structure Recommandée pour Développement

### **Avant de modifier :**
1. Consulter `GUIDE_COULEURS_SIDEBAR.md` pour les modifications UI
2. Consulter `STRUCTURE_PROJET.md` pour l'architecture
3. Consulter `CONFIGURATION_API.md` pour les API

### **Fichiers à ne jamais supprimer :**
- `app.py` - Application principale
- `modules/core/` - Tous les modules principaux
- `.env` - Configuration (mais ne pas commit)
- `README.md` - Documentation principale

### **Fichiers modifiables fréquemment :**
- `modules/core/theme_config.py` - Personnalisation UI
- `modules/core/config.py` - Configuration globale
- `GUIDE_COULEURS_SIDEBAR.md` - Documentation UI

---

## 📊 Statistiques du Projet

- **Modules principaux :** 13 fichiers Python
- **Pages Streamlit :** 6 pages
- **Documentation active :** 6 fichiers MD
- **Documentation archivée :** 15 fichiers MD
- **Scripts utilitaires :** ~17 scripts

---

## 🔄 Maintenance

### **Nettoyage régulier :**
```powershell
# Nettoyer les caches Python
Remove-Item -Recurse -Force __pycache__

# Nettoyer les médias temporaires
Remove-Item -Recurse -Force media\temp\

# Nettoyer les exports anciens
Remove-Item -Force exports\conversations\*.old
```

### **Backup recommandé :**
- `data/` - Données utilisateurs
- `.env` - Configuration
- `modules/` - Code source

---

## 📞 Support

Pour toute question sur la structure du projet, consulter :
1. Ce fichier (`STRUCTURE_PROJET_PROPRE.md`)
2. `README.md` - Guide principal
3. `GUIDE_COULEURS_SIDEBAR.md` - Personnalisation UI
