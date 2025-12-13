# 🚀 INSTRUCTIONS APRÈS REDÉMARRAGE

## ⚡ IMPORTANT : Agir RAPIDEMENT après le redémarrage !

Le service LxssManager fonctionne maintenant, mais il se désactive après quelques secondes.
Vous devez lancer Ubuntu IMMÉDIATEMENT après le redémarrage.

---

## 📋 ÉTAPES À SUIVRE (Dans l'ordre exact)

### **1. Redémarrer Windows MAINTENANT**
```powershell
Restart-Computer -Force
```

### **2. Après le redémarrage (IMMÉDIATEMENT)**

**Option A : Via le Menu Démarrer (PLUS RAPIDE)**
1. Appuyer sur **Windows**
2. Taper **"Ubuntu"**
3. Cliquer sur **Ubuntu 22.04.5 LTS**
4. Attendre l'installation (1-2 minutes)
5. Créer un utilisateur :
   - Username : `webox`
   - Password : `admin123`

**Option B : Via PowerShell Admin**
```powershell
# Ouvrir PowerShell Admin RAPIDEMENT
# Exécuter IMMÉDIATEMENT :
wsl --install -d Ubuntu
```

---

## 🎯 Si Ubuntu s'installe avec succès

1. **Fermer Ubuntu**
2. **Lancer Docker Desktop**
3. **Attendre que Docker démarre** (icône verte)
4. **Installer PostgreSQL** :
   ```powershell
   cd C:\Users\Anthony\CascadeProjects\webox
   .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1
   ```

---

## ⚠️ Si Ubuntu échoue encore

Exécutez ce script qui va maintenir le service actif :

```powershell
cd C:\Users\Anthony\CascadeProjects\webox\scripts
.\MAINTENIR-SERVICE-WSL-ACTIF.ps1
```

Puis lancez Ubuntu pendant que le script tourne.

---

## 💡 Pourquoi ça va fonctionner maintenant ?

- ✅ Le pilote WSL 2 est installé
- ✅ WSL 2 est configuré par défaut
- ✅ Tous les services sont configurés
- ✅ Après le redémarrage, le service sera frais et stable

---

**REDÉMARREZ MAINTENANT ET LANCEZ UBUNTU IMMÉDIATEMENT !** 🚀

---

**Date :** 1er Novembre 2025 12:53  
**Objectif :** Installer Ubuntu avant que le service ne se désactive  
**Temps estimé :** 5 minutes après redémarrage
