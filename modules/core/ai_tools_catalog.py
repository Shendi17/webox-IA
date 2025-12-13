"""Catalogue des meilleurs outils IA du marché"""

AI_TOOLS_CATALOG = {
    "Génération de Texte": [
        {
            "name": "ChatGPT",
            "provider": "OpenAI",
            "description": "Assistant IA conversationnel le plus populaire",
            "url": "https://chat.openai.com",
            "pricing": "Gratuit + Premium (20$/mois)",
            "use_cases": ["Rédaction", "Code", "Analyse", "Brainstorming"],
            "icon": "💬"
        },
        {
            "name": "Claude",
            "provider": "Anthropic",
            "description": "IA conversationnelle avec contexte étendu (200K tokens)",
            "url": "https://claude.ai",
            "pricing": "Gratuit + Pro (20$/mois)",
            "use_cases": ["Analyse de documents", "Rédaction longue", "Code"],
            "icon": "🤖"
        },
        {
            "name": "Gemini",
            "provider": "Google",
            "description": "IA multimodale de Google (texte, images, vidéo)",
            "url": "https://gemini.google.com",
            "pricing": "Gratuit",
            "use_cases": ["Recherche", "Analyse", "Multimodal"],
            "icon": "✨"
        },
        {
            "name": "Perplexity AI",
            "provider": "Perplexity",
            "description": "Moteur de recherche IA avec sources",
            "url": "https://www.perplexity.ai",
            "pricing": "Gratuit + Pro (20$/mois)",
            "use_cases": ["Recherche", "Fact-checking", "Veille"],
            "icon": "🔍"
        }
    ],
    
    "Génération d'Images": [
        {
            "name": "Midjourney",
            "provider": "Midjourney",
            "description": "Génération d'images artistiques de haute qualité",
            "url": "https://www.midjourney.com",
            "pricing": "À partir de 10$/mois",
            "use_cases": ["Art", "Design", "Illustration", "Concept art"],
            "icon": "🎨"
        },
        {
            "name": "DALL-E 3",
            "provider": "OpenAI",
            "description": "Génération d'images à partir de descriptions textuelles",
            "url": "https://openai.com/dall-e-3",
            "pricing": "Via ChatGPT Plus (20$/mois)",
            "use_cases": ["Illustrations", "Marketing", "Design"],
            "icon": "🖼️"
        },
        {
            "name": "Stable Diffusion",
            "provider": "Stability AI",
            "description": "Modèle open-source de génération d'images",
            "url": "https://stability.ai",
            "pricing": "Gratuit (open-source)",
            "use_cases": ["Art", "Prototypage", "Personnalisation"],
            "icon": "🎭"
        },
        {
            "name": "Leonardo AI",
            "provider": "Leonardo",
            "description": "Génération d'images pour jeux vidéo et assets",
            "url": "https://leonardo.ai",
            "pricing": "Gratuit + Premium",
            "use_cases": ["Game design", "Assets", "Concept art"],
            "icon": "🎮"
        }
    ],
    
    "Génération de Vidéo": [
        {
            "name": "Runway",
            "provider": "Runway",
            "description": "Suite complète d'outils IA pour la vidéo",
            "url": "https://runwayml.com",
            "pricing": "Gratuit + À partir de 12$/mois",
            "use_cases": ["Montage vidéo", "Effets spéciaux", "Animation"],
            "icon": "🎬"
        },
        {
            "name": "Pika",
            "provider": "Pika",
            "description": "Génération de vidéos à partir de texte et images",
            "url": "https://pika.art",
            "pricing": "Gratuit + Premium",
            "use_cases": ["Vidéos courtes", "Animation", "Marketing"],
            "icon": "📹"
        },
        {
            "name": "HeyGen",
            "provider": "HeyGen",
            "description": "Création de vidéos avec avatars IA",
            "url": "https://www.heygen.com",
            "pricing": "Gratuit + À partir de 24$/mois",
            "use_cases": ["Présentations", "Formation", "Marketing"],
            "icon": "👤"
        }
    ],
    
    "Génération Audio & Voix": [
        {
            "name": "ElevenLabs",
            "provider": "ElevenLabs",
            "description": "Synthèse vocale ultra-réaliste",
            "url": "https://elevenlabs.io",
            "pricing": "Gratuit + À partir de 5$/mois",
            "use_cases": ["Voix-off", "Audiobooks", "Podcasts"],
            "icon": "🎙️"
        },
        {
            "name": "Suno AI",
            "provider": "Suno",
            "description": "Génération de musique complète avec paroles",
            "url": "https://www.suno.ai",
            "pricing": "Gratuit + Premium",
            "use_cases": ["Musique", "Jingles", "Ambiances"],
            "icon": "🎵"
        },
        {
            "name": "Murf AI",
            "provider": "Murf",
            "description": "Voix-off IA pour vidéos et présentations",
            "url": "https://murf.ai",
            "pricing": "Gratuit + À partir de 19$/mois",
            "use_cases": ["Voix-off", "E-learning", "Publicité"],
            "icon": "🔊"
        }
    ],
    
    "Code & Développement": [
        {
            "name": "GitHub Copilot",
            "provider": "GitHub/OpenAI",
            "description": "Assistant de code IA intégré à l'IDE",
            "url": "https://github.com/features/copilot",
            "pricing": "10$/mois (gratuit pour étudiants)",
            "use_cases": ["Autocomplétion", "Génération de code", "Debugging"],
            "icon": "💻"
        },
        {
            "name": "Cursor",
            "provider": "Cursor",
            "description": "IDE avec IA intégrée",
            "url": "https://cursor.sh",
            "pricing": "Gratuit + Pro (20$/mois)",
            "use_cases": ["Développement", "Refactoring", "Documentation"],
            "icon": "⌨️"
        },
        {
            "name": "Replit AI",
            "provider": "Replit",
            "description": "IDE en ligne avec assistant IA",
            "url": "https://replit.com",
            "pricing": "Gratuit + À partir de 7$/mois",
            "use_cases": ["Prototypage", "Apprentissage", "Collaboration"],
            "icon": "🔧"
        }
    ],
    
    "Productivité & Business": [
        {
            "name": "Notion AI",
            "provider": "Notion",
            "description": "Assistant IA intégré à Notion",
            "url": "https://www.notion.so/product/ai",
            "pricing": "10$/mois (add-on)",
            "use_cases": ["Rédaction", "Résumés", "Organisation"],
            "icon": "📝"
        },
        {
            "name": "Jasper",
            "provider": "Jasper",
            "description": "IA spécialisée en marketing et copywriting",
            "url": "https://www.jasper.ai",
            "pricing": "À partir de 39$/mois",
            "use_cases": ["Marketing", "SEO", "Publicité"],
            "icon": "✍️"
        },
        {
            "name": "Copy.ai",
            "provider": "Copy.ai",
            "description": "Génération de contenu marketing",
            "url": "https://www.copy.ai",
            "pricing": "Gratuit + À partir de 36$/mois",
            "use_cases": ["Copywriting", "Emails", "Réseaux sociaux"],
            "icon": "📢"
        },
        {
            "name": "Grammarly",
            "provider": "Grammarly",
            "description": "Correction et amélioration de texte avec IA",
            "url": "https://www.grammarly.com",
            "pricing": "Gratuit + Premium (12$/mois)",
            "use_cases": ["Correction", "Style", "Ton"],
            "icon": "✅"
        }
    ],
    
    "Design & Créativité": [
        {
            "name": "Canva AI",
            "provider": "Canva",
            "description": "Design graphique avec outils IA",
            "url": "https://www.canva.com",
            "pricing": "Gratuit + Pro (12.99$/mois)",
            "use_cases": ["Design", "Présentations", "Réseaux sociaux"],
            "icon": "🎨"
        },
        {
            "name": "Figma AI",
            "provider": "Figma",
            "description": "Outils IA pour le design UI/UX",
            "url": "https://www.figma.com",
            "pricing": "Gratuit + Professional (12$/mois)",
            "use_cases": ["UI/UX", "Prototypage", "Design system"],
            "icon": "🎯"
        },
        {
            "name": "Looka",
            "provider": "Looka",
            "description": "Création de logos avec IA",
            "url": "https://looka.com",
            "pricing": "À partir de 20$",
            "use_cases": ["Logo", "Branding", "Identité visuelle"],
            "icon": "🏷️"
        }
    ],
    
    "Analyse & Data": [
        {
            "name": "Julius AI",
            "provider": "Julius",
            "description": "Analyse de données avec IA",
            "url": "https://julius.ai",
            "pricing": "Gratuit + Premium",
            "use_cases": ["Analyse de données", "Visualisation", "Insights"],
            "icon": "📊"
        },
        {
            "name": "ChatPDF",
            "provider": "ChatPDF",
            "description": "Analyse et discussion avec des PDFs",
            "url": "https://www.chatpdf.com",
            "pricing": "Gratuit + Plus (5$/mois)",
            "use_cases": ["Analyse de documents", "Résumés", "Recherche"],
            "icon": "📄"
        }
    ],
    
    "Automatisation": [
        {
            "name": "Make (Integromat)",
            "provider": "Make",
            "description": "Automatisation no-code avec IA",
            "url": "https://www.make.com",
            "pricing": "Gratuit + À partir de 9$/mois",
            "use_cases": ["Workflows", "Intégrations", "Automatisation"],
            "icon": "⚙️"
        },
        {
            "name": "Zapier",
            "provider": "Zapier",
            "description": "Automatisation avec intégrations IA",
            "url": "https://zapier.com",
            "pricing": "Gratuit + À partir de 19.99$/mois",
            "use_cases": ["Automatisation", "Intégrations", "Workflows"],
            "icon": "🔗"
        },
        {
            "name": "n8n",
            "provider": "n8n",
            "description": "Automatisation open-source avec IA",
            "url": "https://n8n.io",
            "pricing": "Gratuit (self-hosted) + Cloud",
            "use_cases": ["Workflows", "Automatisation", "Intégrations"],
            "icon": "🔄"
        }
    ]
}


def get_all_categories():
    """Retourne toutes les catégories d'outils"""
    return list(AI_TOOLS_CATALOG.keys())


def get_tools_by_category(category):
    """Retourne les outils d'une catégorie spécifique"""
    return AI_TOOLS_CATALOG.get(category, [])


def search_tools(query):
    """Recherche des outils par nom ou cas d'usage"""
    results = []
    query_lower = query.lower()
    
    for category, tools in AI_TOOLS_CATALOG.items():
        for tool in tools:
            if (query_lower in tool["name"].lower() or 
                query_lower in tool["description"].lower() or
                any(query_lower in use_case.lower() for use_case in tool["use_cases"])):
                results.append({**tool, "category": category})
    
    return results


def get_total_tools_count():
    """Retourne le nombre total d'outils"""
    return sum(len(tools) for tools in AI_TOOLS_CATALOG.values())
