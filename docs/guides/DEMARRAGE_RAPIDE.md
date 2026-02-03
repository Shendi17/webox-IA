# 🚀 DÉMARRAGE RAPIDE - WEBOX MULTI-IA

**Guide d'installation et de configuration en 10 minutes**

---

## ⚡ INSTALLATION EXPRESS

### 1. Prérequis

```bash
# Vérifier Python (3.9+)
python --version

# Vérifier PostgreSQL (optionnel, utilise JSON par défaut)
psql --version
```

### 2. Installation des dépendances

```bash
# Installer les dépendances
pip install -r requirements_fastapi.txt
```

### 3. Configuration minimale

```bash
# Copier le template .env
copy .env.example .env

# Éditer .env et ajouter AU MINIMUM:
# OPENAI_API_KEY=sk-proj-...
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 4. Créer les tables e-commerce

```bash
# Exécuter la migration
.\LANCER_MIGRATION_ECOMMERCE.bat

# Ou directement:
python migrations\create_ecommerce_tables.py
```

### 5. Démarrer le serveur

```bash
# Lancer le serveur
python main.py

# Ou avec reload automatique:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Accéder à l'application

```
🌐 Application: http://localhost:8000
📚 Documentation API: http://localhost:8000/docs
🔍 Health check: http://localhost:8000/health
```

---

## 🧪 TESTS RAPIDES

### Test 1: Vérifier que le serveur fonctionne

```bash
curl http://localhost:8000/health
```

Résultat attendu:
```json
{"status":"ok","app":"WeBox Multi-IA","version":"2.0.0"}
```

### Test 2: Tester le panier

```bash
python TEST_PANIER_API.py
```

### Test 3: Tester les paiements Stripe

```bash
python TEST_PAIEMENT_STRIPE.py check
```

### Test 4: Tester la génération IA

```bash
python TEST_GENERATION_IA.py
```

### Test 5: Audit complet

```bash
python AUDIT_COMPLET_FONCTIONNALITES.py
```

---

## 🔑 CONFIGURATION DES CLÉS API

### Priorité HAUTE (Indispensable)

#### 1. OpenAI (Chat GPT-4 + Images DALL-E)

```bash
# 1. Aller sur https://platform.openai.com
# 2. Créer un compte
# 3. Ajouter un moyen de paiement
# 4. Créer une clé API
# 5. Ajouter dans .env:
OPENAI_API_KEY=sk-proj-...
```

#### 2. Stripe (Paiements)

```bash
# 1. Aller sur https://stripe.com
# 2. Créer un compte
# 3. Aller dans Développeurs > Clés API
# 4. Copier les clés de TEST
# 5. Ajouter dans .env:
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Priorité MOYENNE (Recommandé)

#### 3. Anthropic Claude

```env
ANTHROPIC_API_KEY=sk-ant-...
```

#### 4. Google Gemini

```env
GOOGLE_API_KEY=AIzaSy...
```

#### 5. Groq (Gratuit et rapide)

```env
GROQ_API_KEY=gsk_...
```

### Priorité BASSE (Optionnel)

- Mistral, Stability AI, ElevenLabs, etc.
- Voir `GUIDE_CONFIGURATION_CLES_API.md` pour la liste complète

---

## 📁 STRUCTURE DU PROJET

```
webox/
├── main.py                          # Point d'entrée
├── .env                             # Configuration (à créer)
├── .env.example                     # Template de configuration
│
├── app/
│   ├── routes/                      # Routes API
│   │   ├── auth_routes.py          # Authentification
│   │   ├── cart_routes.py          # Panier (NOUVEAU)
│   │   ├── payment_routes.py       # Paiements
│   │   ├── generation_routes.py    # Génération IA
│   │   └── ...
│   │
│   ├── models/                      # Modèles base de données
│   │   ├── user_db.py              # Utilisateurs
│   │   ├── product_db.py           # Produits & Panier (NOUVEAU)
│   │   ├── generation_db.py        # Générations IA
│   │   └── ...
│   │
│   └── middleware/                  # Middlewares
│       └── auth.py                  # Authentification JWT
│
├── migrations/                      # Scripts de migration
│   └── create_ecommerce_tables.py  # Tables e-commerce (NOUVEAU)
│
├── templates/                       # Templates HTML
│   ├── home.html                   # Page d'accueil
│   ├── pages/                      # Pages
│   │   ├── marketplace.html        # Marketplace
│   │   ├── cart.html               # Panier
│   │   ├── checkout.html           # Paiement
│   │   └── ...
│   └── dashboard/                  # Dashboard
│       └── ...
│
├── static/                          # Fichiers statiques
│   ├── css/
│   ├── js/
│   └── images/
│
├── generated/                       # Fichiers générés par IA
│   ├── images/
│   ├── videos/
│   └── audio/
│
└── docs/                            # Documentation
    ├── RAPPORT_AUDIT_FONCTIONNALITES.md
    ├── GUIDE_CONFIGURATION_CLES_API.md
    ├── ETAPES_SUIVANTES.md
    └── DEMARRAGE_RAPIDE.md (ce fichier)
