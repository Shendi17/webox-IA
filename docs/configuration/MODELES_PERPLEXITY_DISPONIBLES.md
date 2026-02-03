# 📋 MODÈLES PERPLEXITY DISPONIBLES SUR WEBOX

**Date:** 18 Janvier 2026  
**Statut:** ✅ Testé et configuré

---

## ✅ PERPLEXITY - 8 MODÈLES DISPONIBLES

### **Test de connexion:**
- ✅ Clé API valide
- ✅ 8 modèles disponibles
- ✅ Test réussi avec `sonar`

**Réponse test:** "Bonjour !"

---

## 🔍 MODÈLES PERPLEXITY

### **Sonar (Recherche en ligne) 🔍**

| Modèle | Description | Caractéristiques |
|--------|-------------|------------------|
| `sonar` | Sonar - Recherche standard ⭐ | Recherche en ligne, citations, rapide |
| `sonar-pro` | Sonar Pro - Recherche avancée | Recherche approfondie, meilleure qualité |
| `sonar-reasoning` | Sonar Reasoning - Raisonnement avec recherche 🧠 | Raisonnement avancé + recherche web |

**Caractéristiques des modèles Sonar:**
- ✅ **Recherche en temps réel** sur le web
- ✅ **Citations automatiques** avec sources
- ✅ **Informations à jour** (accès internet)
- ✅ **Idéal pour:** Actualités, recherche, vérification de faits

---

### **Llama Sonar (En ligne)**

| Modèle | Description | Caractéristiques |
|--------|-------------|------------------|
| `llama-3.1-sonar-small-128k-online` | Llama 3.1 Sonar Small ⚡ | Rapide, 128k contexte, recherche en ligne |
| `llama-3.1-sonar-large-128k-online` | Llama 3.1 Sonar Large | Puissant, 128k contexte, recherche en ligne |
| `llama-3.1-sonar-huge-128k-online` | Llama 3.1 Sonar Huge | Très puissant, 128k contexte, recherche en ligne |

**Caractéristiques:**
- ✅ **128k tokens de contexte** (documents longs)
- ✅ **Recherche en ligne** intégrée
- ✅ **Basé sur Llama 3.1** (Meta)

---

### **Llama (Sans recherche)**

| Modèle | Description | Caractéristiques |
|--------|-------------|------------------|
| `llama-3.1-8b-instruct` | Llama 3.1 8B Instruct | Rapide, sans recherche web |
| `llama-3.1-70b-instruct` | Llama 3.1 70B Instruct | Puissant, sans recherche web |

**Caractéristiques:**
- ❌ **Pas de recherche en ligne**
- ✅ **Modèles Llama standard** (Meta)
- ✅ **Bon pour:** Tâches générales sans besoin de recherche

---

## 🎯 MODÈLES INTÉGRÉS DANS WEBOX

### **Perplexity - Sélecteur ajouté**

**Fichier:** `templates/dashboard/chat.html`

**Modèles disponibles dans le sélecteur:**
- ✅ Sonar (par défaut) - Recherche standard ⭐
- ✅ Sonar Pro - Recherche avancée
- ✅ Sonar Reasoning - Raisonnement avec recherche 🧠
- ✅ Llama 3.1 Sonar Small - Rapide ⚡
- ✅ Llama 3.1 Sonar Large - Puissant
- ✅ Llama 3.1 Sonar Huge - Très puissant
- ✅ Llama 3.1 8B Instruct
- ✅ Llama 3.1 70B Instruct

---

## 🚀 UTILISATION

### **Pour utiliser Perplexity:**

1. Allez sur `/chat`
2. Cochez "Perplexity (Recherche)" (dans Modèles Spécialisés)
3. Sélectionnez le modèle dans le dropdown
4. Envoyez votre message
5. **Obtenez des réponses avec sources et citations** 🔍

**Modèle par défaut:** `sonar`

---

## 💡 AVANTAGES DE PERPLEXITY

### **Recherche en temps réel 🔍**
- **Accès internet** pour informations à jour
- **Citations automatiques** avec sources
- **Idéal pour:** Actualités, recherche, vérification de faits

### **Modèles Sonar**
- **Sonar:** Rapide, équilibré, parfait pour la plupart des cas
- **Sonar Pro:** Plus approfondi, meilleure qualité de recherche
- **Sonar Reasoning:** Raisonnement avancé + recherche web

### **Grand contexte**
- **128k tokens** pour les modèles Llama Sonar
- Peut traiter des documents très longs

---

## 📊 COMPARAISON DES MODÈLES

### **Pour la recherche web 🔍**

