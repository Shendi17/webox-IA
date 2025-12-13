import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from openai import OpenAI

class AvatarService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Dossiers de stockage
        self.avatar_dir = Path("static/avatars")
        self.avatar_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_avatar(self, avatar_data: Dict) -> Dict:
        """
        Génère un avatar avec DALL-E 3
        
        Args:
            avatar_data: Données de l'avatar (style, gender, description, etc.)
        
        Returns:
            Dict avec URL de l'image
        """
        try:
            if not self.openai_api_key:
                return {
                    "success": False,
                    "error": "Clé API OpenAI non configurée"
                }
            
            start_time = time.time()
            
            # Construire le prompt
            prompt = self._build_prompt(avatar_data)
            
            # Générer l'image avec DALL-E 3
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            generation_time = int(time.time() - start_time)
            
            return {
                "success": True,
                "image_url": image_url,
                "prompt": prompt,
                "generation_time": generation_time,
                "ai_model": "dall-e-3"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération : {str(e)}"
            }
    
    def _build_prompt(self, avatar_data: Dict) -> str:
        """
        Construit un prompt détaillé pour DALL-E 3
        """
        style = avatar_data.get("style", "realistic")
        gender = avatar_data.get("gender", "neutral")
        age_range = avatar_data.get("age_range", "adult")
        description = avatar_data.get("description", "")
        
        # Styles mapping
        style_prompts = {
            "realistic": "photorealistic, high quality, professional portrait",
            "cartoon": "cartoon style, colorful, friendly, animated character",
            "anime": "anime style, manga art, detailed anime character",
            "pixel-art": "pixel art style, 8-bit, retro gaming character",
            "3d": "3D rendered, Pixar style, smooth 3D character",
            "watercolor": "watercolor painting style, artistic, soft colors",
            "sketch": "pencil sketch, hand-drawn, artistic sketch"
        }
        
        # Gender mapping
        gender_prompts = {
            "male": "male",
            "female": "female",
            "neutral": "gender-neutral"
        }
        
        # Age mapping
        age_prompts = {
            "child": "child (8-12 years old)",
            "teen": "teenager (13-19 years old)",
            "adult": "adult (25-40 years old)",
            "senior": "senior (60+ years old)"
        }
        
        # Construire le prompt
        prompt_parts = []
        
        # Style de base
        prompt_parts.append(style_prompts.get(style, style_prompts["realistic"]))
        
        # Sujet principal
        prompt_parts.append(f"{gender_prompts.get(gender, 'person')} {age_prompts.get(age_range, 'adult')}")
        
        # Description personnalisée
        if description:
            prompt_parts.append(description)
        
        # Caractéristiques physiques
        if avatar_data.get("hair_color"):
            prompt_parts.append(f"{avatar_data['hair_color']} hair")
        if avatar_data.get("hair_style"):
            prompt_parts.append(f"{avatar_data['hair_style']} hairstyle")
        if avatar_data.get("eye_color"):
            prompt_parts.append(f"{avatar_data['eye_color']} eyes")
        if avatar_data.get("skin_tone"):
            prompt_parts.append(f"{avatar_data['skin_tone']} skin tone")
        
        # Vêtements et accessoires
        if avatar_data.get("clothing"):
            prompt_parts.append(f"wearing {avatar_data['clothing']}")
        if avatar_data.get("accessories"):
            accessories = avatar_data['accessories']
            if isinstance(accessories, list) and accessories:
                prompt_parts.append(f"with {', '.join(accessories)}")
        
        # Arrière-plan
        if avatar_data.get("background"):
            prompt_parts.append(f"background: {avatar_data['background']}")
        else:
            prompt_parts.append("simple solid color background")
        
        # Qualité et format
        prompt_parts.append("centered composition, profile picture, high quality")
        
        return ", ".join(prompt_parts)
    
    def get_avatar_styles(self) -> List[Dict]:
        """
        Retourne la liste des styles disponibles
        """
        return [
            {
                "id": "realistic",
                "name": "Réaliste",
                "description": "Photo réaliste professionnelle",
                "icon": "📸",
                "example": "Portrait photo de haute qualité"
            },
            {
                "id": "cartoon",
                "name": "Cartoon",
                "description": "Style dessin animé coloré",
                "icon": "🎨",
                "example": "Personnage de dessin animé"
            },
            {
                "id": "anime",
                "name": "Anime",
                "description": "Style manga japonais",
                "icon": "🎌",
                "example": "Personnage d'anime détaillé"
            },
            {
                "id": "pixel-art",
                "name": "Pixel Art",
                "description": "Style rétro 8-bit",
                "icon": "🎮",
                "example": "Sprite de jeu vidéo rétro"
            },
            {
                "id": "3d",
                "name": "3D",
                "description": "Rendu 3D style Pixar",
                "icon": "🎬",
                "example": "Personnage 3D lisse"
            },
            {
                "id": "watercolor",
                "name": "Aquarelle",
                "description": "Peinture aquarelle artistique",
                "icon": "🖌️",
                "example": "Portrait aquarelle doux"
            },
            {
                "id": "sketch",
                "name": "Croquis",
                "description": "Dessin au crayon",
                "icon": "✏️",
                "example": "Esquisse artistique"
            }
        ]
    
    def get_customization_options(self) -> Dict:
        """
        Retourne toutes les options de personnalisation
        """
        return {
            "hair_colors": [
                "black", "brown", "blonde", "red", "gray", "white",
                "blue", "pink", "purple", "green"
            ],
            "hair_styles": [
                "short", "long", "curly", "straight", "wavy",
                "bald", "ponytail", "bun", "braided", "mohawk"
            ],
            "eye_colors": [
                "brown", "blue", "green", "hazel", "gray",
                "amber", "violet"
            ],
            "skin_tones": [
                "fair", "light", "medium", "tan", "brown", "dark"
            ],
            "accessories": [
                "glasses", "sunglasses", "hat", "cap", "headphones",
                "earrings", "necklace", "scarf", "mask"
            ],
            "clothing": [
                "casual t-shirt", "formal suit", "hoodie", "dress",
                "business attire", "sports wear", "uniform"
            ],
            "backgrounds": [
                "solid color", "gradient", "nature", "city",
                "abstract", "studio", "office", "outdoor"
            ],
            "age_ranges": [
                {"id": "child", "name": "Enfant (8-12 ans)"},
                {"id": "teen", "name": "Adolescent (13-19 ans)"},
                {"id": "adult", "name": "Adulte (25-40 ans)"},
                {"id": "senior", "name": "Senior (60+ ans)"}
            ],
            "genders": [
                {"id": "male", "name": "Homme", "icon": "👨"},
                {"id": "female", "name": "Femme", "icon": "👩"},
                {"id": "neutral", "name": "Neutre", "icon": "🧑"}
            ]
        }
    
    def get_avatar_categories(self) -> List[Dict]:
        """
        Retourne les catégories d'avatars
        """
        return [
            {
                "id": "profile",
                "name": "Profil",
                "description": "Avatar pour réseaux sociaux",
                "icon": "👤"
            },
            {
                "id": "gaming",
                "name": "Gaming",
                "description": "Avatar pour jeux vidéo",
                "icon": "🎮"
            },
            {
                "id": "business",
                "name": "Business",
                "description": "Avatar professionnel",
                "icon": "💼"
            },
            {
                "id": "creative",
                "name": "Créatif",
                "description": "Avatar artistique",
                "icon": "🎨"
            },
            {
                "id": "fantasy",
                "name": "Fantasy",
                "description": "Avatar fantastique",
                "icon": "🧙"
            }
        ]
