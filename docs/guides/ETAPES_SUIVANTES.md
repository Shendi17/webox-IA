# 📋 ÉTAPES SUIVANTES - PLAN DE CORRECTION PHASE 1

**Date:** 24 Janvier 2026  
**Statut:** Phase 1.1 ✅ Terminée | Phase 1.2 🔄 En cours

---

## ✅ PHASE 1.1 - E-COMMERCE (TERMINÉ)

### Ce qui a été fait

#### 1. Modèles de données créés
- ✅ `app/models/product_db.py` - Modèles ProductDB, CartItemDB, OrderDB, OrderItemDB
- ✅ Relations ajoutées au modèle UserDB

#### 2. Migration base de données
- ✅ `migrations/create_ecommerce_tables.py` - Script de création des tables
- ✅ 6 produits d'exemple inclus dans la migration

#### 3. API Panier complète
- ✅ `app/routes/cart_routes.py` - Routes API panier
  - `GET /api/cart` - Récupérer le panier
  - `POST /api/cart/add` - Ajouter un produit
  - `PUT /api/cart/{id}` - Modifier la quantité
  - `DELETE /api/cart/{id}` - Supprimer un article
  - `DELETE /api/cart` - Vider le panier
  - `GET /api/cart/count` - Nombre d'articles

#### 4. Intégration
- ✅ Routes cart ajoutées dans `main.py`

#### 5. Scripts de test
- ✅ `LANCER_MIGRATION_ECOMMERCE.bat` - Lancer la migration
- ✅ `TEST_PANIER_API.py` - Tester toutes les fonctionnalités du panier

### Comment tester

```bash
# 1. Créer les tables et ajouter les produits
.\LANCER_MIGRATION_ECOMMERCE.bat

# 2. Démarrer le serveur
python main.py

# 3. Dans un autre terminal, tester l'API panier
python TEST_PANIER_API.py
```

---

## 🔄 PHASE 1.2 - PAIEMENTS (EN COURS)

### Prochaines actions

#### 1. Configuration Stripe ⏳
```bash
# Étapes:
1. Créer un compte Stripe (https://stripe.com)
2. Récupérer les clés de test
3. Ajouter dans .env:
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
```

#### 2. Configuration PayPal ⏳
```bash
# Étapes:
1. Créer un compte développeur PayPal
2. Créer une application
3. Ajouter dans .env:
   PAYPAL_CLIENT_ID=...
   PAYPAL_CLIENT_SECRET=...
   PAYPAL_MODE=sandbox
```

#### 3. Installer dépendances paiement
```bash
pip install stripe paypalrestsdk
```

#### 4. Tester les paiements
- Créer un script de test pour Stripe
- Créer un script de test pour PayPal
- Vérifier le webhook Stripe

### Fichiers à consulter
- 📖 `GUIDE_CONFIGURATION_CLES_API.md` - Guide complet de configuration
- 📄 `app/routes/payment_routes.py` - Routes paiement (déjà existantes)

---

## 🔜 PHASE 1.3 - CONFIGURATION IA

### Actions à venir

#### 1. Configuration OpenAI (HAUTE PRIORITÉ)
```env
OPENAI_API_KEY=sk-proj-...
```
**Permet:**
- Chat GPT-4 / GPT-3.5
- Génération images DALL-E 3
- Génération images DALL-E 2

#### 2. Configuration Anthropic
```env
ANTHROPIC_API_KEY=sk-ant-...
```
**Permet:**
- Chat Claude 3 (Opus, Sonnet, Haiku)

#### 3. Configuration Google
```env
GOOGLE_API_KEY=AIzaSy...
```
**Permet:**
- Chat Gemini Pro
- Gemini Pro Vision

#### 4. Configuration Groq (Recommandé)
```env
GROQ_API_KEY=gsk_...
```
**Permet:**
- Chat ultra-rapide
- Gratuit avec quota généreux

#### 5. Tests génération IA
- Tester génération image DALL-E 3
- Tester chat GPT-4
- Tester chat Claude
- Tester chat Gemini
- Vérifier sauvegarde en base de données

---

## 📊 PROGRESSION GLOBALE

### Phase 1 - Fonctionnalités Critiques

| Sous-phase | Tâches | Complété | Statut |
|------------|--------|----------|--------|
| 1.1 E-commerce | 4/4 | 100% | ✅ Terminé |
| 1.2 Paiements | 0/4 | 0% | 🔄 En cours |
| 1.3 IA | 0/5 | 0% | ⏳ À venir |
| **TOTAL** | **4/13** | **31%** | 🔄 **En cours** |

