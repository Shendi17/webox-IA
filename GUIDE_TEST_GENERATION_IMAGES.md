# 🎨 GUIDE DE TEST - GÉNÉRATION D'IMAGES

**Date:** 25 Mars 2026  
**URL:** http://webox.local:8000/generation

---

## ✅ PROBLÈME RÉSOLU

Le message d'erreur "Génération d'image en cours... (À implémenter)" a été corrigé.

### Modifications Effectuées

1. **Frontend (`generation.html`)**
   - ✅ Fonction `generateImage()` implémentée
   - ✅ Fonction `generateEbook()` implémentée
   - ✅ Fonction `generateShort()` implémentée
   - ✅ Fonction `generateAd()` implémentée
   - ✅ Fonction `generateLogo()` implémentée

2. **Backend - Nouveau Service**
   - ✅ Créé `app/services/image_generation_service.py`
   - ✅ Support de 5 providers d'images:
     - Vertex AI Imagen (Google)
     - OpenAI DALL-E
     - Replicate (Flux, SDXL)
     - Hugging Face (gratuit)
     - Stability AI

3. **Routes API**
   - ✅ Mise à jour de `generation_routes.py`
   - ✅ Routage automatique vers le bon provider selon le modèle

---

## 🧪 COMMENT TESTER

### 1. Accéder à la Page
```
http://webox.local:8000/generation
```

### 2. Onglet Images

#### Test avec DALL-E 3 (OpenAI)
1. Sélectionner **"DALL-E 3 - Haute qualité"**
2. Entrer un prompt: `A futuristic cityscape at sunset, cyberpunk style, neon lights`
3. Taille: `1024x1024`
4. Qualité: `HD`
5. Cliquer sur **"🎨 Générer l'image"**

**Résultat attendu:**
```
Génération lancée ! 
ID: 1
Modèle: dall-e-3
Statut: generating
```

#### Test avec Vertex AI Imagen (Google)
1. Sélectionner **"Imagen 4 Standard - Recommandé"**
2. Entrer un prompt: `Professional business logo, modern minimalist design`
3. Cliquer sur **"🎨 Générer l'image"**

**Résultat attendu:**
```
Génération lancée ! 
ID: 2
Modèle: imagen-4.0-generate-001
Statut: generating
```

#### Test avec Replicate (Flux Pro)
1. Sélectionner **"Flux Pro - Ultra qualité 🎨"**
2. Entrer un prompt: `Beautiful landscape with mountains and lake, photorealistic`
3. Cliquer sur **"🎨 Générer l'image"**

**Résultat attendu:**
```
Génération lancée ! 
ID: 3
Modèle: black-forest-labs/flux-pro
Statut: generating
```

#### Test avec Hugging Face (Gratuit)
1. Sélectionner **"SDXL Base 1.0"**
2. Entrer un prompt: `Cute cat playing with yarn, cartoon style`
3. Cliquer sur **"🎨 Générer l'image"**

**Résultat attendu:**
```
Génération lancée ! 
ID: 4
Modèle: stabilityai/stable-diffusion-xl-base-1.0
Statut: generating
```

---

### 3. Onglet eBooks

1. Sélectionner un modèle (ex: **"Claude 3.5 Sonnet - Cohérence"**)
2. Entrer un sujet: `Guide complet du marketing digital pour débutants`
3. Longueur: `Moyen (5 chapitres)`
4. Cliquer sur **"📚 Générer l'eBook"**

**Résultat attendu:**
```
Génération d'eBook lancée !
ID: 5
Temps estimé: 150s
```

---

### 4. Onglet Shorts

1. Sélectionner un modèle (ex: **"Claude 3.5 Sonnet - Créatif"**)
2. Objectif: `Notoriété`
3. Sujet: `3 erreurs marketing qui coûtent cher`
4. Cliquer sur **"📱 Générer le Short"**

**Résultat attendu:**
```
Génération de Short lancée !
ID: 6
Temps estimé: 120s
```

---

### 5. Onglet Logos

1. Sélectionner **"Imagen 4 Ultra - Meilleure qualité"**
2. Nom de la marque: `TechStart`
3. Secteur: `SaaS`
4. Style: `Moderne`
5. Cliquer sur **"🎨 Générer le logo"**

**Résultat attendu:**
```
Génération de logo lancée !
ID: 7
Modèle: imagen-4.0-ultra-generate-001
```

