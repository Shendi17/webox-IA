# 🔑 CONFIGURATION DES CLÉS API IA

**Date** : 24 Novembre 2025  
**Statut** : ✅ INTÉGRATION TERMINÉE  

---

## 🎯 MODÈLES INTÉGRÉS

### **🔥 Derniers modèles (Recommandés)**
- ✅ **GPT-4o** (OpenAI) - Le plus récent et puissant
- ✅ **Claude 3.5 Sonnet** (Anthropic) - Le plus récent de Claude

### **OpenAI**
- ✅ GPT-4 Turbo
- ✅ GPT-4
- ✅ GPT-3.5 Turbo

### **Anthropic Claude**
- ✅ Claude 3 Opus
- ✅ Claude 3 Sonnet
- ✅ Claude 3 Haiku

### **Google**
- ✅ Gemini Pro

### **Mistral AI**
- ✅ Mistral Large
- ✅ Mistral Medium

---

## 📋 ÉTAPE 1 : INSTALLER LES PACKAGES

Ouvre PowerShell dans le dossier du projet et exécute :

```powershell
# Installer tous les packages IA
pip install openai anthropic google-generativeai mistralai

# Ou un par un :
pip install openai          # Pour GPT-4o, GPT-4, GPT-3.5
pip install anthropic       # Pour Claude 3.5 Sonnet, Claude 3
pip install google-generativeai  # Pour Gemini Pro
pip install mistralai       # Pour Mistral Large/Medium
```

---

## 🔑 ÉTAPE 2 : OBTENIR LES CLÉS API

### **OpenAI (GPT-4o, GPT-4)**

1. Va sur : https://platform.openai.com/api-keys
2. Connecte-toi ou crée un compte
3. Clique sur **"Create new secret key"**
4. Copie la clé (commence par `sk-...`)
5. **Important** : Ajoute des crédits (minimum 5$)

**Coût** :
- GPT-4o : ~$5 / 1M tokens input, ~$15 / 1M tokens output
- GPT-4 Turbo : ~$10 / 1M tokens
- GPT-3.5 Turbo : ~$0.50 / 1M tokens

---

### **Anthropic (Claude 3.5 Sonnet)**

1. Va sur : https://console.anthropic.com/
2. Crée un compte
3. Va dans **"API Keys"**
4. Clique sur **"Create Key"**
5. Copie la clé (commence par `sk-ant-...`)
6. Ajoute des crédits (minimum 5$)

**Coût** :
- Claude 3.5 Sonnet : ~$3 / 1M tokens input, ~$15 / 1M tokens output
- Claude 3 Opus : ~$15 / 1M tokens input, ~$75 / 1M tokens output
- Claude 3 Haiku : ~$0.25 / 1M tokens input, ~$1.25 / 1M tokens output

---

### **Google (Gemini Pro)**

1. Va sur : https://makersuite.google.com/app/apikey
2. Connecte-toi avec ton compte Google
3. Clique sur **"Get API Key"**
4. Copie la clé

**Coût** :
- Gemini Pro : **GRATUIT** jusqu'à 60 requêtes/minute

---

### **Mistral AI**

1. Va sur : https://console.mistral.ai/
2. Crée un compte
3. Va dans **"API Keys"**
4. Crée une nouvelle clé
5. Copie la clé

**Coût** :
- Mistral Large : ~$4 / 1M tokens
- Mistral Medium : ~$2.7 / 1M tokens

---

## ⚙️ ÉTAPE 3 : CONFIGURER LE FICHIER .env

Ouvre le fichier `.env` à la racine du projet et ajoute tes clés :

```env
# ============================================
# CLÉS API IA
# ============================================

# OpenAI (GPT-4o, GPT-4, GPT-3.5)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic (Claude 3.5 Sonnet, Claude 3)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google (Gemini Pro)
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Mistral AI (Mistral Large/Medium)
MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ IMPORTANT** :
- Remplace les `xxx` par tes vraies clés
- Ne partage JAMAIS ces clés
- Le fichier `.env` est dans `.gitignore` (non versionné)

---

## 🚀 ÉTAPE 4 : REDÉMARRER LE SERVEUR

Après avoir ajouté les clés, redémarre le serveur :

```powershell
# Arrête le serveur (Ctrl+C)

