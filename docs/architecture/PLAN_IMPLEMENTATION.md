# 🚀 PLAN D'IMPLÉMENTATION DES FONCTIONNALITÉS

## 📋 Vue d'ensemble

Suite à l'audit complet, voici le plan d'action prioritaire pour rendre toutes les fonctionnalités opérationnelles.

---

## ✅ ÉTAPE 1 : AGENTS IA SPÉCIALISÉS (TERMINÉ)

### Statut : ✅ **IMPLÉMENTÉ**

### Ce qui a été fait :
- ✅ Mise à jour des 8 agents avec contextes professionnels détaillés
- ✅ Routes API fonctionnelles (`/api/assistants/chat`)
- ✅ System prompts spécialisés pour chaque agent

### Agents disponibles :
1. **💼 Agent Commercial** (`sales`) - Vente B2B/B2C, négociation
2. **📱 Agent Marketing** (`marketing`) - Marketing digital, SEO, publicité
3. **💰 Agent Financier** (`finance`) - Finance, comptabilité, analyse
4. **⚙️ Agent Opérations** (`operations`) - Gestion de projet, processus
5. **👥 Agent RH** (`hr`) - Ressources humaines, recrutement
6. **⚖️ Agent Juridique** (`legal`) - Droit des affaires, contrats
7. **💻 Agent Technique** (`tech`) - Développement, architecture
8. **🎯 Agent Stratégie** (`strategy`) - Stratégie d'entreprise, business model

### Mapping frontend → backend :
```javascript
const agentMapping = {
    'ventes': 'sales',
    'marketing': 'marketing',
    'finance': 'finance',
    'operations': 'operations',
    'rh': 'hr',
    'service-client': 'legal',  // À ajuster
    'produit': 'tech',          // À ajuster
    'strategie': 'strategy'
};
```

---

## 🎯 ÉTAPE 2 : GÉNÉRATION MULTI-MÉDIA (EN COURS)

### Priorité : 🔴 **CRITIQUE**

### 5 Fonctionnalités à implémenter :

#### **1. Génération d'Images** 📸
```python
# app/routes/generation_routes.py

@router.post("/api/generation/image")
async def generate_image(
    prompt: str,
    model: str,  # dall-e-3, midjourney, stable-diffusion
    size: str = "1024x1024",
    style: str = "natural",
    user: dict = Depends(get_current_user)
):
    """
    Générer une image avec l'IA choisie
    """
    if model == "dall-e-3":
        # Utiliser OpenAI DALL-E 3
        client = OpenAI(api_key=user_api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="hd",
            n=1
        )
        image_url = response.data[0].url
        
    elif model == "stable-diffusion":
        # Utiliser Stability AI
        pass
        
    # Sauvegarder en DB
    db_image = GeneratedImage(
        user_id=user["id"],
        prompt=prompt,
        model=model,
        image_url=image_url
    )
    db.add(db_image)
    db.commit()
    
    return {"image_url": image_url, "id": db_image.id}
```

#### **2. Génération de Vidéos** 🎬
```python
@router.post("/api/generation/video")
async def generate_video(
    prompt: str,
    model: str,  # runway, pika, luma
    duration: int = 5,
    user: dict = Depends(get_current_user)
):
    """
    Générer une vidéo avec l'IA choisie
    """
    if model == "runway":
        # Utiliser Runway ML API
        pass
    
    return {"video_url": video_url, "id": video_id}
```

#### **3. Génération d'Audio** 🎙️
```python
@router.post("/api/generation/audio")
async def generate_audio(
    prompt: str,
    model: str,  # suno, udio, elevenlabs
    duration: int = 30,
    user: dict = Depends(get_current_user)
):
    """
    Générer de l'audio/musique avec l'IA choisie
    """
    if model == "elevenlabs":
        # Text-to-Speech avec ElevenLabs
        pass
    elif model == "suno":
        # Génération de musique avec Suno
        pass
    
    return {"audio_url": audio_url, "id": audio_id}
```

