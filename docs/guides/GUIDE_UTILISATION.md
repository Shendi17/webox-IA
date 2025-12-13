# 📖 Guide d'Utilisation - WeBox Multi-IA

**Version :** 2.0.0  
**Date :** 1er Novembre 2025

---

## 🚀 DÉMARRAGE RAPIDE

### **1. Lancer l'application**

```powershell
# Dans le dossier du projet
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **2. Accéder à l'application**

Ouvrez votre navigateur et allez sur :
```
http://webox.local:8000
```

### **3. Se connecter**

- **Email :** admin@webox.com
- **Mot de passe :** admin123

---

## 🎯 FONCTIONNALITÉS DISPONIBLES

### **📊 1. Dashboard**

**Accès :** Page d'accueil après connexion

**Fonctionnalités :**
- ✅ Statistiques en temps réel
  - Nombre total de conversations
  - Nombre de messages
  - Activité de la semaine
  - Temps de réponse moyen
- ✅ Top 5 des IA les plus utilisées
- ✅ Accès rapide à toutes les fonctionnalités

**Actions :**
- Cliquez sur n'importe quelle card pour accéder à la fonctionnalité

---

### **💬 2. Chat Multi-IA**

**Accès :** Dashboard → Chat Multi-IA

**Fonctionnalités :**
- ✅ Discuter avec plusieurs IA simultanément
- ✅ Sélection des modèles IA
- ✅ Historique des conversations
- ✅ Paramètres personnalisables

**Comment utiliser :**
1. Sélectionnez les IA dans le sidebar (GPT-4, Claude, Gemini, etc.)
2. Tapez votre message dans la zone de texte
3. Cliquez sur "Envoyer"
4. Les réponses de toutes les IA sélectionnées s'affichent

**⚠️ Prérequis :**
- Au moins une clé API configurée dans `.env`
- Exemples :
  ```env
  OPENAI_API_KEY=sk-...
  ANTHROPIC_API_KEY=sk-ant-...
  GOOGLE_API_KEY=AIza...
  ```

---

### **🤖 3. Agents IA Spécialisés**

**Accès :** Dashboard → Agents IA Spécialisés

**8 Agents disponibles :**

1. **💰 Agent Ventes**
   - Prospection et closing
   - Génération de leads
   - Qualification de prospects

2. **📢 Agent Marketing**
   - Stratégie marketing
   - Création de contenu
   - Campagnes publicitaires

3. **💵 Agent Finance**
   - Analyse financière
   - Gestion de budget
   - Prévisions

4. **⚙️ Agent Opérations**
   - Optimisation des processus
   - Automatisation
   - Gestion de projet

5. **👤 Agent RH**
   - Recrutement
   - Formation
   - Gestion des talents

6. **💬 Agent Service Client**
   - Support 24/7
   - Réponses automatiques
   - Satisfaction client

7. **🎯 Agent Produit**
   - Roadmap produit
   - UX/UI
   - Feedback utilisateurs

8. **🎯 Agent Stratégie**
   - Vision d'entreprise
   - Planification stratégique
   - Analyse concurrentielle

**Comment utiliser :**
1. Cliquez sur "Lancer l'agent"
2. Une fenêtre de chat s'ouvre
3. Posez votre question ou décrivez votre besoin
4. L'agent répond avec son expertise spécialisée
5. Continuez la conversation

**💡 Astuce :** Chaque agent est optimisé pour son domaine d'expertise !

---

### **📚 4. Bibliothèque de Prompts**

**Accès :** Dashboard → Bibliothèque de Prompts

**Fonctionnalités :**
- ✅ Créer des prompts personnalisés
- ✅ Organiser par catégories
- ✅ Ajouter des tags
- ✅ Marquer comme favoris
- ✅ Rechercher et filtrer
- ✅ Copier dans le presse-papiers
- ✅ Compteur d'utilisation

**Comment utiliser :**

**Créer un prompt :**
1. Cliquez sur "➕ Nouveau Prompt"
2. Remplissez le formulaire :
   - Titre
   - Contenu du prompt
   - Catégorie
   - Tags (séparés par des virgules)
   - Cochez "Favori" si nécessaire
3. Cliquez sur "Enregistrer"

**Utiliser un prompt :**
1. Trouvez votre prompt dans la grille
2. Cliquez sur "✨ Utiliser"
3. Le prompt est copié dans votre presse-papiers
4. Collez-le dans le Chat Multi-IA ou ailleurs

**Rechercher :**
- Utilisez la barre de recherche
- Filtrez par catégorie
- Cliquez sur "⭐ Favoris" pour voir uniquement vos favoris

---

### **🎨 5. Génération Multi-Média**

**Accès :** Dashboard → Génération Multi-Média

**3 Onglets disponibles :**

#### **🖼️ Images**
- Modèles : DALL-E 3, Stable Diffusion, Midjourney, Leonardo AI
- Tailles : 1024x1024, 1024x1792, 1792x1024
- Styles : Naturel, Vivid, Artistique

**Comment utiliser :**
1. Sélectionnez le modèle IA
2. Décrivez l'image dans le champ "Description"
3. Choisissez la taille et le style
4. Cliquez sur "🎨 Générer l'image"

#### **🎬 Vidéos**
- Modèles : Runway ML, Pika Labs, Luma AI
- 🚧 En développement

#### **🎙️ Audio**
- Modèles : Suno AI, Udio, ElevenLabs
- 🚧 En développement

**⚠️ Note :** Les fonctionnalités de génération nécessitent des clés API spécifiques.

---

### **👤 6. Mon Profil**

**Accès :** Dashboard → Mon Profil

**Fonctionnalités :**
- Voir vos informations
- Modifier vos préférences
- Gérer vos clés API
- Consulter vos statistiques

---

## 🔑 CONFIGURATION DES CLÉS API

Pour utiliser pleinement l'application, configurez vos clés API dans le fichier `.env` :

### **Chat Multi-IA**

```env
# OpenAI (GPT-4, GPT-3.5)
OPENAI_API_KEY=sk-...

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-...