# Relance-le
python main.py
```

---

## ✅ ÉTAPE 5 : TESTER

1. **Ouvre l'éditeur**
   ```
   http://localhost:8000/projects/2/editor
   ```

2. **Ouvre le chat IA** (bouton 🤖)

3. **Sélectionne un modèle**
   - GPT-4o (Omni - Le plus récent)
   - Claude 3.5 Sonnet (Nouveau)

4. **Envoie un message**
   ```
   Bonjour ! Peux-tu m'aider à créer un bouton HTML avec CSS ?
   ```

5. **Vérifie la réponse**
   - Si tu vois une vraie réponse intelligente → ✅ Ça marche !
   - Si tu vois "⚠️ Clé API non configurée" → Vérifie le .env
   - Si tu vois "⚠️ Package non installé" → Installe le package

---

## 🔍 DÉPANNAGE

### **Erreur : "Clé API non configurée"**

**Cause** : La clé n'est pas dans le `.env` ou mal formatée

**Solution** :
1. Ouvre `.env`
2. Vérifie que la ligne commence par `OPENAI_API_KEY=` (pas d'espace)
3. Vérifie que la clé est complète
4. Redémarre le serveur

---

### **Erreur : "Package non installé"**

**Cause** : Le package Python n'est pas installé

**Solution** :
```powershell
pip install openai anthropic google-generativeai mistralai
```

---

### **Erreur : "Insufficient credits"**

**Cause** : Pas assez de crédits sur ton compte

**Solution** :
1. Va sur le site du provider (OpenAI, Anthropic, etc.)
2. Ajoute des crédits (minimum 5$)
3. Réessaye

---

### **Erreur : "Rate limit exceeded"**

**Cause** : Trop de requêtes en peu de temps

**Solution** :
- Attends quelques secondes
- Ou upgrade ton plan (plus de requêtes/minute)

---

## 💡 RECOMMANDATIONS

### **Pour débuter (Gratuit)**
1. ✅ **Gemini Pro** (Google) - GRATUIT, 60 req/min
2. Teste d'abord avec Gemini
3. Ensuite ajoute les autres si besoin

### **Pour la production**
1. ✅ **GPT-4o** - Le meilleur rapport qualité/prix
2. ✅ **Claude 3.5 Sonnet** - Excellent pour le code
3. ✅ **GPT-3.5 Turbo** - Rapide et économique

### **Budget mensuel estimé**

Pour **100 conversations/jour** (environ 3000/mois) :

| Modèle | Coût/conversation | Coût mensuel |
|--------|-------------------|--------------|
| GPT-4o | ~$0.02 | ~$60 |
| Claude 3.5 Sonnet | ~$0.015 | ~$45 |
| GPT-4 Turbo | ~$0.03 | ~$90 |
| GPT-3.5 Turbo | ~$0.002 | ~$6 |
| Gemini Pro | $0 | **GRATUIT** |

---

## 📊 COMPARAISON DES MODÈLES

| Modèle | Puissance | Vitesse | Coût | Code | Créativité |
|--------|-----------|---------|------|------|------------|
| **GPT-4o** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Claude 3.5 Sonnet** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-4 Turbo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰💰 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Claude 3 Opus | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 💰💰💰💰 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-3.5 Turbo | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 | ⭐⭐⭐ | ⭐⭐⭐ |
| Gemini Pro | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🆓 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎯 EXEMPLE DE .env COMPLET

```env
# ============================================
# CONFIGURATION WEBOX
# ============================================

# Base de données
DATABASE_URL=sqlite:///./webox.db

# Secret pour JWT
SECRET_KEY=votre_secret_key_super_securisee

# ============================================
# CLÉS API IA
# ============================================

# OpenAI (GPT-4o, GPT-4, GPT-3.5)
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# Anthropic (Claude 3.5 Sonnet, Claude 3)
ANTHROPIC_API_KEY=sk-ant-api03-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# Google (Gemini Pro) - GRATUIT
GOOGLE_API_KEY=AIzaSyABC123DEF456GHI789JKL012MNO345PQR678

# Mistral AI (Mistral Large/Medium)
MISTRAL_API_KEY=abc123def456ghi789jkl012mno345pqr678

# ============================================
# AUTRES SERVICES (Optionnel)
# ============================================

# Twilio (pour les appels vocaux)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# SendGrid (pour les emails)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ✅ RÉSUMÉ

```
┌────────────────────────────────────────┐
│   INTÉGRATION IA TERMINÉE ! 🎉         │
├────────────────────────────────────────┤
│ Modèles intégrés  : ✅ 11 modèles      │
│ GPT-4o            : ✅ Prêt            │
│ Claude 3.5 Sonnet : ✅ Prêt            │
│ Gemini Pro        : ✅ Gratuit         │
│ Code backend      : ✅ Fonctionnel     │
│ Interface         : ✅ Sélecteur OK    │
│                                        │
│ À FAIRE :                              │
│ 1. Installer packages (pip install)    │
│ 2. Obtenir clés API                    │
│ 3. Configurer .env                     │
│ 4. Redémarrer serveur                  │
│ 5. Tester ! 🚀                         │
└────────────────────────────────────────┘
```

---

## 🚀 PROCHAINE ÉTAPE

**Maintenant que l'intégration est terminée, tu dois :**

1. **Installer les packages**
   ```powershell
   pip install openai anthropic google-generativeai mistralai
   ```

2. **Obtenir au moins une clé API** (commence par Gemini Pro - gratuit)

3. **Ajouter la clé dans `.env`**

4. **Redémarrer et tester !**

---

**Veux-tu que je t'aide à tester avec Gemini Pro (gratuit) en premier ? 🤖**