#### **4. Création d'eBooks** 📖
```python
@router.post("/api/generation/ebook")
async def generate_ebook(
    title: str,
    subject: str,
    chapters: int = 10,
    tone: str = "professionnel",
    audience: str = "professionnels",
    language: str = "fr",
    options: dict = {},
    user: dict = Depends(get_current_user)
):
    """
    Créer un eBook complet avec GPT-4 + DALL-E + PDF
    """
    # 1. Générer le plan avec GPT-4
    plan_prompt = f"""Crée un plan détaillé pour un eBook intitulé "{title}" sur le sujet : {subject}.
    
    Nombre de chapitres : {chapters}
    Ton : {tone}
    Public cible : {audience}
    
    Fournis un plan structuré avec :
    - Titre de chaque chapitre
    - Sous-sections principales
    - Points clés à aborder
    """
    
    plan = await openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": plan_prompt}]
    )
    
    # 2. Rédiger chaque chapitre
    chapters_content = []
    for i, chapter in enumerate(plan.chapters):
        chapter_prompt = f"""Rédige le chapitre {i+1} : {chapter.title}
        
        Plan du chapitre : {chapter.outline}
        Ton : {tone}
        Public : {audience}
        Longueur : ~2000 mots
        """
        
        content = await openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": chapter_prompt}]
        )
        chapters_content.append(content)
    
    # 3. Générer la couverture avec DALL-E
    if options.get("cover"):
        cover_prompt = f"Couverture professionnelle pour un eBook intitulé '{title}' sur {subject}"
        cover = await openai_client.images.generate(
            model="dall-e-3",
            prompt=cover_prompt,
            size="1024x1792"
        )
        cover_url = cover.data[0].url
    
    # 4. Assembler en PDF avec ReportLab
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    pdf_file = f"ebooks/{user['id']}/{title}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Ajouter le contenu
    for chapter in chapters_content:
        story.append(Paragraph(chapter.title, styles['Heading1']))
        story.append(Paragraph(chapter.content, styles['BodyText']))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    
    # 5. Sauvegarder en DB
    ebook = EBook(
        user_id=user["id"],
        title=title,
        chapters=chapters,
        file_url=pdf_file,
        cover_url=cover_url
    )
    db.add(ebook)
    db.commit()
    
    return {"ebook_id": ebook.id, "file_url": pdf_file}
```

#### **5. Création de Vidéos Short** 📱
```python
@router.post("/api/generation/short")
async def generate_short_video(
    subject: str,
    duration: int = 60,
    format: str = "9:16",
    style: str = "moderne",
    voice: str = "femme-fr",
    options: dict = {},
    user: dict = Depends(get_current_user)
):
    """
    Créer une vidéo short pour TikTok/Reels/Shorts
    """
    # 1. Générer le script avec GPT-4
    script_prompt = f"""Écris un script de {duration} secondes pour une vidéo {format} sur : {subject}
    
    Style : {style}
    Format : TikTok/Reels
    
    Le script doit :
    - Avoir un hook accrocheur dans les 3 premières secondes
    - Être dynamique et engageant
    - Se terminer par un CTA
    - Être découpé en scènes de 5-10 secondes
    """
    
    script = await openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": script_prompt}]
    )
    
    # 2. Générer les visuels avec DALL-E
    scenes = script.scenes  # 3-5 scènes
    visuals = []
    for scene in scenes:
        image = await openai_client.images.generate(
            model="dall-e-3",
            prompt=f"{style} style: {scene.visual_description}",
            size="1024x1024"
        )
        visuals.append(image.data[0].url)
    
    # 3. Générer la voix-off avec ElevenLabs
    voice_file = await elevenlabs_client.text_to_speech(
        text=script.narration,
        voice_id=voice_mapping[voice]
    )
    
    # 4. Assembler la vidéo avec FFmpeg
    import subprocess
    
    # Créer une vidéo à partir des images + voix
    output_file = f"shorts/{user['id']}/{subject[:20]}.mp4"
    
    # Commande FFmpeg pour assembler
    cmd = [
        "ffmpeg",
        "-loop", "1", "-t", str(duration/len(visuals)), "-i", visuals[0],
        # ... autres images
        "-i", voice_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        output_file
    ]
    subprocess.run(cmd)
    
    # 5. Ajouter les sous-titres si demandé
    if options.get("subtitles"):
        # Générer SRT avec Whisper
        pass
    
    # 6. Sauvegarder en DB
    short = VideoShort(
        user_id=user["id"],
        subject=subject,
        duration=duration,
        video_url=output_file
    )
    db.add(short)
    db.commit()
    
    return {"short_id": short.id, "video_url": output_file}
```

