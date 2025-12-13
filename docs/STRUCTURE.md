# 📁 Structure du Projet - WeBox Multi-IA

## 🌳 Arborescence

```
webox/
│
├── 📄 app.py                      # Application principale Streamlit
├── 📄 config.py                   # Configuration et paramètres
├── 📄 ai_providers.py             # Gestionnaires des différentes IA
├── 📄 utils.py                    # Fonctions utilitaires
│
├── 📋 requirements.txt            # Dépendances Python
├── 📋 .env.example                # Template de configuration
├── 📋 .gitignore                  # Fichiers à ignorer par Git
│
├── 🚀 start.ps1                   # Script de démarrage PowerShell
│
├── 📖 README.md                   # Documentation principale
├── 📖 QUICKSTART.md               # Guide de démarrage rapide
├── 📖 GUIDE_UTILISATION.md        # Guide d'utilisation détaillé
├── 📖 EXEMPLES.md                 # Exemples d'utilisation
├── 📖 STRUCTURE.md                # Ce fichier
├── 📖 CHANGELOG.md                # Historique des versions
├── 📖 CONTRIBUTING.md             # Guide de contribution
├── 📖 LICENSE                     # Licence MIT
│
├── ⚙️ .streamlit/                 # Configuration Streamlit
│   └── config.toml                # Thème et paramètres
│
└── 📁 data/                       # Données (créé automatiquement)
    └── conversations/             # Conversations sauvegardées
```

---

## 📄 Description des Fichiers

### Fichiers Principaux

#### `app.py` (18 KB)
**Rôle :** Application principale Streamlit  
**Contenu :**
- Interface utilisateur complète
- Navigation entre les pages
- Gestion du chat multi-IA
- Affichage des assistants
- Bibliothèque de prompts
- Page de configuration

**Sections :**
```python
# Configuration de la page
# CSS personnalisé
# Initialisation de la session
# Sidebar (navigation et sélection)
# Page Chat Multi-IA
# Page Assistants
# Page Bibliothèque de Prompts
# Page Configuration
```

---

#### `config.py` (6 KB)
**Rôle :** Configuration centralisée  
**Contenu :**
- Chargement des variables d'environnement
- Clés API
- Modèles disponibles
- Assistants pré-configurés
- Bibliothèque de prompts

**Structure :**
```python
class Config:
    # Clés API
    OPENAI_API_KEY
    ANTHROPIC_API_KEY
    GOOGLE_API_KEY
    
    # Configuration app
    APP_NAME
    APP_VERSION
    DEBUG
    
    # Modèles disponibles
    AVAILABLE_MODELS = {
        "OpenAI": {...},
        "Anthropic": {...},
        "Google": {...}
    }
    
    # Assistants
    ASSISTANTS = {
        "Rédacteur Marketing": {...},
        "Développeur": {...},
        ...
    }
    
    # Prompts
    PROMPT_LIBRARY = {
        "Marketing": [...],
        "Productivité": [...],
        ...
    }
```

---

#### `ai_providers.py` (8 KB)
**Rôle :** Gestionnaires des fournisseurs d'IA  
**Contenu :**
- Classes pour chaque fournisseur (OpenAI, Anthropic, Google)
- Gestion des requêtes asynchrones
- Vérification croisée
- Gestion multi-IA

**Classes :**
```python
class AIProvider(ABC)
    # Classe de base abstraite

class OpenAIProvider(AIProvider)
    # Gestion de GPT-4, GPT-3.5

class AnthropicProvider(AIProvider)
    # Gestion de Claude

class GoogleProvider(AIProvider)
    # Gestion de Gemini

class MultiAIManager
    # Orchestration de plusieurs IA
    # Requêtes parallèles
    # Vérification croisée
```

---

#### `utils.py` (7 KB)
**Rôle :** Fonctions utilitaires  
**Contenu :**
- Gestion des conversations
- Construction de prompts
- Analyse de réponses
- Export de données

**Classes :**
```python
class ConversationManager
    # Sauvegarde/chargement de conversations
    # Gestion de l'historique

class PromptBuilder
    # Construction de prompts structurés
    # Templates réutilisables

class ResponseAnalyzer
    # Comparaison de réponses
    # Extraction de points clés
    # Calcul de similarité

class ExportManager
    # Export en Markdown
    # Export en JSON
    # Export en TXT
```

---

### Fichiers de Configuration

#### `requirements.txt`
**Dépendances principales :**
```
streamlit==1.31.0          # Framework UI
openai==1.12.0             # API OpenAI
anthropic==0.18.1          # API Anthropic
google-generativeai==0.3.2 # API Google
fastapi==0.109.2           # Backend (futur)
python-dotenv==1.0.1       # Variables d'env
```

#### `.env.example`
**Template de configuration :**
```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

#### `.streamlit/config.toml`
**Configuration Streamlit :**
```toml
[theme]
primaryColor = "#667eea"    # Violet
backgroundColor = "#ffffff"  # Blanc
```

---

### Documentation

#### `README.md` (2 KB)
- Vue d'ensemble du projet
- Installation rapide
- Fonctionnalités principales
- Technologies utilisées

#### `QUICKSTART.md` (6 KB)
- Guide de démarrage en 5 minutes
- Installation express
- Premiers tests
- Problèmes courants

#### `GUIDE_UTILISATION.md` (8 KB)
- Guide complet d'utilisation
- Toutes les fonctionnalités
- Paramètres avancés
- Bonnes pratiques
- Dépannage

#### `EXEMPLES.md` (10 KB)
- 15+ exemples concrets
- Cas d'usage par domaine
- Templates réutilisables
- Exercices pratiques

#### `CONTRIBUTING.md` (8 KB)
- Guide de contribution
- Standards de code
- Process de développement
- Templates d'issues/PR

#### `CHANGELOG.md` (3 KB)
- Historique des versions
- Roadmap future
- Fonctionnalités prévues

---

## 🔄 Flux de Données

```
Utilisateur
    ↓
