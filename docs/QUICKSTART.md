# ⚡ Démarrage Rapide - WeBox Multi-IA

Guide ultra-rapide pour démarrer avec WeBox Multi-IA en 5 minutes.

---

## 🚀 Installation Express (3 étapes)

### Étape 1 : Installer Python
Si vous n'avez pas Python, téléchargez-le depuis [python.org](https://www.python.org/downloads/)

Vérifiez l'installation :
```bash
python --version
```

### Étape 2 : Installer les Dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Configurer les Clés API
```bash
# Copiez le fichier d'exemple
cp .env.example .env

# Éditez .env et ajoutez vos clés API
# Vous pouvez commencer avec une seule clé API
```

---

## 🔑 Obtenir vos Clés API (5 minutes)

### Option 1 : OpenAI (Recommandé pour commencer)
1. Allez sur [platform.openai.com](https://platform.openai.com/)
2. Créez un compte
3. Allez dans "API Keys"
4. Créez une nouvelle clé
5. Copiez-la dans `.env` :
   ```
   OPENAI_API_KEY=sk-...
   ```

### Option 2 : Anthropic (Claude)
1. Allez sur [console.anthropic.com](https://console.anthropic.com/)
2. Créez un compte
3. Créez une clé API
4. Ajoutez-la dans `.env` :
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### Option 3 : Google AI (Gemini)
1. Allez sur [makersuite.google.com](https://makersuite.google.com/app/apikey)
2. Créez une clé API
3. Ajoutez-la dans `.env` :
   ```
   GOOGLE_API_KEY=AIza...
   ```

**💡 Astuce :** Vous pouvez commencer avec une seule IA et ajouter les autres plus tard !

---

## ▶️ Lancer l'Application

### Méthode 1 : Script PowerShell (Windows)
```bash
.\start.ps1
```

### Méthode 2 : Commande Directe
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## 🎯 Premier Test (1 minute)

### Test Simple
1. Sélectionnez une IA dans la barre latérale
2. Tapez dans le chat : "Bonjour, peux-tu te présenter ?"
3. Appuyez sur Entrée
4. ✅ Ça marche !

### Test Multi-IA
1. Sélectionnez 2 ou 3 IA
2. Posez une question : "Quels sont les avantages de l'IA pour les entreprises ?"
3. Comparez les réponses
4. 🎉 Vous utilisez le multi-IA !

---

## 📚 Premiers Pas

### 1. Essayer un Assistant
1. Allez dans "🎯 Assistants"
2. Cliquez sur "Rédacteur Marketing"
3. Retournez au "💬 Chat"
4. Demandez : "Rédige un slogan pour une startup tech"

### 2. Utiliser un Prompt Pré-fait
1. Allez dans "📚 Bibliothèque de Prompts"
2. Choisissez "Email de vente"
3. Cliquez sur "Utiliser"
4. Retournez au chat pour voir le résultat

### 3. Vérification Croisée
1. Posez une question technique
2. Recevez une réponse
3. Cliquez sur "🔍 Vérifier"
4. Une autre IA analysera la réponse

---

## 💡 Exemples Rapides à Tester

### Marketing
```
Crée un post LinkedIn sur l'importance de l'IA en 2025
```

### Code
```
Crée une fonction Python pour calculer la suite de Fibonacci
```

### Analyse
```
Analyse SWOT d'une startup de livraison de repas
```

### Créativité
```
Propose 5 noms créatifs pour une application de méditation
```

---

## 🎨 Personnalisation Rapide

### Changer la Température
- **0.0-0.3** : Réponses précises (code, traduction)
- **0.4-0.7** : Équilibré (usage général)
- **0.8-1.0** : Créatif (brainstorming)

### Ajuster les Tokens
- **500-1000** : Réponses courtes
- **1000-2000** : Réponses moyennes (recommandé)
- **2000-4000** : Réponses longues

---

## 🐛 Problèmes Courants

### "Aucune IA configurée"
**Solution :** Vérifiez votre fichier `.env` et vos clés API

### "Module not found"
**Solution :**
```bash
pip install -r requirements.txt --force-reinstall
```

### "Port already in use"
**Solution :**
```bash
streamlit run app.py --server.port 8502
```

### L'application ne s'ouvre pas
**Solution :** Ouvrez manuellement `http://localhost:8501` dans votre navigateur

---

## 📖 Ressources

- **Guide Complet** : Consultez `GUIDE_UTILISATION.md`
- **Exemples** : Consultez `EXEMPLES.md`
- **Support** : Ouvrez une issue sur GitHub

---

## 🎯 Prochaines Étapes

1. ✅ Testez les différentes IA
2. ✅ Explorez les assistants
3. ✅ Créez vos propres prompts
4. ✅ Organisez vos conversations en dossiers
5. ✅ Utilisez la vérification croisée

---

## 🚀 Cas d'Usage Populaires

### Pour Entrepreneurs
- Rédaction de contenu marketing
- Analyse de marché
- Planification stratégique

### Pour Développeurs
- Génération de code
- Revue de code
- Documentation

### Pour Créatifs
- Brainstorming d'idées
- Rédaction de contenu
- Naming et branding

### Pour Étudiants
- Aide aux devoirs
- Résumés de cours
- Apprentissage de concepts

---

## 💪 Conseils Pro

1. **Commencez simple** : Une question à la fois
2. **Soyez précis** : Plus le prompt est détaillé, meilleure est la réponse
3. **Comparez** : Utilisez plusieurs IA pour avoir différentes perspectives
4. **Itérez** : Affinez vos questions progressivement
5. **Organisez** : Créez des dossiers pour vos différents projets

---

## 🎉 Vous êtes Prêt !

Vous avez maintenant tout ce qu'il faut pour utiliser WeBox Multi-IA efficacement.

**Besoin d'aide ?**
- 📖 Consultez le guide complet : `GUIDE_UTILISATION.md`
- 💡 Voir des exemples : `EXEMPLES.md`
- 🐛 Signaler un bug : Ouvrez une issue

**Bon usage ! 🚀**

---

## ⏱️ Récapitulatif 5 Minutes

```bash
# 1. Installer (1 min)
pip install -r requirements.txt

# 2. Configurer (2 min)
cp .env.example .env
# Éditez .env avec votre clé API

# 3. Lancer (30 sec)
streamlit run app.py

# 4. Tester (1 min 30)
# Sélectionnez une IA
# Posez une question
# ✅ C'est parti !
```

**Total : 5 minutes pour être opérationnel ! ⚡**