# Google (Gemini)
GOOGLE_API_KEY=AIza...

# Mistral AI
MISTRAL_API_KEY=...
```

### **Génération d'Images**

```env
# Stability AI (Stable Diffusion)
STABILITY_API_KEY=...

# Leonardo AI
LEONARDO_API_KEY=...
```

### **Audio/Voix**

```env
# ElevenLabs
ELEVENLABS_API_KEY=...

# Google Cloud TTS
GOOGLE_CLOUD_API_KEY=...
```

### **Où obtenir les clés ?**

- **OpenAI :** https://platform.openai.com/api-keys
- **Anthropic :** https://console.anthropic.com/
- **Google :** https://makersuite.google.com/app/apikey
- **Stability AI :** https://platform.stability.ai/
- **ElevenLabs :** https://elevenlabs.io/

---

## 💡 ASTUCES & CONSEILS

### **Pour le Chat Multi-IA**

1. **Comparez les réponses** - Utilisez plusieurs IA pour avoir différentes perspectives
2. **Ajustez la température** - Plus basse = plus précis, plus haute = plus créatif
3. **Sauvegardez vos conversations** - L'historique est automatiquement enregistré

### **Pour les Agents**

1. **Soyez spécifique** - Plus votre demande est précise, meilleure sera la réponse
2. **Utilisez le bon agent** - Chaque agent est spécialisé dans son domaine
3. **Continuez la conversation** - Les agents gardent le contexte

### **Pour les Prompts**

1. **Organisez par catégories** - Créez des catégories claires (Marketing, Code, Ventes, etc.)
2. **Utilisez des tags** - Facilitez la recherche avec des tags pertinents
3. **Testez et affinez** - Améliorez vos prompts au fil du temps
4. **Partagez** - Marquez comme "Public" pour partager avec l'équipe

---

## 🐛 RÉSOLUTION DE PROBLÈMES

### **Problème : "Erreur lors de l'envoi du message"**

**Solutions :**
1. Vérifiez que vous avez configuré au moins une clé API dans `.env`
2. Vérifiez que la clé API est valide
3. Vérifiez votre connexion internet
4. Redémarrez le backend

### **Problème : "Non authentifié"**

**Solutions :**
1. Reconnectez-vous
2. Videz le cache du navigateur
3. Vérifiez que les cookies sont activés

### **Problème : "Les statistiques ne s'affichent pas"**

**Solutions :**
1. Rafraîchissez la page (F5)
2. Créez quelques conversations pour avoir des données
3. Vérifiez la console du navigateur (F12)

### **Problème : "L'agent ne répond pas"**

**Solutions :**
1. Vérifiez qu'une clé API est configurée
2. Attendez quelques secondes (l'IA peut prendre du temps)
3. Vérifiez votre quota API

---

## 📊 STATISTIQUES & MÉTRIQUES

### **Dashboard**

Le dashboard affiche automatiquement :
- Nombre total de conversations créées
- Nombre total de messages envoyés
- Conversations créées cette semaine
- Temps de réponse moyen des IA
- Top 5 des IA les plus utilisées

### **Mise à jour**

Les statistiques se mettent à jour :
- Automatiquement au chargement de la page
- En temps réel après chaque action

---

## 🎓 EXEMPLES D'UTILISATION

### **Exemple 1 : Créer une stratégie marketing**

1. Allez sur "Agents IA Spécialisés"
2. Cliquez sur "Lancer l'agent" pour l'Agent Marketing
3. Demandez : "Crée-moi une stratégie marketing pour lancer un nouveau produit SaaS"
4. L'agent vous fournit une stratégie complète

### **Exemple 2 : Comparer des réponses IA**

1. Allez sur "Chat Multi-IA"
2. Sélectionnez GPT-4, Claude et Gemini
3. Posez une question complexe
4. Comparez les 3 réponses pour avoir une vue d'ensemble

### **Exemple 3 : Créer une bibliothèque de prompts**

1. Allez sur "Bibliothèque de Prompts"
2. Créez des prompts pour vos tâches récurrentes :
   - "Email de prospection B2B"
   - "Analyse de données financières"
   - "Rédaction d'article de blog SEO"
3. Utilisez-les rapidement quand vous en avez besoin

---

## 🚀 PROCHAINES FONCTIONNALITÉS

### **En développement :**

- 🎬 Génération de vidéos (Runway ML, Pika Labs)
- 🎵 Génération de musique (Suno AI, Udio)
- 📞 Assistant vocal avec reconnaissance vocale
- 🤝 Collaboration en équipe
- 📁 Gestionnaire de médias avancé
- ⚡ Automatisation Pipedream
- 🔧 Catalogue d'outils IA étendu

---

## 📞 SUPPORT

Pour toute question ou problème :

1. Consultez ce guide
2. Vérifiez la console du navigateur (F12)
3. Vérifiez les logs du backend
4. Consultez `FONCTIONNALITES_IMPLEMENTEES.md`

---

## 🎉 CONCLUSION

**WeBox Multi-IA** est votre plateforme tout-en-un pour l'intelligence artificielle !

**Profitez de toutes les fonctionnalités et n'hésitez pas à explorer ! 🚀**

---

**Bon travail avec WeBox Multi-IA ! 🤖✨**
