# ⚙️ Configuration des APIs - WeBox Multi-IA

## 🎯 Démarrage Rapide

### **Étape 1: Copier le fichier de configuration**

```bash
# Copier .env.example vers .env
copy .env.example .env
```

### **Étape 2: Remplir les clés essentielles**

Ouvrir `.env` et remplir au minimum:

```env
# MINIMUM REQUIS pour démarrer
OPENAI_API_KEY=sk-votre-clé-ici
```

### **Étape 3: Lancer l'application**

```bash
streamlit run app.py
```

---

## 📋 Liste des APIs par Catégorie

### **🤖 IA Conversationnelles (13 APIs)**

| API | Statut | Priorité | Coût |
|-----|--------|----------|------|
| OpenAI | ⭐ REQUIS | 1 | Variable |
| Anthropic Claude | 🌟 Recommandé | 2 | Variable |
| Google Gemini | 🌟 Recommandé | 3 | GRATUIT |
| Mistral AI | ⚪ Optionnel | - | Variable |
| Cohere | ⚪ Optionnel | - | Gratuit limité |
| Perplexity | ⚪ Optionnel | - | Variable |
| DeepSeek | ⚪ Optionnel | - | Variable |
| Groq | ⚪ Optionnel | - | Gratuit beta |
| Together AI | ⚪ Optionnel | - | Variable |
| Replicate | ⚪ Optionnel | - | Pay-per-use |
| Hugging Face | ⚪ Optionnel | - | Gratuit |
| xAI (Grok) | ⚪ Optionnel | - | À venir |

### **🎨 Génération d'Images (4 APIs)**

| API | Statut | Priorité | Coût |
|-----|--------|----------|------|
| Stability AI | 🌟 Recommandé | 6 | ~0.02$/image |
| Midjourney | ⚪ Optionnel | - | Via Discord |
| Leonardo AI | ⚪ Optionnel | - | Crédits |
| Ideogram | ⚪ Optionnel | - | Variable |

### **🎙️ Génération Audio (5 APIs)**

| API | Statut | Priorité | Coût |
|-----|--------|----------|------|
| ElevenLabs | 🌟 Recommandé | 7 | 10K gratuits/mois |
| Play.ht | ⚪ Optionnel | - | Variable |
| Murf AI | ⚪ Optionnel | - | Abonnement |
| Suno AI | ⚪ Optionnel | - | À venir |
| Udio | ⚪ Optionnel | - | À venir |

### **🎬 Génération Vidéo (5 APIs)**

| API | Statut | Priorité | Coût |
|-----|--------|----------|------|
| Runway ML | 🌟 Recommandé | 8 | Crédits |
| Pika Labs | ⚪ Optionnel | - | À venir |
| Synthesia | ⚪ Optionnel | - | Abonnement |
| D-ID | ⚪ Optionnel | - | Pay-per-use |
| HeyGen | ⚪ Optionnel | - | Crédits |

### **📞 Assistant Vocal (2 APIs)**

| API | Statut | Priorité | Coût |
|-----|--------|----------|------|
| Twilio | ⭐ REQUIS (vocal) | 4 | ~0.01€/min |
| Google Cloud | ⭐ REQUIS (vocal) | 5 | ~0.006$/min |

### **🔧 Outils Spécialisés (7 APIs)**

| API | Statut | Coût |
|-----|--------|------|
| Pinecone | ⚪ Optionnel | Gratuit (1 index) |
| Weaviate | ⚪ Optionnel | Variable |
| Langchain Smith | ⚪ Optionnel | Gratuit limité |
| Zapier | ⚪ Optionnel | Selon plan |
| Make | ⚪ Optionnel | Selon plan |
| Airtable | ⚪ Optionnel | Gratuit base |
| Notion | ⚪ Optionnel | Gratuit |

### **🔍 Recherche & Analyse (4 APIs)**

| API | Statut | Coût |
|-----|--------|------|
| Serper | 🌟 Recommandé | 2500 gratuits |
| SerpAPI | ⚪ Optionnel | 100 gratuits/mois |
| Brave Search | ⚪ Optionnel | 2000 gratuits/mois |
| Wolfram Alpha | ⚪ Optionnel | 2000 gratuits/mois |

### **💻 Code & Développement (3 APIs)**

| API | Statut | Coût |
|-----|--------|------|
| GitHub | ⚪ Optionnel | Gratuit (public) |
| Replit | ⚪ Optionnel | Variable |
| CodeSandbox | ⚪ Optionnel | Gratuit base |

### **📊 Analytics (3 APIs)**

| API | Statut | Coût |
|-----|--------|------|
| Sentry | ⚪ Optionnel | 5K gratuits/mois |
| Mixpanel | ⚪ Optionnel | 100K gratuits/mois |
| PostHog | ⚪ Optionnel | 1M gratuits/mois |

