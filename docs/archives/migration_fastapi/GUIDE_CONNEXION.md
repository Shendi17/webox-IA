# 🔐 GUIDE DE CONNEXION - WeBox Multi-IA

## ✅ PROBLÈME RÉSOLU !

Le problème de connexion a été **corrigé**. Les routes utilisent maintenant correctement `Form(...)` pour lire les données du formulaire.

---

## 🚀 COMMENT SE CONNECTER

### **Étape 1 : Ouvrir la page de connexion**

Dans ton navigateur, va sur :
```
http://webox.local:8000/login
```

### **Étape 2 : Entrer les identifiants**

**Compte Admin par défaut :**
```
Email: admin@webox.com
Mot de passe: admin123
```

### **Étape 3 : Cliquer sur "Se connecter"**

Tu devrais voir :
1. ✅ Message vert : "Bienvenue Administrateur !"
2. ✅ Redirection automatique vers `/dashboard`

---

## 🎯 CE QUI A ÉTÉ CORRIGÉ

### **Avant (❌ Ne fonctionnait pas)**
```python
# Les routes cherchaient les données dans l'URL
@router.post("/login")
async def login(email: str, password: str):
    # ❌ Cherche : /login?email=...&password=...
```

### **Après (✅ Fonctionne)**
```python
# Les routes lisent les données du formulaire
@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    # ✅ Lit le formulaire HTML correctement
```

---

## 📋 CHECKLIST DE VÉRIFICATION

### ✅ Avant de te connecter

- [ ] Le serveur est démarré (`.\start_webox_local.ps1`)
- [ ] Tu vois : `Application startup complete`
- [ ] L'URL est : `http://webox.local:8000/login`

### ✅ Pendant la connexion

- [ ] Email : `admin@webox.com`
- [ ] Mot de passe : `admin123`
- [ ] Pas d'espaces avant/après l'email
- [ ] Mot de passe exact (sensible à la casse)

### ✅ Après la connexion

- [ ] Message vert : "Bienvenue Administrateur !"
- [ ] Redirection vers `/dashboard`
- [ ] Tu vois ton nom en haut : "Bonjour, Administrateur 👋"
- [ ] Les boutons "Dashboard" et "Déconnexion" sont visibles

---

## 🐛 SI ÇA NE FONCTIONNE TOUJOURS PAS

### **1. Vérifier que le serveur est à jour**

```powershell
# Arrêter le serveur (Ctrl+C)
# Puis relancer
.\start_webox_local.ps1
```

### **2. Vider le cache du navigateur**

```
Ctrl + Shift + R (Windows)
Cmd + Shift + R (Mac)
```

### **3. Tester avec curl**

```powershell
curl -X POST http://webox.local:8000/login `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "email=admin@webox.com&password=admin123&remember_me=false"
```

**Résultat attendu :**
```json
{
  "success": true,
  "message": "Bienvenue Administrateur !",
  "redirect": "/dashboard"
}
```

### **4. Vérifier les logs du serveur**

Dans le terminal où tourne le serveur, tu devrais voir :
```
INFO:     127.0.0.1:XXXXX - "POST /login HTTP/1.1" 200 OK
```

Si tu vois `422` ou `400`, il y a encore un problème.

---

## 🆕 CRÉER UN NOUVEAU COMPTE

### **Étape 1 : Aller sur la page d'inscription**
```
http://webox.local:8000/register
```

### **Étape 2 : Remplir le formulaire**
```
Nom complet: Ton Nom
Email: ton@email.com
Mot de passe: motdepasse123 (min. 6 caractères)
```

### **Étape 3 : Cliquer sur "Créer mon compte"**

Tu devrais voir :
1. ✅ Message vert : "Compte créé avec succès !"
2. ✅ Redirection vers `/login`

### **Étape 4 : Te connecter avec ton nouveau compte**

---

## 🔑 GESTION DES MOTS DE PASSE

### **Sécurité**
- ✅ Les mots de passe sont hashés avec SHA-256
- ✅ Jamais stockés en clair
- ✅ Cookies httponly (protection XSS)

### **Réinitialiser le compte admin**

Si tu as oublié le mot de passe admin :
```powershell
python fix_admin.py
```

Cela réinitialisera le compte à :
```
Email: admin@webox.com
Mot de passe: admin123
```

---

## 📱 APRÈS LA CONNEXION

### **Dashboard**
Tu as accès à :
- 💬 **Chat Multi-IA** - Discuter avec 12+ IA
- 🎨 **Génération** - Images, vidéos, audio
- 👤 **Profil** - Tes informations
- 📊 **Statistiques** - Ton utilisation

### **Navigation**
- **Header** - Toujours visible en haut
- **Bouton Dashboard** - Retour au tableau de bord
- **Bouton Déconnexion** - Se déconnecter

---

## 🎉 TOUT FONCTIONNE !

**Tu peux maintenant :**
1. ✅ Te connecter avec `admin@webox.com` / `admin123`
2. ✅ Créer de nouveaux comptes
3. ✅ Accéder au dashboard
4. ✅ Utiliser toutes les fonctionnalités
5. ✅ Te déconnecter

---

## 📞 BESOIN D'AIDE ?

### **Vérifier l'état du système**

```powershell
# Test du mot de passe
python test_login.py

# Résultat attendu :
# ✅ Les hash correspondent !
# ✅ Utilisateur trouvé: Administrateur
# ✅ verify_password('admin123') = TRUE
```

### **Logs du serveur**

Le serveur affiche toutes les requêtes :
```
INFO: 127.0.0.1:XXXXX - "GET /login HTTP/1.1" 200 OK
INFO: 127.0.0.1:XXXXX - "POST /login HTTP/1.1" 200 OK
INFO: 127.0.0.1:XXXXX - "GET /dashboard HTTP/1.1" 200 OK
```

---

**Dernière mise à jour :** 30 octobre 2025, 12:30  
**Statut :** ✅ **TOUT FONCTIONNE**

🚀 **Bonne utilisation de WeBox Multi-IA !**
