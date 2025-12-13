# 📁 Structure du Projet WeBox Multi-IA

## 🎯 Organisation Réorganisée et Optimisée

Le projet a été réorganisé pour une meilleure clarté et maintenabilité.

---

## 📂 Structure des Dossiers

```
webox/
│
├── 📱 app.py                      # Application principale Streamlit
├── 📋 requirements.txt            # Dépendances Python
├── 🔐 .env                        # Variables d'environnement (non versionné)
├── 📝 .env.example                # Exemple de configuration
├── 🚫 .gitignore                  # Fichiers à ignorer
├── 📄 LICENSE                     # Licence du projet
│
├── 📂 modules/                    # Modules Python backend
│   ├── __init__.py
│   │
│   ├── 📂 core/                   # Modules principaux
│   │   ├── __init__.py
│   │   ├── ai_providers.py        # Gestionnaires IA (OpenAI, Claude, Gemini, etc.)
│   │   ├── ai_tools_catalog.py    # Catalogue de 50+ outils IA
│   │   ├── auth.py                # Authentification utilisateurs
│   │   ├── blog_manager.py        # Gestion du blog
│   │   ├── collaboration.py       # Collaboration multi-IA
│   │   ├── config.py              # Configuration globale
│   │   ├── generation_providers.py # Génération images/audio/vidéo
│   │   ├── landing_page.py        # Page d'accueil
│   │   ├── media_manager.py       # Gestion des médias
│   │   ├── pipedream_assistant.py # Assistant Pipedream
│   │   ├── session_manager.py     # Gestion des sessions
│   │   └── utils.py               # Utilitaires
│   │
│   ├── 📂 agents/                 # Système d'agents IA spécialisés
│   │   ├── __init__.py
│   │   ├── ai_agent_framework.py  # Framework d'orchestration
│   │   ├── specialized_agents.py  # 8 agents prédéfinis
│   │   ├── agent_communication.py # Communication inter-agents
│   │   ├── agent_knowledge_base.py # Base de connaissances
│   │   └── demo_agents_ia.py      # Script de démonstration
│   │
│   └── 📂 voice/                  # Assistant vocal IA
│       ├── __init__.py
│       ├── voice_telephony.py     # Gestion Twilio
│       ├── voice_stt.py           # Google Speech-to-Text
│       ├── voice_tts.py           # Google Text-to-Speech
│       └── voice_conversation_manager.py # Gestionnaire de conversations
│
├── 📂 pages/                      # Pages Streamlit
│   ├── agents_ia.py               # Page Agents IA
│   ├── assistant_vocal.py         # Page Assistant Vocal
│   ├── blog.py                    # Page Blog
│   ├── generation_audio.py        # Page Génération Audio
│   ├── generation_images.py       # Page Génération Images
│   └── generation_video.py        # Page Génération Vidéo
│
├── 📂 docs/                       # Documentation complète
│   ├── README.md                  # Documentation principale
│   ├── AGENTS_IA_DOCUMENTATION.md # Doc Agents IA (1000 lignes)
│   ├── AGENTS_IA_RESUME.md        # Résumé Agents IA
│   ├── ASSISTANT_VOCAL_IA.md      # Doc Assistant Vocal (800 lignes)
│   ├── ASSISTANT_VOCAL_RESUME.md  # Résumé Assistant Vocal
│   ├── IMPLEMENTATION_COMPLETE.md # Résumé global
│   ├── GUIDE_*.md                 # Guides divers
│   ├── TOP_50_IA*.md              # Catalogues IA
│   └── *.txt                      # Fichiers texte de documentation
│
├── 📂 scripts/                    # Scripts d'installation et setup
│   ├── LANCER-WEBOX.bat           # Lancer l'application (Windows)
│   ├── INSTALL_ASSISTANT_VOCAL.bat # Installer Assistant Vocal
│   ├── *.ps1                      # Scripts PowerShell
│   └── *.bat                      # Scripts batch
│
├── 📂 data/                       # Données et fichiers JSON
│   ├── agent_knowledge_base.json  # Base de connaissances agents
│   ├── blog_articles.json         # Articles de blog
│   ├── sessions.json              # Sessions utilisateurs
│   └── users.json                 # Utilisateurs
│
├── 📂 media/                      # Médias générés (images, audio, vidéo)
│
├── 📂 exports/                    # Exports et sauvegardes
│
└── 📂 .streamlit/                 # Configuration Streamlit
    └── config.toml
```

