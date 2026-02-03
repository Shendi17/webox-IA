# 📋 MODÈLES DEEPSEEK ET GROQ DISPONIBLES SUR WEBOX

**Date:** 17 Janvier 2026  
**Statut:** ✅ Testé et configuré

---

## ✅ DEEPSEEK - 2 MODÈLES DISPONIBLES

### **Test de connexion:**
- ✅ Clé API valide
- ✅ 2 modèles disponibles
- ⚠️ **Erreur 402 - Insufficient Balance** (Pas de crédits)

---

### **Modèles DeepSeek disponibles**

| Modèle | Description | Statut |
|--------|-------------|--------|
| `deepseek-chat` | Chat équilibré | ⚠️ Nécessite crédits |
| `deepseek-reasoner` | Raisonnement avancé 🧠 | ⚠️ Nécessite crédits |

**Note:** Votre compte DeepSeek n'a pas de crédits disponibles. Vous devez recharger votre compte pour utiliser ces modèles.

---

## ✅ GROQ - 20 MODÈLES DISPONIBLES

### **Test de connexion:**
- ✅ Clé API valide
- ✅ 20 modèles disponibles
- ✅ Test réussi avec `llama-3.3-70b-versatile`

**Réponse test:** "Bonjour, je suis ravi de faire votre connaissance et d'avoir l'occasion de discuter avec vous en français."

---

### **Llama (Meta) 🦙**

| Modèle | Description |
|--------|-------------|
| `llama-3.3-70b-versatile` | Llama 3.3 70B - Le plus puissant ⭐ |
| `llama-3.1-8b-instant` | Llama 3.1 8B - Ultra rapide ⚡ |
| `meta-llama/llama-4-maverick-17b-128e-instruct` | Llama 4 Maverick 17B |
| `meta-llama/llama-4-scout-17b-16e-instruct` | Llama 4 Scout 17B |
| `meta-llama/llama-guard-4-12b` | Llama Guard 4 12B - Modération |
| `meta-llama/llama-prompt-guard-2-22m` | Llama Prompt Guard 2 22M |
| `meta-llama/llama-prompt-guard-2-86m` | Llama Prompt Guard 2 86M |

---

### **Qwen**

| Modèle | Description |
|--------|-------------|
| `qwen/qwen3-32b` | Qwen 3 32B |

---

### **OpenAI OSS**

| Modèle | Description |
|--------|-------------|
| `openai/gpt-oss-120b` | GPT OSS 120B |
| `openai/gpt-oss-20b` | GPT OSS 20B |
| `openai/gpt-oss-safeguard-20b` | GPT OSS Safeguard 20B |

---

### **Autres modèles Groq**

| Modèle | Description |
|--------|-------------|
| `groq/compound` | Groq Compound |
| `groq/compound-mini` | Groq Compound Mini |
| `moonshotai/kimi-k2-instruct` | Kimi K2 Instruct |
| `moonshotai/kimi-k2-instruct-0905` | Kimi K2 Instruct (Sept 2025) |
| `allam-2-7b` | Allam 2 7B |
| `canopylabs/orpheus-arabic-saudi` | Orpheus Arabic Saudi 🇸🇦 |
| `canopylabs/orpheus-v1-english` | Orpheus v1 English |
| `whisper-large-v3` | Whisper Large v3 - Audio 🎙️ |
| `whisper-large-v3-turbo` | Whisper Large v3 Turbo 🎙️ |

---

## 🎯 MODÈLES INTÉGRÉS DANS WEBOX

### **DeepSeek - Sélecteur ajouté**

**Fichier:** `templates/dashboard/chat.html`

**Modèles disponibles dans le sélecteur:**
- ✅ DeepSeek Chat (par défaut)
- ✅ DeepSeek Reasoner - Raisonnement avancé 🧠

**⚠️ Important:** Nécessite des crédits sur votre compte DeepSeek.

---

### **Groq - Sélecteur ajouté**

**Fichier:** `templates/dashboard/chat.html`

**Modèles disponibles dans le sélecteur:**
- ✅ Llama 3.3 70B Versatile (par défaut) ⭐
- ✅ Llama 3.1 8B Instant - Ultra rapide ⚡
- ✅ Llama 4 Maverick 17B
- ✅ Llama 4 Scout 17B
- ✅ Qwen 3 32B
- ✅ GPT OSS 120B
- ✅ GPT OSS 20B
- ✅ Groq Compound
- ✅ Groq Compound Mini
- ✅ Kimi K2 Instruct

---

## 🚀 UTILISATION

### **Pour utiliser DeepSeek:**

1. **Rechargez votre compte DeepSeek** (nécessaire)
2. Allez sur `/chat`
3. Cochez "DeepSeek" (dans Modèles Spécialisés)
4. Sélectionnez le modèle dans le dropdown
5. Envoyez votre message

