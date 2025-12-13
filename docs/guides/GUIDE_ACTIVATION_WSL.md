# 🐧 Guide d'Activation de WSL pour Docker PostgreSQL

## Étapes Complètes

### Étape 1 : Activer WSL (Administrateur requis)

1. **Ouvrir PowerShell en tant qu'administrateur**
   - Clic droit sur le menu Démarrer
   - Sélectionner "Terminal (Admin)" ou "PowerShell (Admin)"

2. **Naviguer vers le dossier scripts**
   ```powershell
   cd C:\Users\Anthony\CascadeProjects\webox\scripts
   ```

3. **Exécuter le script d'activation**
   ```powershell
   .\ACTIVER-WSL.ps1
   ```

4. **Redémarrer Windows** (obligatoire)

---

### Étape 2 : Installer WSL 2 (Après redémarrage)

1. **Ouvrir PowerShell en tant qu'administrateur**

2. **Installer WSL 2**
   ```powershell
   wsl --install
   ```

3. **Redémarrer Windows** (obligatoire)

---

### Étape 3 : Configurer WSL (Après 2ème redémarrage)

1. **Ouvrir PowerShell**

2. **Définir WSL 2 comme version par défaut**
   ```powershell
   wsl --set-default-version 2
   ```

3. **Vérifier l'installation**
   ```powershell
   wsl --status
   ```

---

### Étape 4 : Lancer Docker Desktop

1. **Ouvrir Docker Desktop**
   - Il devrait maintenant démarrer sans erreur WSL

2. **Attendre que Docker soit complètement démarré**
   - L'icône Docker dans la barre des tâches devient verte

---

### Étape 5 : Installer PostgreSQL Docker

1. **Ouvrir PowerShell** (pas besoin d'admin)

2. **Naviguer vers le dossier**
   ```powershell
   cd C:\Users\Anthony\CascadeProjects\webox
   ```

3. **Exécuter le script**
   ```powershell
   .\scripts\INSTALLER-DOCKER-POSTGRESQL.ps1
   ```

---

## Temps Estimé

- **Étape 1 :** 2 minutes + redémarrage (2 min)
- **Étape 2 :** 5 minutes + redémarrage (2 min)
- **Étape 3 :** 1 minute
- **Étape 4 :** 2 minutes
- **Étape 5 :** 2 minutes

**Total :** ~15-20 minutes (incluant les redémarrages)

---

## Vérifications

### Vérifier WSL
```powershell
wsl --status
wsl --list --verbose
```

### Vérifier Docker
```powershell
docker --version
docker ps
```

### Vérifier PostgreSQL
```powershell
docker ps | Select-String "webox-postgres"
docker logs webox-postgres
```

---

## En Cas de Problème

### WSL ne s'installe pas
- Vérifier que la virtualisation est activée dans le BIOS
- Vérifier Windows Update (WSL nécessite Windows 10 version 2004+ ou Windows 11)

### Docker ne démarre pas
- Vérifier que WSL 2 est bien installé : `wsl --status`
- Redémarrer Docker Desktop
- Redémarrer Windows

### PostgreSQL ne démarre pas
- Vérifier les logs : `docker logs webox-postgres`
- Vérifier que le port 5432 n'est pas utilisé : `netstat -ano | findstr :5432`

---

## Après Installation Réussie

1. **Créer les tables**
   ```powershell
   python create_tables.py
   ```

2. **Créer l'utilisateur admin**
   ```powershell
   python create_test_user.py
   ```

3. **Lancer le backend**
   ```powershell
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Tester la connexion**
   - http://webox.local:8000/login
   - Email : admin@webox.com
   - Password : admin123

---

**Date :** 31 Octobre 2025  
**Objectif :** Activer WSL pour Docker PostgreSQL  
**Durée estimée :** 15-20 minutes
