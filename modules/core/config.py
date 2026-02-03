"""Configuration de l'application WeBox Multi-IA"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration centralisée de l'application"""
    
    # Clés API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Vertex AI (Google Cloud)
    VERTEX_AI_PROJECT_ID = os.getenv("VERTEX_AI_PROJECT_ID", "")
    VERTEX_AI_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
    REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY", "")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    XAI_API_KEY = os.getenv("XAI_API_KEY", "")
    
    # Clés API pour génération de médias
    STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")  # Stable Diffusion
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")  # ElevenLabs (voix)
    RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")  # Runway (vidéo)
    
    # Configuration de l'application
    APP_NAME = os.getenv("APP_NAME", "WeBox Multi-IA")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Catégories d'IA pour le Chat (Texte & Code)
    AI_CATEGORIES = {
        "💬 Texte & Conversation": {
            "description": "IA généralistes pour le texte, la conversation et l'analyse",
            "providers": ["OpenAI", "Anthropic", "Google", "Mistral", "Cohere"]
        },
        "🔍 Recherche & Web": {
            "description": "IA avec accès à internet et recherche en temps réel",
            "providers": ["Perplexity", "xAI"]
        },
        "💻 Code & Développement": {
            "description": "IA spécialisées en programmation et développement",
            "providers": ["DeepSeek", "Groq"]
        },
        "🌐 Open-Source & Communauté": {
            "description": "Accès à des modèles open-source via des plateformes",
            "providers": ["Together", "Replicate", "HuggingFace"]
        }
    }
    
    # Catalogue complet des 50 IA (toutes catégories)
    AI_CATALOG = {
        "💬 Texte & Conversation": [
            {"name": "GPT-4 Turbo", "provider": "OpenAI", "url": "https://platform.openai.com", "price": "$10-30/1M tokens", "integrated": True},
            {"name": "Claude 3.5 Sonnet", "provider": "Anthropic", "url": "https://www.anthropic.com", "price": "$3-15/1M tokens", "integrated": True},
            {"name": "Gemini 1.5 Pro", "provider": "Google", "url": "https://ai.google.dev", "price": "GRATUIT", "integrated": True},
            {"name": "Mistral Large", "provider": "Mistral AI", "url": "https://mistral.ai", "price": "$8/1M tokens", "integrated": True},
            {"name": "Command R+", "provider": "Cohere", "url": "https://cohere.com", "price": "$3-15/1M tokens", "integrated": True},
            {"name": "Perplexity 70B", "provider": "Perplexity", "url": "https://www.perplexity.ai", "price": "Variable", "integrated": True},
            {"name": "Grok Beta", "provider": "xAI", "url": "https://x.ai", "price": "Sur demande", "integrated": True},
            {"name": "Qwen 2 72B", "provider": "Alibaba", "url": "https://qwenlm.github.io", "price": "$0.20/1M", "integrated": True},
            {"name": "Llama 3.1 70B", "provider": "Meta", "url": "https://llama.meta.com", "price": "GRATUIT", "integrated": True},
            {"name": "Mixtral 8x7B", "provider": "Mistral", "url": "https://mistral.ai", "price": "GRATUIT", "integrated": True},
            {"name": "Yi 34B", "provider": "01.AI", "url": "https://www.01.ai", "price": "GRATUIT", "integrated": False},
            {"name": "Falcon 180B", "provider": "TII", "url": "https://falconllm.tii.ae", "price": "GRATUIT", "integrated": False},
            {"name": "Vicuna 33B", "provider": "LMSYS", "url": "https://lmsys.org", "price": "GRATUIT", "integrated": False},
            {"name": "ChatGLM 3", "provider": "Tsinghua", "url": "https://chatglm.cn", "price": "GRATUIT", "integrated": False},
            {"name": "Baichuan 2", "provider": "Baichuan", "url": "https://www.baichuan-ai.com", "price": "GRATUIT", "integrated": False},
        ],
        "💻 Code & Programmation": [
            {"name": "DeepSeek Coder", "provider": "DeepSeek", "url": "https://platform.deepseek.com", "price": "$0.14/1M tokens", "integrated": True},
            {"name": "GPT-4 Turbo", "provider": "OpenAI", "url": "https://platform.openai.com", "price": "$10-30/1M tokens", "integrated": True},
            {"name": "Claude 3.5 Sonnet", "provider": "Anthropic", "url": "https://www.anthropic.com", "price": "$3-15/1M tokens", "integrated": True},
            {"name": "CodeLlama 70B", "provider": "Meta", "url": "https://ai.meta.com/blog/code-llama", "price": "GRATUIT", "integrated": True},
            {"name": "GitHub Copilot", "provider": "GitHub", "url": "https://github.com/features/copilot", "price": "$10/mois", "integrated": False},
            {"name": "Cursor AI", "provider": "Cursor", "url": "https://cursor.sh", "price": "$20/mois", "integrated": False},
            {"name": "Replit Ghostwriter", "provider": "Replit", "url": "https://replit.com", "price": "$10/mois", "integrated": False},
            {"name": "Tabnine", "provider": "Tabnine", "url": "https://www.tabnine.com", "price": "Gratuit/$12/mois", "integrated": False},
            {"name": "CodeWhisperer", "provider": "AWS", "url": "https://aws.amazon.com/codewhisperer", "price": "GRATUIT", "integrated": False},
            {"name": "Phind", "provider": "Phind", "url": "https://www.phind.com", "price": "Gratuit/$15/mois", "integrated": False},
        ],
        "🎨 Images & Génération Visuelle": [
            {"name": "Midjourney V6", "provider": "Midjourney", "url": "https://www.midjourney.com", "price": "$10-60/mois", "integrated": False},
            {"name": "DALL-E 3", "provider": "OpenAI", "url": "https://platform.openai.com", "price": "$0.04-0.12/image", "integrated": False},
            {"name": "Stable Diffusion XL", "provider": "Stability AI", "url": "https://stability.ai", "price": "GRATUIT", "integrated": False},
            {"name": "Adobe Firefly", "provider": "Adobe", "url": "https://www.adobe.com/firefly", "price": "Inclus CC", "integrated": False},
            {"name": "Leonardo AI", "provider": "Leonardo", "url": "https://leonardo.ai", "price": "Gratuit/$10-48/mois", "integrated": False},
            {"name": "Ideogram", "provider": "Ideogram", "url": "https://ideogram.ai", "price": "Gratuit/$8-48/mois", "integrated": False},
            {"name": "Flux.1", "provider": "Black Forest Labs", "url": "https://blackforestlabs.ai", "price": "Variable", "integrated": False},
            {"name": "Playground AI", "provider": "Playground", "url": "https://playground.com", "price": "GRATUIT/$15/mois", "integrated": False},
            {"name": "DreamStudio", "provider": "Stability AI", "url": "https://dreamstudio.ai", "price": "Pay-per-use", "integrated": False},
            {"name": "Canva AI", "provider": "Canva", "url": "https://www.canva.com", "price": "Gratuit/$12.99/mois", "integrated": False},
        ],
        "🎬 Vidéo & Animation": [
            {"name": "Runway Gen-2", "provider": "Runway", "url": "https://runwayml.com", "price": "$12-76/mois", "integrated": False},
            {"name": "Pika Labs", "provider": "Pika", "url": "https://pika.art", "price": "Gratuit/$10-70/mois", "integrated": False},
            {"name": "Sora", "provider": "OpenAI", "url": "https://openai.com/sora", "price": "Beta", "integrated": False},
            {"name": "Synthesia", "provider": "Synthesia", "url": "https://www.synthesia.io", "price": "$29-89/mois", "integrated": False},
            {"name": "HeyGen", "provider": "HeyGen", "url": "https://www.heygen.com", "price": "Gratuit/$29-89/mois", "integrated": False},
            {"name": "D-ID", "provider": "D-ID", "url": "https://www.d-id.com", "price": "$5.9-300/mois", "integrated": False},
            {"name": "Descript", "provider": "Descript", "url": "https://www.descript.com", "price": "Gratuit/$12-24/mois", "integrated": False},
            {"name": "Fliki", "provider": "Fliki", "url": "https://fliki.ai", "price": "Gratuit/$21-88/mois", "integrated": False},
        ],
        "🎙️ Audio & Voix": [
            {"name": "ElevenLabs", "provider": "ElevenLabs", "url": "https://elevenlabs.io", "price": "Gratuit/$5-330/mois", "integrated": False},
            {"name": "Suno AI", "provider": "Suno", "url": "https://www.suno.ai", "price": "Gratuit/$10-30/mois", "integrated": False},
            {"name": "Udio", "provider": "Udio", "url": "https://www.udio.com", "price": "Gratuit/$10-30/mois", "integrated": False},
            {"name": "Murf AI", "provider": "Murf", "url": "https://murf.ai", "price": "Gratuit/$19-99/mois", "integrated": False},
            {"name": "Play.ht", "provider": "Play.ht", "url": "https://play.ht", "price": "Gratuit/$31-99/mois", "integrated": False},
            {"name": "Whisper", "provider": "OpenAI", "url": "https://openai.com/research/whisper", "price": "GRATUIT/$0.006/min", "integrated": False},
            {"name": "AssemblyAI", "provider": "AssemblyAI", "url": "https://www.assemblyai.com", "price": "Pay-per-use", "integrated": False},
        ]
    }
    
    # Modèles disponibles
    AVAILABLE_MODELS = {
        "OpenAI": {
            "gpt-4-turbo": "GPT-4 Turbo (Le plus puissant)",
            "gpt-4": "GPT-4 (Équilibré)",
            "gpt-3.5-turbo": "GPT-3.5 Turbo (Rapide)",
            "gpt-4o": "GPT-4o (Multimodal)",
        },
        "Anthropic": {
            "claude-3-opus-20240229": "Claude 3 Opus (Le plus puissant)",
            "claude-3-sonnet-20240229": "Claude 3 Sonnet (Équilibré)",
            "claude-3-haiku-20240307": "Claude 3 Haiku (Rapide)",
            "claude-3-5-sonnet-20240620": "Claude 3.5 Sonnet (Nouveau)",
        },
        "Google": {
            "gemini-pro": "Gemini Pro",
            "gemini-pro-vision": "Gemini Pro Vision",
            "gemini-1.5-pro": "Gemini 1.5 Pro (Contexte étendu)",
        },
        "Mistral": {
            "mistral-large-latest": "Mistral Large (Le plus puissant)",
            "mistral-medium-latest": "Mistral Medium (Équilibré)",
            "mistral-small-latest": "Mistral Small (Rapide)",
            "open-mistral-7b": "Open Mistral 7B (Open Source)",
        },
        "Cohere": {
            "command-r-plus": "Command R+ (Le plus puissant)",
            "command-r": "Command R (Équilibré)",
            "command": "Command (Rapide)",
            "command-light": "Command Light (Ultra rapide)",
        },
        "Perplexity": {
            "pplx-70b-online": "Perplexity 70B Online (Recherche web)",
            "pplx-7b-online": "Perplexity 7B Online (Rapide)",
            "codellama-70b-instruct": "CodeLlama 70B (Code)",
        },
        "DeepSeek": {
            "deepseek-chat": "DeepSeek Chat (Général)",
            "deepseek-coder": "DeepSeek Coder (Code expert)",
            "deepseek-reasoner": "DeepSeek Reasoner (Raisonnement)",
        },
        "Groq": {
            "llama-3.1-70b-versatile": "Llama 3.1 70B (Versatile)",
            "llama-3.1-8b-instant": "Llama 3.1 8B (Ultra rapide)",
            "mixtral-8x7b-32768": "Mixtral 8x7B (Contexte long)",
            "gemma-7b-it": "Gemma 7B (Google)",
        },
        "Together": {
            "meta-llama/Llama-3-70b-chat-hf": "Llama 3 70B Chat",
            "meta-llama/Llama-3-8b-chat-hf": "Llama 3 8B Chat",
            "mistralai/Mixtral-8x7B-Instruct-v0.1": "Mixtral 8x7B",
            "Qwen/Qwen2-72B-Instruct": "Qwen 2 72B (Alibaba)",
        },
        "Replicate": {
            "meta/llama-2-70b-chat": "Llama 2 70B Chat",
            "mistralai/mixtral-8x7b-instruct-v0.1": "Mixtral 8x7B",
            "meta/codellama-70b-instruct": "CodeLlama 70B",
        },
        "HuggingFace": {
            "meta-llama/Meta-Llama-3-70B-Instruct": "Llama 3 70B",
            "mistralai/Mixtral-8x7B-Instruct-v0.1": "Mixtral 8x7B",
            "Qwen/Qwen2-72B-Instruct": "Qwen 2 72B",
        },
        "xAI": {
            "grok-beta": "Grok Beta (Accès Twitter/X)",
            "grok-vision-beta": "Grok Vision Beta (Multimodal)",
        }
    }
    
    # Assistants pré-configurés
    ASSISTANTS = {
        "Rédacteur Marketing": {
            "description": "Expert en rédaction de contenu marketing et publicitaire",
            "system_prompt": "Tu es un expert en marketing et copywriting. Tu crées du contenu engageant, persuasif et optimisé pour convertir. Tu maîtrises les techniques de storytelling et de persuasion.",
            "icon": "📝"
        },
        "Développeur": {
            "description": "Assistant pour le développement et le code",
            "system_prompt": "Tu es un développeur expert en Python, JavaScript, et autres langages. Tu fournis du code propre, bien documenté et optimisé. Tu expliques tes choix techniques.",
            "icon": "💻"
        },
        "Analyste Business": {
            "description": "Analyse de données et stratégie business",
            "system_prompt": "Tu es un analyste business expérimenté. Tu analyses les données, identifies les tendances et fournis des recommandations stratégiques actionnables.",
            "icon": "📊"
        },
        "Coach Personnel": {
            "description": "Accompagnement et développement personnel",
            "system_prompt": "Tu es un coach personnel bienveillant et motivant. Tu aides à définir des objectifs, à surmonter les obstacles et à développer de nouvelles compétences.",
            "icon": "🎯"
        },
        "Traducteur": {
            "description": "Traduction professionnelle multilingue",
            "system_prompt": "Tu es un traducteur professionnel maîtrisant de nombreuses langues. Tu fournis des traductions précises, naturelles et adaptées au contexte culturel.",
            "icon": "🌍"
        },
        "Créatif": {
            "description": "Génération d'idées créatives et innovantes",
            "system_prompt": "Tu es un créatif innovant et imaginatif. Tu génères des idées originales, des concepts créatifs et des solutions innovantes pour tous types de projets.",
            "icon": "💡"
        }
    }
    
    # Bibliothèque de prompts
    PROMPT_LIBRARY = {
        "Marketing": [
            {
                "name": "Email de vente",
                "prompt": "Rédige un email de vente pour [produit/service] ciblant [audience]. Inclus un objet accrocheur, une accroche, les bénéfices clés et un call-to-action.",
                "category": "Marketing"
            },
            {
                "name": "Post LinkedIn",
                "prompt": "Crée un post LinkedIn engageant sur [sujet] qui génère de l'interaction. Utilise un hook fort, du storytelling et une question finale.",
                "category": "Marketing"
            },
            {
                "name": "Page de vente",
                "prompt": "Rédige une page de vente complète pour [produit/service] incluant : titre accrocheur, problème, solution, bénéfices, témoignages, garantie et CTA.",
                "category": "Marketing"
            }
        ],
        "Productivité": [
            {
                "name": "Planification de projet",
                "prompt": "Crée un plan détaillé pour [projet] incluant : objectifs, étapes clés, ressources nécessaires, timeline et indicateurs de succès.",
                "category": "Productivité"
            },
            {
                "name": "Résumé de réunion",
                "prompt": "Résume cette réunion en identifiant : points clés discutés, décisions prises, actions à mener (qui fait quoi pour quand), et prochaines étapes.",
                "category": "Productivité"
            }
        ],
        "Développement": [
            {
                "name": "Revue de code",
                "prompt": "Analyse ce code et fournis : points forts, problèmes potentiels, suggestions d'amélioration, et bonnes pratiques à appliquer.",
                "category": "Développement"
            },
            {
                "name": "Documentation",
                "prompt": "Génère une documentation complète pour ce code incluant : description, paramètres, valeurs de retour, exemples d'utilisation et notes importantes.",
                "category": "Développement"
            }
        ],
        "Analyse": [
            {
                "name": "Analyse SWOT",
                "prompt": "Réalise une analyse SWOT complète pour [entreprise/projet] : Forces, Faiblesses, Opportunités, Menaces avec recommandations stratégiques.",
                "category": "Analyse"
            }
        ]
    }

config = Config()
