import os
import json
from typing import Dict, List
import google.generativeai as genai
from openai import OpenAI

class ReactNativeService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def get_templates(self) -> List[Dict]:
        """Retourne la liste des templates React Native"""
        return [
            {
                "id": "social",
                "name": "Social Media",
                "icon": "👥",
                "description": "App de réseau social avec profils et posts",
                "screens": ["Home", "Profile", "Feed", "Messages", "Settings"],
                "features": ["Authentication", "Posts", "Likes", "Comments", "Chat"]
            },
            {
                "id": "fitness",
                "name": "Fitness",
                "icon": "💪",
                "description": "App de fitness avec exercices et suivi",
                "screens": ["Home", "Workouts", "Progress", "Profile", "Settings"],
                "features": ["Workouts", "Timer", "Progress Tracking", "Goals"]
            },
            {
                "id": "food",
                "name": "Food Delivery",
                "icon": "🍔",
                "description": "App de livraison de nourriture",
                "screens": ["Home", "Menu", "Cart", "Orders", "Profile"],
                "features": ["Menu", "Cart", "Orders", "Payment", "Tracking"]
            },
            {
                "id": "finance",
                "name": "Finance",
                "icon": "💰",
                "description": "App de gestion financière",
                "screens": ["Dashboard", "Transactions", "Budget", "Analytics", "Settings"],
                "features": ["Transactions", "Budget", "Charts", "Reports"]
            },
            {
                "id": "productivity",
                "name": "Productivity",
                "icon": "✅",
                "description": "App de productivité et tâches",
                "screens": ["Tasks", "Calendar", "Projects", "Notes", "Settings"],
                "features": ["Tasks", "Calendar", "Reminders", "Notes"]
            }
        ]
    
    def get_navigation_types(self) -> List[Dict]:
        """Retourne les types de navigation"""
        return [
            {"id": "stack", "name": "Stack Navigator", "description": "Navigation par empilement"},
            {"id": "tab", "name": "Tab Navigator", "description": "Navigation par onglets"},
            {"id": "drawer", "name": "Drawer Navigator", "description": "Menu latéral"}
        ]
    
    async def generate_app_code(self, template: str, app_name: str, 
                                navigation_type: str) -> Dict:
        """Génère le code React Native"""
        try:
            prompt = f"""Tu es un expert React Native. Génère le code pour une app mobile.

TEMPLATE: {template}
NOM: {app_name}
NAVIGATION: {navigation_type}

GÉNÈRE le code React Native avec :

1. APP.JS (code principal)
2. NAVIGATION (configuration)
3. SCREENS (liste des écrans avec code)
4. COMPONENTS (composants réutilisables)
5. DEPENDENCIES (packages npm nécessaires)

Réponds UNIQUEMENT en JSON valide :
{{
    "app_js": "code App.js...",
    "navigation_js": "code navigation...",
    "screens": [
        {{
            "name": "HomeScreen",
            "code": "code du screen..."
        }}
    ],
    "components": [
        {{
            "name": "Button",
            "code": "code du composant..."
        }}
    ],
    "dependencies": {{
        "@react-navigation/native": "^6.0.0",
        "react-native-screens": "^3.0.0"
    }}
}}"""

            response = self.gemini_model.generate_content(prompt)
            
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            code = json.loads(response_text.strip())
            
            return {
                "success": True,
                "code": code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur : {str(e)}"
            }
    
    async def generate_icon(self, app_name: str, template: str) -> Dict:
        """Génère l'icône de l'app"""
        try:
            template_styles = {
                "social": "social media, people, connection",
                "fitness": "fitness, health, sport",
                "food": "food, restaurant, delivery",
                "finance": "money, finance, banking",
                "productivity": "tasks, productivity, organization"
            }
            
            style = template_styles.get(template, "modern, professional")
            
            prompt = f"""Mobile app icon for "{app_name}"
Style: {style}
Design: flat design, simple, modern, professional
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
    
    def generate_package_json(self, app_name: str, dependencies: Dict) -> str:
        """Génère le package.json"""
        package = {
            "name": app_name.lower().replace(" ", "-"),
            "version": "1.0.0",
            "main": "node_modules/expo/AppEntry.js",
            "scripts": {
                "start": "expo start",
                "android": "expo start --android",
                "ios": "expo start --ios",
                "web": "expo start --web"
            },
            "dependencies": {
                "react": "18.2.0",
                "react-native": "0.72.0",
                "expo": "~49.0.0",
                **dependencies
            },
            "devDependencies": {
                "@babel/core": "^7.20.0"
            }
        }
        
        return json.dumps(package, indent=2)
