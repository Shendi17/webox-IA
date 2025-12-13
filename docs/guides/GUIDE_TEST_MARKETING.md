# 📖 GUIDE DE TEST - MODULE MARKETING

**Date** : 23 Novembre 2025  
**Module** : Phase 5 - Marketing & Business  

---

## 🎯 OBJECTIF

Tester toutes les fonctionnalités du module Marketing après les corrections.

---

## ✅ CORRECTIONS EFFECTUÉES

1. ✅ **Erreur 500** : Chemins de templates corrigés
2. ✅ **Popups d'erreur** : Remplacés par messages élégants
3. ✅ **Colonne preheader** : Ajoutée à la base de données

---

## 🚀 ÉTAPES DE TEST

### **1. Vérifier que le serveur tourne**

```bash
# Le serveur devrait être déjà lancé
# Si ce n'est pas le cas :
python main.py
```

**Résultat attendu** :
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
```

---

### **2. Se connecter au dashboard**

#### **Option A : Créer un compte**
```
http://webox.local:8000/register
```

Remplis le formulaire :
- Nom d'utilisateur
- Email
- Mot de passe

#### **Option B : Se connecter avec un compte existant**
```
http://webox.local:8000/login
```

Utilise tes identifiants existants.

---

### **3. Accéder au Dashboard Marketing**

Une fois connecté, accède à :
```
http://webox.local:8000/marketing-dashboard
```

**Ce que tu devrais voir** :
- ✅ Statistiques principales (Leads, Tunnels, Emails, Conversion)
- ✅ Actions rapides (4 boutons)
- ✅ Graphique de performance
- ✅ Pipeline CRM
- ✅ Activité récente

**Si tu vois "Chargement..." puis rien** :
- C'est normal, il n'y a pas encore de données
- Les statistiques afficheront 0

---

### **4. Tester le CRM**

```
http://webox.local:8000/crm
```

#### **Créer un lead**
1. Clique sur **"+ Ajouter un lead"**
2. Remplis le formulaire :
   - Nom : Jean Dupont
   - Email : jean@example.com
   - Téléphone : +33612345678
   - Entreprise : ACME Corp
   - Poste : CEO
   - Valeur estimée : 5000
   - Statut : new
   - Source : website
3. Clique sur **"💾 Créer"**

**Résultat attendu** :
- ✅ Message de succès dans la console
- ✅ Lead apparaît dans la liste
- ✅ Score calculé automatiquement

#### **Voir les détails d'un lead**
1. Clique sur **"👁️ Voir"** sur un lead
2. Modal s'ouvre avec les détails
3. Tu peux ajouter une interaction
4. Tu peux calculer le score

---

### **5. Tester Email Marketing**

```
http://webox.local:8000/email-marketing
```

#### **Créer une campagne manuellement**
1. Clique sur **"+ Créer une campagne"**
2. Remplis le formulaire :
   - Nom : Newsletter Novembre
   - Sujet : Découvrez nos nouveautés !
   - Preheader : Plus de 50 fonctionnalités ajoutées
   - Contenu HTML : `<h1>Bonjour !</h1><p>Voici nos nouveautés...</p>`
3. Clique sur **"💾 Créer"**

**Résultat attendu** :
- ✅ Message de succès
- ✅ Campagne apparaît dans la liste
- ✅ Statut : Brouillon

#### **Générer une campagne avec IA** 🤖
1. Clique sur **"🤖 Générer avec IA"**
2. Remplis le formulaire :
   - Type : newsletter
   - Sujet : Nouveautés du mois
   - Audience : Clients actifs
   - Ton : professional
   - Objectif : Augmenter l'engagement
3. Clique sur **"🤖 Générer"**

**Résultat attendu** :
- ✅ Message "Génération en cours..."
- ✅ Campagne créée automatiquement
- ✅ Nom, sujet, contenu générés par IA

---

### **6. Tester Tunnels de Vente**

```
http://webox.local:8000/funnels
```

#### **Créer un tunnel manuellement**
1. Clique sur **"+ Créer un tunnel"**
2. Remplis le formulaire :
   - Nom : Formation Marketing
   - Type : webinar
   - Description : Tunnel pour webinaire marketing
3. Clique sur **"💾 Créer"**

**Résultat attendu** :
- ✅ Message de succès
- ✅ Tunnel apparaît dans la liste
- ✅ Statut : Brouillon

#### **Générer un tunnel avec IA** 🤖
1. Clique sur **"🤖 Générer avec IA"**
2. Remplis le formulaire :
   - Type : webinar
   - Sujet : Marketing Digital 2025
   - Audience : Entrepreneurs
   - Objectif : Générer des leads qualifiés
   - Budget : 1000
3. Clique sur **"🤖 Générer"**

**Résultat attendu** :
- ✅ Message "Génération en cours..."
- ✅ Tunnel créé automatiquement
- ✅ Nom, description générés par IA

---

## 🐛 PROBLÈMES POSSIBLES

### **Problème 1 : "Erreur lors du chargement"**

**Cause** : Tu n'es pas authentifié

**Solution** :
1. Va sur `/login`
2. Connecte-toi
3. Retourne sur la page Marketing

---

### **Problème 2 : "401 Unauthorized"**

**Cause** : Session expirée

**Solution** :
1. Déconnecte-toi
2. Reconnecte-toi
3. Réessaye

---

### **Problème 3 : Popup d'erreur**

**Cause** : Ancienne version en cache

**Solution** :
1. Vide le cache du navigateur (Ctrl+Shift+Del)
2. Rafraîchis la page (Ctrl+F5)
3. Réessaye

---

### **Problème 4 : "no such column: preheader"**

**Cause** : Migration non exécutée

**Solution** :
```bash
python migrations/add_preheader_column.py
```

---

## 📊 CHECKLIST DE TEST

### **Dashboard Marketing**
- [ ] Page charge sans erreur
- [ ] Statistiques affichées
- [ ] Graphique visible
- [ ] Actions rapides fonctionnelles

### **CRM**
- [ ] Liste des leads affichée
- [ ] Création de lead fonctionne
- [ ] Détails du lead s'affichent
- [ ] Ajout d'interaction fonctionne
- [ ] Calcul du score fonctionne
- [ ] Suppression de lead fonctionne

### **Email Marketing**
- [ ] Liste des campagnes affichée
- [ ] Création manuelle fonctionne
- [ ] Génération IA fonctionne 🤖
- [ ] Statistiques affichées
- [ ] Suppression de campagne fonctionne

### **Tunnels de Vente**
- [ ] Liste des tunnels affichée
- [ ] Création manuelle fonctionne
- [ ] Génération IA fonctionne 🤖
- [ ] Activation/Désactivation fonctionne
- [ ] Statistiques affichées
- [ ] Suppression de tunnel fonctionne

---

## 🎯 RÉSULTATS ATTENDUS

### **Si tout fonctionne**
```
✅ Toutes les pages chargent
✅ Pas de popup d'erreur
✅ Création de données fonctionne
✅ Génération IA fonctionne
✅ Statistiques s'affichent
✅ Navigation fluide
```

### **Si problèmes**
```
❌ Erreurs dans la console (F12)
❌ Popups d'erreur
❌ Pages ne chargent pas
❌ Données ne se créent pas
```

**Dans ce cas** :
1. Ouvre la console (F12)
2. Note les erreurs
3. Vérifie les logs du serveur
4. Partage les erreurs

---

## 📝 RAPPORT DE TEST

### **Template**

```markdown
# Test du Module Marketing

**Date** : 23 Novembre 2025
**Testeur** : [Ton nom]

## Dashboard Marketing
- [ ] ✅ Fonctionne
- [ ] ❌ Problème : [Description]

## CRM
- [ ] ✅ Fonctionne
- [ ] ❌ Problème : [Description]

## Email Marketing
- [ ] ✅ Fonctionne
- [ ] ❌ Problème : [Description]

## Tunnels de Vente
- [ ] ✅ Fonctionne
- [ ] ❌ Problème : [Description]

## Génération IA
- [ ] ✅ Email : Fonctionne
- [ ] ✅ Tunnels : Fonctionne
- [ ] ❌ Problème : [Description]

## Conclusion
- [ ] ✅ Tout fonctionne
- [ ] ⚠️ Quelques problèmes mineurs
- [ ] ❌ Problèmes majeurs
```

---

## 🎉 CONCLUSION

**Le module Marketing est prêt à être testé !**

**Étapes** :
1. ✅ Connecte-toi au dashboard
2. ✅ Accède aux pages Marketing
3. ✅ Teste toutes les fonctionnalités
4. ✅ Vérifie la génération IA
5. ✅ Rapporte les éventuels problèmes

**Bon test ! 🚀**