---

## 🔄 ÉTAPE 3 : COMBINAISONS IA (WORKFLOWS)

### Priorité : 🔴 **CRITIQUE**

```python
# app/routes/combinations_routes.py

@router.post("/api/combinations/execute")
async def execute_workflow(
    steps: List[dict],
    user: dict = Depends(get_current_user)
):
    """
    Exécuter un workflow de combinaisons IA
    
    Exemple de steps :
    [
        {"ai": "gpt-4", "prompt": "Écris un article sur {subject}"},
        {"ai": "dall-e-3", "prompt": "Crée une image pour : {previous_output}"},
        {"ai": "elevenlabs", "prompt": "Lis ce texte : {step_1_output}"}
    ]
    """
    results = []
    context = {}
    
    for i, step in enumerate(steps):
        # Remplacer les variables dans le prompt
        prompt = step["prompt"]
        for key, value in context.items():
            prompt = prompt.replace(f"{{{key}}}", value)
        
        # Exécuter l'étape
        if step["ai"] == "gpt-4":
            result = await openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            output = result.choices[0].message.content
            
        elif step["ai"] == "dall-e-3":
            result = await openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt
            )
            output = result.data[0].url
        
        # Sauvegarder le résultat
        results.append({
            "step": i + 1,
            "ai": step["ai"],
            "output": output
        })
        
        # Ajouter au contexte
        context[f"step_{i+1}_output"] = output
        context["previous_output"] = output
    
    return {"results": results}


@router.post("/api/combinations/save")
async def save_workflow(
    name: str,
    description: str,
    steps: List[dict],
    user: dict = Depends(get_current_user)
):
    """
    Sauvegarder un workflow pour réutilisation
    """
    workflow = Workflow(
        user_id=user["id"],
        name=name,
        description=description,
        steps=json.dumps(steps)
    )
    db.add(workflow)
    db.commit()
    
    return {"workflow_id": workflow.id}


@router.get("/api/combinations/templates")
async def get_templates():
    """
    Retourner les templates prédéfinis
    """
    return [
        {
            "id": "content-creation",
            "name": "Création de Contenu",
            "description": "Article + Image + Audio",
            "steps": [
                {"ai": "gpt-4", "prompt": "Écris un article sur {subject}"},
                {"ai": "dall-e-3", "prompt": "Illustration pour : {step_1_output}"},
                {"ai": "elevenlabs", "prompt": "Lis : {step_1_output}"}
            ]
        },
        {
            "id": "video-production",
            "name": "Production Vidéo",
            "description": "Script + Visuels + Montage",
            "steps": [
                {"ai": "claude", "prompt": "Script vidéo sur {subject}"},
                {"ai": "midjourney", "prompt": "Visuels pour : {step_1_output}"},
                {"ai": "runway", "prompt": "Vidéo avec : {step_2_output}"}
            ]
        }
    ]
```

---

## 📊 ÉTAPE 4 : CATALOGUE D'OUTILS IA

### Priorité : 🟡 **IMPORTANTE**

```python
# app/routes/catalog_routes.py

@router.get("/api/catalog/tools")
async def get_tools(
    category: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Liste des 54 outils IA catalogués
    """
    tools = [
        {
            "id": 1,
            "name": "GPT-4",
            "category": "Texte",
            "description": "Modèle de langage le plus avancé",
            "pricing": "0.03$/1K tokens",
            "logo": "openai.png"
        },
        # ... 53 autres outils
    ]
    
    # Filtrer par catégorie
    if category:
        tools = [t for t in tools if t["category"] == category]
    
    # Recherche
    if search:
        tools = [t for t in tools if search.lower() in t["name"].lower()]
    
    return tools


@router.post("/api/catalog/tools/{id}/favorite")
async def toggle_favorite(
    id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ajouter/retirer des favoris
    """
    favorite = db.query(Favorite).filter_by(
        user_id=user["id"],
        tool_id=id
    ).first()
    
    if favorite:
        db.delete(favorite)
        action = "removed"
    else:
        favorite = Favorite(user_id=user["id"], tool_id=id)
        db.add(favorite)
        action = "added"
    
    db.commit()
    return {"action": action}
```

