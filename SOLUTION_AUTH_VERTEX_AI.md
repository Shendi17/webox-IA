# ✅ SOLUTION - Authentification Vertex AI

**Date:** 25 Mars 2026  
**Problème:** `Unable to authenticate your request` avec Vertex AI Imagen

---

## 🔍 PROBLÈME

Vertex AI Imagen échoue avec l'erreur:
```
Unable to authenticate your request.
Depending on your runtime environment, you can complete authentication by:
- if in local JupyterLab instance: `!gcloud auth login`
- if in Colab:
    -`from google.colab import auth`
    -`auth.authenticate_user()`
- if in service account or other: please follow guidance in https://cloud.google.com/docs/authentication
```

**Cause:** Les credentials Google Cloud ne sont pas correctement configurés pour `vertexai.init()`.

---

## ✅ CORRECTION APPLIQUÉE

### Configuration explicite des credentials

**Fichier:** `app/services/image_generation_service.py`

**Ajout avant `vertexai.init()`:**
```python
# Configurer les credentials avant d'initialiser
if self.google_credentials and os.path.exists(self.google_credentials):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.google_credentials

vertexai.init(project=self.vertex_project_id, location=self.vertex_location)
```

---

## 📋 VÉRIFICATION DE LA CONFIGURATION

### Fichier .env

Vérifier que ces variables sont bien définies:
```env
VERTEX_AI_PROJECT_ID=webox-482718
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json
```

### Fichier de credentials

Le fichier `webox-482718-f86837e5ce03.json` doit exister et contenir les credentials du service account.

**Vérification:**
```bash
# Vérifier que le fichier existe
ls C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json
```

---

## 🚀 REDÉMARRER LE SERVEUR

Après la correction, redémarrer le serveur:

```bash
# Arrêter le serveur (Ctrl+C)
.\start.ps1
```

---

## 🧪 TESTER VERTEX AI IMAGEN

1. Aller sur http://webox.local:8000/generation
2. Sélectionner **"Imagen 4 Standard"** (recommandé pour les tests)
3. Entrer un prompt simple: "A beautiful sunset over mountains"
4. Cliquer "Générer"

**Résultat attendu:**
- ✅ Génération réussie
- 🖼️ Image sauvegardée dans `generated/images/`
- ✅ Image affichée dans l'historique

---

## 📊 ALTERNATIVES SI LE PROBLÈME PERSISTE

### Option 1: Utiliser gcloud auth (Recommandé pour développement)

```bash
# Authentifier avec gcloud
gcloud auth application-default login

# Sélectionner le bon projet
gcloud config set project webox-482718
```

**Avantage:** Plus simple pour le développement local

### Option 2: Vérifier le service account

Le fichier JSON doit contenir:
```json
{
  "type": "service_account",
  "project_id": "webox-482718",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  ...
}
```

### Option 3: Tester avec DALL-E en attendant

Si Vertex AI pose problème, utiliser DALL-E qui fonctionne:
1. Sélectionner **"DALL-E 3 - Haute qualité"**
2. Générer une image
3. ✅ Devrait fonctionner immédiatement

---

## 🎯 PROVIDERS DISPONIBLES

### Providers fonctionnels (confirmés)
- ✅ **OpenAI DALL-E** - Fonctionne
- ✅ **Replicate Flux** - Fonctionne
- ✅ **Hugging Face SDXL** - Fonctionne (gratuit)
- ✅ **Stability AI SD 3.5** - Fonctionne

### Provider nécessitant authentification
- ⚠️ **Vertex AI Imagen** - Nécessite credentials Google Cloud

---

## 📝 NOTES IMPORTANTES

### Deprecation Warning

Le message suivant est normal et peut être ignoré:
```
UserWarning: This feature is deprecated as of June 24, 2025 and will be removed on June 24, 2026.
```

C'est un avertissement de Google concernant une future migration de l'API. Le code fonctionne toujours.

### Permissions requises

Le service account doit avoir les permissions:
- `Vertex AI User`
- `Storage Object Creator` (pour sauvegarder les images)

---

## 🔍 DIAGNOSTIC

### Test rapide des credentials

```python
import os
from dotenv import load_dotenv
load_dotenv()

creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"Credentials: {creds}")
print(f"Exists: {os.path.exists(creds) if creds else False}")
```

**Résultat attendu:**
```
Credentials: C:\Users\Anthony\CascadeProjects\webox\webox-482718-f86837e5ce03.json
Exists: True
```

---

**Statut:** ✅ **CORRECTION APPLIQUÉE**  
**Action requise:** **REDÉMARRER LE SERVEUR**  
**Alternative:** **Utiliser DALL-E si Vertex AI pose problème**
