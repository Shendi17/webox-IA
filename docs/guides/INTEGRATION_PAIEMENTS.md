# 💳 INTÉGRATION DES MOYENS DE PAIEMENT - WEBOX

## 📋 Vue d'ensemble

Ce document décrit l'intégration complète des moyens de paiement dans WeBox :
- **Stripe** : Paiements par carte bancaire (Visa, Mastercard, Amex)
- **PayPal** : Paiements via compte PayPal
- **Virement bancaire** : Paiements par virement SEPA

---

## 🏗️ Architecture

### **Fichiers créés**

1. **`app/services/payment_service.py`** - Service de gestion des paiements
2. **`app/routes/payment_routes.py`** - Routes API pour les paiements
3. **`templates/pages/checkout.html`** - Page de paiement (modifiée)
4. **`.env.example`** - Configuration des clés API (mise à jour)

### **Fichiers modifiés**

1. **`main.py`** - Ajout des routes de paiement
2. **`templates/pages/checkout.html`** - Intégration Stripe Elements et PayPal SDK

---

## 🔧 Configuration

### **1. Clés API Stripe**

```bash
# Dans votre fichier .env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**Obtenir les clés :**
1. Créer un compte sur https://dashboard.stripe.com/
2. Aller dans **Développeurs > Clés API**
3. Copier la clé publique (`pk_test_...`) et la clé secrète (`sk_test_...`)
4. Pour le webhook : **Développeurs > Webhooks > Ajouter un endpoint**
   - URL : `https://votre-domaine.com/api/payment/stripe/webhook`
   - Événements : `payment_intent.succeeded`, `payment_intent.payment_failed`

### **2. Clés API PayPal**

```bash
# Dans votre fichier .env
PAYPAL_CLIENT_ID=...
PAYPAL_CLIENT_SECRET=...
PAYPAL_MODE=sandbox
PAYPAL_RETURN_URL=http://webox.local:8000/api/payment/paypal/success
PAYPAL_CANCEL_URL=http://webox.local:8000/api/payment/paypal/cancel
```

**Obtenir les clés :**
1. Créer un compte sur https://developer.paypal.com/
2. Aller dans **Dashboard > My Apps & Credentials**
3. Créer une application (Sandbox pour tests, Live pour production)
4. Copier le **Client ID** et le **Secret**

### **3. Informations bancaires**

```bash
# Dans votre fichier .env
BANK_NAME=Banque WeBox
BANK_IBAN=FR76 XXXX XXXX XXXX XXXX XXXX XXX
BANK_BIC=WBOXFRPP
BANK_ACCOUNT_HOLDER=WeBox SAS
```

---

## 📦 Installation des dépendances

```bash
pip install stripe
pip install paypalrestsdk
```

Ou ajouter dans `requirements.txt` :
```
stripe>=7.0.0
paypalrestsdk>=1.13.1
```

---

## 🚀 Utilisation

### **Page Checkout**

La page `/checkout` propose 3 méthodes de paiement :

#### **1. Carte bancaire (Stripe)**
- Formulaire sécurisé avec Stripe Elements
- Validation en temps réel
- Support 3D Secure
- Paiement instantané

#### **2. PayPal**
- Bouton PayPal intégré
- Redirection vers PayPal
- Retour automatique après paiement
- Protection des achats PayPal

#### **3. Virement bancaire**
- Affichage des coordonnées bancaires
- Génération d'une référence unique
- Délai de traitement : 2-3 jours ouvrés
- Vérification manuelle ou automatique

---

## 🔄 Flux de paiement

### **Stripe (Carte bancaire)**

```
1. Utilisateur remplit le formulaire
2. Clic sur "Valider le paiement"
3. Création d'un Payment Intent via API
4. Stripe Elements valide la carte
5. Confirmation du paiement
6. Redirection vers page de confirmation
```

**Code JavaScript :**
```javascript
async function processStripePayment() {
    // Créer l'intention de paiement
    const response = await fetch('/api/payment/stripe/create-intent', {
        method: 'POST',
        body: JSON.stringify({ amount: 95.96, currency: 'eur' })
    });
    
    const data = await response.json();
    
    // Confirmer le paiement
    const result = await stripe.confirmCardPayment(data.client_secret, {
        payment_method: { card: cardElement }
    });
    
    if (result.paymentIntent.status === 'succeeded') {
        // Paiement réussi
    }
}
```

### **PayPal**

```
1. Utilisateur sélectionne PayPal
2. Clic sur le bouton PayPal
3. Création d'une commande via API
4. Redirection vers PayPal
5. Utilisateur se connecte et valide
6. Retour sur WeBox avec confirmation
```

**Code JavaScript :**
```javascript
paypal.Buttons({
    createOrder: function() {
        return fetch('/api/payment/paypal/create-order', {
            method: 'POST',
            body: JSON.stringify({ amount: 95.96 })
        }).then(res => res.json()).then(data => data.order_id);
    },
    onApprove: function(data) {
        return fetch(`/api/payment/paypal/success?paymentId=${data.orderID}`)
            .then(() => goToStep(3));
    }
}).render('#paypal-button-container');
```

