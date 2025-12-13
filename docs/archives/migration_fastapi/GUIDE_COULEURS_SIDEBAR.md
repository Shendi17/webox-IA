# 🎨 GUIDE DE MODIFICATION DES COULEURS DE LA SIDEBAR

## 📍 Fichier à Modifier
**`modules/core/theme_config.py`**

---

## 🎯 TOUS LES ÉLÉMENTS DANS L'ORDRE D'APPARITION

### 1️⃣ **LIENS EN HAUT** (app, agents ia, assistant vocal, blog, generation audio, generation images, generation video)
```python
# Ligne 28
"top_links_text": "#ffffff",  # Couleur des liens - BLANC

# Ligne 29
"top_links_hover": "rgba(255, 215, 0, 0.1)",  # Fond au survol
```
**Style :** Normal (pas de gras)

---

### 2️⃣ **TITRE PRINCIPAL** (🤖 WeBox Multi-IA)
```python
# Ligne 34
"main_title_text": "#ffd700",  # JAUNE
```
**Style :** Normal (pas de gras), centré

---

### 3️⃣ **NOM UTILISATEUR** (👤 Administrateur)
```python
# Ligne 39
"user_name_text": "#ffd700",  # JAUNE
```
**Style :** Normal (pas de gras), centré, taille 1.1rem

---

### 4️⃣ **SÉPARATEURS HORIZONTAUX** (<hr>)
```python
# Ligne 44
"separator_color": "#ffd700",  # JAUNE
```

---

### 5️⃣ **SOUS-TITRES** (📍 Navigation, 🤖 Sélection des IA)
```python
# Ligne 49
"subtitle_text": "#ffd700",  # JAUNE
```
**Style :** Normal (pas de gras)

---

### 6️⃣ **BOUTONS RADIO NAVIGATION** (💬 Chat Multi-IA, 🎯 Assistants, 📚 Prompts, etc.)
```python
# Ligne 54
"radio_text": "#ffffff",  # Texte - BLANC

# Ligne 55
"radio_hover_bg": "rgba(255, 215, 0, 0.1)",  # Fond au survol
```
**Style :** Normal (pas de gras), taille 1.05rem, padding 0.8rem 1rem

**Liste complète :**
- 💬 Chat Multi-IA
- 🎯 Assistants
- 📚 Prompts
- 🎨 Images IA
- 🎙️ Audio IA
- 🎬 Vidéo IA
- 📞 Assistant Vocal
- 🤖 Agents IA
- 🔧 Catalogue IA
- 🔄 Combinaisons
- ⚡ Pipedream
- 📰 Blog
- 📖 Documentation
- ⚙️ Configuration

---

### 7️⃣ **EXPANDERS OUVERTS** (💬 Texte & Conversation, 🔍 Recherche & Web, 💻 Code & Développement, 🌐 Open-Source)
```python
# Ligne 60
"expander_open_title": "#000000",  # Titre cliquable - NOIR

# Ligne 61
"expander_open_content": "#ffffff",  # Contenu - BLANC
```
**Style :** Normal (pas de gras)

---

### 8️⃣ **EXPANDERS FERMÉS** (⚙️ Paramètres avancés, ➕ Nouveau dossier, 📁 Général)
```python
# Ligne 66
"expander_closed_title": "#ffffff",  # Titre cliquable - BLANC

# Ligne 67
"expander_closed_content": "#ffffff",  # Contenu - BLANC
```
**Style :** Normal (pas de gras)

---

### 9️⃣ **STYLE GÉNÉRAL DES EXPANDERS**
```python
# Ligne 72
"expander_background": "rgba(255, 255, 255, 0.05)",  # Fond

# Ligne 73
"expander_border": "rgba(255, 215, 0, 0.3)",  # Bordure
```

---

### 🔟 **DROPDOWNS** (Choose options)
```python
# Ligne 78
"dropdown_text": "#000000",  # Texte - NOIR

# Ligne 79
"dropdown_bg": "#ffffff",  # Fond - BLANC

# Ligne 80
"dropdown_border": "#ffd700",  # Bordure - JAUNE
```