---

## 🎯 Modules Principaux

### **1. modules/core/** - Modules Principaux

| Fichier | Description | Lignes |
|---------|-------------|--------|
| `ai_providers.py` | Gestionnaires pour 12+ IA (OpenAI, Claude, Gemini, etc.) | ~600 |
| `ai_tools_catalog.py` | Catalogue de 50+ outils IA organisés par catégories | ~300 |
| `config.py` | Configuration globale de l'application | ~400 |
| `generation_providers.py` | Génération d'images, audio, vidéo | ~300 |
| `auth.py` | Système d'authentification | ~100 |
| `collaboration.py` | Collaboration multi-IA | ~200 |
| `pipedream_assistant.py` | Assistant pour créer des workflows Pipedream | ~400 |

### **2. modules/agents/** - Agents IA Spécialisés

| Fichier | Description | Lignes |
|---------|-------------|--------|
| `ai_agent_framework.py` | Framework d'orchestration des agents | ~450 |
| `specialized_agents.py` | 8 agents prédéfinis (Ventes, Marketing, Finance, etc.) | ~350 |
| `agent_communication.py` | Communication et collaboration inter-agents | ~300 |
| `agent_knowledge_base.py` | Base de connaissances partagée | ~250 |
| `demo_agents_ia.py` | Script de démonstration | ~200 |

**8 Agents Disponibles:**
- 💰 Agent Ventes
- 📢 Agent Marketing
- 💵 Agent Finance
- ⚙️ Agent Opérations
- 👤 Agent RH
- 💬 Agent Service Client
- 🎯 Agent Produit
- 🎯 Agent Stratégie

### **3. modules/voice/** - Assistant Vocal IA

| Fichier | Description | Lignes |
|---------|-------------|--------|
| `voice_telephony.py` | Gestion Twilio (appels, SMS) | ~200 |
| `voice_stt.py` | Google Speech-to-Text | ~170 |
| `voice_tts.py` | Google Text-to-Speech (10 voix) | ~240 |
| `voice_conversation_manager.py` | Gestionnaire de conversations vocales | ~350 |

---

## 📄 Pages Streamlit

| Page | Description | Fonctionnalités |
|------|-------------|-----------------|
| `agents_ia.py` | Gestion des agents IA | 5 onglets : Agents, Tâches, Collaboration, KB, Dashboard |
| `assistant_vocal.py` | Assistant vocal | Appels, SMS, Test vocal, Flux, Historique |
| `blog.py` | Blog | Articles, Top 50 IA |
| `generation_images.py` | Génération d'images | DALL-E, Stable Diffusion, Midjourney |
| `generation_audio.py` | Génération audio | ElevenLabs, OpenAI TTS |
| `generation_video.py` | Génération vidéo | Runway, Pika Labs |

---

## 📚 Documentation

### **Documentation Principale**

| Fichier | Contenu | Lignes |
|---------|---------|--------|
| `AGENTS_IA_DOCUMENTATION.md` | Documentation complète Agents IA | 1000 |
| `ASSISTANT_VOCAL_IA.md` | Documentation complète Assistant Vocal | 800 |
| `IMPLEMENTATION_COMPLETE.md` | Résumé global des 2 systèmes | 600 |
| `TOP_50_IA_INTEGREES.md` | Catalogue des 50+ IA intégrées | 500 |

### **Guides Rapides**

- `AGENTS_IA_RESUME.md` - Guide rapide Agents IA
- `ASSISTANT_VOCAL_RESUME.md` - Guide rapide Assistant Vocal
- `QUICKSTART.md` - Démarrage rapide
- `GUIDE_UTILISATION.md` - Guide d'utilisation

---

## 🔧 Scripts

### **Scripts de Lancement**

- `LANCER-WEBOX.bat` - Lancer l'application (Windows)
- `lancer-webox.ps1` - Lancer l'application (PowerShell)

### **Scripts d'Installation**

