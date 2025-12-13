# 🚀 Démarrage Rapide - Génération de Médias IA

## ⚡ En 5 Minutes !

Générez des images et de l'audio avec WeBox Multi-IA en quelques étapes simples.

---

## 📋 Prérequis

✅ WeBox Multi-IA installé
✅ Python 3.8+
✅ Clés API (au moins une)

---

## 🔑 Étape 1 : Obtenir les Clés API

### **Option A : DALL-E 3 (Images)** - Recommandé

1. Allez sur https://platform.openai.com
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Cliquez sur "Create new secret key"
5. Copiez la clé (commence par `sk-...`)
6. Ajoutez des crédits ($5-10 minimum)

**Prix :** ~$0.04-0.12 par image

### **Option B : Stable Diffusion (Images)** - Gratuit au début

1. Allez sur https://platform.stability.ai
2. Créez un compte
3. Allez dans "API Keys"
4. Générez une clé API
5. Copiez la clé

**Prix :** Crédits gratuits au départ, puis pay-per-use

### **Option C : ElevenLabs (Audio)** - Plan gratuit disponible

1. Allez sur https://elevenlabs.io
2. Créez un compte
3. Allez dans "Profile" → "API Key"
4. Copiez la clé

**Prix :** 10,000 caractères/mois gratuits

---

## ⚙️ Étape 2 : Configuration

### **Méthode 1 : Fichier .env (Recommandé)**

1. Ouvrez le fichier `.env` (ou créez-le depuis `.env.example`)
2. Ajoutez vos clés :

```env
# Pour DALL-E 3 et OpenAI TTS
OPENAI_API_KEY=sk-votre_cle_ici

# Pour Stable Diffusion
STABILITY_API_KEY=sk-votre_cle_ici

# Pour ElevenLabs
ELEVENLABS_API_KEY=votre_cle_ici
```

3. Sauvegardez le fichier

### **Méthode 2 : Variables d'environnement**

**Windows (PowerShell) :**
```powershell
$env:OPENAI_API_KEY="sk-votre_cle_ici"
$env:STABILITY_API_KEY="sk-votre_cle_ici"
$env:ELEVENLABS_API_KEY="votre_cle_ici"
```

---

## 🚀 Étape 3 : Lancer WeBox

```bash
# Méthode 1 : Script de lancement
LANCER-WEBOX.bat

# Méthode 2 : Commande directe
streamlit run app.py
```

---

## 🎨 Étape 4 : Générer votre Première Image

1. **Connectez-vous** (admin@webox.com / admin123)
2. **Cliquez sur** "🎨 Images IA" dans le menu
3. **Sélectionnez** DALL-E 3 ou Stable Diffusion
4. **Entrez un prompt**, par exemple :
   ```
   Un chat astronaute flottant dans l'espace, 
   style digital art, haute qualité, 8K
   ```
5. **Cliquez sur** "🎨 Générer l'image"
6. **Attendez** 10-30 secondes
7. **Téléchargez** votre image !

---

## 🎙️ Étape 5 : Générer votre Premier Audio

1. **Cliquez sur** "🎙️ Audio IA" dans le menu
2. **Sélectionnez** ElevenLabs ou OpenAI TTS
3. **Entrez du texte**, par exemple :
   ```
   Bienvenue dans WeBox Multi-IA, 
   la plateforme la plus complète pour 
   générer des images et de l'audio avec l'IA.
   ```
4. **Choisissez** une voix
5. **Cliquez sur** "🎙️ Générer l'audio"
6. **Écoutez** et téléchargez !

---

## 📊 Vérifier que Tout Fonctionne

### **Test 1 : Vérifier les Providers**

Dans WeBox, allez dans "⚙️ Configuration" et vérifiez :
- ✅ OpenAI : Configuré
- ✅ Stability AI : Configuré (si ajouté)
- ✅ ElevenLabs : Configuré (si ajouté)

### **Test 2 : Générer une Image de Test**

Prompt simple : `A red apple on a table`

Si ça fonctionne → ✅ Tout est OK !

### **Test 3 : Générer un Audio de Test**

Texte simple : `Hello, this is a test.`

Si ça fonctionne → ✅ Tout est OK !

---

## ❌ Problèmes Courants

### **Erreur : "Provider non configuré"**

**Solution :**
1. Vérifiez que la clé API est dans `.env`
2. Vérifiez qu'il n'y a pas d'espaces avant/après
3. Relancez WeBox

### **Erreur : "Invalid API Key"**

**Solution :**
1. Vérifiez que la clé est correcte
2. Vérifiez que vous avez des crédits
3. Régénérez une nouvelle clé si nécessaire

### **Erreur : "Rate limit exceeded"**

