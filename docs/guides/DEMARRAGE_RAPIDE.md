# 🚀 Démarrage Rapide - WeBox Multi-IA

## ⚡ En 3 Étapes

### **1. Configurer les APIs** (2 minutes)

```bash
# Copier le fichier de configuration
copy .env.example .env
```

Ouvrir `.env` et ajouter **au minimum** :

```env
OPENAI_API_KEY=sk-votre-clé-ici
```

> 💡 **Astuce:** Commencez avec juste OpenAI, ajoutez les autres progressivement

---

### **2. Installer les dépendances** (1 minute)

```bash
pip install -r requirements.txt
```

---

### **3. Lancer l'application** (10 secondes)

```bash
# Option 1: Script Windows
scripts\LANCER-WEBOX.bat

# Option 2: Direct
streamlit run app.py
```

**Accès:** http://localhost:8501

**Identifiants par défaut:**
- Email: `admin@webox.com`
- Mot de passe: `admin123`

---

## 🎯 Configurations Rapides

### **🆓 Configuration Gratuite (0€)**

```env
GOOGLE_API_KEY=votre-clé        # Gemini Pro - GRATUIT
GROQ_API_KEY=votre-clé          # Llama 3 - GRATUIT
SERPER_API_KEY=votre-clé        # Recherche - GRATUIT
```

**Fonctionnalités:**
- ✅ Chat avec Gemini Pro
- ✅ Recherche web
- ✅ Modèles rapides (Groq)

---

### **💵 Configuration Basique (5€/mois)**

```env
OPENAI_API_KEY=votre-clé        # GPT-3.5 + DALL-E
GOOGLE_API_KEY=votre-clé        # Gemini - GRATUIT
```

**Fonctionnalités:**
- ✅ Tout le gratuit
- ✅ GPT-3.5 Turbo
- ✅ Génération d'images (DALL-E)
- ✅ Agents IA

---

### **💎 Configuration Standard (30€/mois)**

```env
OPENAI_API_KEY=votre-clé        # GPT-4 + DALL-E
ANTHROPIC_API_KEY=votre-clé     # Claude 3
GOOGLE_API_KEY=votre-clé        # Gemini
STABILITY_API_KEY=votre-clé     # Stable Diffusion
ELEVENLABS_API_KEY=votre-clé    # Voix réalistes
```

**Fonctionnalités:**
- ✅ Tout le basique
- ✅ GPT-4
- ✅ Claude 3
- ✅ Génération d'images HD
- ✅ Voix ultra-réalistes

---

### **🚀 Configuration Complète (100€/mois)**

Toutes les APIs activées

**Fonctionnalités:**
- ✅ Toutes les fonctionnalités
- ✅ Assistant Vocal
- ✅ Génération vidéo
- ✅ Automatisations

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Documentation principale |
| `CONFIGURATION_API.md` | Guide de configuration |
| `docs/GUIDE_OBTENTION_CLES_API.md` | Comment obtenir les clés |
| `STRUCTURE_PROJET.md` | Structure du projet |

---

## 🎯 Fonctionnalités Principales

### **💬 Chat Multi-IA**
Discutez avec 12+ IA différentes

### **🤖 Agents IA Spécialisés**
8 agents experts (Ventes, Marketing, Finance, etc.)

### **📞 Assistant Vocal**
Appels téléphoniques automatisés

### **🎨 Génération de Médias**
Images, Audio, Vidéo

### **🔧 Catalogue IA**
50+ outils IA catalogués

---

## 🆘 Problèmes Courants

### **Erreur: Module not found**
```bash
pip install -r requirements.txt
```

### **Erreur: Invalid API key**
Vérifiez que votre clé est correctement copiée dans `.env`

### **Port déjà utilisé**
```bash
streamlit run app.py --server.port 8502
```

---

## 📞 Support

- **Documentation:** Dossier `docs/`
- **Configuration:** `CONFIGURATION_API.md`
- **Structure:** `STRUCTURE_PROJET.md`

---

**🎉 Vous êtes prêt ! Lancez WeBox et explorez les fonctionnalités ! 🚀**
