# 📖 Guide d'Utilisation - WeBox Multi-IA

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier de configuration
cp .env.example .env
```

### 2. Configuration des Clés API

Éditez le fichier `.env` et ajoutez vos clés API :

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

### 3. Lancement de l'Application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

---

## 🎯 Fonctionnalités Principales

### 💬 Chat Multi-IA

**Utilisation :**
1. Sélectionnez une ou plusieurs IA dans la barre latérale
2. Choisissez le modèle pour chaque IA
3. Posez votre question dans le chat
4. Comparez les réponses de chaque IA côte à côte

**Avantages :**
- Obtenez plusieurs perspectives sur la même question
- Identifiez les réponses les plus pertinentes
- Vérifiez la cohérence des informations

**Exemple d'utilisation :**
```
Question : "Comment améliorer le SEO de mon site web ?"

Vous obtiendrez des réponses de :
- GPT-4 : Approche technique et détaillée
- Claude : Approche stratégique et structurée
- Gemini : Approche pratique avec exemples
```

---

### 🎯 Assistants Spécialisés

Les assistants sont pré-configurés pour des tâches spécifiques :

#### 📝 Rédacteur Marketing
- **Utilisation :** Création de contenu marketing, publicités, emails
- **Exemple :** "Rédige un email de lancement pour mon nouveau produit"

#### 💻 Développeur
- **Utilisation :** Aide au code, debugging, architecture
- **Exemple :** "Crée une fonction Python pour valider des emails"

#### 📊 Analyste Business
- **Utilisation :** Analyse de données, stratégie, KPIs
- **Exemple :** "Analyse ces données de ventes et propose des recommandations"

#### 🎯 Coach Personnel
- **Utilisation :** Développement personnel, objectifs, motivation
- **Exemple :** "Aide-moi à définir mes objectifs professionnels pour 2025"

#### 🌍 Traducteur
- **Utilisation :** Traduction professionnelle multilingue
- **Exemple :** "Traduis ce texte en anglais, espagnol et allemand"

#### 💡 Créatif
- **Utilisation :** Brainstorming, idées innovantes, concepts
- **Exemple :** "Propose 10 idées de noms pour ma startup"

---

### 📚 Bibliothèque de Prompts

**Prompts pré-configurés par catégorie :**

#### Marketing
- Email de vente
- Post LinkedIn
- Page de vente
- Campagne publicitaire

#### Productivité
- Planification de projet
- Résumé de réunion
- To-do list intelligente

#### Développement
- Revue de code
- Documentation
- Tests unitaires

#### Analyse
- Analyse SWOT
- Étude de marché
- Analyse de données

**Comment utiliser un prompt :**
1. Allez dans "📚 Bibliothèque de Prompts"
2. Sélectionnez une catégorie
3. Cliquez sur le prompt souhaité
4. Cliquez sur "Utiliser"
5. Le prompt est ajouté au chat

**Créer un prompt personnalisé :**
1. Descendez en bas de la page
2. Remplissez le formulaire :
   - Nom du prompt
   - Catégorie
   - Contenu
3. Cliquez sur "Créer le prompt"

---

### 🔍 Vérification Croisée

**Qu'est-ce que c'est ?**
La vérification croisée permet de faire analyser une réponse par une autre IA pour :
- Vérifier la précision des informations
- Identifier les erreurs potentielles
- Obtenir des suggestions d'amélioration

**Comment l'utiliser :**
1. Après avoir reçu une réponse dans le chat
2. Cliquez sur "🔍 Vérifier" en bas de page
3. Une autre IA analysera la réponse et fournira un feedback

**Exemple :**
```
Question : "Explique-moi la blockchain"
Réponse de GPT-4 : [explication détaillée]