**Solution :**
1. Attendez quelques minutes
2. Vérifiez vos limites de compte
3. Passez à un plan payant si nécessaire

### **Image/Audio ne se génère pas**

**Solution :**
1. Vérifiez votre connexion internet
2. Vérifiez les logs d'erreur
3. Essayez avec un prompt plus simple
4. Vérifiez vos crédits API

---

## 💡 Conseils pour de Meilleurs Résultats

### **Images**

✅ **Soyez précis** : "Un chat tigré orange" > "Un chat"
✅ **Mentionnez le style** : "style digital art", "photorealistic"
✅ **Ajoutez des détails** : "lumière naturelle", "haute qualité"
✅ **Spécifiez l'ambiance** : "atmosphère mystérieuse", "couleurs vives"

### **Audio**

✅ **Ponctuez bien** : Utilisez des virgules et points
✅ **Ajoutez des pauses** : Utilisez "..." pour les pauses
✅ **Évitez les abréviations** : "Monsieur" > "M."
✅ **Texte clair** : Évitez les caractères spéciaux

---

## 📈 Aller Plus Loin

### **Galerie d'Images**

1. Allez dans "🎨 Images IA" → Onglet "Galerie"
2. Consultez toutes vos images
3. Filtrez par modèle
4. Téléchargez ou supprimez

### **Bibliothèque Audio**

1. Allez dans "🎙️ Audio IA" → Onglet "Bibliothèque"
2. Consultez tous vos fichiers audio
3. Réécoutez vos créations
4. Téléchargez ou supprimez

### **Combiner avec le Chat**

1. Utilisez le Chat Multi-IA pour générer des prompts
2. Copiez le prompt généré
3. Utilisez-le dans la génération d'images
4. Résultat : Images encore meilleures !

---

## 💰 Coûts Estimés

### **Images**

| Service | Coût par Image | 10 Images | 100 Images |
|---------|----------------|-----------|------------|
| **DALL-E 3** | $0.04-0.12 | $0.40-1.20 | $4-12 |
| **Stable Diffusion** | Variable | ~$0.50 | ~$5 |

### **Audio**

| Service | Coût | 1000 caractères | 10,000 caractères |
|---------|------|-----------------|-------------------|
| **ElevenLabs** | Gratuit (10k/mois) | Gratuit | Gratuit |
| **OpenAI TTS** | $15/1M chars | ~$0.015 | ~$0.15 |

---

## 🎯 Exemples de Projets

### **Projet 1 : Créer un Avatar**

1. Générez une image de portrait avec DALL-E 3
2. Prompt : "Professional headshot of a person, studio lighting"
3. Utilisez pour votre profil

### **Projet 2 : Podcast IA**

1. Écrivez votre script dans le Chat Multi-IA
2. Générez l'audio avec ElevenLabs
3. Téléchargez et publiez

### **Projet 3 : Illustrations de Blog**

1. Pour chaque section, générez une image
2. Utilisez Stable Diffusion pour réduire les coûts
3. Téléchargez et intégrez dans votre blog

---

## 📚 Ressources

### **Documentation**

- 📖 `GENERATION_MEDIA_IA.md` - Documentation complète
- 📖 `TOP_50_IA_INTEGREES.md` - Catalogue des 50 IA
- 📖 `.env.example` - Exemple de configuration

### **Liens Utiles**

- 🌐 OpenAI Platform : https://platform.openai.com
- 🌐 Stability AI : https://platform.stability.ai
- 🌐 ElevenLabs : https://elevenlabs.io
- 🌐 OpenAI Pricing : https://openai.com/pricing

---

## ✅ Checklist de Démarrage

- [ ] Clés API obtenues
- [ ] Fichier `.env` configuré
- [ ] WeBox lancé
- [ ] Connexion réussie
- [ ] Première image générée
- [ ] Premier audio généré
- [ ] Galerie consultée
- [ ] Médias téléchargés

---

## 🎉 Vous êtes Prêt !

**Vous pouvez maintenant :**

✅ Générer des images illimitées
✅ Créer de l'audio professionnel
✅ Gérer vos créations
✅ Télécharger tous vos médias
✅ Expérimenter avec différents styles

---

## 🆘 Besoin d'Aide ?

**Consultez :**
- 📖 `GENERATION_MEDIA_IA.md` pour la doc complète
- 📖 `TOP_50_IA_INTEGREES.md` pour toutes les IA
- ⚙️ Page "Configuration" dans WeBox

**Problème persistant ?**
- Vérifiez les logs dans le terminal
- Vérifiez votre connexion internet
- Vérifiez vos crédits API

---

**🚀 Bon Démarrage avec WeBox Multi-IA ! 🎨🎙️**
