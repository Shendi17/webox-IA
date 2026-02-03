# 🔧 SOLUTION - Erreur 429 OpenAI dans le Chat

**Date:** 17 Janvier 2026  
**Problème:** Le chat affiche une erreur 429 "insufficient_quota" alors que le test de connexion fonctionne

---

## 🔍 DIAGNOSTIC

### **Tests effectués:**
1. ✅ Script de test standalone (`test_openai_connection.py`) → **FONCTIONNE**
2. ✅ Clé API chargée par l'application (`check_env.py`) → **CORRECTE** (164 caractères)
3. ❌ Chat Multi-IA → **ERREUR 429**

---

## 💡 CAUSE IDENTIFIÉE

**Le serveur WeBox utilise une ANCIENNE clé API mise en cache.**

### **Pourquoi ?**

1. **Le serveur a été démarré AVANT que vous changiez la clé API**
2. **Python charge les variables d'environnement au démarrage**
3. **Le serveur continue d'utiliser l'ancienne clé (expirée/sans quota)**
4. **Le script de test charge la NOUVELLE clé à chaque exécution**

---

## ✅ SOLUTION

### **Redémarrer le serveur pour charger la nouvelle clé API**

1. **Arrêtez le serveur actuel:**
   - Appuyez sur `Ctrl+C` dans le terminal où le serveur tourne
   - Ou fermez le terminal

2. **Redémarrez le serveur:**
   ```powershell
   python main.py
   ```

3. **Attendez le message:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

4. **Testez le chat:**
   - Allez sur http://127.0.0.1:8000/chat
   - Envoyez un message avec GPT-4
   - ✅ Devrait fonctionner maintenant

---

## 🔄 POURQUOI LE TEST FONCTIONNAIT ?

Le script `test_openai_connection.py` :
- Charge le fichier `.env` à chaque exécution
- Utilise la **nouvelle clé API** (celle avec $10 de crédit)
- Fonctionne correctement

Le serveur WeBox :
- Charge le fichier `.env` **une seule fois au démarrage**
- Continue d'utiliser l'**ancienne clé API** (celle sans crédit)
- Affiche l'erreur 429

---

## 📋 VÉRIFICATION APRÈS REDÉMARRAGE

Après avoir redémarré le serveur, vérifiez dans les logs de démarrage :

```
✅ OpenAI configuré
✅ Clé API: sk-proj-WQkWT-iJRb1H...
```

Si vous voyez une clé différente, c'est que le serveur charge encore l'ancienne.

---

## 🚨 SI LE PROBLÈME PERSISTE

### **Option 1 : Vérifier le fichier .env**

1. Ouvrez le fichier `.env` (pas `.env.example`)
2. Vérifiez que `OPENAI_API_KEY` contient votre nouvelle clé
3. Pas d'espaces avant ou après le `=`
4. Format correct : `OPENAI_API_KEY=sk-proj-...`

### **Option 2 : Forcer le rechargement**

```powershell
# Arrêter tous les processus Python
taskkill /F /IM python.exe

# Redémarrer
python main.py
```

### **Option 3 : Vérifier qu'il n'y a qu'un seul serveur**

```powershell
# Lister les processus Python
tasklist | findstr python

# Si plusieurs processus, arrêtez-les tous
taskkill /F /IM python.exe
```

---

## ✅ RÉSUMÉ

**Problème:** Cache de l'ancienne clé API  
**Solution:** Redémarrer le serveur  
**Commande:** `python main.py`  
**Temps:** 10 secondes  

---

**Après redémarrage, le chat devrait fonctionner avec votre nouvelle clé API ($10 de crédit).**
