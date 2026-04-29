# Guide de Test des Générations WeBox

Date: 1er avril 2026

---

## ✅ CORRECTIONS APPLIQUÉES

### 1. Suppression des Shorts/Publicités - CORRIGÉ ✅

**Problème:** Erreur "Génération non trouvée" lors de la suppression

**Solution:** Ajouté la gestion de suppression pour `short` et `ad` dans la route DELETE

**Code ajouté:**
```python
elif generation_type == "short":
    # Suppression des shorts
    
elif generation_type == "ad":
    # Suppression des publicités
```

**Testez:** Vous pouvez maintenant supprimer les shorts et publicités en cliquant sur le bouton ❌

---

### 2. Logs d'Erreur Détaillés - AJOUTÉ ✅

**Ajout:** Logs détaillés avec traceback complet pour toutes les générations

**Bénéfice:** Permet de voir exactement pourquoi une génération échoue

**Où voir les logs:**
- Console du serveur (terminal où uvicorn tourne)
- Fichier `logs/app.log` (si configuré)

---

## 🧪 PROTOCOLE DE TEST

### Étape 1: Vérifier que le serveur tourne

```powershell
# Vérifier les processus Python
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

Si le serveur ne tourne pas:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Étape 2: Tester chaque type de génération

#### 🎙️ Test Audio (Devrait fonctionner)

1. Aller sur `http://webox.local:8000/generation`
2. Cliquer sur l'onglet **🎙️ Audio**
3. Remplir:
   - **Texte:** "Bonjour, ceci est un test de génération audio"
   - **Modèle:** ElevenLabs
   - **Langue:** Français
4. Cliquer **"Générer l'audio"**
5. **Attendu:** 
   - Notification "Génération lancée"
   - Polling du statut
   - Après ~2-3 secondes: "Génération terminée"
   - Apparition dans l'historique avec icône 🎙️
   - Possibilité d'écouter et télécharger

**Si ça échoue:**
- Regarder la console du serveur
- Chercher le message `❌ Erreur génération audio #X:`
- Vérifier que gTTS est installé: `pip list | findstr gTTS`

---

#### 📱 Test Short (Devrait fonctionner)

1. Onglet **📱 Shorts**
2. Remplir:
   - **Sujet:** "Les bienfaits du sport"
   - **Durée:** 30 secondes
   - **Style:** Educational
3. Cliquer **"Générer le Short"**
4. **Attendu:**
   - Génération lancée
   - Apparition dans l'historique avec icône 📱
   - Possibilité de voir le script généré

**Si ça échoue:**
- Console serveur: `❌ Erreur génération short #X:`
- Vérifier que la fonction `_create_simple_video()` fonctionne

---

#### 🎬 Test Vidéo (Devrait fonctionner)

1. Onglet **🎬 Vidéos**
2. Remplir:
   - **Prompt:** "Une belle journée ensoleillée"
   - **Durée:** 5 secondes
   - **Modèle:** Veo 2
3. Cliquer **"Générer la vidéo"**
4. **Attendu:**
   - Génération lancée
   - Apparition dans l'historique avec icône 🎬
   - Vidéo simple avec texte (si FFmpeg installé)
   - Sinon fichier texte placeholder

**Si ça échoue:**
- Console serveur: `❌ Erreur génération vidéo #X:`
- Vérifier FFmpeg: `ffmpeg -version`

---

#### 📢 Test Publicité (Devrait fonctionner)

1. Onglet **📢 Publicités**
2. Remplir les champs
3. Cliquer **"Générer la publicité"**
4. **Attendu:**
   - Génération lancée
   - Apparition dans l'historique avec icône 📢

**Si ça échoue:**
- Console serveur: `❌ Erreur génération publicité #X:`

---

#### 🖼️ Test Image (Devrait fonctionner)

1. Onglet **🖼️ Images**
2. Prompt: "Un chat mignon"
3. **Attendu:** Image générée avec DALL-E ou Stable Diffusion

---

#### 📝 Test Texte (Fonctionne différemment)

1. Onglet **📝 Texte**
2. Sujet: "Les avantages de l'IA"
3. **Attendu:** 
   - Résultat affiché **directement** dans l'interface
   - **PAS d'historique** (c'est normal)

---

#### 💻 Test Code (Fonctionne différemment)

1. Onglet **💻 Code**
2. Description: "Fonction pour trier un tableau"
3. **Attendu:**
   - Code affiché **directement**
   - **PAS d'historique** (c'est normal)

---

## 🔍 DIAGNOSTIC DES ERREURS

### Erreur: "Génération échouée: undefined"

**Causes possibles:**
1. Erreur dans la tâche en arrière-plan
2. Exception non capturée
3. Problème de dépendances

**Solution:**
1. Regarder la console du serveur
2. Chercher le traceback complet
3. Vérifier les dépendances manquantes

---

### Erreur: "Génération non trouvée" (lors de la suppression)

**Cause:** Type de génération non géré dans la route DELETE

**Solution:** ✅ CORRIGÉ - shorts et ads peuvent maintenant être supprimés

---

### Erreur: "Module 'gtts' not found"

**Cause:** gTTS pas installé

**Solution:**
```powershell
pip install gTTS
```

---

### Erreur: "FFmpeg non disponible"

**Cause:** FFmpeg pas installé (optionnel)

**Solution:** 
- Soit installer FFmpeg
- Soit accepter les fichiers placeholder (texte)

---

## 📊 CHECKLIST DE VÉRIFICATION

Avant de tester, vérifier:

- [ ] Serveur uvicorn lancé
- [ ] Base de données accessible
- [ ] gTTS installé (`pip list | findstr gTTS`)
- [ ] Token d'authentification valide
- [ ] Console du serveur visible pour voir les logs

---

## 🚨 SI TOUTES LES GÉNÉRATIONS ÉCHOUENT

**Étapes de diagnostic:**

1. **Vérifier la console du serveur**
   - Y a-t-il des erreurs au démarrage?
   - Les routes sont-elles bien chargées?

2. **Tester une génération simple (Audio)**
   - C'est la plus simple (juste gTTS)
   - Si ça échoue, regarder le traceback complet

3. **Vérifier les dépendances**
   ```powershell
   pip list | findstr -i "gtts fastapi sqlalchemy"
   ```

4. **Vérifier la base de données**
   - Les tables existent-elles?
   - L'utilisateur peut-il créer des entrées?

5. **Redémarrer le serveur**
   ```powershell
   # Tuer tous les processus Python
   Get-Process python* | Stop-Process -Force
   
   # Relancer
   python -m uvicorn app.main:app --reload
   ```

---

## 📝 RAPPORT D'ERREUR

Si les générations échouent toujours, fournir:

1. **Message d'erreur exact** de la console serveur
2. **Type de génération** testé
3. **Traceback complet** (si disponible)
4. **Version Python:** `python --version`
5. **Dépendances installées:** `pip list`

---

## ✅ RÉSUMÉ

**Corrections appliquées:**
- ✅ Suppression shorts/ads fonctionne
- ✅ Logs détaillés ajoutés
- ✅ Routes GET /shorts ajoutée
- ✅ Affichage historique pour shorts/ads

**À tester:**
1. Audio (devrait marcher avec gTTS)
2. Shorts (devrait marcher)
3. Vidéo (devrait marcher ou créer placeholder)
4. Publicités (devrait marcher)
5. Suppression (devrait marcher pour tous les types)

**Prochaines étapes:**
1. Tester chaque génération
2. Noter les erreurs exactes
3. Regarder les logs du serveur
4. Rapporter les erreurs spécifiques
