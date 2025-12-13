# 📱 PHASE 3 : RÉSEAUX SOCIAUX - ARCHITECTURE

**Date** : 15 Novembre 2025  
**Statut** : 🔄 **EN COURS D'IMPLÉMENTATION**

---

## 🎯 OBJECTIF

Créer un système complet de gestion des réseaux sociaux avec :
- Connexion OAuth multi-plateformes
- Calendrier de publication
- Création de posts avec IA
- Cross-posting
- Statistiques d'engagement

---

## 🏗️ ARCHITECTURE TECHNIQUE

### **1. Base de données**

#### **Table : social_accounts**
```sql
CREATE TABLE social_accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    platform VARCHAR(50) NOT NULL,  -- instagram, facebook, twitter, linkedin, tiktok, youtube
    account_name VARCHAR(255),
    account_id VARCHAR(255),
    access_token TEXT,  -- Encrypted
    refresh_token TEXT,  -- Encrypted
    expires_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME,
    updated_at DATETIME
);
```

#### **Table : scheduled_posts**
```sql
CREATE TABLE scheduled_posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    media_urls JSON,  -- ['url1', 'url2']
    platforms JSON,  -- ['instagram', 'facebook']
    hashtags JSON,  -- ['#tag1', '#tag2']
    scheduled_time DATETIME,
    status VARCHAR(50),  -- scheduled, published, failed, cancelled
    published_at DATETIME,
    error_message TEXT,
    created_at DATETIME
);
```

#### **Table : post_analytics**
```sql
CREATE TABLE post_analytics (
    id INTEGER PRIMARY KEY,
    post_id INTEGER NOT NULL,
    platform VARCHAR(50),
    platform_post_id VARCHAR(255),
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    engagement_rate FLOAT,
    updated_at DATETIME
);
```

---

## 🔐 AUTHENTIFICATION OAUTH

### **Plateformes supportées**

#### **1. Instagram (Meta API)**
```python
INSTAGRAM_CONFIG = {
    'client_id': os.getenv('INSTAGRAM_CLIENT_ID'),
    'client_secret': os.getenv('INSTAGRAM_CLIENT_SECRET'),
    'redirect_uri': 'https://webox.com/api/social/callback/instagram',
    'scope': 'instagram_basic,instagram_content_publish'
}
```

#### **2. Facebook (Meta API)**
```python
FACEBOOK_CONFIG = {
    'client_id': os.getenv('FACEBOOK_APP_ID'),
    'client_secret': os.getenv('FACEBOOK_APP_SECRET'),
    'redirect_uri': 'https://webox.com/api/social/callback/facebook',
    'scope': 'pages_manage_posts,pages_read_engagement'
}
```

#### **3. Twitter/X (API v2)**
```python
TWITTER_CONFIG = {
    'client_id': os.getenv('TWITTER_CLIENT_ID'),
    'client_secret': os.getenv('TWITTER_CLIENT_SECRET'),
    'redirect_uri': 'https://webox.com/api/social/callback/twitter',
    'scope': 'tweet.read,tweet.write,users.read'
}
```

#### **4. LinkedIn**
```python
LINKEDIN_CONFIG = {
    'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
    'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
    'redirect_uri': 'https://webox.com/api/social/callback/linkedin',
    'scope': 'w_member_social,r_basicprofile'
}
```

#### **5. TikTok**
```python
TIKTOK_CONFIG = {
    'client_key': os.getenv('TIKTOK_CLIENT_KEY'),
    'client_secret': os.getenv('TIKTOK_CLIENT_SECRET'),
    'redirect_uri': 'https://webox.com/api/social/callback/tiktok',
    'scope': 'video.upload,user.info.basic'
}
```

#### **6. YouTube (Google API)**
```python
YOUTUBE_CONFIG = {
    'client_id': os.getenv('GOOGLE_CLIENT_ID'),
    'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
    'redirect_uri': 'https://webox.com/api/social/callback/youtube',
    'scope': 'https://www.googleapis.com/auth/youtube.upload'
}
```

