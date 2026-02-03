# 🔍 DIAGNOSTIC - Erreur OpenAI "Insufficient Quota"

**Date:** 17 Janvier 2026  
**Erreur reçue:** `Error code: 429 - insufficient_quota`

---

## ❌ PROBLÈME IDENTIFIÉ

L'erreur **"You exceeded your current quota"** signifie que :

1. **Votre clé API OpenAI n'a pas de crédit disponible**
2. **OU** Vous êtes sur un plan gratuit qui a expiré
3. **OU** Votre carte bancaire n'est pas correctement liée au compte

---

## ✅ CONFIGURATION ACTUELLE (Vérifiée)

### **Modèle utilisé dans WeBox**
- **Nom du modèle:** `gpt-4o` (correct ✅)
- **Fichier:** `modules/core/ai_providers.py` ligne 46
- **Ce modèle existe et est valide**

### **Mapping frontend → backend**
- Frontend: `gpt4` → Backend: `OpenAI` ✅
- Pas de problème de configuration

---

## 🚨 CAUSES POSSIBLES

### **1. Compte OpenAI gratuit (Tier Free)**
- **Limite:** $5 de crédit gratuit (expire après 3 mois)
- **Si expiré:** Vous devez passer à un plan payant

### **2. Carte bancaire non ajoutée**
- Même si vous avez "activé la facturation", **vous devez ajouter une carte bancaire valide**

### **3. Quota mensuel dépassé**
- Si vous avez défini une limite de dépense mensuelle, vous l'avez peut-être atteinte

### **4. Paiement échoué**
- Votre dernière facture n'a pas été payée
- Carte expirée ou refusée

---

## 🔧 SOLUTIONS À APPLIQUER

### **ÉTAPE 1 : Vérifier votre compte OpenAI**

1. **Allez sur:** https://platform.openai.com/account/billing/overview
2. **Vérifiez:**
   - ✅ Avez-vous un solde de crédit disponible ?
   - ✅ Votre carte bancaire est-elle ajoutée ?
   - ✅ Votre plan est-il actif (Tier 1, 2, 3, etc.) ?

---

### **ÉTAPE 2 : Ajouter une carte bancaire (SI PAS DÉJÀ FAIT)**

1. **Allez sur:** https://platform.openai.com/account/billing/payment-methods
2. **Cliquez sur:** "Add payment method"
3. **Ajoutez votre carte bancaire**
4. **Définissez une limite de dépense mensuelle** (ex: $10, $20, $50)

**⚠️ IMPORTANT:** Même si vous avez "activé la facturation", **OpenAI ne vous laissera PAS utiliser l'API sans carte bancaire valide**.

---

### **ÉTAPE 3 : Vérifier les limites de quota**

1. **Allez sur:** https://platform.openai.com/account/limits
2. **Vérifiez votre Tier actuel:**
   - **Tier Free:** $5 gratuit (expire après 3 mois)
   - **Tier 1:** Après avoir dépensé $5
   - **Tier 2:** Après avoir dépensé $50
   - **Tier 3+:** Quotas plus élevés

3. **Si vous êtes en Tier Free expiré:**
   - Ajoutez une carte bancaire
   - Rechargez votre compte avec au moins $5

---

### **ÉTAPE 4 : Recharger votre compte (SI NÉCESSAIRE)**

1. **Allez sur:** https://platform.openai.com/account/billing/overview
2. **Cliquez sur:** "Add to credit balance"
3. **Ajoutez au moins $10** pour commencer

---

### **ÉTAPE 5 : Vérifier l'usage actuel**

1. **Allez sur:** https://platform.openai.com/account/usage
2. **Vérifiez combien vous avez dépensé ce mois-ci**
3. **Si vous avez atteint votre limite mensuelle:**
   - Augmentez la limite dans les paramètres de facturation

---

## 💡 ALTERNATIVE TEMPORAIRE

En attendant de résoudre le problème OpenAI, vous pouvez utiliser **d'autres modèles gratuits** :

### **1. Groq (Ultra-rapide et GRATUIT)**
- **Modèles:** Llama 3, Mixtral
- **Quota:** Gratuit en beta
- **Clé API:** https://console.groq.com/

### **2. Google Gemini (GRATUIT)**
- **Modèles:** Gemini 2.5 Flash, Gemini 2.5 Pro
- **Quota:** Gratuit jusqu'à certaines limites
- **Clé API:** https://makersuite.google.com/app/apikey

### **3. DeepSeek (Économique)**
- **Modèles:** DeepSeek Chat, DeepSeek Coder
- **Quota:** Très bon rapport qualité/prix
- **Clé API:** https://platform.deepseek.com/

---

## 📋 CHECKLIST DE VÉRIFICATION

Cochez ce que vous avez fait :

- [ ] Vérifié le solde de crédit sur https://platform.openai.com/account/billing/overview
- [ ] Ajouté une carte bancaire valide
- [ ] Défini une limite de dépense mensuelle
- [ ] Vérifié que je ne suis pas en Tier Free expiré
- [ ] Rechargé mon compte avec au moins $10
- [ ] Vérifié que ma dernière facture a été payée

---

## 🎯 CE QUE VOUS DEVEZ FAIRE MAINTENANT

### **Option A : Résoudre le problème OpenAI (Recommandé)**

1. **Allez sur:** https://platform.openai.com/account/billing/overview
2. **Ajoutez une carte bancaire** si ce n'est pas déjà fait
3. **Rechargez votre compte avec $10-20**
4. **Attendez 5-10 minutes** que le crédit soit disponible
5. **Retestez WeBox**

### **Option B : Utiliser une alternative gratuite (Temporaire)**

1. **Créez un compte Groq:** https://console.groq.com/
2. **Obtenez votre clé API**
3. **Ajoutez-la dans votre fichier `.env`:**
   ```
   GROQ_API_KEY=votre_clé_ici
   ```
4. **Utilisez Groq dans WeBox** (ultra-rapide et gratuit)

---

## ⚠️ ERREURS COURANTES

### **"J'ai activé la facturation mais ça ne marche toujours pas"**
→ **Vous devez AUSSI ajouter une carte bancaire valide**

### **"J'ai ajouté une carte mais l'erreur persiste"**
→ **Attendez 5-10 minutes** que le système OpenAI se mette à jour

### **"Mon compte dit $0.00"**
→ **Rechargez votre compte** avec au moins $10

### **"Je suis en Tier Free"**
→ **Passez à Tier 1** en dépensant au moins $5 ou en ajoutant une carte

---

## 📞 SUPPORT OPENAI

Si le problème persiste après avoir tout vérifié :

- **Email:** support@openai.com
- **Documentation:** https://platform.openai.com/docs/guides/error-codes
- **Status:** https://status.openai.com/

---

## ✅ RÉSUMÉ

**Le problème n'est PAS dans WeBox.**  
**Le problème est dans votre compte OpenAI.**

**Action immédiate:**
1. Ajoutez une carte bancaire sur https://platform.openai.com/account/billing/payment-methods
2. Rechargez votre compte avec $10-20
3. Attendez 5-10 minutes
4. Retestez

**OU utilisez Groq/Gemini gratuitement en attendant.**

---

**Dernière mise à jour : 17 Janvier 2026**
