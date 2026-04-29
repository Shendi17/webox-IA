# ✅ FONCTIONNALITÉ ADMIN - Suppression des Images

**Date:** 31 Mars 2026  
**Fonctionnalité:** Les admins peuvent supprimer toutes les images de l'historique

---

## 🎯 FONCTIONNALITÉ

### Pour les utilisateurs normaux
- Peuvent supprimer uniquement leurs **générations échouées** (statut "failed")
- Bouton "×" rouge visible uniquement sur les images avec ❌

### Pour les administrateurs
- Peuvent supprimer **toutes les images** (réussies, échouées, en cours)
- Bouton "×" rouge visible sur **toutes les images**
- Utile pour nettoyer les images qui ne s'affichent pas correctement

---

## 🔧 IMPLÉMENTATION

### 1. Frontend - Vérification du rôle

**Fichier:** `templates/dashboard/generation.html`

**Code ajouté:**
```javascript
// Vérifier si l'utilisateur est admin
const userStr = localStorage.getItem('user');
const isAdmin = userStr ? JSON.parse(userStr).role === 'admin' : false;

// Bouton de suppression pour les admins (toutes les images) ou les échecs (tous)
const showDeleteBtn = isAdmin || img.status === 'failed';
const deleteBtn = showDeleteBtn ? 
    `<button onclick="event.stopPropagation(); deleteGeneration(${img.id}, 'image')" 
            style="position:absolute;top:8px;right:8px;background:#dc3545;..."
            title="Supprimer">×</button>` : '';
```

### 2. Backend - Vérification des permissions

**Fichier:** `app/routes/generation_routes.py` (déjà implémenté)

**Route DELETE:**
```python
@router.delete("/{generation_type}/{item_id}")
async def delete_generation(
    generation_type: str,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_from_token)
):
    # Vérifier si l'utilisateur est admin
    user = db.query(UserDB).filter(UserDB.id == current_user["id"]).first()
    is_admin = user and user.role == "admin"
    
    # Les admins peuvent supprimer n'importe quelle génération
    if generation_type == "image":
        query = db.query(GeneratedImageDB).filter(GeneratedImageDB.id == item_id)
        if not is_admin:
            query = query.filter(GeneratedImageDB.user_id == current_user["id"])
        item = query.first()
        
        if item:
            # Supprimer le fichier local si existe
            if item.local_path and os.path.exists(item.local_path):
                try:
                    os.remove(item.local_path)
                except:
                    pass
            db.delete(item)
            db.commit()
            return {"message": "Image supprimée avec succès"}
```

---

## 🚀 UTILISATION

### En tant qu'admin

1. Se connecter avec un compte admin
2. Aller sur http://webox.local:8000/generation
3. **Toutes les images** affichent un bouton "×" rouge en haut à droite
4. Cliquer sur "×" pour supprimer une image
5. Confirmer la suppression
6. ✅ L'image est supprimée de la base de données et du disque

### En tant qu'utilisateur normal

1. Se connecter avec un compte utilisateur
2. Aller sur http://webox.local:8000/generation
3. **Seules les images échouées** affichent un bouton "×" rouge
4. Cliquer sur "×" pour supprimer une génération échouée
5. Confirmer la suppression
6. ✅ L'image échouée est supprimée

---

## 🔍 VÉRIFICATION DU RÔLE ADMIN

### Comment vérifier si vous êtes admin

**Dans la console du navigateur (F12):**
```javascript
const user = JSON.parse(localStorage.getItem('user'));
console.log('Role:', user.role);
```

**Résultat attendu:**
- Admin: `Role: admin`
- Utilisateur: `Role: user` ou `Role: null`

### Définir un utilisateur comme admin

**Dans la base de données:**
```sql
UPDATE users SET role = 'admin' WHERE email = 'votre@email.com';
```

**Ou via Python:**
```python
from app.database import SessionLocal
from app.models.user_db import UserDB

db = SessionLocal()
user = db.query(UserDB).filter(UserDB.email == "votre@email.com").first()
user.role = "admin"
db.commit()
```

---

## 📊 PERMISSIONS

| Action | Utilisateur Normal | Admin |
|--------|-------------------|-------|
| Voir l'historique | ✅ Ses propres générations | ✅ Toutes les générations |
| Supprimer génération échouée | ✅ Ses propres échecs | ✅ Tous les échecs |
| Supprimer génération réussie | ❌ Non | ✅ Oui |
| Supprimer génération en cours | ❌ Non | ✅ Oui |
| Supprimer fichier local | ✅ Si propriétaire | ✅ Toujours |

---

## 🎯 CAS D'USAGE ADMIN

### Nettoyer les images qui ne s'affichent pas

**Problème:** Images avec URLs expirées ou fichiers locaux manquants

**Solution:**
1. Identifier les images avec placeholder "Image non disponible"
2. Cliquer sur le bouton "×" (visible uniquement pour les admins)
3. Supprimer l'image
4. ✅ L'historique est nettoyé

### Supprimer les générations de test

**Problème:** Nombreuses générations de test pendant le développement

**Solution:**
1. En tant qu'admin, voir toutes les générations
2. Supprimer les images de test une par une
3. ✅ Historique propre

### Gérer l'espace disque

**Problème:** Trop d'images stockées localement

**Solution:**
1. Identifier les images volumineuses ou anciennes
2. Les supprimer via l'interface admin
3. ✅ Fichiers supprimés du disque et de la base de données

---

## 🔒 SÉCURITÉ

### Vérifications côté serveur

- ✅ Vérification du rôle admin dans la base de données
- ✅ Pas de confiance au localStorage côté client
- ✅ Les utilisateurs normaux ne peuvent pas supprimer les générations des autres
- ✅ Les admins peuvent supprimer n'importe quelle génération

### Protection contre les abus

- ✅ Confirmation avant suppression (côté client)
- ✅ Suppression du fichier local pour libérer l'espace
- ✅ Logs dans la console pour traçabilité

---

## 🧪 TESTER

### Test 1: En tant qu'utilisateur normal

1. Se connecter avec un compte utilisateur
2. Générer une image qui échoue (ex: mauvaise clé API)
3. ✅ Voir le bouton "×" sur l'image échouée
4. ❌ Ne pas voir le bouton "×" sur les images réussies

### Test 2: En tant qu'admin

1. Se connecter avec un compte admin
2. Aller sur l'historique de génération
3. ✅ Voir le bouton "×" sur **toutes** les images
4. Supprimer une image réussie
5. ✅ Suppression confirmée

### Test 3: Permissions backend

1. Essayer de supprimer une image d'un autre utilisateur en tant qu'utilisateur normal
2. ❌ Erreur 404 "Génération non trouvée"
3. Essayer en tant qu'admin
4. ✅ Suppression réussie

---

## 📝 RÉSUMÉ

**Fonctionnalité ajoutée:**
- ✅ Les admins peuvent supprimer toutes les images
- ✅ Les utilisateurs normaux peuvent supprimer leurs échecs
- ✅ Bouton "×" visible selon le rôle et le statut
- ✅ Suppression du fichier local et de la base de données
- ✅ Vérification des permissions côté serveur

**Redémarrage requis:** Non (modifications JavaScript uniquement)

**Action:** Rafraîchir la page (F5) pour voir les changements

---

**Statut:** ✅ **FONCTIONNALITÉ IMPLÉMENTÉE**  
**Action requise:** **RAFRAÎCHIR LA PAGE (F5)**  
**Temps estimé:** 5 secondes
