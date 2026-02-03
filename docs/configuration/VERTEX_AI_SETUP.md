# Configuration Vertex AI pour WeBox

## 📋 Prérequis

Vous avez déjà :
- ✅ Un projet Google Cloud
- ✅ L'ID du projet
- ✅ Un fichier de credentials JSON (clé de compte de service)

## 🔧 Configuration dans WeBox

### 1. Ajouter les variables dans le fichier `.env`

Ouvrez votre fichier `.env` et ajoutez ces lignes :

```bash
# Vertex AI (Google Cloud)
VERTEX_AI_PROJECT_ID=votre-project-id
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=C:/chemin/vers/votre-credentials.json
```

### 2. Détails des variables

**VERTEX_AI_PROJECT_ID**
- Votre ID de projet Google Cloud
- Exemple : `mon-projet-123456`
- Trouvable dans : Google Cloud Console > Tableau de bord

**VERTEX_AI_LOCATION**
- Région où Vertex AI est activé
- Valeur par défaut : `us-central1`
- Autres options : `europe-west1`, `asia-southeast1`, etc.
- Choisissez la région la plus proche de votre localisation

**GOOGLE_APPLICATION_CREDENTIALS**
- Chemin COMPLET vers votre fichier JSON de credentials
- Exemple Windows : `C:/Users/Anthony/google-credentials.json`
- Exemple Linux/Mac : `/home/anthony/google-credentials.json`
- ⚠️ Utilisez des slashes `/` même sous Windows

### 3. Obtenir le fichier de credentials JSON

Si vous n'avez pas encore le fichier JSON :

1. Allez sur https://console.cloud.google.com/
2. Sélectionnez votre projet
3. Menu ☰ > IAM et administration > Comptes de service
4. Cliquez sur votre compte de service (ou créez-en un)
5. Onglet "Clés" > "Ajouter une clé" > "Créer une clé"
6. Choisissez "JSON" et téléchargez le fichier
7. Placez le fichier dans un endroit sûr sur votre ordinateur
8. Copiez le chemin complet dans `.env`

### 4. Activer l'API Vertex AI

1. Allez sur https://console.cloud.google.com/
2. Menu ☰ > APIs et services > Bibliothèque
3. Recherchez "Vertex AI API"
4. Cliquez sur "Activer"

### 5. Permissions requises

Votre compte de service doit avoir les rôles :
- `Vertex AI User` ou `Vertex AI Administrator`
- `Service Account Token Creator` (optionnel)

Pour vérifier/ajouter :
1. Menu ☰ > IAM et administration > IAM
2. Trouvez votre compte de service
3. Cliquez sur ✏️ Modifier
4. Ajoutez les rôles si nécessaires

## 🚀 Utilisation

Une fois configuré :

1. **Redémarrez votre serveur WeBox**
   ```bash
   # Arrêtez le serveur (Ctrl+C)
   # Puis relancez
   python main.py
   ```

2. **Testez dans le Chat Multi-IA**
   - Cochez "✨ Gemini 2.0 Flash"
   - Envoyez un message
   - Vous utilisez maintenant Vertex AI !

## 🔍 Vérification

Le système détecte automatiquement :
- Si Vertex AI est configuré → Utilise Vertex AI
- Sinon, si Google AI API Key existe → Utilise Google AI Studio
- Sinon → Affiche un message d'erreur

## 💰 Tarification Vertex AI

- **Gemini 2.0 Flash** : ~$0.075 / 1M tokens (entrée)
- **Gemini 1.5 Pro** : ~$1.25 / 1M tokens (entrée)
- Crédit gratuit de $300 pour les nouveaux comptes Google Cloud

## ❓ Dépannage

### Erreur "Project not found"
- Vérifiez que `VERTEX_AI_PROJECT_ID` est correct
- Vérifiez que l'API Vertex AI est activée

### Erreur "Permission denied"
- Vérifiez les permissions du compte de service
- Ajoutez le rôle "Vertex AI User"

### Erreur "Credentials not found"
- Vérifiez le chemin dans `GOOGLE_APPLICATION_CREDENTIALS`
- Utilisez un chemin absolu complet
- Vérifiez que le fichier JSON existe

### Le modèle n'est pas disponible
- Certains modèles ne sont disponibles que dans certaines régions
- Essayez de changer `VERTEX_AI_LOCATION`
- Consultez : https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models

## 📚 Ressources

- Documentation Vertex AI : https://cloud.google.com/vertex-ai/docs
- Modèles disponibles : https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models
- Tarification : https://cloud.google.com/vertex-ai/pricing
- Console Google Cloud : https://console.cloud.google.com/

## ✅ Exemple de configuration complète

```bash
# Dans votre fichier .env

# Vertex AI (Google Cloud)
VERTEX_AI_PROJECT_ID=mon-projet-webox-123456
VERTEX_AI_LOCATION=europe-west1
GOOGLE_APPLICATION_CREDENTIALS=C:/Users/Anthony/Documents/webox-vertex-credentials.json
```

Après avoir configuré ces 3 variables, Vertex AI sera automatiquement utilisé pour Gemini ! 🎉