---

## 📋 ROUTES API

### **Authentification**
```python
GET  /api/social/connect/{platform}           # Initier OAuth
GET  /api/social/callback/{platform}          # Callback OAuth
POST /api/social/disconnect/{platform}        # Déconnecter
GET  /api/social/accounts                     # Liste des comptes
POST /api/social/accounts/{id}/refresh        # Refresh token
```

### **Posts**
```python
POST /api/social/posts                        # Créer un post
GET  /api/social/posts                        # Lister les posts
GET  /api/social/posts/{id}                   # Détails d'un post
PUT  /api/social/posts/{id}                   # Modifier un post
DELETE /api/social/posts/{id}                 # Supprimer un post
POST /api/social/posts/{id}/publish           # Publier maintenant
POST /api/social/posts/{id}/schedule          # Programmer
POST /api/social/posts/{id}/cancel            # Annuler
```

### **IA**
```python
POST /api/social/generate/caption             # Générer caption
POST /api/social/generate/hashtags            # Générer hashtags
POST /api/social/suggest/times                # Meilleurs moments
POST /api/social/analyze/content              # Analyser contenu
```

### **Statistiques**
```python
GET  /api/social/stats/overview               # Vue d'ensemble
GET  /api/social/stats/{platform}             # Stats par plateforme
GET  /api/social/stats/engagement             # Taux d'engagement
GET  /api/social/stats/growth                 # Croissance followers
GET  /api/social/stats/best-posts             # Meilleurs posts
```

---

## 🎨 INTERFACE UTILISATEUR

### **1. Section Comptes connectés**
```html
<div class="accounts-grid">
    <div class="account-card instagram">
        <div class="platform-icon">📷</div>
        <h3>Instagram</h3>
        <button onclick="connectInstagram()">Connecter</button>
    </div>
    <!-- Autres plateformes... -->
</div>
```

### **2. Calendrier de publication**
```javascript
// Utiliser FullCalendar.js
const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: scheduledPosts,
    eventClick: (info) => editPost(info.event.id)
});
```

### **3. Créateur de post**
```html
<div class="post-creator">
    <textarea id="postContent" placeholder="Écrivez votre post..."></textarea>
    <div class="media-upload">
        <button onclick="uploadMedia()">📷 Ajouter média</button>
    </div>
    <div class="platforms-selector">
        <label><input type="checkbox" name="instagram"> Instagram</label>
        <label><input type="checkbox" name="facebook"> Facebook</label>
        <!-- Autres... -->
    </div>
    <button onclick="generateCaption()">✨ Générer avec IA</button>
    <button onclick="schedulePost()">📅 Programmer</button>
</div>
```

---

## 🤖 GÉNÉRATION IA

### **Génération de captions**
```python
async def generate_caption(topic: str, tone: str, platform: str):
    prompt = f"""
    Créer une caption {tone} pour {platform} sur le sujet : {topic}
    
    Contraintes:
    - Instagram: 2200 caractères max
    - Twitter: 280 caractères max
    - LinkedIn: Professionnel
    - TikTok: Court et accrocheur
    """
    
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### **Génération de hashtags**
```python
async def generate_hashtags(content: str, platform: str, count: int = 10):
    prompt = f"""
    Générer {count} hashtags pertinents pour ce post {platform}:
    {content}
    
    Critères:
    - Populaires mais pas trop génériques
    - Pertinents au contenu
    - Mix de tailles (grands/moyens/petits)
    """
    
    # GPT-4 génère les hashtags
    return ['#tag1', '#tag2', ...]
```

### **Meilleurs moments de publication**
```python
async def suggest_best_times(platform: str, user_id: int):
    # Analyser l'historique des posts
    analytics = get_user_analytics(user_id, platform)
    
    # Calculer les moments avec le meilleur engagement
    best_times = analyze_engagement_patterns(analytics)
    
    return {
        'monday': ['09:00', '18:00'],
        'tuesday': ['10:00', '19:00'],
        # ...
    }
