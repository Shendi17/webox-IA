# 🚀 WeBox Marketing IA

**La Plateforme Marketing IA la Plus Complète du Marché**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)]()

---

## 🎯 Vue d'Ensemble

**WeBox** est la plateforme marketing IA tout-en-un qui combine **13 modules professionnels** pour gérer l'intégralité de votre présence digitale :

- 🌐 **Website Builder IA** - Sites web complets en quelques clics
- 🎯 **Tunnels de Vente** - Funnels automatisés avec 5 templates
- 📱 **Réseaux Sociaux** - Gestion de 6 plateformes
- 👤 **Influenceurs IA** - Création d'influenceurs virtuels
- 📧 **Email Marketing** - Campagnes automatisées
- 📊 **Présentations IA** - PowerPoint/PDF automatiques
- 🎨 **Génération Multi-Média** - Images, vidéos, audio, logos (7 types)
- 💬 **Chat Multi-IA** - 20+ modèles d'IA
- 🤖 **Agents IA** - 12 agents spécialisés
- 📞 **Assistant Vocal** - Appels automatisés
- 🌐 **Landing Pages** - Pages optimisées
- 🔄 **Automatisation** - Workflows intelligents
- 📚 **Bibliothèque Prompts** - Gestion de prompts

**= Wix + Webflow + ClickFunnels + Canva + Buffer + Mailchimp + 20 autres outils IA**

---

## ✨ Fonctionnalités Principales

### **1. Chat Multi-IA**
Discutez avec 12+ modèles d'IA différents :
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)
- Google (Gemini Pro)
- Mistral AI
- Perplexity
- Et plus encore...

### **2. Agents IA Spécialisés** 🆕
8 agents experts pour automatiser votre entreprise :
- 💰 **Ventes** - Prospection, closing, CRM
- 📢 **Marketing** - Stratégie, contenu, SEO
- 💵 **Finance** - Analyse, budget, prévisions
- ⚙️ **Opérations** - Processus, optimisation
- 👤 **RH** - Recrutement, formation
- 💬 **Service Client** - Support, satisfaction
- 🎯 **Produit** - Roadmap, UX
- 🎯 **Stratégie** - Vision, planification

**Fonctionnalités:**
- Tâches individuelles avec priorités
- Collaboration multi-agents
- Base de connaissances partagée
- Métriques et monitoring

### **3. Assistant Vocal IA** 🆕
Automatisez vos appels téléphoniques :
- ☎️ Appels sortants/entrants (Twilio)
- 🎤 Reconnaissance vocale (Google STT)
- 🔊 Synthèse vocale (10 voix françaises)
- 💬 Conversation IA (GPT-4)
- 📋 4 flux d'appels prédéfinis

### **4. Génération de Médias**
- 🎨 **Images** - DALL-E, Stable Diffusion, Midjourney
- 🎙️ **Audio** - ElevenLabs, OpenAI TTS
- 🎬 **Vidéo** - Runway, Pika Labs

### **5. Catalogue IA**
50+ outils IA organisés par catégories :
- Texte & Écriture
- Images & Design
- Audio & Musique
- Vidéo & Animation
- Code & Développement
- Recherche & Analyse
- Productivité
- Et plus...

---

## 🚀 Installation

### **Prérequis**
- Python 3.8+
- pip

### **1. Cloner le projet**

```bash
git clone https://github.com/votre-repo/webox-multi-ia.git
cd webox-multi-ia
```

### **2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

### **3. Configuration**

Créer un fichier `.env` à partir de `.env.example` :

```env
# OpenAI (requis pour la plupart des fonctionnalités)
OPENAI_API_KEY=sk-...

# Autres IA (optionnel)
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
MISTRAL_API_KEY=...

# Assistant Vocal (optionnel)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+33...
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Génération de médias (optionnel)
ELEVENLABS_API_KEY=...
STABILITY_API_KEY=...
```

### **4. Lancer l'application**

```bash
# Windows
scripts\LANCER-WEBOX.bat

# Linux/Mac ou directement
streamlit run app.py
```

### **5. Accéder à l'application**

Ouvrir le navigateur : `http://localhost:8501`

**Identifiants par défaut:**
- Email: `admin@webox.com`
- Mot de passe: `admin123`

---

## 📁 Structure du Projet

```
webox/
├── app.py                    # Application principale
├── requirements.txt          # Dépendances
├── modules/                  # Modules Python
│   ├── core/                # Modules principaux
│   ├── agents/              # Agents IA spécialisés
│   └── voice/               # Assistant vocal
├── pages/                    # Pages Streamlit
├── docs/                     # Documentation
├── scripts/                  # Scripts d'installation
└── data/                     # Données JSON
```