---

## 🗄️ ÉTAPE 5 : SCHÉMAS DE BASE DE DONNÉES

### Tables à créer :

```sql
-- Table pour les images générées
CREATE TABLE generated_images (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    prompt TEXT NOT NULL,
    model VARCHAR(50) NOT NULL,
    size VARCHAR(20),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table pour les vidéos générées
CREATE TABLE generated_videos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    prompt TEXT NOT NULL,
    model VARCHAR(50) NOT NULL,
    duration INTEGER,
    video_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table pour les eBooks
CREATE TABLE ebooks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    chapters INTEGER NOT NULL,
    tone VARCHAR(50),
    audience VARCHAR(50),
    language VARCHAR(10),
    format VARCHAR(20),
    cover_url VARCHAR(500),
    file_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'generating',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table pour les vidéos short
CREATE TABLE video_shorts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    subject TEXT NOT NULL,
    duration INTEGER NOT NULL,
    format VARCHAR(20),
    style VARCHAR(50),
    voice VARCHAR(50),
    video_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'generating',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table pour les workflows
CREATE TABLE workflows (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    steps JSON NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table pour les favoris du catalogue
CREATE TABLE catalog_favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tool_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, tool_id)
);
```

---

## 📦 ÉTAPE 6 : DÉPENDANCES À INSTALLER

```bash
# Génération de PDF
pip install reportlab weasyprint

# Génération d'EPUB
pip install ebooklib

# Traitement vidéo
pip install ffmpeg-python

# Clients API
pip install openai anthropic google-generativeai elevenlabs

# Traitement d'images
pip install pillow

# Async
pip install aiohttp aiofiles
```

---

## ⏱️ ESTIMATION DU TEMPS

| Étape | Tâche | Temps | Priorité |
|-------|-------|-------|----------|
| ✅ 1 | Agents IA | 8h | 🔴 P1 |
| 🔄 2.1 | Génération Images | 8h | 🔴 P1 |
| 🔄 2.2 | Génération Vidéos | 8h | 🔴 P1 |
| 🔄 2.3 | Génération Audio | 6h | 🔴 P1 |
| 🔄 2.4 | Création eBooks | 10h | 🔴 P1 |
| 🔄 2.5 | Création Vidéos Short | 8h | 🔴 P1 |
| ⏳ 3 | Combinaisons IA | 16h | 🔴 P1 |
| ⏳ 4 | Catalogue IA | 8h | 🟡 P2 |
| ⏳ 5 | Base de données | 4h | 🔴 P1 |

**Total Priorité 1** : 68 heures (8.5 jours)  
**Total Priorité 2** : 8 heures (1 jour)

---

## 🎯 RECOMMANDATION

### **Phase 1 (Semaine 1)** :
1. ✅ Agents IA (FAIT)
2. Génération Images + Vidéos + Audio (22h)
3. Base de données (4h)

### **Phase 2 (Semaine 2)** :
4. Création eBooks + Vidéos Short (18h)
5. Combinaisons IA (16h)

### **Phase 3 (Semaine 3)** :
6. Catalogue IA (8h)
7. Tests et optimisations (16h)

---

## 📝 CHECKLIST DE PROGRESSION

### Agents IA :
- [x] Contextes spécialisés créés
- [x] Routes API fonctionnelles
- [ ] Tests avec vrais utilisateurs

### Génération Multi-Média :
- [ ] Images (DALL-E, Midjourney, SD)
- [ ] Vidéos (Runway, Pika, Luma)
- [ ] Audio (Suno, Udio, ElevenLabs)
- [ ] eBooks (GPT-4 + PDF)
- [ ] Vidéos Short (GPT-4 + FFmpeg)

### Combinaisons IA :
- [ ] Workflow builder
- [ ] Exécution de workflows
- [ ] Templates prédéfinis
- [ ] Sauvegarde de workflows

### Catalogue IA :
- [ ] Liste des 54 outils
- [ ] Recherche dynamique
- [ ] Filtres par catégorie
- [ ] Favoris

---

**🚀 Prêt à commencer l'implémentation ! Par quelle fonctionnalité veux-tu commencer ?**
