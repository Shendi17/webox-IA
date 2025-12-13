# 🤖 WeBox Multi-IA

Une plateforme multi-IA tout-en-un inspirée de Polyia.io, permettant d'accéder aux meilleures IA du marché sur une seule interface.

## 🌟 Fonctionnalités

- **Accès Multi-IA** : Échangez avec GPT-4, Claude, Gemini et d'autres IA sur la même interface
- **Assistants IA Spécialisés** : Accédez à des assistants pré-configurés pour différentes tâches
- **Bibliothèque de Prompts** : Prompts clé en main et création personnalisée
- **Comparaison de Résultats** : Comparez facilement les réponses de différentes IA
- **Organisation par Dossiers** : Organisez vos conversations par thématique
- **Vérification Croisée** : Améliorez la qualité avec la vérification entre IA
- **Interface Moderne** : UI intuitive et responsive

## 🚀 Installation

1. Clonez le repository
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez vos clés API :
```bash
cp .env.example .env
# Éditez .env avec vos clés API
```

4. Lancez l'application :
```bash
streamlit run app.py
```

## 🔑 Configuration des API

Vous aurez besoin de clés API pour :
- **OpenAI** (GPT-4, GPT-3.5) : https://platform.openai.com/api-keys
- **Anthropic** (Claude) : https://console.anthropic.com/
- **Google** (Gemini) : https://makersuite.google.com/app/apikey

## 📖 Utilisation

1. Sélectionnez une ou plusieurs IA dans la barre latérale
2. Choisissez un assistant spécialisé ou créez votre propre prompt
3. Posez vos questions et comparez les résultats
4. Organisez vos conversations dans des dossiers thématiques

## 🛠️ Technologies

- **Frontend** : Streamlit
- **Backend** : FastAPI
- **IA** : OpenAI, Anthropic, Google Gemini
- **Base de données** : SQLAlchemy

## 📝 Licence

MIT License - 2025 WeBox Multi-IA

## 🤝 Support

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.
