"""
Script pour créer la table articles et ajouter des articles de démonstration
"""
from app.database import engine, Base, SessionLocal
from app.models.article_db import ArticleDB
from datetime import datetime, timedelta

# Créer la table
Base.metadata.create_all(bind=engine)
print('✅ Table articles créée !')

# Ajouter des articles de démonstration
db = SessionLocal()

articles_demo = [
    {
        "title": "GPT-4 Turbo : La Révolution de l'IA Conversationnelle",
        "slug": "gpt-4-turbo-revolution-ia",
        "excerpt": "Découvrez les nouvelles capacités de GPT-4 Turbo et comment l'utiliser pour automatiser vos tâches quotidiennes.",
        "content": """# GPT-4 Turbo : Une Nouvelle Ère

GPT-4 Turbo représente une avancée majeure dans le domaine de l'intelligence artificielle. Avec une fenêtre de contexte étendue à 128K tokens, il peut désormais traiter des documents entiers.

## Nouvelles Fonctionnalités

- **Contexte étendu** : Jusqu'à 128 000 tokens
- **Vision améliorée** : Analyse d'images plus précise
- **JSON Mode** : Réponses structurées garanties
- **Prix réduits** : 3x moins cher que GPT-4

## Cas d'Usage

1. Analyse de documents longs
2. Génération de code complexe
3. Traduction de contenu volumineux
4. Assistance technique avancée

Commencez dès maintenant à utiliser GPT-4 Turbo sur WeBox !""",
        "category": "Nouveautés",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
        "is_featured": True,
        "reading_time": 5
    },
    {
        "title": "Comment Créer des Prompts Efficaces pour l'IA",
        "slug": "creer-prompts-efficaces-ia",
        "excerpt": "Maîtrisez l'art du prompt engineering pour obtenir les meilleurs résultats de vos IAs.",
        "content": """# L'Art du Prompt Engineering

Le prompt engineering est une compétence essentielle pour tirer le meilleur parti des IAs modernes.

## Principes de Base

### 1. Soyez Spécifique
Plus votre prompt est précis, meilleurs seront les résultats.

### 2. Donnez du Contexte
L'IA a besoin de comprendre le contexte pour répondre correctement.

### 3. Utilisez des Exemples
Les exemples aident l'IA à comprendre ce que vous attendez.

## Template de Prompt Efficace

```
Rôle : Tu es un expert en [domaine]
Tâche : [description précise]
Format : [format souhaité]
Contraintes : [limitations]
```

Essayez ces techniques dans votre prochain chat !""",
        "category": "Tutoriels",
        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800",
        "reading_time": 7
    },
    {
        "title": "Les 10 Meilleurs Outils IA pour 2025",
        "slug": "10-meilleurs-outils-ia-2025",
        "excerpt": "Notre sélection des outils IA incontournables pour booster votre productivité.",
        "content": """# Top 10 des Outils IA en 2025

Voici notre sélection des outils IA les plus puissants et utiles.

## 1. ChatGPT (OpenAI)
L'IA conversationnelle de référence.

## 2. Claude (Anthropic)
Excellence en analyse de documents.

## 3. Midjourney
Génération d'images artistiques.

## 4. DALL-E 3
Images réalistes et précises.

## 5. Runway ML
Édition vidéo par IA.

## 6. ElevenLabs
Synthèse vocale ultra-réaliste.

## 7. Perplexity
Moteur de recherche IA.

## 8. Notion AI
Productivité augmentée.

## 9. GitHub Copilot
Assistant de code.

## 10. Jasper
Rédaction marketing.

Tous ces outils sont disponibles sur WeBox !""",
        "category": "Outils",
        "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800",
        "reading_time": 10
    },
    {
        "title": "Automatiser son Business avec l'IA : Guide Complet",
        "slug": "automatiser-business-ia-guide",
        "excerpt": "Découvrez comment automatiser vos processus métier grâce à l'intelligence artificielle.",
        "content": """# Automatisation Business avec l'IA

L'IA peut transformer votre entreprise en automatisant des tâches répétitives.

## Domaines d'Automatisation

### Service Client
- Chatbots intelligents 24/7
- Analyse de sentiment
- Routing automatique

### Marketing
- Génération de contenu
- Personnalisation emails
- Analyse de performance

### Ventes
- Qualification de leads
- Prédiction de churn
- Recommandations produits

### Opérations
- Traitement de documents
- Planification optimisée
- Maintenance prédictive

## ROI Attendu

- 40% de réduction des coûts
- 60% de gain de temps
- 80% de satisfaction client

Commencez votre transformation IA aujourd'hui !""",
        "category": "Guides",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
        "reading_time": 12
    },
    {
        "title": "IA vs Humain : Qui Gagne en 2025 ?",
        "slug": "ia-vs-humain-2025",
        "excerpt": "Analyse comparative des performances de l'IA et des humains dans différents domaines.",
        "content": """# IA vs Humain : Le Match

Une analyse objective des forces et faiblesses de chacun.

## Domaines où l'IA Excelle

✅ Traitement de données massives
✅ Tâches répétitives
✅ Calculs complexes
✅ Disponibilité 24/7

## Domaines où l'Humain Excelle

✅ Créativité originale
✅ Empathie et émotions
✅ Jugement éthique
✅ Adaptation à l'inattendu

## La Vraie Question

Ce n'est pas "IA vs Humain" mais "IA + Humain".

La collaboration homme-machine est l'avenir.

## Conclusion

L'IA est un outil puissant qui augmente nos capacités, elle ne nous remplace pas.

Apprenez à collaborer avec l'IA pour maximiser votre potentiel !""",
        "category": "Analyses",
        "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800",
        "reading_time": 8
    }
]

for article_data in articles_demo:
    # Vérifier si l'article existe déjà
    existing = db.query(ArticleDB).filter(ArticleDB.slug == article_data["slug"]).first()
    if not existing:
        article = ArticleDB(**article_data)
        db.add(article)
        print(f"✅ Article créé : {article_data['title']}")

db.commit()
db.close()

print('\n🎉 Articles de démonstration créés avec succès !')
