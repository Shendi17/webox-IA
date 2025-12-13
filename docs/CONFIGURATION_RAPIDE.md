# ⚡ Configuration Rapide - WeBox Multi-IA

## 🎯 Étapes Simples

### 1️⃣ Les dépendances sont déjà installées ✅

### 2️⃣ Configurer vos Clés API

Le fichier `.env` a été créé. **Ouvrez-le avec Notepad** et ajoutez vos clés API :

```env
# Au minimum UNE clé API est nécessaire
OPENAI_API_KEY=sk-votre-clé-openai-ici
ANTHROPIC_API_KEY=sk-ant-votre-clé-anthropic-ici
GOOGLE_API_KEY=AIza-votre-clé-google-ici
```

#### 🔑 Où obtenir les clés API ?

**OpenAI (GPT-4) - RECOMMANDÉ POUR COMMENCER**
1. Allez sur https://platform.openai.com/api-keys
2. Créez un compte si nécessaire
3. Cliquez sur "Create new secret key"
4. Copiez la clé (commence par `sk-`)
5. Collez-la dans `.env` : `OPENAI_API_KEY=sk-...`

**Anthropic (Claude)**
1. Allez sur https://console.anthropic.com/
2. Créez un compte
3. Générez une clé API
4. Copiez la clé (commence par `sk-ant-`)
5. Collez-la dans `.env` : `ANTHROPIC_API_KEY=sk-ant-...`

**Google AI (Gemini)**
1. Allez sur https://makersuite.google.com/app/apikey
2. Cliquez sur "Create API Key"
3. Copiez la clé (commence par `AIza`)
4. Collez-la dans `.env` : `GOOGLE_API_KEY=AIza...`

---

### 3️⃣ Lancer l'Application

**Méthode Simple :**
```powershell
.\lancer-webox.ps1
```

**Ou directement :**
```powershell
streamlit run app.py
```

---

### 4️⃣ Accéder à l'Application

L'application s'ouvrira automatiquement dans votre navigateur à :
- **http://localhost:8501**

---

## 🌐 Configuration de webox.local (OPTIONNEL)

Si vous voulez accéder via **http://webox.local:8501** :

### Option A : Configuration Manuelle

1. **Ouvrez PowerShell en tant qu'Administrateur**
   - Clic droit sur PowerShell → "Exécuter en tant qu'administrateur"

2. **Exécutez :**
   ```powershell
   cd c:\Users\Anthony\CascadeProjects\webox
   .\configure-hosts.ps1
   ```

3. **Accédez à :**
   - http://webox.local:8501

### Option B : Configuration Manuelle du fichier hosts

1. **Ouvrez en tant qu'Administrateur :**
   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

2. **Ajoutez cette ligne à la fin :**
   ```
   127.0.0.1    webox.local
   ```

3. **Sauvegardez et fermez**

4. **Accédez à :**
   - http://webox.local:8501

---

## ✅ Vérification

### Test 1 : Vérifier que Streamlit fonctionne
```powershell
streamlit --version
```
Devrait afficher : `Streamlit, version 1.50.0` (ou supérieur)

### Test 2 : Vérifier les clés API
Ouvrez `.env` et vérifiez que vous avez au moins une clé configurée.

### Test 3 : Lancer l'application
```powershell
.\lancer-webox.ps1
```

---

## 🐛 Problèmes Courants

### "Aucune IA configurée"
**Solution :** Vérifiez que vos clés API sont correctement configurées dans `.env`

### "streamlit: command not found"
**Solution :**
```powershell
pip install streamlit --upgrade
```

### Le navigateur ne s'ouvre pas
**Solution :** Ouvrez manuellement http://localhost:8501

### Port déjà utilisé
**Solution :** Changez le port
```powershell
streamlit run app.py --server.port 8502
```

---

## 📝 Récapitulatif

```
✅ Dépendances installées
⏳ Configurer .env avec vos clés API
⏳ Lancer avec .\lancer-webox.ps1
⏳ Accéder à http://localhost:8501
```

---

## 🎉 C'est Prêt !

Une fois vos clés API configurées, lancez simplement :

```powershell
.\lancer-webox.ps1
```

Et profitez de WeBox Multi-IA ! 🚀
