# Configuration Vertex AI pour l'Île de la Réunion 🇷🇪

## 🎯 Votre situation

Vous êtes à l'Île de la Réunion et Google AI Studio n'est pas accessible dans votre région. Vous devez donc utiliser **Vertex AI** via Google Cloud Platform.

## ⚠️ Problème actuel

L'erreur que vous recevez indique que le système essaie d'utiliser **Generative Language API** (Google AI Studio) au lieu de **Vertex AI API**.

```
❌ Erreur: Generative Language API has not been used in project...
```

## ✅ Solution complète

### Étape 1 : Installer Google Cloud CLI

1. **Téléchargez** Google Cloud CLI :
   - Windows : https://cloud.google.com/sdk/docs/install#windows
   - Téléchargez l'installateur et exécutez-le

2. **Installez** en suivant l'assistant d'installation

3. **Redémarrez** votre terminal PowerShell

### Étape 2 : Authentification avec gcloud

Ouvrez PowerShell et exécutez :

```powershell
# Se connecter à Google Cloud
gcloud auth application-default login
```

- Une fenêtre de navigateur s'ouvrira
- Connectez-vous avec votre compte Google
- Autorisez l'accès

```powershell
# Configurer votre projet
gcloud config set project VOTRE-PROJECT-ID
```

Remplacez `VOTRE-PROJECT-ID` par votre ID de projet (dans votre cas : `26997462856` ou le nom du projet)

### Étape 3 : Activer l'API Vertex AI

**Option A : Via la console web**

1. Allez sur https://console.cloud.google.com/
2. Sélectionnez votre projet
3. Menu ☰ > APIs et services > Bibliothèque
4. Recherchez **"Vertex AI API"** (PAS "Generative Language API")
5. Cliquez sur **"Activer"**

**Option B : Via gcloud CLI**

```powershell
gcloud services enable aiplatform.googleapis.com
```

### Étape 4 : Configuration du fichier .env

Dans votre fichier `.env`, configurez :

```bash
# Vertex AI Configuration
VERTEX_AI_PROJECT_ID=26997462856
VERTEX_AI_LOCATION=europe-west1

# NE METTEZ PAS GOOGLE_APPLICATION_CREDENTIALS si vous utilisez gcloud auth
# NE METTEZ PAS GOOGLE_API_KEY (c'est pour Google AI Studio qui n'est pas accessible)
```

**Important** : 
- Utilisez `europe-west1` comme région (plus proche de la Réunion)
- Ne mettez PAS `GOOGLE_APPLICATION_CREDENTIALS` si vous utilisez `gcloud auth`
- Ne mettez PAS `GOOGLE_API_KEY`

### Étape 5 : Installer les dépendances Python

```powershell
pip install google-cloud-aiplatform
```

### Étape 6 : Redémarrer le serveur

```powershell
# Arrêtez le serveur (Ctrl+C si en cours)
# Puis relancez
python main.py
```

## 🔍 Vérification

Pour vérifier que tout est bien configuré :

```powershell
# Vérifier l'authentification
gcloud auth application-default print-access-token

# Vérifier le projet configuré
gcloud config get-value project

# Vérifier que l'API est activée
gcloud services list --enabled | findstr aiplatform
```

Vous devriez voir `aiplatform.googleapis.com` dans la liste.

## 📋 Checklist complète

- [ ] Google Cloud CLI installé
- [ ] Authentification avec `gcloud auth application-default login`
- [ ] Projet configuré avec `gcloud config set project`
- [ ] API Vertex AI activée (`aiplatform.googleapis.com`)
- [ ] Dépendance Python installée (`google-cloud-aiplatform`)
- [ ] `.env` configuré avec `VERTEX_AI_PROJECT_ID` et `VERTEX_AI_LOCATION`
- [ ] `.env` NE contient PAS `GOOGLE_API_KEY`
- [ ] Serveur redémarré

## 🌍 Régions disponibles pour Vertex AI

Pour l'Île de la Réunion, les meilleures régions sont :

1. **europe-west1** (Belgique) - RECOMMANDÉ
2. **europe-west4** (Pays-Bas)
3. **asia-southeast1** (Singapour)

Utilisez `europe-west1` dans votre `.env` :
```bash
VERTEX_AI_LOCATION=europe-west1
```

## ❓ Dépannage

### Erreur "Generative Language API"
✅ **Solution** : Vous avez configuré `GOOGLE_API_KEY` dans `.env`. Supprimez-le !

### Erreur "Permission denied"
```powershell
gcloud auth application-default login
```
Reconnectez-vous.

### Erreur "Project not found"
Vérifiez que `VERTEX_AI_PROJECT_ID` correspond bien à votre ID de projet :
```powershell
gcloud projects list
```

### Erreur "API not enabled"
```powershell
gcloud services enable aiplatform.googleapis.com
```

### Le modèle n'est pas disponible
Certains modèles Gemini 2.0 sont en preview. Essayez :
- `gemini-1.5-pro` (stable)
- `gemini-1.5-flash` (rapide et stable)

## 💰 Tarification Vertex AI

- **Gemini 1.5 Flash** : ~$0.075 / 1M tokens (entrée)
- **Gemini 1.5 Pro** : ~$1.25 / 1M tokens (entrée)
- Crédit gratuit de **$300** pour les nouveaux comptes Google Cloud

## 📞 Support

Si vous avez des problèmes :
1. Vérifiez que vous avez bien suivi toutes les étapes
2. Vérifiez les logs du serveur pour voir les erreurs détaillées
3. Assurez-vous que `GOOGLE_API_KEY` n'est PAS dans votre `.env`

## ✅ Configuration finale de votre .env

Voici exactement ce que vous devez avoir dans votre `.env` :

```bash
# ============================================
# VERTEX AI (pour Île de la Réunion)
# ============================================
VERTEX_AI_PROJECT_ID=26997462856
VERTEX_AI_LOCATION=europe-west1

# NE PAS METTRE :
# GOOGLE_API_KEY=...  ❌ (ne fonctionne pas à la Réunion)
# GOOGLE_APPLICATION_CREDENTIALS=...  ❌ (utilisez gcloud auth à la place)
```

Après cette configuration, Gemini fonctionnera via Vertex AI ! 🎉