Voir [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md) pour plus de détails.

---

## 📚 Documentation

### **Documentation Complète**
- [Agents IA - Documentation](docs/AGENTS_IA_DOCUMENTATION.md) (1000 lignes)
- [Assistant Vocal - Documentation](docs/ASSISTANT_VOCAL_IA.md) (800 lignes)
- [Implémentation Complète](docs/IMPLEMENTATION_COMPLETE.md)

### **Guides Rapides**
- [Agents IA - Résumé](docs/AGENTS_IA_RESUME.md)
- [Assistant Vocal - Résumé](docs/ASSISTANT_VOCAL_RESUME.md)
- [Démarrage Rapide](docs/QUICKSTART.md)

### **Catalogues**
- [Top 50 IA Intégrées](docs/TOP_50_IA_INTEGREES.md)
- [Guide par Catégorie](docs/GUIDE_IA_PAR_CATEGORIE.txt)

---

## 💡 Exemples d'Utilisation

### **Exemple 1 : Tâche Simple avec un Agent**

```python
from modules.agents.ai_agent_framework import agent_orchestrator
from modules.agents.specialized_agents import initialize_all_agents
import asyncio

# Initialiser les agents
initialize_all_agents()

# Créer une tâche
task = agent_orchestrator.create_task(
    agent_id="agent_ventes",
    description="Analyser les performances commerciales du dernier trimestre",
    priority=4
)

# Exécuter
result = asyncio.run(agent_orchestrator.execute_next_task())
print(result['result'])
```

### **Exemple 2 : Collaboration Multi-Agents**

```python
from modules.agents.agent_communication import collaboration_manager

result = asyncio.run(collaboration_manager.create_collaboration_task(
    task_description="Créer une stratégie de lancement produit complète",
    involved_agents=["agent_produit", "agent_marketing", "agent_ventes"],
    coordinator_agent="agent_strategie"
))

print(result['synthesis'])
```

### **Exemple 3 : Appel Vocal Automatisé**

```python
from modules.voice.voice_telephony import twilio_manager

twilio_manager.make_call(
    to_number="+33612345678",
    message="Bonjour, votre commande est prête pour le retrait."
)
```

---

## 💰 Coûts Estimés

### **Agents IA**
- Tâche simple : ~0.03$
- Collaboration (3 agents) : ~0.25$
- **100 tâches/mois : ~6$**

### **Assistant Vocal**
- Appel 1 min : ~0.06€
- **100 appels/mois : ~6€**

### **Total pour usage modéré : ~12€/mois**

---

## 🎯 Cas d'Usage

### **Startups**
- Automatisation de la prospection
- Analyse de marché
- Support client 24/7
- Génération de contenu

### **PME**
- Gestion multi-départements
- Optimisation des coûts
- Stratégie de croissance
- Formation des équipes

### **Entreprises**
- Transformation digitale
- Excellence opérationnelle
- Innovation produit
- Planification stratégique

---

## 🛠️ Technologies

- **Frontend:** Streamlit
- **Backend:** Python 3.8+
- **IA:** OpenAI, Anthropic, Google, Mistral, etc.
- **Téléphonie:** Twilio
- **Vocal:** Google Cloud STT/TTS
- **Base de données:** JSON (fichiers locaux)

---

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| **Modules complets** | 13 |
| **Routes API** | 74 |
| **Tables DB** | 34 |
| **Pages frontend** | 20+ |
| **Lignes de code** | 5,219 |
| **Modèles IA** | 20+ |
| **Templates** | 25+ |
| **Économie vs concurrence** | 80% |

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

Voir [CONTRIBUTING.md](docs/CONTRIBUTING.md) pour plus de détails.

---

## 📝 License

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus d'informations.

---

## 🙏 Remerciements

- OpenAI pour GPT-4
- Anthropic pour Claude
- Google pour Gemini et Cloud Services
- Twilio pour la téléphonie
- Streamlit pour le framework

---

## 📞 Support

- **Documentation:** Dossier `docs/`
- **Issues:** [GitHub Issues](https://github.com/votre-repo/webox-multi-ia/issues)
- **Email:** support@webox.com

---

## 🗺️ Roadmap

### **Court Terme**
- [ ] Tests unitaires
- [ ] CI/CD
- [ ] Docker

### **Moyen Terme**
- [ ] API REST
- [ ] Intégrations externes (CRM, ERP)
- [ ] Modèles locaux (Llama, Mistral)

### **Long Terme**
- [ ] Application mobile
- [ ] Marketplace d'agents
- [ ] Déploiement cloud

---

**🎉 WeBox Multi-IA - Automatisez votre entreprise avec l'IA ! 🚀**

Made with ❤️ by the WeBox Team
