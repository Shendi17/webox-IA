"""Model - Données de la landing page"""


class LandingPageData:
    """Classe contenant toutes les données de la landing page"""
    
    # Titre
    TITLE_EMOJI = "🚀"
    TITLE_WEBOX = "WeBox"
    TITLE_MULTI_IA = "Studio Créatif IA"
    SUBTITLE = "La Plateforme IA la Plus Complète du Marché - Marketing + Studio Créatif"
    
    # Hero description
    HERO_FEATURES = "🚀 <strong>20 Modules Professionnels</strong> • 💬 Chat Multi-IA • 🎨 Studio Créatif (7 outils) • 🌐 Website Builder • 🎯 Tunnels de Vente • 📱 PWA Generator • 📄 Documents IA • 🎙️ Podcasts IA • 👤 Avatars IA • 📺 Séries IA"
    HERO_DESCRIPTION = "Créez votre présence digitale complète avec l'IA : Sites web, applications mobiles, podcasts, séries, avatars, analyse de documents et bien plus encore !"
    
    # Stats
    STATS = [
        {"number": "20+", "label": "Modules Complets"},
        {"number": "90+", "label": "Routes API"},
        {"number": "3", "label": "Modèles IA (GPT-4, Claude, Gemini)"},
        {"number": "15+", "label": "Tables DB"},
        {"number": "GRATUIT", "label": "Gemini 2.0 Flash"}
    ]
    
    # Fonctionnalités (3 colonnes)
    FEATURES_COL1 = [
        {
            "icon": "🎨",
            "title": "Studio Créatif IA (7 Outils)",
            "description": "Suite complète d'outils IA pour créer du contenu professionnel : podcasts, avatars, séries, apps et plus.",
            "features": [
                "🎙️ Podcast Creator (Scripts + Audio + Cover)",
                "👤 Avatar Generator (7 styles)",
                "📺 Séries IA (Scripts + Scènes + Images)",
                "📱 PWA Generator (6 templates)",
                "📄 Documents IA (Analyse + Extraction)",
                "🤖 Agent IA 24/7 (Chat intelligent)",
                "✨ Génération Multi-Format"
            ]
        },
        {
            "icon": "🌐",
            "title": "Website Builder IA",
            "description": "Créez des sites web complets en quelques clics. L'IA génère tout automatiquement : design, contenu, images.",
            "features": [
                "🎨 5 templates professionnels",
                "📄 Sites multi-pages (4-10 pages)",
                "📝 Blog intégré",
                "🛍️ E-commerce (optionnel)",
                "🔗 Sous-domaine automatique",
                "📊 Analytics intégré"
            ]
        },
        {
            "icon": "🎯",
            "title": "Tunnels de Vente",
            "description": "Créez des funnels automatisés pour convertir vos visiteurs en clients. 5 templates prêts à l'emploi.",
            "features": [
                "🎯 Lead Generation",
                "💰 Vente Produit",
                "🎥 Webinaire",
                "🚀 Lancement Produit",
                "🛍️ E-commerce"
            ]
        }
    ]
    
    FEATURES_COL2 = [
        {
            "icon": "📱",
            "title": "Réseaux Sociaux & Influenceurs IA",
            "description": "Gérez tous vos réseaux sociaux et créez des influenceurs virtuels pour votre marque.",
            "features": [
                "📱 6 plateformes (FB, IG, Twitter, LinkedIn, TikTok, YouTube)",
                "📅 Programmation de posts",
                "✍️ Génération de captions par IA",
                "#️⃣ Hashtags automatiques",
                "👤 Création d'influenceurs IA",
                "📊 Analytics complets"
            ]
        },
        {
            "icon": "📧",
            "title": "Email Marketing & Présentations",
            "description": "Créez des campagnes email professionnelles et des présentations PowerPoint avec l'IA.",
            "features": [
                "📧 Campagnes email automatisées",
                "📊 Analytics (ouvertures, clics)",
                "📊 Présentations IA (5-50 slides)",
                "💼 Export PowerPoint, PDF, Vidéo",
                "🎨 4 templates professionnels",
                "🌐 Landing pages optimisées"
            ]
        }
    ]
    
    FEATURES_COL3 = [
        {
            "icon": "🎨",
            "title": "Génération Multi-Média (7 types)",
            "description": "Créez tout type de contenu avec l'IA : images, vidéos, audio, logos, publicités et plus.",
            "features": [
                "🖼️ Images (DALL-E, Stable Diffusion)",
                "🎬 Vidéos (Runway, Pika)",
                "🔊 Audio & Voix (ElevenLabs)",
                "📚 eBooks complets",
                "📱 Video Shorts (TikTok, Reels)",
                "📺 Publicités vidéo",
                "🎨 Logos professionnels"
            ]
        },
        {
            "icon": "💬",
            "title": "Chat Multi-IA & Agents",
            "description": "Dialoguez avec 20+ modèles d'IA et utilisez 12 agents spécialisés pour automatiser votre business.",
            "features": [
                "💬 GPT-4, Claude 3.5, Gemini Pro",
                "🤖 12 agents IA spécialisés",
                "📞 Assistant vocal IA (Twilio)",
                "🔄 Workflows d'automatisation",
                "📚 Bibliothèque de prompts",
                "🔧 Catalogue de 50+ outils IA"
            ]
        }
    ]
    
    # Témoignages
    TESTIMONIALS = [
        {
            "text": "WeBox a révolutionné notre marketing ! Le Website Builder nous a permis de créer notre site en 30 minutes. Les tunnels de vente ont doublé nos conversions !",
            "author": "Marie Dubois",
            "role": "CEO, TechStart"
        },
        {
            "text": "Incroyable ! J'ai créé mon site, mes landing pages, mes campagnes email et mes posts sociaux en une journée. WeBox remplace 10 outils que je payais avant.",
            "author": "Thomas Martin",
            "role": "Entrepreneur Digital"
        },
        {
            "text": "Le ROI est fou ! Nous avons économisé 80% sur nos coûts marketing. Les influenceurs IA génèrent du contenu 24/7. Je recommande à 100% !",
            "author": "Sophie Laurent",
            "role": "Directrice Marketing, InnovateCorp"
        }
    ]
    
    # Pourquoi choisir WeBox
    WHY_CHOOSE = [
        {"icon": "⚡", "title": "Rapide et Efficace", "description": "Automatisez vos tâches en quelques clics. Interface intuitive et réactive."},
        {"icon": "🔒", "title": "Sécurisé", "description": "Vos données sont protégées et chiffrées. Conformité RGPD garantie."},
        {"icon": "🎯", "title": "Précis", "description": "Des résultats de haute qualité à chaque fois. IA de dernière génération."},
        {"icon": "💰", "title": "Économique", "description": "Un seul abonnement pour 50+ APIs. Économisez jusqu'à 80% sur vos coûts IA."},
        {"icon": "🔄", "title": "Mis à jour", "description": "Nouvelles fonctionnalités chaque semaine. Toujours à la pointe de l'IA."},
        {"icon": "🌍", "title": "Multilingue", "description": "Support de 100+ langues. Interface disponible en français, anglais, espagnol."}
    ]
    
    # Footer
    VERSION = "v2.0"
    FOOTER_TAGLINE = "Plateforme IA Ultra-Complète - Marketing + Studio Créatif"
    FOOTER_FEATURES = "✨ 20+ Modules • 90+ Routes API • Studio Créatif (7 outils) • Website Builder • PWA Generator • Podcasts IA • Avatars IA • Séries IA • Documents IA • Agent IA 24/7"
    COPYRIGHT = "© 2025 WeBox Studio Créatif IA • Développé avec ❤️ • FastAPI • Python • OpenAI • Anthropic • Google Gemini 2.0"
