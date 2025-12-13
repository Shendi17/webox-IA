import os
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from openai import OpenAI

class PWAService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def get_templates(self) -> List[Dict]:
        """Retourne la liste des templates PWA disponibles"""
        return [
            {
                "id": "landing",
                "name": "Landing Page",
                "icon": "🚀",
                "description": "Page d'atterrissage moderne pour présenter votre produit",
                "features": ["Hero section", "Features", "Pricing", "Contact", "CTA"],
                "pages": ["Home", "About", "Contact"]
            },
            {
                "id": "portfolio",
                "name": "Portfolio",
                "icon": "💼",
                "description": "Portfolio professionnel pour présenter vos projets",
                "features": ["Gallery", "Projects", "Skills", "Resume", "Contact"],
                "pages": ["Home", "Projects", "About", "Contact"]
            },
            {
                "id": "blog",
                "name": "Blog",
                "icon": "📝",
                "description": "Blog moderne avec articles et catégories",
                "features": ["Articles", "Categories", "Search", "Comments", "RSS"],
                "pages": ["Home", "Articles", "Categories", "About"]
            },
            {
                "id": "ecommerce",
                "name": "E-Commerce",
                "icon": "🛒",
                "description": "Boutique en ligne avec panier et paiement",
                "features": ["Products", "Cart", "Checkout", "Orders", "Wishlist"],
                "pages": ["Home", "Shop", "Product", "Cart", "Checkout"]
            },
            {
                "id": "dashboard",
                "name": "Dashboard",
                "icon": "📊",
                "description": "Tableau de bord avec statistiques et graphiques",
                "features": ["Stats", "Charts", "Tables", "Notifications", "Settings"],
                "pages": ["Dashboard", "Analytics", "Reports", "Settings"]
            },
            {
                "id": "restaurant",
                "name": "Restaurant",
                "icon": "🍽️",
                "description": "Site de restaurant avec menu et réservations",
                "features": ["Menu", "Reservations", "Gallery", "Reviews", "Contact"],
                "pages": ["Home", "Menu", "Reservations", "About"]
            }
        ]
    
    def get_color_themes(self) -> List[Dict]:
        """Retourne les thèmes de couleurs disponibles"""
        return [
            {"id": "purple", "name": "Purple", "primary": "#667eea", "secondary": "#764ba2"},
            {"id": "blue", "name": "Blue", "primary": "#4facfe", "secondary": "#00f2fe"},
            {"id": "green", "name": "Green", "primary": "#11998e", "secondary": "#38ef7d"},
            {"id": "orange", "name": "Orange", "primary": "#f093fb", "secondary": "#f5576c"},
            {"id": "pink", "name": "Pink", "primary": "#fa709a", "secondary": "#fee140"},
            {"id": "dark", "name": "Dark", "primary": "#2c3e50", "secondary": "#34495e"}
        ]
    
    async def generate_content(self, template: str, app_name: str, description: str) -> Dict:
        """Génère le contenu pour une PWA"""
        try:
            prompt = f"""Tu es un expert en création de contenu web. Génère du contenu pour une PWA.

TYPE: {template}
NOM: {app_name}
DESCRIPTION: {description}

GÉNÈRE un contenu complet et professionnel avec :

1. PAGES (selon le template)
Pour chaque page :
- Titre
- Sous-titre
- Contenu principal (paragraphes)
- Call-to-action

2. SECTIONS
Pour chaque section :
- Titre
- Description
- Items/éléments

3. SEO
- Meta title (60 caractères max)
- Meta description (160 caractères max)
- 5-10 keywords

Réponds UNIQUEMENT en JSON valide :
{{
    "pages": [
        {{
            "id": "home",
            "title": "...",
            "subtitle": "...",
            "content": "...",
            "cta": "..."
        }}
    ],
    "sections": [
        {{
            "id": "features",
            "title": "...",
            "description": "...",
            "items": ["...", "...", "..."]
        }}
    ],
    "seo": {{
        "title": "...",
        "description": "...",
        "keywords": ["...", "...", "..."]
    }}
}}"""

            response = self.gemini_model.generate_content(prompt)
            
            # Parser la réponse
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            content = json.loads(response_text.strip())
            
            return {
                "success": True,
                "content": content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur : {str(e)}"
            }
    
    async def generate_icon(self, app_name: str, template: str) -> Dict:
        """Génère une icône pour la PWA"""
        try:
            template_styles = {
                "landing": "modern, minimalist, gradient",
                "portfolio": "professional, elegant, creative",
                "blog": "clean, readable, modern",
                "ecommerce": "shopping, colorful, friendly",
                "dashboard": "data, analytics, professional",
                "restaurant": "food, appetizing, elegant"
            }
            
            style = template_styles.get(template, "modern, professional")
            
            prompt = f"""App icon for "{app_name}"
Style: {style}
Design: flat design, simple, recognizable, professional
Format: square icon, centered, clean background
High quality, suitable for mobile app icon"""
            
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            return {
                "success": True,
                "icon_url": response.data[0].url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur : {str(e)}"
            }
    
    def generate_manifest(self, app_name: str, short_name: str, description: str,
                         theme_color: str, background_color: str, icon_url: str) -> Dict:
        """Génère le manifest.json pour la PWA"""
        return {
            "name": app_name,
            "short_name": short_name or app_name[:12],
            "description": description,
            "start_url": "/",
            "display": "standalone",
            "theme_color": theme_color,
            "background_color": background_color,
            "orientation": "portrait-primary",
            "icons": [
                {
                    "src": icon_url,
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": icon_url,
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ],
            "categories": ["productivity", "utilities"],
            "screenshots": []
        }
    
    def generate_service_worker(self, cache_strategy: str = "network-first") -> str:
        """Génère le service worker pour la PWA"""
        
        if cache_strategy == "cache-first":
            strategy = """
    // Cache First Strategy
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request).then(fetchResponse => {
                return caches.open(CACHE_NAME).then(cache => {
                    cache.put(event.request, fetchResponse.clone());
                    return fetchResponse;
                });
            });
        })
    );"""
        else:  # network-first
            strategy = """
    // Network First Strategy
    event.respondWith(
        fetch(event.request).then(response => {
            return caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, response.clone());
                return response;
            });
        }).catch(() => {
            return caches.match(event.request);
        })
    );"""
        
        return f"""// Service Worker for PWA
const CACHE_NAME = 'pwa-cache-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/styles.css',
    '/script.js',
    '/manifest.json'
];

// Install
self.addEventListener('install', event => {{
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {{
            return cache.addAll(urlsToCache);
        }})
    );
}});

// Activate
self.addEventListener('activate', event => {{
    event.waitUntil(
        caches.keys().then(cacheNames => {{
            return Promise.all(
                cacheNames.map(cacheName => {{
                    if (cacheName !== CACHE_NAME) {{
                        return caches.delete(cacheName);
                    }}
                }})
            );
        }})
    );
}});

// Fetch
self.addEventListener('fetch', event => {{
{strategy}
}});

// Push Notifications
self.addEventListener('push', event => {{
    const options = {{
        body: event.data ? event.data.text() : 'New notification',
        icon: '/icon-192x192.png',
        badge: '/badge-72x72.png'
    }};
    
    event.waitUntil(
        self.registration.showNotification('PWA App', options)
    );
}});
"""
    
    def generate_html_template(self, template: str, content: Dict, 
                               theme_color: str) -> str:
        """Génère le HTML pour la PWA"""
        
        pages_html = ""
        if content.get("pages"):
            for page in content["pages"]:
                pages_html += f"""
        <section id="{page['id']}" class="page-section">
            <h1>{page['title']}</h1>
            <p class="subtitle">{page.get('subtitle', '')}</p>
            <div class="content">{page.get('content', '')}</div>
            {f'<button class="cta-button">{page["cta"]}</button>' if page.get('cta') else ''}
        </section>
"""
        
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="{theme_color}">
    <title>{content.get('seo', {}).get('title', 'PWA App')}</title>
    <meta name="description" content="{content.get('seo', {}).get('description', '')}">
    <link rel="manifest" href="/manifest.json">
    <link rel="icon" href="/icon-192x192.png">
    <link rel="apple-touch-icon" href="/icon-192x192.png">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .page-section {{
            min-height: 100vh;
            padding: 4rem 2rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        h1 {{ font-size: 3rem; margin-bottom: 1rem; color: {theme_color}; }}
        .subtitle {{ font-size: 1.5rem; color: #666; margin-bottom: 2rem; }}
        .content {{ max-width: 800px; margin: 2rem auto; }}
        .cta-button {{
            padding: 1rem 2rem;
            background: {theme_color};
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
            margin-top: 2rem;
        }}
        .cta-button:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    {pages_html}
    
    <script>
        // Register Service Worker
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js')
                .then(reg => console.log('Service Worker registered'))
                .catch(err => console.log('Service Worker registration failed'));
        }}
        
        // Install prompt
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            // Show install button
        }});
    </script>
</body>
</html>"""
    
    def get_cache_strategies(self) -> List[Dict]:
        """Retourne les stratégies de cache disponibles"""
        return [
            {
                "id": "network-first",
                "name": "Network First",
                "description": "Essaie le réseau d'abord, puis le cache"
            },
            {
                "id": "cache-first",
                "name": "Cache First",
                "description": "Utilise le cache d'abord, puis le réseau"
            }
        ]