```

---

## 🎯 FONCTIONNALITÉS PRINCIPALES

### ✅ Fonctionnalités opérationnelles

- **Authentification** : Inscription, connexion, gestion profil
- **Chat IA** : GPT-4, Claude, Gemini, Mistral, Groq
- **Génération Images** : DALL-E 3, DALL-E 2
- **Marketplace** : Affichage produits, détails
- **Panier** : Ajout, suppression, modification (NOUVEAU ✨)
- **Paiements** : Stripe, PayPal (à configurer)
- **Blog** : Création, édition articles
- **Dashboard** : Interface utilisateur complète

### ⚠️ Fonctionnalités partielles

- **Génération Vidéo** : Structure prête, APIs à implémenter
- **Génération Audio** : Structure prête, APIs à implémenter
- **Admin** : Dashboard basique, à enrichir
- **Analytics** : Statistiques basiques

### ❌ À implémenter

- Recherche produits
- Filtres marketplace
- Codes promo
- Notifications temps réel
- Export conversations
- Factures PDF

---

## 🐛 DÉPANNAGE

### Le serveur ne démarre pas

```bash
# Vérifier les dépendances
pip install -r requirements_fastapi.txt

# Vérifier les imports
python -c "from app.database import engine; print('OK')"
```

### Erreur "Table does not exist"

```bash
# Exécuter les migrations
python migrations\create_ecommerce_tables.py
```

### Erreur "API Key not found"

```bash
# Vérifier le fichier .env
type .env

# Redémarrer le serveur après modification
```

### Erreur de paiement Stripe

```bash
# Vérifier la configuration
python TEST_PAIEMENT_STRIPE.py check

# Vérifier que vous êtes en mode test
# Les clés doivent commencer par sk_test_ et pk_test_
```

### Erreur génération IA

```bash
# Vérifier les clés API
python check_env.py

# Vérifier les quotas et crédits sur les plateformes
```

---

## 📊 COMMANDES UTILES

### Développement

```bash
# Lancer avec reload automatique
uvicorn main:app --reload

# Lancer sur un port spécifique
uvicorn main:app --port 8080

# Lancer en mode debug
uvicorn main:app --reload --log-level debug
```

### Base de données

```bash
# Voir les tables
python -c "from app.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"

# Compter les produits
python -c "from app.database import SessionLocal; from app.models.product_db import ProductDB; db = SessionLocal(); print(f'Produits: {db.query(ProductDB).count()}'); db.close()"
```

### Tests

```bash
# Test panier
python TEST_PANIER_API.py

# Test paiement (vérification config)
python TEST_PAIEMENT_STRIPE.py check

# Test paiement (complet)
python TEST_PAIEMENT_STRIPE.py

# Test génération IA
python TEST_GENERATION_IA.py

# Audit complet
python AUDIT_COMPLET_FONCTIONNALITES.py
```

---

## 📚 DOCUMENTATION

### Guides disponibles

- 📖 `RAPPORT_AUDIT_FONCTIONNALITES.md` - Audit complet (130+ fonctionnalités)
- 📖 `GUIDE_CONFIGURATION_CLES_API.md` - Configuration détaillée des APIs
- 📖 `ETAPES_SUIVANTES.md` - Plan de correction Phase 1
- 📖 `DEMARRAGE_RAPIDE.md` - Ce guide

### APIs externes

- [Stripe](https://stripe.com/docs)
- [OpenAI](https://platform.openai.com/docs)
- [Anthropic](https://docs.anthropic.com)
- [Google AI](https://ai.google.dev/docs)

---

## 🎓 PROCHAINES ÉTAPES

### Cette semaine

1. ✅ Créer les tables e-commerce
2. ✅ Tester l'API panier
3. ⏳ Configurer Stripe
4. ⏳ Configurer OpenAI
5. ⏳ Tester les paiements

### Semaine prochaine

6. Configurer autres APIs IA (Claude, Gemini)
7. Implémenter vraies APIs vidéo/audio
8. Enrichir le dashboard admin
9. Ajouter recherche et filtres marketplace
10. Tests complets end-to-end

---

## 💡 CONSEILS

### Développement

- Utiliser `--reload` pour le développement
- Consulter `/docs` pour l'API interactive
- Vérifier les logs en cas d'erreur
- Tester avec les scripts fournis

### Sécurité

- Ne jamais commiter `.env`
- Utiliser des clés de test en développement
- Changer tous les secrets en production
- Activer HTTPS en production

### Performance

- Les APIs IA peuvent être lentes (10-30s)
- Utiliser les tâches en arrière-plan
- Implémenter un cache si nécessaire
- Monitorer les coûts des APIs

### Coûts

- **OpenAI** : ~$0.03/1K tokens (GPT-4)
- **Stripe** : 1.4% + 0.25€ par transaction
- **Groq** : Gratuit (pour l'instant)
- **Gemini** : Gratuit jusqu'à 60 req/min

---

## 🆘 SUPPORT

### Problème non résolu ?

1. Consulter `RAPPORT_AUDIT_FONCTIONNALITES.md`
2. Vérifier `ETAPES_SUIVANTES.md`
3. Lire `GUIDE_CONFIGURATION_CLES_API.md`
4. Exécuter les scripts de test
5. Vérifier les logs du serveur

### Ressources

- Documentation FastAPI : https://fastapi.tiangolo.com
- Documentation SQLAlchemy : https://docs.sqlalchemy.org
- Documentation Stripe : https://stripe.com/docs
- Documentation OpenAI : https://platform.openai.com/docs

---

**Dernière mise à jour :** 24 Janvier 2026  
**Version :** 2.0.0  
**Statut :** Phase 1 en cours (31% complété)

🚀 **Bon développement avec WeBox Multi-IA !**