---

## 🔍 VÉRIFICATION DES RÉSULTATS

### Via l'API
```bash
# Récupérer le statut d'une image
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/generation/image/1

# Lister toutes les images
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/generation/images
```

### Via l'Historique
L'historique devrait se recharger automatiquement après chaque génération et afficher les nouvelles créations.

---

## 📊 MODÈLES DISPONIBLES PAR PROVIDER

### Vertex AI Imagen (Google) 🌟
- `imagen-4.0-ultra-generate-001` - Meilleure qualité
- `imagen-4.0-generate-001` - Standard (recommandé)
- `imagen-4.0-fast-generate-001` - Rapide
- `imagen-3.0-generate-002` - Imagen 3 v2
- `imagen-3.0-generate-001` - Imagen 3 v1

### OpenAI DALL-E
- `dall-e-3` - Haute qualité ($0.04-$0.08)
- `dall-e-2` - Standard ($0.02)

### Replicate
- `black-forest-labs/flux-pro` - Ultra qualité
- `black-forest-labs/flux-dev` - Développement
- `stability-ai/sdxl` - Stable Diffusion XL
- `stability-ai/stable-diffusion` - Stable Diffusion

### Hugging Face (Gratuit) ⚡
- `stabilityai/stable-diffusion-xl-base-1.0` - SDXL Base
- `stabilityai/stable-diffusion-3-medium` - SD 3 Medium
- `black-forest-labs/FLUX.1-dev` - Flux Dev

### Stability AI
- `stable-diffusion-3.5-large` - SD 3.5 Large
- `stable-diffusion-3.5-medium` - SD 3.5 Medium
- `stable-diffusion-xl-1024-v1-0` - SDXL 1.0

---

## ⚠️ PRÉREQUIS

### Clés API Requises

Pour tester chaque provider, vous devez avoir les clés correspondantes dans votre `.env`:

```bash
# OpenAI (DALL-E)
OPENAI_API_KEY=sk-...

# Vertex AI (Imagen)
VERTEX_AI_PROJECT_ID=webox-482718
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json

# Replicate
REPLICATE_API_KEY=r8_...

# Hugging Face
HUGGINGFACE_API_KEY=hf_...

# Stability AI
STABILITY_API_KEY=sk-...
```

### Authentification
Vous devez être connecté avec un token valide. Le token est automatiquement récupéré depuis `localStorage.getItem('token')`.

---

## 🐛 DÉPANNAGE

### Erreur: "Veuillez entrer une description"
**Cause:** Le champ prompt est vide  
**Solution:** Entrer une description dans le champ "Description (Prompt)"

### Erreur: "Clé [Provider] non configurée"
**Cause:** La clé API n'est pas dans le `.env`  
**Solution:** Ajouter la clé correspondante dans `.env` et redémarrer le serveur

### Erreur: "Erreur de connexion"
**Cause:** Le serveur backend n'est pas démarré  
**Solution:** Vérifier que le serveur tourne sur `http://localhost:8000`

### Erreur: "401 Unauthorized"
**Cause:** Token d'authentification invalide ou expiré  
**Solution:** Se reconnecter à l'application

### Erreur: "Modèle non supporté"
**Cause:** Le modèle sélectionné n'est pas implémenté  
**Solution:** Choisir un autre modèle dans la liste

---

## 📁 FICHIERS GÉNÉRÉS

Les images générées sont sauvegardées dans:
```
generated/images/
  - imagen_20260325_141530.png
  - hf_20260325_141545.png
  - sd_20260325_141600.png
```

Les eBooks générés sont sauvegardés dans:
```
generated/ebooks/
  - ebook_1.pdf
  - ebook_2.txt
```

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Tester la génération d'images avec DALL-E
2. ✅ Tester avec Vertex AI Imagen (si configuré)
3. ✅ Tester avec Replicate (si configuré)
4. ✅ Tester la génération d'eBooks
5. ✅ Tester la génération de Shorts
6. ✅ Vérifier l'historique des générations
7. ⏳ Implémenter l'affichage des images dans l'historique
8. ⏳ Ajouter un système de progression en temps réel

---

**Statut:** ✅ **FONCTIONNEL**  
**Prêt pour:** Tests utilisateur  
**Dernière mise à jour:** 25 Mars 2026