Interface Streamlit (app.py)
    ↓
Configuration (config.py)
    ↓
MultiAIManager (ai_providers.py)
    ↓
    ├→ OpenAIProvider → API OpenAI
    ├→ AnthropicProvider → API Anthropic
    └→ GoogleProvider → API Google
    ↓
Réponses agrégées
    ↓
Affichage dans l'interface
    ↓
Sauvegarde (utils.py)
```

---

## 🎯 Points d'Entrée

### Démarrage de l'Application
```bash
# Windows PowerShell
.\start.ps1

# Ligne de commande directe
streamlit run app.py
```

### Fichier Principal
- **Point d'entrée :** `app.py`
- **Port par défaut :** 8501
- **URL :** http://localhost:8501

---

## 📦 Modules et Dépendances

### Dépendances Principales
```
streamlit          → Interface utilisateur
openai            → GPT-4, GPT-3.5
anthropic         → Claude
google-generativeai → Gemini
python-dotenv     → Configuration
asyncio           → Requêtes asynchrones
```

### Modules Python Standard
```
os                → Gestion fichiers
json              → Sérialisation
datetime          → Timestamps
typing            → Type hints
abc               → Classes abstraites
```

---

## 🔐 Sécurité

### Fichiers Sensibles (dans .gitignore)
```
.env              # Clés API (NE JAMAIS COMMITER)
__pycache__/      # Cache Python
*.pyc             # Bytecode compilé
data/             # Données utilisateur
.streamlit/secrets.toml  # Secrets Streamlit
```

### Bonnes Pratiques
- ✅ Clés API dans `.env`
- ✅ `.env` dans `.gitignore`
- ✅ Utiliser `.env.example` comme template
- ❌ Ne jamais commiter `.env`
- ❌ Ne jamais hardcoder les clés API

---

## 🚀 Extensibilité

### Ajouter un Nouveau Fournisseur d'IA

1. **Créer une classe dans `ai_providers.py` :**
```python
class NewAIProvider(AIProvider):
    def __init__(self):
        # Configuration
        
    def is_configured(self) -> bool:
        # Vérification
        
    async def generate_response(self, ...):
        # Génération de réponse
```

2. **Ajouter dans `config.py` :**
```python
AVAILABLE_MODELS = {
    "NewAI": {
        "model-1": "Description",
        "model-2": "Description"
    }
}
```

3. **Enregistrer dans `MultiAIManager` :**
```python
self.providers = {
    ...
    "NewAI": NewAIProvider()
}
```

### Ajouter un Nouvel Assistant

Dans `config.py` :
```python
ASSISTANTS = {
    "Nouvel Assistant": {
        "description": "Description",
        "system_prompt": "Prompt système",
        "icon": "🎯"
    }
}
```

### Ajouter des Prompts

Dans `config.py` :
```python
PROMPT_LIBRARY = {
    "Nouvelle Catégorie": [
        {
            "name": "Nom du prompt",
            "prompt": "Contenu du prompt",
            "category": "Catégorie"
        }
    ]
}
```

---

## 📊 Statistiques du Projet

### Lignes de Code
```
app.py              : ~600 lignes
config.py           : ~200 lignes
ai_providers.py     : ~300 lignes
utils.py            : ~250 lignes
Total Code          : ~1350 lignes
```

### Documentation
```
README.md           : ~100 lignes
QUICKSTART.md       : ~250 lignes
GUIDE_UTILISATION.md: ~400 lignes
EXEMPLES.md         : ~500 lignes
Total Docs          : ~1250 lignes
```

### Taille Totale
```
Code Python         : ~35 KB
Documentation       : ~40 KB
Configuration       : ~5 KB
Total               : ~80 KB
```

---

## 🎨 Architecture

### Pattern MVC Adapté
```
Model (Données)
├── config.py          # Configuration
├── ai_providers.py    # Logique métier
└── utils.py           # Utilitaires

View (Interface)
└── app.py             # Interface Streamlit

Controller (Orchestration)
└── ai_providers.py    # MultiAIManager
```

### Design Patterns Utilisés
- **Singleton** : Configuration globale
- **Factory** : Création de providers
- **Strategy** : Différents fournisseurs d'IA
- **Observer** : Session state Streamlit

---

## 🔮 Évolution Future

### Structure Prévue v2.0
```
webox/
├── app/
│   ├── pages/         # Pages Streamlit
│   ├── components/    # Composants réutilisables
│   └── styles/        # CSS personnalisé
├── core/
│   ├── providers/     # Fournisseurs IA
│   ├── models/        # Modèles de données
│   └── services/      # Services métier
├── api/               # API REST (FastAPI)
├── tests/             # Tests unitaires
└── docs/              # Documentation
```

---

**Structure maintenue et documentée pour faciliter la contribution ! 🚀**
