# 🔴 INSTRUCTIONS URGENTES - TEST MODAL

**Date** : 16 Novembre 2025 - 13:06

---

## ⚠️ PROBLÈME

Le modal n'est toujours pas centré malgré les corrections CSS appliquées.

**Cause probable** : Cache navigateur très persistant

---

## 🔧 SOLUTION : VIDER LE CACHE COMPLÈTEMENT

### **Méthode 1 : Hard Refresh (OBLIGATOIRE)**

1. **Ouvrir la page** `/website-builder`
2. **Ouvrir DevTools** : `F12`
3. **Aller dans l'onglet Network**
4. **Cocher "Disable cache"** (en haut)
5. **Faire un hard refresh** : `Ctrl + Shift + R`
6. **Tester** : Cliquer sur un template

---

### **Méthode 2 : Vider le cache manuellement**

#### **Chrome/Edge**
1. `Ctrl + Shift + Delete`
2. Sélectionner "Images et fichiers en cache"
3. Période : "Dernière heure"
4. Cliquer "Effacer les données"
5. Rafraîchir : `F5`

#### **Firefox**
1. `Ctrl + Shift + Delete`
2. Sélectionner "Cache"
3. Cliquer "Effacer maintenant"
4. Rafraîchir : `F5`

---

### **Méthode 3 : Mode navigation privée**

1. **Ouvrir une fenêtre privée** : `Ctrl + Shift + N`
2. **Aller sur** `http://localhost:8000/website-builder`
3. **Tester** : Cliquer sur un template
4. **Vérifier** : Le modal doit être centré

---

## 🐛 DÉBOGAGE

### **Console JavaScript**

Quand tu cliques sur un template, tu devrais voir dans la console :

```
Modal classes: modal active
Modal display: flex
```

**Si tu vois ça** : Le JavaScript fonctionne ✅  
**Si tu ne vois pas ça** : Problème JavaScript ❌

---

### **Inspecteur CSS**

1. **Ouvrir DevTools** : `F12`
2. **Sélectionner le modal** (élément `#createModal`)
3. **Regarder les styles appliqués**

**Tu devrais voir** :
```css
#createModal.modal.active {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
```

**Si tu ne vois pas ça** : Le CSS n'est pas chargé → Cache ❌

---

## 📊 CHECKLIST DE TEST

### **Avant de tester**
- [ ] DevTools ouvert (`F12`)
- [ ] Onglet Network ouvert
- [ ] "Disable cache" coché
- [ ] Console visible

### **Test**
- [ ] Hard refresh (`Ctrl + Shift + R`)
- [ ] Cliquer sur un template
- [ ] Vérifier la console (logs)
- [ ] Vérifier le centrage du modal

### **Résultat attendu**
- [ ] Console affiche : `Modal classes: modal active`
- [ ] Console affiche : `Modal display: flex`
- [ ] Modal est **centré** sur l'écran

---

## 🎯 SI ÇA NE FONCTIONNE TOUJOURS PAS

### **Vérifier le CSS chargé**

1. **DevTools** → **Sources**
2. **Ouvrir** `dashboard.css`
3. **Chercher** `#createModal.modal.active`
4. **Vérifier** que le CSS contient :
   ```css
   #createModal.modal.active {
       display: flex !important;
       align-items: center !important;
       justify-content: center !important;
   }
   ```

**Si le CSS n'est pas là** :
- Le fichier n'a pas été sauvegardé
- Le serveur n'a pas rechargé le fichier
- Le cache est vraiment très persistant

---

## 🔄 REDÉMARRER LE SERVEUR

Si vraiment rien ne fonctionne :

1. **Arrêter le serveur** : `Ctrl + C`
2. **Attendre 5 secondes**
3. **Relancer** : `python main.py`
4. **Attendre que le serveur démarre**
5. **Ouvrir en navigation privée**
6. **Tester**

---

## 📸 CAPTURES À FOURNIR

Si le problème persiste, fournis :

1. **Console** : Screenshot des logs JavaScript
2. **Network** : Screenshot montrant `dashboard.css` chargé
3. **Elements** : Screenshot de l'inspecteur sur `#createModal`
4. **Computed** : Screenshot des styles calculés du modal

---

## ✅ RÉSULTAT ATTENDU

### **Modal centré**
```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│         ┌─────────────┐            │
│         │   MODAL     │            │
│         │   CENTRÉ    │            │
│         └─────────────┘            │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

### **Console**
```
Modal classes: modal active
Modal display: flex
```

---

**Si après tout ça, le modal n'est toujours pas centré, il y a un autre problème CSS que nous devrons investiguer plus en profondeur.** 🔍