```

---

## 📊 SYSTÈME DE STATISTIQUES

### **Collecte des données**
```python
async def fetch_platform_analytics(account_id: int):
    account = get_account(account_id)
    
    if account.platform == 'instagram':
        data = await fetch_instagram_insights(account)
    elif account.platform == 'facebook':
        data = await fetch_facebook_insights(account)
    # ...
    
    save_analytics(data)
```

### **Calcul du taux d'engagement**
```python
def calculate_engagement_rate(post):
    total_interactions = post.likes + post.comments + post.shares
    engagement_rate = (total_interactions / post.views) * 100
    return round(engagement_rate, 2)
```

---

## ⏰ SYSTÈME DE SCHEDULING

### **Background task avec Celery**
```python
@celery.task
def check_scheduled_posts():
    now = datetime.utcnow()
    posts = ScheduledPost.query.filter(
        ScheduledPost.scheduled_time <= now,
        ScheduledPost.status == 'scheduled'
    ).all()
    
    for post in posts:
        publish_post.delay(post.id)

@celery.task
def publish_post(post_id):
    post = ScheduledPost.query.get(post_id)
    
    for platform in post.platforms:
        try:
            if platform == 'instagram':
                publish_to_instagram(post)
            elif platform == 'facebook':
                publish_to_facebook(post)
            # ...
            
            post.status = 'published'
        except Exception as e:
            post.status = 'failed'
            post.error_message = str(e)
```

---

## 🔒 SÉCURITÉ

### **Chiffrement des tokens**
```python
from cryptography.fernet import Fernet

def encrypt_token(token: str) -> str:
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    key = os.getenv('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.decrypt(encrypted_token.encode()).decode()
```

### **Refresh automatique des tokens**
```python
async def refresh_access_token(account_id: int):
    account = get_account(account_id)
    
    if account.expires_at < datetime.utcnow():
        new_token = await request_new_token(
            account.platform,
            account.refresh_token
        )
        
        account.access_token = encrypt_token(new_token)
        account.expires_at = datetime.utcnow() + timedelta(days=60)
        db.commit()
```

---

## 📦 DÉPENDANCES REQUISES

```txt
# OAuth & API
requests-oauthlib==1.3.1
python-twitter==3.5
facebook-sdk==3.1.0
linkedin-api==2.0.0

# Scheduling
celery==5.3.0
redis==4.5.0

# Chiffrement
cryptography==41.0.0

# Calendrier
python-dateutil==2.8.2
```

---

## 🚀 PROCHAINES ÉTAPES D'IMPLÉMENTATION

### **Étape 1 : Modèles de base de données** ✅
- Créer `SocialAccountDB`
- Créer `ScheduledPostDB`
- Créer `PostAnalyticsDB`

### **Étape 2 : Routes d'authentification**
- Implémenter OAuth pour chaque plateforme
- Gestion des callbacks
- Stockage sécurisé des tokens

### **Étape 3 : Interface utilisateur**
- Page `social.html` complète
- Calendrier interactif
- Créateur de posts

### **Étape 4 : Génération IA**
- Captions intelligentes
- Hashtags optimisés
- Suggestions de timing

### **Étape 5 : Système de publication**
- Background tasks
- Cross-posting
- Gestion des erreurs

### **Étape 6 : Statistiques**
- Collecte des données
- Dashboards
- Rapports

---

## 💰 ESTIMATION DES COÛTS

| Service | Coût |
|---------|------|
| GPT-4 (captions) | $0.03 par caption |
| GPT-4 (hashtags) | $0.01 par set |
| API Instagram | Gratuit (limites) |
| API Facebook | Gratuit (limites) |
| API Twitter | $100/mois (Basic) |
| API LinkedIn | Gratuit |
| API TikTok | Gratuit |
| API YouTube | Gratuit |

**Total estimé** : $100-150/mois pour usage professionnel

---

**Phase 3 en cours d'implémentation...**