| Modèle | Vitesse | Qualité | Usage recommandé |
|--------|---------|---------|------------------|
| **sonar** | ⚡⚡⚡ | ⭐⭐⭐ | Recherche rapide, actualités |
| **sonar-pro** | ⚡⚡ | ⭐⭐⭐⭐ | Recherche approfondie |
| **sonar-reasoning** | ⚡ | ⭐⭐⭐⭐⭐ | Analyse complexe avec recherche |

---

### **Pour les documents longs 📄**

| Modèle | Contexte | Recherche web | Usage recommandé |
|--------|----------|---------------|------------------|
| **llama-3.1-sonar-small-128k-online** | 128k | ✅ | Documents longs + recherche rapide |
| **llama-3.1-sonar-large-128k-online** | 128k | ✅ | Documents longs + recherche puissante |
| **llama-3.1-sonar-huge-128k-online** | 128k | ✅ | Documents très longs + recherche avancée |

---

### **Sans recherche web**

| Modèle | Usage recommandé |
|--------|------------------|
| **llama-3.1-8b-instruct** | Tâches générales rapides |
| **llama-3.1-70b-instruct** | Tâches générales puissantes |

---

## 🔧 MODIFICATIONS EFFECTUÉES

### **1. Script de test créé**
- `test_perplexity_connection.py` - Test de connexion Perplexity

### **2. Sélecteur ajouté** - `@C:/Users/Anthony/CascadeProjects/webox/templates/dashboard/chat.html`
- Sélecteur Perplexity avec 8 modèles (lignes 679-698)

### **3. JavaScript mis à jour**
- Gestion du modèle Perplexity sélectionné (lignes 1066-1070)
- Affichage dynamique du nom (lignes 1356-1362)

### **4. Documentation créée**
- `MODELES_PERPLEXITY_DISPONIBLES.md` - Liste complète des modèles

---

## 🎯 CAS D'USAGE

### **Recherche d'actualités 📰**
- **Modèle:** `sonar` ou `sonar-pro`
- **Pourquoi:** Accès en temps réel aux dernières informations

### **Vérification de faits ✅**
- **Modèle:** `sonar-pro`
- **Pourquoi:** Recherche approfondie avec citations

### **Analyse complexe avec recherche 🧠**
- **Modèle:** `sonar-reasoning`
- **Pourquoi:** Raisonnement avancé + recherche web

### **Documents longs avec recherche 📄**
- **Modèle:** `llama-3.1-sonar-large-128k-online`
- **Pourquoi:** 128k contexte + recherche en ligne

### **Chat général sans recherche 💬**
- **Modèle:** `llama-3.1-70b-instruct`
- **Pourquoi:** Puissant, pas besoin de recherche web

---

## ⚡ CARACTÉRISTIQUES UNIQUES

### **Citations automatiques**
Les modèles Sonar incluent automatiquement des citations avec numéros de référence:
```
Réponse: "Bonjour ![1][2][5]"
```

### **Informations à jour**
- Accès en temps réel au web
- Pas de limite de date de connaissance
- Idéal pour les questions sur l'actualité

### **Grand contexte**
- 128k tokens pour les modèles Llama Sonar
- Peut traiter des documents entiers

---

## 📈 RECOMMANDATIONS

### **Pour débuter 🌟**
- **Sonar** - Parfait pour la plupart des cas
- Rapide, efficace, avec recherche web

### **Pour la qualité 💎**
- **Sonar Pro** - Recherche plus approfondie
- Meilleure qualité de réponses

### **Pour l'analyse 🧠**
- **Sonar Reasoning** - Raisonnement avancé
- Idéal pour les questions complexes

### **Pour les documents 📚**
- **Llama 3.1 Sonar Large 128k** - Grand contexte
- Parfait pour analyser de longs documents

---

## 📊 RÉSUMÉ

| Élément | Valeur |
|---------|--------|
| **Modèles totaux** | 8 |
| **Modèles dans sélecteur** | 8 |
| **Modèle par défaut** | `sonar` |
| **Recherche web** | ✅ Oui (modèles Sonar) |
| **Contexte max** | 128k tokens |
| **Citations** | ✅ Automatiques |
| **Statut** | ✅ Fonctionnel |

---

## 🔗 LIENS UTILES

### **Perplexity**
- Console: https://www.perplexity.ai/settings/api
- Documentation: https://docs.perplexity.ai
- Playground: https://www.perplexity.ai

---

## 💰 TARIFICATION

**Perplexity propose un plan gratuit avec limites:**
- Requêtes limitées par jour
- Accès aux modèles Sonar
- Parfait pour tester

**Plan Pro:**
- Requêtes illimitées
- Accès à tous les modèles
- Support prioritaire

---

**Perplexity est maintenant intégré et prêt à l'emploi !** 🚀

**Utilisez les modèles Sonar pour des recherches en temps réel avec citations !** 🔍

---

**Dernière mise à jour : 18 Janvier 2026**
