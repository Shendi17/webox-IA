# 🔑 Guide d'Obtention des Clés API - WeBox Multi-IA

## 📋 Table des Matières

1. [Clés Essentielles (REQUIS)](#clés-essentielles)
2. [Clés Recommandées](#clés-recommandées)
3. [Clés Optionnelles](#clés-optionnelles)
4. [Instructions Détaillées](#instructions-détaillées)
5. [Coûts et Quotas](#coûts-et-quotas)

---

## 🎯 Clés Essentielles (REQUIS)

Ces clés sont **nécessaires** pour utiliser les fonctionnalités de base de WeBox.

### **1. OpenAI API Key** ⭐ PRIORITÉ 1

**Pourquoi:** Utilisé pour GPT-4, GPT-3.5, DALL-E, Whisper, TTS, et les agents IA

**Comment obtenir:**
1. Aller sur https://platform.openai.com/
2. Créer un compte ou se connecter
3. Aller dans "API Keys" dans le menu
4. Cliquer sur "Create new secret key"
5. Copier la clé (elle ne sera affichée qu'une fois!)
6. Ajouter un moyen de paiement dans "Billing"

**Coût:**
- GPT-4: ~0.03$ / 1K tokens (input), ~0.06$ / 1K tokens (output)
- GPT-3.5: ~0.0005$ / 1K tokens
- DALL-E 3: ~0.04$ par image
- Whisper: ~0.006$ par minute
- TTS: ~0.015$ / 1K caractères

**Quota gratuit:** 5$ de crédit pour les nouveaux comptes

---

## 🌟 Clés Recommandées

Ces clés améliorent significativement l'expérience.

### **2. Anthropic Claude API** ⭐ PRIORITÉ 2

**Pourquoi:** Claude 3 est excellent pour l'analyse, le raisonnement et les tâches complexes

**Comment obtenir:**
1. Aller sur https://console.anthropic.com/
2. Créer un compte
3. Aller dans "API Keys"
4. Créer une nouvelle clé
5. Ajouter un moyen de paiement

**Coût:**
- Claude 3 Opus: ~0.015$ / 1K tokens (input), ~0.075$ / 1K tokens (output)
- Claude 3 Sonnet: ~0.003$ / 1K tokens (input), ~0.015$ / 1K tokens (output)
- Claude 3 Haiku: ~0.00025$ / 1K tokens (input), ~0.00125$ / 1K tokens (output)

**Quota gratuit:** 5$ de crédit pour les nouveaux comptes

---

### **3. Google AI (Gemini) API** ⭐ PRIORITÉ 3

**Pourquoi:** Gemini Pro est gratuit jusqu'à certaines limites et très performant

**Comment obtenir:**
1. Aller sur https://makersuite.google.com/app/apikey
2. Se connecter avec un compte Google
3. Cliquer sur "Get API key"
4. Créer une clé pour votre projet

**Coût:**
- Gemini Pro: GRATUIT jusqu'à 60 requêtes/minute
- Gemini Pro Vision: GRATUIT jusqu'à 60 requêtes/minute

**Quota gratuit:** Très généreux, idéal pour commencer!

---

### **4. Twilio (Pour Assistant Vocal)** ⭐ PRIORITÉ 4

**Pourquoi:** Nécessaire pour les appels téléphoniques automatisés

**Comment obtenir:**
1. Aller sur https://www.twilio.com/
2. Créer un compte (essai gratuit disponible)
3. Aller dans "Console"
4. Copier "Account SID" et "Auth Token"
5. Acheter un numéro de téléphone (~1€/mois)

**Coût:**
- Appels sortants: ~0.01€/minute
- Appels entrants: ~0.0085€/minute
- SMS: ~0.075€/SMS
- Numéro de téléphone: ~1€/mois

**Quota gratuit:** 15$ de crédit pour l'essai

---

### **5. Google Cloud (Pour Assistant Vocal)** ⭐ PRIORITÉ 5

**Pourquoi:** Speech-to-Text et Text-to-Speech pour l'assistant vocal

**Comment obtenir:**
1. Aller sur https://console.cloud.google.com/
2. Créer un nouveau projet
3. Activer "Cloud Speech-to-Text API"
4. Activer "Cloud Text-to-Speech API"
5. Aller dans "IAM & Admin" > "Service Accounts"
6. Créer un compte de service
7. Créer une clé JSON
8. Télécharger le fichier JSON
9. Mettre le chemin complet dans GOOGLE_APPLICATION_CREDENTIALS

**Coût:**
- Speech-to-Text: ~0.006$ par 15 secondes
- Text-to-Speech: ~4$ par million de caractères

**Quota gratuit:** 300$ de crédit pour 90 jours (nouveaux comptes)

---

## 🎨 Clés pour Génération de Médias

### **6. Stability AI (Stable Diffusion)**

**Pourquoi:** Génération d'images de haute qualité

**Comment obtenir:**
1. Aller sur https://platform.stability.ai/
2. Créer un compte
3. Aller dans "API Keys"
4. Créer une nouvelle clé

**Coût:** ~0.02$ par image

---

### **7. ElevenLabs (Voix ultra-réalistes)**

**Pourquoi:** Meilleure qualité de synthèse vocale

**Comment obtenir:**
1. Aller sur https://elevenlabs.io/
2. Créer un compte
3. Aller dans "Profile" > "API Key"

**Coût:** 10,000 caractères gratuits/mois, puis ~0.30$ / 1K caractères

---

### **8. Runway ML (Génération vidéo)**

**Pourquoi:** Génération de vidéos IA (Gen-2, Gen-3)

**Comment obtenir:**
1. Aller sur https://runwayml.com/
2. Créer un compte
3. S'abonner à un plan (API en accès limité)

**Coût:** Système de crédits, ~10$/mois minimum

---

## 🔧 Clés pour Outils Spécialisés

### **9. Pinecone (Base de données vectorielle)**

**Pourquoi:** Pour la recherche sémantique et RAG

**Comment obtenir:**
1. Aller sur https://www.pinecone.io/
2. Créer un compte
3. Créer un index
4. Copier l'API Key et l'Environment

**Quota gratuit:** 1 index gratuit (Starter plan)

---

### **10. Serper (Google Search API)**

**Pourquoi:** Recherche Google via API

**Comment obtenir:**
1. Aller sur https://serper.dev/
2. Créer un compte
3. Copier l'API Key

**Quota gratuit:** 2,500 requêtes gratuites

---

## 📊 Résumé des Coûts Mensuels

### **Configuration Minimale (GRATUIT)**
- Google Gemini Pro: GRATUIT
- Serper: GRATUIT (2,500 recherches)
- **Total: 0€/mois**

### **Configuration Basique (~10€/mois)**
- OpenAI GPT-3.5: ~5€
- Google Gemini: GRATUIT
- Serper: GRATUIT
- **Total: ~5€/mois**

### **Configuration Standard (~30€/mois)**
- OpenAI (GPT-4 + DALL-E): ~15€
- Anthropic Claude: ~5€
- Google Cloud (STT/TTS): ~3€
- Twilio (100 appels): ~6€
- **Total: ~30€/mois**

### **Configuration Complète (~100€/mois)**
- OpenAI: ~30€
- Anthropic: ~15€
- Google Cloud: ~10€
- Twilio: ~10€
- Stability AI: ~10€
- ElevenLabs: ~10€
- Runway: ~10€
- Autres: ~5€
- **Total: ~100€/mois**

---

## 🎯 Ordre de Priorité d'Obtention

### **Phase 1 - Démarrage (GRATUIT)**
1. ✅ Google AI (Gemini) - GRATUIT
2. ✅ Serper - GRATUIT (2,500 recherches)

### **Phase 2 - Fonctionnalités de Base (~5€/mois)**
3. ✅ OpenAI (GPT-3.5) - ~5€

### **Phase 3 - Fonctionnalités Avancées (~30€/mois)**
4. ✅ OpenAI (GPT-4) - ~15€
5. ✅ Anthropic Claude - ~5€
6. ✅ Twilio + Google Cloud (Assistant Vocal) - ~10€

### **Phase 4 - Génération de Médias (~60€/mois)**
7. ✅ Stability AI (Images) - ~10€
8. ✅ ElevenLabs (Voix) - ~10€
9. ✅ Runway (Vidéo) - ~10€

### **Phase 5 - Outils Spécialisés (~100€/mois)**
10. ✅ Pinecone (RAG) - ~10€
11. ✅ Autres APIs selon besoins

---

## 💡 Conseils pour Économiser

### **1. Commencez Gratuit**
- Utilisez Google Gemini Pro (gratuit)
- Utilisez Serper pour les recherches (2,500 gratuites)
- Testez avec les quotas gratuits

### **2. Optimisez l'Usage**
- Utilisez GPT-3.5 au lieu de GPT-4 quand possible
- Mettez en cache les résultats
- Limitez la longueur des réponses (max_tokens)

### **3. Surveillez les Coûts**
- Configurez des alertes de budget
- Utilisez les dashboards de chaque service
- Vérifiez régulièrement votre usage

### **4. Profitez des Crédits Gratuits**
- OpenAI: 5$ pour nouveaux comptes
- Anthropic: 5$ pour nouveaux comptes
- Google Cloud: 300$ pour 90 jours
- Twilio: 15$ pour l'essai

---

## 🔒 Sécurité des Clés API

### **Bonnes Pratiques**

1. **NE JAMAIS** partager vos clés API
2. **NE JAMAIS** commiter vos clés dans Git
3. Utiliser le fichier `.env` (ignoré par Git)
4. Régénérer les clés si compromises
5. Utiliser des clés différentes pour dev/prod
6. Configurer des limites de dépenses
7. Surveiller l'usage régulièrement

### **Rotation des Clés**

- Changez vos clés tous les 3-6 mois
- Utilisez des clés différentes par environnement
- Documentez où chaque clé est utilisée

---

## 📝 Checklist de Configuration

### **Clés Essentielles**
- [ ] OpenAI API Key configurée
- [ ] Fichier `.env` créé
- [ ] Clés testées

### **Clés Recommandées**
- [ ] Anthropic Claude configuré
- [ ] Google AI (Gemini) configuré
- [ ] Twilio configuré (si assistant vocal)
- [ ] Google Cloud configuré (si assistant vocal)

### **Clés Optionnelles**
- [ ] Stability AI (images)
- [ ] ElevenLabs (voix)
- [ ] Runway (vidéo)
- [ ] Pinecone (RAG)
- [ ] Autres selon besoins

---

## 🆘 Dépannage

### **Problème: Clé API invalide**
- Vérifiez que la clé est correctement copiée (pas d'espaces)
- Vérifiez que la clé n'a pas expiré
- Vérifiez que le moyen de paiement est configuré

### **Problème: Quota dépassé**
- Vérifiez votre usage dans le dashboard
- Augmentez vos limites si nécessaire
- Attendez le renouvellement du quota

### **Problème: Erreur de facturation**
- Vérifiez que votre moyen de paiement est valide
- Vérifiez que vous n'avez pas atteint votre limite de dépenses
- Contactez le support du service

---

## 📚 Ressources Utiles

### **Documentation Officielle**
- [OpenAI Docs](https://platform.openai.com/docs)
- [Anthropic Docs](https://docs.anthropic.com/)
- [Google AI Docs](https://ai.google.dev/)
- [Twilio Docs](https://www.twilio.com/docs)

### **Comparateurs de Prix**
- [AI Price Comparison](https://artificialanalysis.ai/)
- [LLM Pricing](https://llmpricecheck.com/)

### **Communautés**
- [OpenAI Community](https://community.openai.com/)
- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA)
- [Hugging Face Forums](https://discuss.huggingface.co/)

---

**🔑 Vous êtes maintenant prêt à configurer toutes les APIs de WeBox Multi-IA ! 🚀**