**Modèle par défaut:** `deepseek-chat`

---

### **Pour utiliser Groq:**

1. Allez sur `/chat`
2. Cochez "Groq (Ultra-rapide)" (dans Modèles Spécialisés)
3. Sélectionnez le modèle dans le dropdown
4. Envoyez votre message

**Modèle par défaut:** `llama-3.3-70b-versatile`

---

## 📊 COMPARAISON DES MODÈLES

### **DeepSeek**

| Modèle | Usage | Caractéristiques |
|--------|-------|------------------|
| **deepseek-chat** | Chat général | Équilibré, polyvalent |
| **deepseek-reasoner** | Raisonnement complexe | Analyse approfondie, logique avancée |

---

### **Groq (Ultra-rapide ⚡)**

| Modèle | Usage | Caractéristiques |
|--------|-------|------------------|
| **llama-3.3-70b-versatile** | Tâches complexes | Le plus puissant, polyvalent |
| **llama-3.1-8b-instant** | Réponses rapides | Ultra rapide, efficace |
| **llama-4-maverick-17b** | Tâches avancées | Nouvelle génération Llama 4 |
| **qwen/qwen3-32b** | Multilingue | Excellent pour le chinois |
| **openai/gpt-oss-120b** | Très puissant | 120B paramètres |
| **groq/compound** | Tâches spécialisées | Modèle propriétaire Groq |

---

## 💡 AVANTAGES DE GROQ

### **Vitesse exceptionnelle ⚡**
- **Inférence ultra-rapide** grâce aux LPU (Language Processing Units)
- Jusqu'à **10x plus rapide** que les GPU traditionnels
- Idéal pour les applications en temps réel

### **Large choix de modèles**
- 20 modèles disponibles
- Llama 3.3, Llama 4, Qwen, GPT OSS
- Modèles de modération et audio (Whisper)

### **Gratuit avec limites généreuses**
- Pas de frais pour commencer
- Limites de taux élevées
- Parfait pour le développement

---

## 🔧 MODIFICATIONS EFFECTUÉES

### **1. Scripts de test créés**
- `test_deepseek_connection.py` - Test de connexion DeepSeek
- `test_groq_connection.py` - Test de connexion Groq

### **2. Sélecteurs ajoutés** - `@C:/Users/Anthony/CascadeProjects/webox/templates/dashboard/chat.html`
- Sélecteur DeepSeek avec 2 modèles (lignes 667-678)
- Sélecteur Groq avec 10 modèles (lignes 643-666)

### **3. JavaScript mis à jour**
- Gestion des modèles DeepSeek sélectionnés (lignes 1043-1047)
- Gestion des modèles Groq sélectionnés (lignes 1038-1042)
- Affichage dynamique des noms (lignes 1317-1331)

### **4. Documentation créée**
- `MODELES_DEEPSEEK_GROQ_DISPONIBLES.md` - Liste complète des modèles

---

## ⚠️ NOTES IMPORTANTES

### **DeepSeek**
- **Erreur 402 - Insufficient Balance**
- Vous devez recharger votre compte sur https://platform.deepseek.com
- Les modèles sont disponibles mais nécessitent des crédits

### **Groq**
- ✅ **Fonctionne parfaitement**
- Gratuit avec limites généreuses
- Ultra-rapide grâce aux LPU
- Recommandé pour les réponses en temps réel

---

## 📈 RECOMMANDATIONS

### **Pour la vitesse ⚡**
- **Groq Llama 3.1 8B Instant** - Le plus rapide
- Idéal pour les chatbots en temps réel

### **Pour la puissance 💪**
- **Groq Llama 3.3 70B Versatile** - Le plus puissant sur Groq
- **DeepSeek Reasoner** - Raisonnement avancé (nécessite crédits)

### **Pour le développement 🛠️**
- **Groq** - Gratuit, rapide, fiable
- Parfait pour tester et développer

---

## 📊 RÉSUMÉ

| API | Modèles totaux | Modèles dans sélecteur | Modèle par défaut | Statut |
|-----|----------------|------------------------|-------------------|--------|
| **DeepSeek** | 2 | 2 | `deepseek-chat` | ⚠️ Nécessite crédits |
| **Groq** | 20 | 10 | `llama-3.3-70b-versatile` | ✅ Fonctionnel |

---

## 🔗 LIENS UTILES

### **DeepSeek**
- Console: https://platform.deepseek.com
- Documentation: https://platform.deepseek.com/docs
- Recharge: https://platform.deepseek.com/billing

### **Groq**
- Console: https://console.groq.com
- Documentation: https://console.groq.com/docs
- Playground: https://console.groq.com/playground

---

**Groq est maintenant intégré et prêt à l'emploi !** 🚀  
**DeepSeek nécessite un rechargement de crédits pour fonctionner.** ⚠️

---

**Dernière mise à jour : 17 Janvier 2026**