### **Virement bancaire**

```
1. Utilisateur sélectionne Virement
2. Affichage des coordonnées bancaires
3. Génération d'une référence unique
4. Utilisateur effectue le virement
5. Vérification manuelle ou automatique
6. Activation de la commande
```

---

## 🛡️ Sécurité

### **Stripe**
- ✅ Cryptage SSL/TLS
- ✅ PCI-DSS Level 1 compliant
- ✅ 3D Secure (SCA)
- ✅ Détection de fraude intégrée
- ✅ Webhooks signés

### **PayPal**
- ✅ Protection des achats
- ✅ Cryptage de bout en bout
- ✅ Authentification 2FA
- ✅ Détection de fraude

### **Bonnes pratiques**
- Ne jamais stocker les numéros de carte
- Utiliser HTTPS en production
- Valider les webhooks
- Logger les transactions
- Gérer les erreurs proprement

---

## 💰 Coûts

### **Stripe**
- **Europe** : 1.4% + 0.25€ par transaction
- **International** : 2.9% + 0.25€ par transaction
- Pas de frais mensuels
- Pas de frais de setup

### **PayPal**
- **Europe** : 3.4% + 0.35€ par transaction
- **International** : 4.4% + 0.35€ par transaction
- Pas de frais mensuels
- Conversion de devises : 2.5%

### **Virement bancaire**
- **Gratuit** (pas de frais API)
- Délai : 2-3 jours ouvrés
- Vérification manuelle recommandée

---

## 🧪 Tests

### **Mode Test Stripe**

Cartes de test :
```
Succès : 4242 4242 4242 4242
Échec : 4000 0000 0000 0002
3D Secure : 4000 0027 6000 3184
```

Date d'expiration : N'importe quelle date future  
CVV : N'importe quel 3 chiffres

### **Mode Sandbox PayPal**

1. Créer des comptes sandbox sur https://developer.paypal.com/
2. Utiliser les identifiants sandbox pour tester
3. Utiliser `PAYPAL_MODE=sandbox` dans `.env`

### **Virement bancaire**

Tester avec une référence fictive et vérifier l'affichage des coordonnées.

---

## 📊 Webhooks

### **Stripe Webhook**

Endpoint : `/api/payment/stripe/webhook`

Événements gérés :
- `payment_intent.succeeded` - Paiement réussi
- `payment_intent.payment_failed` - Paiement échoué

Configuration :
```python
@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
    )
    
    if event['type'] == 'payment_intent.succeeded':
        # Mettre à jour la commande
        pass
```

---

## 🔍 Monitoring

### **Logs à surveiller**
- Tentatives de paiement
- Paiements réussis/échoués
- Erreurs API
- Webhooks reçus

### **Métriques importantes**
- Taux de conversion
- Taux d'échec par méthode
- Montant moyen des transactions
- Temps de traitement

---

## 🐛 Dépannage

### **Erreur : "Stripe is not defined"**
- Vérifier que le SDK Stripe est chargé : `<script src="https://js.stripe.com/v3/"></script>`

### **Erreur : "Invalid API Key"**
- Vérifier les clés dans `.env`
- S'assurer d'utiliser `pk_test_` pour les tests

### **PayPal ne se charge pas**
- Vérifier le Client ID dans l'URL du SDK
- Vérifier la connexion internet
- Consulter la console JavaScript

### **Virement : référence non générée**
- Vérifier que `generateBankReference()` est appelé
- Vérifier l'élément `#bankReference` dans le HTML

---

## 📚 Ressources

### **Documentation officielle**
- Stripe : https://stripe.com/docs
- PayPal : https://developer.paypal.com/docs/
- Stripe Elements : https://stripe.com/docs/payments/elements

### **Exemples de code**
- Stripe Checkout : https://stripe.com/docs/payments/checkout
- PayPal Buttons : https://developer.paypal.com/docs/checkout/

### **Support**
- Stripe Support : https://support.stripe.com/
- PayPal Support : https://www.paypal.com/fr/smarthelp/

---

## ✅ Checklist de mise en production

- [ ] Obtenir les clés API production (Stripe & PayPal)
- [ ] Configurer les webhooks en production
- [ ] Activer HTTPS
- [ ] Tester tous les flux de paiement
- [ ] Configurer les emails de confirmation
- [ ] Mettre en place le monitoring
- [ ] Vérifier la conformité PCI-DSS
- [ ] Configurer les remboursements
- [ ] Tester les cas d'erreur
- [ ] Former l'équipe support

---

## 🎯 Prochaines étapes

1. **Abonnements récurrents** - Intégrer Stripe Subscriptions
2. **Apple Pay / Google Pay** - Ajouter les paiements mobiles
3. **Crypto-monnaies** - Intégrer Coinbase Commerce
4. **Facturation automatique** - Générer des factures PDF
5. **Multi-devises** - Support EUR, USD, GBP, etc.

---

**Date de création** : 23 janvier 2026  
**Version** : 1.0  
**Auteur** : Cascade AI
