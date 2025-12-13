# 🔄 VIDER LE CACHE DU NAVIGATEUR

**Problème** : Les modifications CSS ne s'affichent pas immédiatement car le navigateur garde l'ancienne version en cache.

---

## 🚀 SOLUTION RAPIDE

### **Méthode 1 : Hard Refresh (Recommandé)**

#### **Windows / Linux**
- **Chrome / Edge / Firefox** : `Ctrl + Shift + R` ou `Ctrl + F5`
- **Opera** : `Ctrl + F5`

#### **macOS**
- **Chrome / Edge** : `Cmd + Shift + R`
- **Safari** : `Cmd + Option + R`
- **Firefox** : `Cmd + Shift + R`

---

### **Méthode 2 : Vider le cache complet**

#### **Chrome / Edge**
1. Appuie sur `Ctrl + Shift + Delete` (Windows) ou `Cmd + Shift + Delete` (Mac)
2. Sélectionne "Images et fichiers en cache"
3. Période : "Dernière heure" ou "Toutes les périodes"
4. Clique sur "Effacer les données"

#### **Firefox**
1. Appuie sur `Ctrl + Shift + Delete` (Windows) ou `Cmd + Shift + Delete` (Mac)
2. Sélectionne "Cache"
3. Période : "Tout"
4. Clique sur "Effacer maintenant"

---

### **Méthode 3 : Mode Développeur (Pour tester)**

#### **Chrome / Edge / Firefox**
1. Appuie sur `F12` pour ouvrir les DevTools
2. Fais un **clic droit** sur le bouton de rafraîchissement (à côté de l'URL)
3. Sélectionne "Vider le cache et actualiser de force"

---

## 🎯 POUR WEBOX

Après avoir modifié le fichier CSS (`dashboard.css`), fais :

1. **Hard Refresh** : `Ctrl + Shift + R` (Windows) ou `Cmd + Shift + R` (Mac)
2. Vérifie que les sélecteurs fonctionnent maintenant
3. Si ça ne marche toujours pas, vide le cache complet (Méthode 2)

---

## ✅ VÉRIFICATION

Pour vérifier que le nouveau CSS est chargé :

1. Ouvre les DevTools (`F12`)
2. Va dans l'onglet **Network** (Réseau)
3. Rafraîchis la page
4. Cherche `dashboard.css` dans la liste
5. Vérifie la taille du fichier (doit être ~15-20 KB)
6. Clique dessus et vérifie que tu vois les nouvelles règles :
   ```css
   .dashboard-card input,
   .dashboard-card select,
   .dashboard-card textarea,
   .dashboard-card button {
       pointer-events: auto !important;
   }
   ```

---

## 🔧 MODE DÉVELOPPEMENT (Désactiver le cache)

Pour éviter ce problème pendant le développement :

1. Ouvre les DevTools (`F12`)
2. Va dans **Settings** (icône engrenage) ou `F1`
3. Coche "Disable cache (while DevTools is open)"
4. Garde les DevTools ouverts pendant le développement

---

**🎉 Après un Hard Refresh, tous les formulaires devraient fonctionner !**
