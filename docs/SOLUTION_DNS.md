# 🔧 Solution au Problème DNS - webox.local

## ❌ Problème Actuel

```
http://webox.local/ 
Ce site est inaccessible
L'adresse DNS de webox.local est introuvable
DNS_PROBE_POSSIBLE
```

**Cause :** Le fichier hosts Windows n'a pas été configuré pour résoudre `webox.local` vers `127.0.0.1`

---

## ✅ Solution Automatique (RECOMMANDÉE)

### Étape 1 : Ouvrir PowerShell en Administrateur

1. **Appuyez sur** `Windows + X`
2. **Sélectionnez** "Terminal (Admin)" ou "Windows PowerShell (Admin)"
3. **Cliquez sur** "Oui" pour autoriser

### Étape 2 : Naviguer vers le dossier

```powershell
cd c:\Users\Anthony\CascadeProjects\webox
```

### Étape 3 : Exécuter le script de correction

```powershell
.\fix-webox-local.ps1
```

### Étape 4 : Tester

Ouvrez votre navigateur et accédez à :
```
http://webox.local:8501
```

⚠️ **IMPORTANT : N'oubliez pas le port `:8501`**

---

## 🔧 Solution Manuelle (Alternative)

Si le script ne fonctionne pas, voici la méthode manuelle :

### Étape 1 : Ouvrir le fichier hosts

1. **Ouvrez Notepad en tant qu'Administrateur**
   - Clic droit sur Notepad → "Exécuter en tant qu'administrateur"

2. **Ouvrez le fichier :**
   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

### Étape 2 : Ajouter l'entrée

À la fin du fichier, ajoutez cette ligne :

```
127.0.0.1    webox.local
```

### Étape 3 : Sauvegarder

- **Fichier** → **Enregistrer**
- Fermez Notepad

### Étape 4 : Vider le cache DNS

Ouvrez PowerShell (en admin) et exécutez :

```powershell
ipconfig /flushdns
```

### Étape 5 : Tester

Ouvrez votre navigateur et accédez à :
```
http://webox.local:8501
```

---

## 🌐 URLs Disponibles

Après configuration, vous pourrez accéder à l'application via :

| URL | Description |
|-----|-------------|
| `http://localhost:8501` | ✅ Fonctionne toujours (par défaut) |
| `http://127.0.0.1:8501` | ✅ Fonctionne toujours (par défaut) |
| `http://webox.local:8501` | ✅ Après configuration du fichier hosts |

⚠️ **Note Importante :** Le port `:8501` est OBLIGATOIRE car Streamlit écoute sur ce port.

---

## ❓ Pourquoi webox.local et pas juste webox.local ?

**Question :** Pourquoi dois-je utiliser `http://webox.local:8501` ?

**Réponse :** 
- Streamlit est un serveur Python qui écoute sur le port **8501**
- Le port **80** (HTTP par défaut) n'est pas utilisé
- Vous devez donc spécifier le port `:8501`

### Option : Utiliser le port 80 (Avancé)

Si vous voulez vraiment utiliser `http://webox.local` sans port :

1. **Arrêtez l'application actuelle** (Ctrl+C)

2. **Lancez sur le port 80** (nécessite les droits admin) :
   ```powershell
   streamlit run app.py --server.port 80
   ```

3. **Accédez à :**
   ```
   http://webox.local
   ```

⚠️ **Inconvénient :** Nécessite des droits administrateur à chaque lancement.

---

## 🔍 Vérification

### Vérifier que le fichier hosts est correct

```powershell
Get-Content C:\Windows\System32\drivers\etc\hosts | Select-String "webox"
```

**Résultat attendu :**
```
127.0.0.1    webox.local
```

### Tester la résolution DNS

```powershell
ping webox.local
```

**Résultat attendu :**
```
Envoi d'une requête 'ping' sur webox.local [127.0.0.1]...
```

---

## 🐛 Problèmes Courants

### 1. "Accès refusé" lors de la modification du fichier hosts

**Solution :** Vous devez exécuter PowerShell ou Notepad **en tant qu'Administrateur**

### 2. "Le site est toujours inaccessible"

**Solutions :**
1. Videz le cache DNS : `ipconfig /flushdns`
2. Redémarrez le navigateur
3. Essayez en navigation privée
4. Vérifiez que Streamlit est bien lancé

### 3. "ERR_CONNECTION_REFUSED"

**Solution :** L'application Streamlit n'est pas lancée. Exécutez :
```powershell
.\lancer-webox.ps1
```

### 4. "DNS_PROBE_POSSIBLE" persiste

**Solutions :**
1. Vérifiez le fichier hosts : `notepad C:\Windows\System32\drivers\etc\hosts`
2. Assurez-vous que la ligne est bien : `127.0.0.1    webox.local`
3. Pas de `#` devant la ligne
4. Videz le cache DNS : `ipconfig /flushdns`

---

## 💡 Recommandation Finale

**Pour simplifier, utilisez simplement :**

```
http://localhost:8501
```

C'est plus simple et fonctionne immédiatement sans configuration !

---

## 📞 Besoin d'Aide ?

Si le problème persiste après avoir suivi ces étapes :

1. Vérifiez que l'application est bien lancée : `.\lancer-webox.ps1`
2. Testez avec `http://localhost:8501` d'abord
3. Consultez les logs dans le terminal PowerShell

---

## ✅ Checklist de Vérification

- [ ] PowerShell ouvert en tant qu'Administrateur
- [ ] Script `fix-webox-local.ps1` exécuté
- [ ] Cache DNS vidé (`ipconfig /flushdns`)
- [ ] Application Streamlit lancée
- [ ] Port `:8501` inclus dans l'URL
- [ ] Navigateur redémarré

---

**Une fois configuré, webox.local fonctionnera parfaitement ! 🚀**