---

### 1️⃣1️⃣ **INPUTS ET FORMULAIRES**
```python
# Ligne 85
"input_text": "#000000",  # Texte saisi - NOIR

# Ligne 86
"input_background": "#ffffff",  # Fond - BLANC

# Ligne 87
"input_border": "#ffd700",  # Bordure - JAUNE

# Ligne 88
"input_placeholder": "#666666",  # Texte placeholder - GRIS
```

---

### 1️⃣2️⃣ **BOUTONS STREAMLIT** (boutons jaunes en bas)
```python
# Ligne 93
"button_text": "#1a1a2e",  # Texte - BLEU FONCÉ
```

---

## 🎨 PALETTE DE COULEURS SUGGÉRÉES

```python
# Blanc
"#ffffff"

# Noir
"#000000"

# Jaune (principal)
"#ffd700"

# Gris clair
"#e0e0e0"

# Gris foncé
"#666666"

# Bleu foncé
"#1a1a2e"

# Bleu
"#4169e1"

# Orange
"#ff8c00"

# Vert clair
"#00ff88"

# Rose
"#ff69b4"
```

---

## ⚡ APRÈS MODIFICATION

1. **Sauvegarde** le fichier (`Ctrl + S`)
2. **Relance** l'application : `.\restart_app.ps1`
3. **Recharge** la page : `Ctrl + Shift + R`

---

## 💡 ASTUCE

**Pour modifier rapidement une couleur :**
1. Cherche le numéro de ligne dans ce guide
2. Ouvre `modules/core/theme_config.py`
3. Va à la ligne indiquée
4. Change la valeur hexadécimale
5. Sauvegarde et relance

**Exemple :**
```python
# Avant
"expander_open_title": "#000000",  # NOIR

# Après
"expander_open_title": "#ffd700",  # JAUNE
```

---

## 🎯 RÉSUMÉ RAPIDE

| # | Élément | Ligne | Couleur | Style |
|---|---------|-------|---------|-------|
| 1️⃣ | Liens en haut | 28 | Blanc | Normal |
| 2️⃣ | Titre principal | 34 | Jaune | Normal, centré |
| 3️⃣ | Nom utilisateur | 39 | Jaune | Normal, centré |
| 4️⃣ | Séparateurs | 44 | Jaune | - |
| 5️⃣ | Sous-titres | 49 | Jaune | Normal |
| 6️⃣ | Boutons radio | 54 | Blanc | Normal |
| 7️⃣ | Expanders ouverts (titre) | 60 | Noir | Normal |
| 7️⃣ | Expanders ouverts (contenu) | 61 | Blanc | Normal |
| 8️⃣ | Expanders fermés (titre) | 66 | Blanc | Normal |
| 8️⃣ | Expanders fermés (contenu) | 67 | Blanc | Normal |
| 🔟 | Dropdowns (texte) | 78 | Noir | - |
| 🔟 | Dropdowns (fond) | 79 | Blanc | - |
| 1️⃣1️⃣ | Inputs (texte) | 85 | Noir | - |
| 1️⃣1️⃣ | Inputs (fond) | 86 | Blanc | - |
| 1️⃣2️⃣ | Boutons Streamlit | 93 | Bleu foncé | - |

---

## 📋 ORDRE D'APPARITION DANS LA SIDEBAR

1. **Liens en haut** (app, agents ia, blog, etc.)
2. **Titre principal** (🤖 WeBox Multi-IA)
3. **Nom utilisateur** (👤 Administrateur)
4. **Séparateur** (<hr>)
5. **Sous-titre** (📍 Navigation)
6. **Boutons radio** (💬 Chat Multi-IA, 🎯 Assistants, etc.)
7. **Séparateur** (<hr>)
8. **Sous-titre** (🤖 Sélection des IA)
9. **Expanders ouverts** (💬 Texte & Conversation, etc.)
10. **Expanders fermés** (⚙️ Paramètres, ➕ Nouveau dossier, 📁 Général)
