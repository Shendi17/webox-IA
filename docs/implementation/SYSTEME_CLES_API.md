# 🔑 Système de Clés API - WeBox

## 📋 Vue d'ensemble

WeBox utilise un **système hybride** de gestion des clés API avec deux niveaux :

### 1️⃣ **Clés API Globales (Admin)**
- Configurées par l'**administrateur** dans son profil
- Utilisées par **TOUS les utilisateurs** par défaut
- Idéal pour un **modèle d'abonnement**
- L'admin paie les coûts API et facture les utilisateurs

### 2️⃣ **Clés API Personnelles (Optionnel)**
- Configurées par chaque utilisateur individuellement
- **Priorité sur les clés globales**
- Permet aux utilisateurs avancés d'utiliser leurs propres clés

---

## 🎯 Cas d'usage

### Scénario 1 : Modèle d'abonnement (Recommandé)
```
Admin (toi) :
├── Configure les clés API globales (OpenAI, Anthropic, etc.)
├── Paie les coûts API
└── Facture les utilisateurs via abonnement mensuel/annuel

Utilisateurs :
├── Paient leur abonnement
├── Utilisent les IAs sans configurer de clés
└── Pas de frais API directs
```

### Scénario 2 : Utilisateur avec clés personnelles
```
Utilisateur avancé :
├── Configure ses propres clés API
├── Paie directement ses coûts API
└── Ses clés ont la priorité sur les clés globales
```

---

## 🔐 Logique de sélection des clés

Quand un utilisateur utilise une IA, le système suit cette logique :

```
1. Vérifier si l'utilisateur a une clé personnelle
   ├── OUI → Utiliser la clé personnelle
   └── NON → Passer à l'étape 2

2. Vérifier si une clé globale existe
   ├── OUI → Utiliser la clé globale (admin)
   └── NON → Erreur "Aucune clé API disponible"
```

---

## 💻 Utilisation dans le code

### Récupérer une clé API pour un utilisateur

```python
from app.utils.api_keys import get_api_key

# Dans une route API
@router.post("/chat")
async def chat(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Récupérer la clé OpenAI (personnelle ou globale)
    openai_key = get_api_key(db, current_user, "openai")
    
    if not openai_key:
        raise HTTPException(
            status_code=400,
            detail="Aucune clé OpenAI disponible"
        )
    
    # Utiliser la clé pour appeler l'API
    # ...
```

### Vérifier l'accès à un provider

```python
from app.utils.api_keys import has_api_access

if has_api_access(db, current_user, "anthropic"):
    # L'utilisateur peut utiliser Anthropic
    pass
```

### Connaître la source de la clé

```python
from app.utils.api_keys import get_api_key_source

source = get_api_key_source(db, current_user, "openai")
# Retourne : "personal", "global" ou "none"
```

---

## 🛠️ Configuration Admin

### Comment configurer les clés globales :

1. Connecte-toi en tant qu'**admin**
2. Va dans **Mon Profil** (`/profile`)
3. Tu verras une section spéciale **"👑 Clés API Globales (Admin)"**
4. Entre tes clés API :
   - OpenAI : `sk-...`
   - Anthropic : `sk-ant-...`
   - Google : `AIza...`
   - Mistral : `...`
   - Groq : `gsk_...`
5. Clique sur **"👑 Sauvegarder les clés globales"**

✅ **Tous les utilisateurs peuvent maintenant utiliser les IAs !**

---

## 🔒 Sécurité

- ✅ Toutes les clés sont **chiffrées** (AES-256)
- ✅ Stockées dans la base de données PostgreSQL
- ✅ Jamais affichées en clair (masquées : `sk-12...89`)
- ✅ Seuls les admins peuvent voir/modifier les clés globales
- ✅ Chaque utilisateur ne voit que ses propres clés personnelles

---

## 💰 Modèle économique

### Option A : Abonnement (Recommandé)
```
Coûts :
- Tu paies les APIs (OpenAI, Anthropic, etc.)
- Coût estimé : 50-200€/mois selon usage

Revenus :
- Abonnement utilisateur : 20-50€/mois
- Objectif : 10+ utilisateurs payants = rentable
```

### Option B : Freemium
```
Gratuit :
- Utilisateurs utilisent leurs propres clés
- Pas de coûts pour toi

Premium :
- Utilisateurs utilisent tes clés globales
- Abonnement : 20-50€/mois
```

---

## 📊 Suivi des coûts

Pour suivre tes coûts API :

1. **OpenAI** : https://platform.openai.com/usage
2. **Anthropic** : https://console.anthropic.com/settings/usage
3. **Google** : https://console.cloud.google.com/billing

💡 **Astuce** : Configure des alertes de budget sur chaque plateforme !

---

## 🚀 Prochaines étapes

1. ✅ Configure tes clés globales
2. ⏳ Ajoute un système de quotas par utilisateur
3. ⏳ Ajoute un système de facturation (Stripe)
4. ⏳ Ajoute des statistiques d'utilisation par utilisateur
5. ⏳ Ajoute des limites de requêtes (rate limiting)

---

## ❓ FAQ

**Q : Les utilisateurs voient-ils mes clés API ?**
R : Non, elles sont chiffrées et masquées. Seul le statut "Configuré/Non configuré" est visible.

**Q : Un utilisateur peut-il utiliser mes clés sans payer ?**
R : Oui, sauf si tu ajoutes un système de vérification d'abonnement (prochaine étape).

**Q : Que se passe-t-il si je n'ai pas de clé globale ?**
R : Les utilisateurs doivent configurer leurs propres clés personnelles.

**Q : Puis-je limiter l'utilisation par utilisateur ?**
R : Pas encore, mais c'est prévu dans les prochaines versions (quotas).
