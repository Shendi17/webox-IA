# 🔑 GUIDE DE CONFIGURATION DES CLÉS API

**Date:** 24 Janvier 2026  
**Objectif:** Configurer toutes les clés API nécessaires pour WeBox

---

## 📋 TABLE DES MATIÈRES

1. [Paiements (Stripe & PayPal)](#paiements)
2. [Intelligence Artificielle](#intelligence-artificielle)
3. [Génération Média](#génération-média)
4. [Configuration du fichier .env](#configuration-env)
5. [Vérification](#vérification)

---

## 💳 PAIEMENTS

### Stripe

#### 1. Créer un compte Stripe
- Aller sur https://stripe.com
- Créer un compte (gratuit)
- Activer le mode Test

#### 2. Récupérer les clés API
1. Aller dans **Développeurs** > **Clés API**
2. Copier les clés suivantes :
   - **Clé publiable** (commence par `pk_test_`)
   - **Clé secrète** (commence par `sk_test_`)

#### 3. Configurer le webhook
1. Aller dans **Développeurs** > **Webhooks**
2. Cliquer sur **Ajouter un endpoint**
3. URL du webhook : `https://votre-domaine.com/api/payment/stripe/webhook`
4. Sélectionner les événements :
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Copier la **Clé de signature du webhook** (commence par `whsec_`)

#### Variables .env
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

### PayPal

#### 1. Créer un compte développeur PayPal
- Aller sur https://developer.paypal.com
- Se connecter ou créer un compte
- Aller dans **Dashboard**

#### 2. Créer une application
1. Cliquer sur **My Apps & Credentials**
2. Cliquer sur **Create App**
3. Nom de l'app : `WeBox`
4. Type : **Merchant**

#### 3. Récupérer les clés
Dans l'onglet **Sandbox** :
- **Client ID** (commence par `A...`)
- **Secret** (cliquer sur "Show" pour voir)

#### Variables .env
```env
PAYPAL_CLIENT_ID=AZaQ...
PAYPAL_CLIENT_SECRET=EL...
PAYPAL_MODE=sandbox
```

> **Note:** Pour la production, utiliser les clés de l'onglet **Live** et mettre `PAYPAL_MODE=live`

---

## 🤖 INTELLIGENCE ARTIFICIELLE

### OpenAI (GPT-4, DALL-E)

#### 1. Créer un compte OpenAI
- Aller sur https://platform.openai.com
- Créer un compte
- Ajouter un moyen de paiement (requis)

#### 2. Récupérer la clé API
1. Aller dans **API Keys**
2. Cliquer sur **Create new secret key**
3. Copier la clé (commence par `sk-`)

> ⚠️ **Important:** La clé n'est affichée qu'une seule fois !

#### Variables .env
```env
OPENAI_API_KEY=sk-proj-...
```

#### Tarifs (approximatifs)
- GPT-4: ~$0.03 / 1K tokens
- GPT-3.5-Turbo: ~$0.002 / 1K tokens
- DALL-E 3: $0.04 - $0.12 par image

---

### Anthropic (Claude)

#### 1. Créer un compte Anthropic
- Aller sur https://console.anthropic.com
- Créer un compte
- Ajouter un moyen de paiement

#### 2. Récupérer la clé API
1. Aller dans **API Keys**
2. Cliquer sur **Create Key**
3. Copier la clé (commence par `sk-ant-`)

#### Variables .env
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

#### Tarifs
- Claude 3 Opus: ~$0.015 / 1K tokens
- Claude 3 Sonnet: ~$0.003 / 1K tokens

---

### Google (Gemini)

#### 1. Créer un projet Google Cloud
- Aller sur https://console.cloud.google.com
- Créer un nouveau projet

#### 2. Activer l'API Gemini
1. Aller dans **APIs & Services** > **Library**
2. Rechercher "Generative Language API"
3. Cliquer sur **Enable**

#### 3. Créer une clé API
1. Aller dans **APIs & Services** > **Credentials**
2. Cliquer sur **Create Credentials** > **API Key**
3. Copier la clé (commence par `AIza`)

#### Variables .env
```env
GOOGLE_API_KEY=AIzaSy...
```

#### Tarifs
- Gemini Pro: Gratuit jusqu'à 60 requêtes/minute
- Gemini Pro Vision: Gratuit jusqu'à 60 requêtes/minute

---

### Mistral AI

#### 1. Créer un compte Mistral
- Aller sur https://console.mistral.ai
- Créer un compte

#### 2. Récupérer la clé API
1. Aller dans **API Keys**
2. Créer une nouvelle clé
3. Copier la clé

#### Variables .env
```env
MISTRAL_API_KEY=...
```

---

### Groq

#### 1. Créer un compte Groq
- Aller sur https://console.groq.com
- Créer un compte

#### 2. Récupérer la clé API
1. Aller dans **API Keys**
2. Créer une nouvelle clé (commence par `gsk_`)
3. Copier la clé

#### Variables .env
```env
GROQ_API_KEY=gsk_...
```

#### Avantages
- **Très rapide** (inférence ultra-rapide)
- **Gratuit** pour l'instant (quota généreux)

---

## 🎨 GÉNÉRATION MÉDIA

### Stability AI (Stable Diffusion)

#### 1. Créer un compte
- Aller sur https://platform.stability.ai
- Créer un compte

#### 2. Récupérer la clé API
1. Aller dans **Account** > **API Keys**
2. Créer une nouvelle clé (commence par `sk-`)
3. Copier la clé

#### Variables .env
```env
STABILITY_API_KEY=sk-...
```

---

### ElevenLabs (Voix)

#### 1. Créer un compte
- Aller sur https://elevenlabs.io
- Créer un compte

#### 2. Récupérer la clé API
1. Aller dans **Profile** > **API Keys**
2. Copier la clé

#### Variables .env
```env
ELEVENLABS_API_KEY=...
```

---

### Runway ML (Vidéo)

#### 1. Créer un compte
- Aller sur https://runwayml.com
- Créer un compte

#### 2. Accéder à l'API
- Contacter le support pour accès API (en beta)

#### Variables .env
```env
RUNWAY_API_KEY=...
```

---

## ⚙️ CONFIGURATION .ENV

### Créer le fichier .env

Créer un fichier `.env` à la racine du projet avec toutes les clés :

```env
# ==========================================
# BASE DE DONNÉES
# ==========================================
DATABASE_URL=postgresql://user:password@localhost:5432/webox

# ==========================================
# SÉCURITÉ
# ==========================================
JWT_SECRET_KEY=votre_secret_key_tres_longue_et_aleatoire
ENCRYPTION_KEY=votre_encryption_key_32_caracteres

# ==========================================
# PAIEMENTS
# ==========================================

# Stripe (Test)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PayPal (Sandbox)
PAYPAL_CLIENT_ID=AZaQ...
PAYPAL_CLIENT_SECRET=EL...
PAYPAL_MODE=sandbox

# ==========================================
# INTELLIGENCE ARTIFICIELLE
# ==========================================

# OpenAI (GPT-4, DALL-E)
OPENAI_API_KEY=sk-proj-...

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Google (Gemini)
GOOGLE_API_KEY=AIzaSy...

# Mistral AI
MISTRAL_API_KEY=...

# Groq
GROQ_API_KEY=gsk_...

# ==========================================
# GÉNÉRATION MÉDIA
# ==========================================

# Stability AI (Stable Diffusion)
STABILITY_API_KEY=sk-...

# ElevenLabs (Voix)
ELEVENLABS_API_KEY=...

# Runway ML (Vidéo)
RUNWAY_API_KEY=...

# ==========================================
# EMAIL (Optionnel)
# ==========================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-app
```

### Sécurité

⚠️ **IMPORTANT:**
- Ne **JAMAIS** commiter le fichier `.env` dans Git
- Vérifier que `.env` est dans `.gitignore`
- Utiliser des clés de test en développement
- Utiliser des clés de production uniquement en production

---

## ✅ VÉRIFICATION

### Script de vérification

Créer un fichier `check_env.py` :

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("\n🔍 VÉRIFICATION DES CLÉS API\n")
print("="*60)

keys = {
    "Paiements": {
        "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY"),
        "STRIPE_PUBLISHABLE_KEY": os.getenv("STRIPE_PUBLISHABLE_KEY"),
        "PAYPAL_CLIENT_ID": os.getenv("PAYPAL_CLIENT_ID"),
    },
    "IA - Texte": {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    },
    "IA - Média": {
        "STABILITY_API_KEY": os.getenv("STABILITY_API_KEY"),
        "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY"),
    }
}

for category, category_keys in keys.items():
    print(f"\n{category}")
    print("-"*60)
    for key_name, key_value in category_keys.items():
        if key_value:
            masked = f"{key_value[:8]}...{key_value[-4:]}" if len(key_value) > 12 else "****"
            print(f"✅ {key_name}: {masked}")
        else:
            print(f"❌ {key_name}: NON CONFIGURÉ")

print("\n" + "="*60)
```

Exécuter :
```bash
python check_env.py
```

---

## 📊 PRIORITÉS DE CONFIGURATION

### 🔴 PRIORITÉ HAUTE (Fonctionnalités critiques)

1. **OpenAI** - Pour chat GPT-4 et génération images DALL-E
2. **Stripe** - Pour les paiements
3. **Base de données** - PostgreSQL

### 🟡 PRIORITÉ MOYENNE (Fonctionnalités importantes)

4. **Anthropic** - Pour chat Claude
5. **Google** - Pour chat Gemini
6. **PayPal** - Alternative de paiement
7. **Groq** - Chat ultra-rapide

### 🟢 PRIORITÉ BASSE (Fonctionnalités avancées)

8. **Mistral** - Chat alternatif
9. **Stability AI** - Génération images alternatives
10. **ElevenLabs** - Génération voix
11. **Runway ML** - Génération vidéo

---

## 🚀 DÉMARRAGE RAPIDE

### Configuration minimale pour démarrer

```env
# Minimum requis
DATABASE_URL=postgresql://user:password@localhost:5432/webox
JWT_SECRET_KEY=changez_moi_en_production
OPENAI_API_KEY=sk-proj-...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Avec cette configuration minimale, vous pouvez :
- ✅ Utiliser le chat GPT-4
- ✅ Générer des images DALL-E
- ✅ Accepter des paiements Stripe
- ✅ Gérer les utilisateurs

---

## 📞 SUPPORT

### Problèmes courants

**Erreur "API Key not found"**
- Vérifier que le fichier `.env` existe
- Vérifier que `python-dotenv` est installé
- Redémarrer le serveur après modification du `.env`

**Erreur "Invalid API Key"**
- Vérifier que la clé est correcte (pas d'espaces)
- Vérifier que la clé n'a pas expiré
- Vérifier que le compte a du crédit

**Erreur "Rate limit exceeded"**
- Attendre quelques minutes
- Vérifier les quotas de l'API
- Passer à un plan payant si nécessaire

---

## 📚 RESSOURCES

- [Documentation Stripe](https://stripe.com/docs)
- [Documentation PayPal](https://developer.paypal.com/docs)
- [Documentation OpenAI](https://platform.openai.com/docs)
- [Documentation Anthropic](https://docs.anthropic.com)
- [Documentation Google AI](https://ai.google.dev/docs)
- [Documentation Groq](https://console.groq.com/docs)

---

**Dernière mise à jour:** 24 Janvier 2026