- `INSTALL_ASSISTANT_VOCAL.bat` - Installer les dépendances Assistant Vocal
- `SETUP-COMPLET.ps1` - Installation complète
- `CONFIGURER-WEBOX-LOCAL.bat` - Configuration locale

### **Scripts de Maintenance**

- `RESTAURER-HOSTS.ps1` - Restaurer le fichier hosts
- `fix-webox-local.ps1` - Corriger la configuration locale

---

## 💾 Données

### **Fichiers JSON**

| Fichier | Description |
|---------|-------------|
| `agent_knowledge_base.json` | Base de connaissances des agents (7+ entrées) |
| `blog_articles.json` | Articles du blog |
| `sessions.json` | Sessions utilisateurs |
| `users.json` | Utilisateurs enregistrés |

---

## 🚀 Démarrage Rapide

### **1. Installation**

```bash
pip install -r requirements.txt
```

### **2. Configuration**

Créer un fichier `.env` à partir de `.env.example` :

```env
# OpenAI (requis)
OPENAI_API_KEY=sk-...

# Autres IA (optionnel)
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...

# Assistant Vocal (optionnel)
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
GOOGLE_APPLICATION_CREDENTIALS=...
```

### **3. Lancement**

```bash
# Windows
scripts\LANCER-WEBOX.bat

# Ou directement
streamlit run app.py
```

### **4. Accès**

Ouvrir le navigateur : `http://localhost:8501`

---

## 📊 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| **Fichiers Python** | 30+ |
| **Lignes de code** | ~5,000 |
| **Modules** | 3 (core, agents, voice) |
| **Pages Streamlit** | 6 |
| **Documentation** | 2,800 lignes |
| **Agents IA** | 8 |
| **Providers IA** | 12+ |
| **Outils IA catalogués** | 50+ |

---

## 🎯 Fonctionnalités Principales

### **1. Chat Multi-IA**
- 12+ IA disponibles (OpenAI, Claude, Gemini, etc.)
- Streaming en temps réel
- Historique des conversations
- Export des conversations

### **2. Agents IA Spécialisés**
- 8 agents experts (Ventes, Marketing, Finance, etc.)
- Collaboration multi-agents
- Base de connaissances
- Métriques et monitoring

### **3. Assistant Vocal IA**
- Appels téléphoniques automatisés (Twilio)
- Reconnaissance vocale (Google STT)
- Synthèse vocale (Google TTS - 10 voix)
- 4 flux d'appels prédéfinis

### **4. Génération de Médias**
- **Images:** DALL-E, Stable Diffusion, Midjourney
- **Audio:** ElevenLabs, OpenAI TTS
- **Vidéo:** Runway, Pika Labs

### **5. Catalogue IA**
- 50+ outils IA organisés par catégories
- Recherche et filtrage
- Descriptions détaillées

### **6. Pipedream Assistant**
- Création de workflows automatisés
- Templates prédéfinis
- Intégration avec 1000+ apps

---

## 🔐 Sécurité

- Authentification utilisateurs
- Variables d'environnement pour les clés API
- Fichier `.env` non versionné
- Sessions sécurisées

---

## 📈 Évolution du Projet

### **Version Actuelle: 2.0**

**Nouveautés:**
- ✅ Réorganisation complète de la structure
- ✅ Système d'agents IA spécialisés
- ✅ Assistant vocal IA
- ✅ Documentation exhaustive (2,800 lignes)
- ✅ Structure modulaire claire

**Prochaines Étapes:**
- [ ] Tests unitaires
- [ ] CI/CD
- [ ] Déploiement cloud
- [ ] API REST
- [ ] Application mobile

---

## 🤝 Contribution

Le projet est organisé de manière modulaire pour faciliter les contributions :

1. **Ajouter une IA:** Modifier `modules/core/ai_providers.py`
2. **Ajouter un agent:** Modifier `modules/agents/specialized_agents.py`
3. **Ajouter une page:** Créer un fichier dans `pages/`
4. **Ajouter de la documentation:** Créer un fichier dans `docs/`

---

## 📞 Support

- **Documentation:** Dossier `docs/`
- **Scripts de démo:** `modules/agents/demo_agents_ia.py`
- **Exemples:** Voir les fichiers `RESUME.md`

---

**🎉 Structure optimisée pour une meilleure maintenabilité et scalabilité ! 🚀**