---

## 📊 Total: 50+ APIs Disponibles

- ⭐ **REQUIS:** 1 (OpenAI)
- 🌟 **Recommandé:** 6
- ⚪ **Optionnel:** 43+

---

## 💰 Budgets Recommandés

### **🆓 Configuration Gratuite (0€/mois)**
```env
GOOGLE_API_KEY=votre-clé        # Gemini Pro - GRATUIT
SERPER_API_KEY=votre-clé        # 2500 recherches gratuites
BRAVE_SEARCH_API_KEY=votre-clé  # 2000 recherches gratuites
```

### **💵 Configuration Basique (5-10€/mois)**
```env
OPENAI_API_KEY=votre-clé        # GPT-3.5 - ~5€
GOOGLE_API_KEY=votre-clé        # Gemini - GRATUIT
```

### **💎 Configuration Standard (30-50€/mois)**
```env
OPENAI_API_KEY=votre-clé        # GPT-4 + DALL-E - ~20€
ANTHROPIC_API_KEY=votre-clé     # Claude 3 - ~10€
GOOGLE_API_KEY=votre-clé        # Gemini - GRATUIT
STABILITY_API_KEY=votre-clé     # Images - ~10€
```

### **🚀 Configuration Complète (100€+/mois)**
Toutes les APIs activées pour fonctionnalités maximales

---

## 🎯 Configuration par Fonctionnalité

### **Pour le Chat Multi-IA uniquement**
```env
OPENAI_API_KEY=votre-clé
ANTHROPIC_API_KEY=votre-clé
GOOGLE_API_KEY=votre-clé
```

### **Pour les Agents IA**
```env
OPENAI_API_KEY=votre-clé        # REQUIS
```

### **Pour l'Assistant Vocal**
```env
OPENAI_API_KEY=votre-clé                    # REQUIS
TWILIO_ACCOUNT_SID=votre-sid                # REQUIS
TWILIO_AUTH_TOKEN=votre-token               # REQUIS
TWILIO_PHONE_NUMBER=+33123456789            # REQUIS
GOOGLE_APPLICATION_CREDENTIALS=chemin.json  # REQUIS
```

### **Pour la Génération d'Images**
```env
OPENAI_API_KEY=votre-clé        # DALL-E
STABILITY_API_KEY=votre-clé     # Stable Diffusion
```

### **Pour la Génération Audio**
```env
OPENAI_API_KEY=votre-clé        # OpenAI TTS
ELEVENLABS_API_KEY=votre-clé    # ElevenLabs
```

### **Pour la Génération Vidéo**
```env
RUNWAY_API_KEY=votre-clé        # Runway ML
```

---

## 📝 Fichiers de Configuration

### **`.env.example`**
- Template avec toutes les APIs disponibles
- Commentaires détaillés
- Liens vers les plateformes
- Coûts estimés

### **`.env`** (à créer)
- Vos vraies clés API
- **JAMAIS** commité dans Git
- Copie de `.env.example`

### **`.gitignore`**
- Contient `.env` pour éviter les commits accidentels

---

## 🔐 Sécurité

### **Bonnes Pratiques**

✅ **À FAIRE:**
- Utiliser `.env` pour les clés
- Copier `.env.example` vers `.env`
- Ajouter `.env` au `.gitignore`
- Régénérer les clés si compromises
- Configurer des limites de dépenses

❌ **À NE PAS FAIRE:**
- Commiter `.env` dans Git
- Partager vos clés API
- Utiliser les mêmes clés en dev/prod
- Laisser des clés dans le code

---

## 🆘 Aide

### **Documentation Complète**
📖 `docs/GUIDE_OBTENTION_CLES_API.md` - Guide détaillé pour chaque API

### **Support**
- Voir `README.md`
- Consulter la documentation dans `docs/`

---

## ✅ Checklist de Configuration

### **Démarrage Minimum**
- [ ] Fichier `.env` créé
- [ ] `OPENAI_API_KEY` configurée
- [ ] Application testée

### **Configuration Recommandée**
- [ ] `ANTHROPIC_API_KEY` ajoutée
- [ ] `GOOGLE_API_KEY` ajoutée
- [ ] Toutes les clés testées

### **Configuration Complète**
- [ ] Assistant Vocal configuré (Twilio + Google Cloud)
- [ ] Génération d'images configurée
- [ ] Génération audio configurée
- [ ] Tous les modules testés

---

**⚙️ Configurez vos APIs au fur et à mesure selon vos besoins ! 🚀**

**Commencez avec OpenAI, puis ajoutez les autres progressivement.**