---

## 🎯 OBJECTIFS IMMÉDIATS

### Cette semaine

1. **Configurer Stripe** (2h)
   - Créer compte
   - Récupérer clés
   - Tester paiement

2. **Configurer OpenAI** (1h)
   - Créer compte
   - Ajouter moyen de paiement
   - Récupérer clé API
   - Tester génération

3. **Tester le panier** (30min)
   - Exécuter migration
   - Tester API complète
   - Vérifier persistance

### Semaine prochaine

4. **Configurer autres IA** (2h)
   - Anthropic (Claude)
   - Google (Gemini)
   - Groq

5. **Tests complets** (2h)
   - Tester toutes les générations IA
   - Tester flux paiement complet
   - Vérifier marketplace

---

## 🛠️ COMMANDES UTILES

### Démarrage
```bash
# Lancer le serveur
python main.py

# Lancer en mode reload (développement)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Migrations
```bash
# Créer tables e-commerce
python migrations\create_ecommerce_tables.py

# Vérifier les tables
python -c "from app.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

### Tests
```bash
# Tester le panier
python TEST_PANIER_API.py

# Audit complet
python AUDIT_COMPLET_FONCTIONNALITES.py

# Vérifier les clés API
python check_env.py
```

### Base de données
```bash
# Se connecter à PostgreSQL
psql -U postgres -d webox

# Voir les tables
\dt

# Voir les produits
SELECT id, name, price FROM products;

# Voir le panier d'un utilisateur
SELECT * FROM cart_items WHERE user_id = 1;
```

---

## 📝 NOTES IMPORTANTES

### Sécurité
- ⚠️ Ne jamais commiter le fichier `.env`
- ⚠️ Utiliser des clés de test en développement
- ⚠️ Changer les secrets en production

### Performance
- Les APIs IA peuvent être lentes (10-30s pour images/vidéos)
- Utiliser les tâches en arrière-plan (BackgroundTasks)
- Implémenter un système de cache si nécessaire

### Coûts
- **OpenAI:** ~$0.03/1K tokens (GPT-4), $0.04-0.12/image (DALL-E)
- **Anthropic:** ~$0.015/1K tokens (Claude Opus)
- **Stripe:** 1.4% + 0.25€ par transaction (Europe)
- **PayPal:** ~2.9% + 0.35€ par transaction

### Quotas gratuits
- **Google Gemini:** 60 requêtes/minute (gratuit)
- **Groq:** Quota généreux (gratuit pour l'instant)

---

## 🆘 BESOIN D'AIDE ?

### Problèmes courants

**Le serveur ne démarre pas**
```bash
# Vérifier les dépendances
pip install -r requirements_fastapi.txt

# Vérifier la connexion DB
python -c "from app.database import engine; print(engine)"
```

**Les tables n'existent pas**
```bash
# Exécuter la migration
python migrations\create_ecommerce_tables.py
```

**Erreur "API Key not found"**
```bash
# Vérifier le fichier .env
cat .env  # Linux/Mac
type .env  # Windows

# Redémarrer le serveur après modification
```

**Erreur de paiement**
```bash
# Vérifier les clés Stripe/PayPal
python check_env.py

# Vérifier les logs du serveur
```

---

## 📚 DOCUMENTATION

### Fichiers de référence
- 📖 `RAPPORT_AUDIT_FONCTIONNALITES.md` - Audit complet
- 📖 `GUIDE_CONFIGURATION_CLES_API.md` - Configuration des clés
- 📖 `README.md` - Documentation générale

### APIs externes
- [Stripe Docs](https://stripe.com/docs)
- [PayPal Docs](https://developer.paypal.com/docs)
- [OpenAI Docs](https://platform.openai.com/docs)
- [Anthropic Docs](https://docs.anthropic.com)

---

## ✅ CHECKLIST AVANT DE CONTINUER

Avant de passer à la phase suivante, vérifier :

- [ ] Tables e-commerce créées (products, cart_items, orders)
- [ ] Produits d'exemple ajoutés
- [ ] API panier testée et fonctionnelle
- [ ] Clés Stripe configurées
- [ ] Clés PayPal configurées (optionnel)
- [ ] Au moins une clé IA configurée (OpenAI recommandé)
- [ ] Serveur démarre sans erreur
- [ ] Tests manuels effectués

---

**Prochaine mise à jour:** Après Phase 1.2 (Paiements)  
**Dernière modification:** 24 Janvier 2026
