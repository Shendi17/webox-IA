# 🌐 Configuration de webox.local

## ✅ STATUT ACTUEL

Le fichier `hosts` est **déjà configuré** avec l'entrée :
```
127.0.0.1    webox.local
```

---

## 🚀 ACCÈS À L'APPLICATION

### **Option 1 : Avec le port 8000 (RECOMMANDÉ)**

#### Démarrage
```powershell
.\start_webox_local.ps1
```

#### Accès
```
http://webox.local:8000
```

**Avantages :**
- ✅ Pas besoin de droits administrateur
- ✅ Pas de conflit avec d'autres services
- ✅ Configuration standard

---

### **Option 2 : Sans port (port 80)**

#### Démarrage (nécessite admin)
```powershell
# Clic droit sur PowerShell > Exécuter en tant qu'administrateur
.\start_webox_port80.ps1
```

#### Accès
```
http://webox.local
```

**Avantages :**
- ✅ URL plus courte
- ✅ Pas besoin de spécifier le port

**Inconvénients :**
- ⚠️ Nécessite les droits administrateur
- ⚠️ Le port 80 peut être utilisé par d'autres services (IIS, Apache, etc.)

---

## 🔧 CONFIGURATION MANUELLE

### 1. Vérifier le fichier hosts

**Emplacement :**
```
C:\Windows\System32\drivers\etc\hosts
```

**Contenu requis :**
```
127.0.0.1    webox.local
```

### 2. Vider le cache DNS (si nécessaire)

```powershell
ipconfig /flushdns
```

### 3. Tester la résolution DNS

```powershell
ping webox.local
```

**Résultat attendu :**
```
Envoi d'une requête 'ping' sur webox.local [127.0.0.1]
```

---

## 🐛 DÉPANNAGE

### Problème 1 : "webox.local" ne se résout pas

**Solution :**
```powershell
# Vider le cache DNS
ipconfig /flushdns

# Vérifier le fichier hosts
notepad C:\Windows\System32\drivers\etc\hosts

# Ajouter si absent :
127.0.0.1    webox.local
```

### Problème 2 : Port 80 déjà utilisé

**Identifier le processus :**
```powershell
Get-NetTCPConnection -LocalPort 80 | Select-Object OwningProcess
```

**Arrêter le processus :**
```powershell
Stop-Process -Id <PID> -Force
```

**OU utiliser le port 8000 :**
```powershell
.\start_webox_local.ps1
# Accès : http://webox.local:8000
```

### Problème 3 : "Accès refusé" sur le port 80

**Cause :** Le port 80 nécessite des droits administrateur sous Windows

**Solution :**
1. Clic droit sur PowerShell
2. "Exécuter en tant qu'administrateur"
3. Relancer le script

**OU utiliser le port 8000 (pas besoin d'admin) :**
```powershell
.\start_webox_local.ps1
```

### Problème 4 : Le serveur ne démarre pas

**Vérifier les dépendances :**
```powershell
pip install -r requirements_fastapi.txt
```

**Vérifier le port :**
```powershell
# Voir si le port est utilisé
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

---

## 📊 COMPARAISON DES OPTIONS

| Aspect | Port 8000 | Port 80 |
|--------|-----------|---------|
| **URL** | `http://webox.local:8000` | `http://webox.local` |
| **Droits admin** | ❌ Non requis | ✅ Requis |
| **Conflits** | ❌ Rares | ⚠️ Possibles (IIS, Apache) |
| **Configuration** | ✅ Simple | ⚠️ Complexe |
| **Recommandé** | ✅ Oui | ⚠️ Optionnel |

---

## 🎯 RECOMMANDATION

**Utilise le port 8000 (Option 1) :**
```powershell
.\start_webox_local.ps1
```

**Accès :**
```
http://webox.local:8000
```

**Pourquoi ?**
- ✅ Pas besoin de droits admin
- ✅ Pas de conflits avec d'autres services
- ✅ Configuration standard pour le développement
- ✅ Plus simple et plus fiable

---

## 🚀 DÉMARRAGE RAPIDE

### 1. Ouvrir PowerShell
```powershell
cd C:\Users\Anthony\CascadeProjects\webox
```

### 2. Lancer le serveur
```powershell
.\start_webox_local.ps1
```

### 3. Ouvrir le navigateur
```
http://webox.local:8000
```

---

## ✅ URLS DISPONIBLES

Une fois le serveur démarré, tu peux accéder à :

### Avec webox.local
- `http://webox.local:8000` - Landing page
- `http://webox.local:8000/login` - Connexion
- `http://webox.local:8000/register` - Inscription
- `http://webox.local:8000/dashboard` - Dashboard
- `http://webox.local:8000/docs` - Documentation API

### Avec localhost (équivalent)
- `http://localhost:8000`
- `http://127.0.0.1:8000`

---

## 🔐 COMPTE DE TEST

```
Email: admin@webox.com
Mot de passe: admin123
```

---

## 📝 NOTES

- Le fichier `hosts` est **déjà configuré** ✅
- L'entrée `127.0.0.1 webox.local` existe déjà (ligne 37)
- Pas besoin de modifier le fichier hosts
- Il suffit de démarrer le serveur avec le bon script

---

## 🎉 C'EST PRÊT !

Lance simplement :
```powershell
.\start_webox_local.ps1
```

Et accède à :
```
http://webox.local:8000
```