Vérification par Claude :
✅ Points corrects : [liste]
⚠️ Points à clarifier : [liste]
💡 Suggestions : [liste]
```

---

### 📁 Organisation par Dossiers

**Créer un dossier :**
1. Dans la barre latérale, cliquez sur "➕ Nouveau dossier"
2. Entrez le nom du dossier
3. Cliquez sur "Créer"

**Organiser vos conversations :**
- Marketing
- Développement
- Personnel
- Projets clients
- Recherche
- etc.

**Créer une nouvelle conversation :**
1. Cliquez sur "➕ Nouvelle conversation"
2. Choisissez le dossier
3. Donnez un nom à la conversation
4. Commencez à discuter

---

## ⚙️ Paramètres Avancés

### Température (0.0 - 1.0)
- **0.0 - 0.3 :** Réponses précises et déterministes (idéal pour code, traduction)
- **0.4 - 0.7 :** Équilibré (usage général)
- **0.8 - 1.0 :** Créatif et varié (idéal pour brainstorming, écriture créative)

### Tokens Maximum
- **500 - 1000 :** Réponses courtes et concises
- **1000 - 2000 :** Réponses moyennes (recommandé)
- **2000 - 4000 :** Réponses longues et détaillées

---

## 💡 Cas d'Usage Pratiques

### 1. Rédaction de Contenu
```
Sélectionnez : Rédacteur Marketing
Prompt : "Rédige un article de blog de 800 mots sur [sujet]"
Comparez les styles de GPT-4 et Claude
```

### 2. Développement de Code
```
Sélectionnez : Développeur
Prompt : "Crée une API REST en Python avec FastAPI pour [fonctionnalité]"
Vérifiez le code avec plusieurs IA
```

### 3. Analyse Stratégique
```
Sélectionnez : Analyste Business
Prompt : "Analyse SWOT de mon entreprise dans le secteur [X]"
Comparez les analyses de différentes IA
```

### 4. Apprentissage
```
Prompt : "Explique-moi [concept complexe] comme si j'avais 10 ans"
Comparez les explications pour trouver la plus claire
```

### 5. Traduction Professionnelle
```
Sélectionnez : Traducteur
Prompt : "Traduis ce texte en [langue] en conservant le ton professionnel"
Vérifiez la qualité avec plusieurs IA
```

---

## 🎓 Bonnes Pratiques

### Rédaction de Prompts Efficaces

**✅ À FAIRE :**
- Soyez spécifique et précis
- Donnez du contexte
- Indiquez le format souhaité
- Précisez le ton et le style
- Donnez des exemples si nécessaire

**❌ À ÉVITER :**
- Prompts trop vagues
- Questions multiples en une
- Manque de contexte
- Instructions contradictoires

### Exemples de Bons Prompts

**Mauvais :**
```
"Écris quelque chose sur le marketing"
```

**Bon :**
```
"Rédige un guide pratique de 500 mots sur le marketing digital 
pour les petites entreprises. Inclus 5 stratégies concrètes avec 
des exemples. Ton professionnel mais accessible."
```

---

## 🔒 Sécurité et Confidentialité

### Protection des Clés API
- Ne partagez JAMAIS vos clés API
- Utilisez le fichier `.env` (non versionné)
- Régénérez vos clés si elles sont compromises

### Données Sensibles
- Ne partagez pas d'informations confidentielles
- Les conversations sont stockées localement
- Vérifiez les politiques de confidentialité des fournisseurs d'IA

---

## 🆘 Dépannage

### "Aucune IA configurée"
**Solution :** Vérifiez que vos clés API sont correctement configurées dans le fichier `.env`

### "Erreur API"
**Solutions :**
- Vérifiez votre connexion internet
- Vérifiez que vos clés API sont valides
- Vérifiez votre quota/crédit API

### L'application ne démarre pas
**Solutions :**
```bash
# Réinstallez les dépendances
pip install -r requirements.txt --force-reinstall

# Vérifiez la version de Python (3.8+)
python --version

# Lancez en mode debug
streamlit run app.py --logger.level=debug
```

---

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation
2. Vérifiez les issues GitHub
3. Contactez le support

---

## 🎉 Astuces et Raccourcis

- **Ctrl + K** : Focus sur le chat
- **Ctrl + /** : Nouvelle conversation
- **Ctrl + Shift + C** : Copier la dernière réponse
- Utilisez les flèches ↑↓ pour naviguer dans l'historique

---

**Bon usage de WeBox Multi-IA ! 🚀**
