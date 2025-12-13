import os
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from openai import OpenAI

class SeriesService:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Configuration Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configuration OpenAI
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    def get_genres(self) -> List[Dict]:
        """Retourne la liste des genres disponibles"""
        return [
            {"id": "drama", "name": "Drame", "icon": "🎭", "description": "Histoires émotionnelles et profondes"},
            {"id": "comedy", "name": "Comédie", "icon": "😂", "description": "Histoires drôles et légères"},
            {"id": "sci-fi", "name": "Science-Fiction", "icon": "🚀", "description": "Futur, technologie, espace"},
            {"id": "fantasy", "name": "Fantasy", "icon": "🧙", "description": "Magie, créatures fantastiques"},
            {"id": "thriller", "name": "Thriller", "icon": "🔍", "description": "Suspense et mystère"},
            {"id": "romance", "name": "Romance", "icon": "💕", "description": "Histoires d'amour"},
            {"id": "action", "name": "Action", "icon": "⚔️", "description": "Aventure et action"},
            {"id": "horror", "name": "Horreur", "icon": "👻", "description": "Peur et suspense"},
            {"id": "mystery", "name": "Mystère", "icon": "🕵️", "description": "Énigmes et investigations"},
            {"id": "adventure", "name": "Aventure", "icon": "🗺️", "description": "Exploration et découverte"}
        ]
    
    def get_styles(self) -> List[Dict]:
        """Retourne la liste des styles visuels"""
        return [
            {"id": "realistic", "name": "Réaliste", "icon": "📸", "description": "Style photo réaliste"},
            {"id": "cartoon", "name": "Cartoon", "icon": "🎨", "description": "Style dessin animé"},
            {"id": "anime", "name": "Anime", "icon": "🎌", "description": "Style manga japonais"},
            {"id": "comic", "name": "Comic", "icon": "💥", "description": "Style bande dessinée"},
            {"id": "watercolor", "name": "Aquarelle", "icon": "🖌️", "description": "Style peinture aquarelle"},
            {"id": "3d", "name": "3D", "icon": "🎬", "description": "Rendu 3D moderne"}
        ]
    
    def get_target_audiences(self) -> List[Dict]:
        """Retourne les publics cibles"""
        return [
            {"id": "kids", "name": "Enfants", "icon": "👶", "age": "3-8 ans"},
            {"id": "teens", "name": "Adolescents", "icon": "🧒", "age": "9-17 ans"},
            {"id": "adults", "name": "Adultes", "icon": "👨", "age": "18+ ans"},
            {"id": "all", "name": "Tout public", "icon": "👨‍👩‍👧‍👦", "age": "Tous âges"}
        ]
    
    async def generate_series_concept(self, title: str, description: str, genre: str, 
                                     target_audience: str, num_episodes: int) -> Dict:
        """
        Génère le concept complet d'une série
        """
        try:
            prompt = f"""Tu es un scénariste professionnel. Crée un concept détaillé pour une série TV.

INFORMATIONS :
- Titre : {title}
- Description : {description}
- Genre : {genre}
- Public cible : {target_audience}
- Nombre d'épisodes : {num_episodes}

GÉNÈRE UN CONCEPT COMPLET avec :

1. SYNOPSIS (200-300 mots)
Un résumé captivant de la série entière.

2. PERSONNAGES PRINCIPAUX (3-5 personnages)
Pour chaque personnage :
- Nom
- Âge
- Rôle
- Personnalité (3-4 traits)
- Objectif principal
- Conflit interne

3. ARC NARRATIF
- Point de départ
- Développement (milieu)
- Climax
- Résolution

4. THÈMES PRINCIPAUX (2-3 thèmes)

5. STRUCTURE DES ÉPISODES
Pour chaque épisode (numéroté de 1 à {num_episodes}) :
- Titre de l'épisode
- Résumé (50-100 mots)
- Événements clés

Réponds UNIQUEMENT en JSON valide avec cette structure :
{{
    "synopsis": "...",
    "characters": [
        {{
            "name": "...",
            "age": 25,
            "role": "...",
            "personality": ["trait1", "trait2", "trait3"],
            "goal": "...",
            "conflict": "..."
        }}
    ],
    "storyline": {{
        "beginning": "...",
        "middle": "...",
        "climax": "...",
        "resolution": "..."
    }},
    "themes": ["theme1", "theme2"],
    "episodes": [
        {{
            "number": 1,
            "title": "...",
            "summary": "...",
            "key_events": ["event1", "event2"]
        }}
    ]
}}"""

            response = self.gemini_model.generate_content(prompt)
            
            # Parser la réponse JSON
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            concept = json.loads(response_text.strip())
            
            return {
                "success": True,
                "concept": concept
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération : {str(e)}"
            }
    
    async def generate_episode_script(self, series_title: str, episode_number: int, 
                                     episode_title: str, episode_summary: str,
                                     characters: List[Dict], duration: int) -> Dict:
        """
        Génère le script complet d'un épisode
        """
        try:
            characters_desc = "\n".join([
                f"- {c['name']} ({c['role']}): {', '.join(c['personality'])}"
                for c in characters
            ])
            
            prompt = f"""Tu es un scénariste professionnel. Écris le script complet d'un épisode.

SÉRIE : {series_title}
ÉPISODE {episode_number} : {episode_title}
RÉSUMÉ : {episode_summary}
DURÉE : {duration} minutes

PERSONNAGES :
{characters_desc}

GÉNÈRE UN SCRIPT COMPLET avec :

1. STRUCTURE EN SCÈNES (5-8 scènes pour {duration} minutes)
Pour chaque scène :
- Numéro de scène
- Titre de la scène
- Lieu (INT/EXT et description)
- Moment de la journée
- Description de l'action (50-100 mots)
- Dialogues (naturels et engageants)
- Personnages présents
- Ambiance/Mood

Réponds UNIQUEMENT en JSON valide :
{{
    "script": "Script narratif complet...",
    "scenes": [
        {{
            "number": 1,
            "title": "...",
            "location": "INT. LIEU - JOUR",
            "time_of_day": "day",
            "description": "...",
            "dialogue": "PERSONNAGE: Texte...\\nPERSONNAGE2: Texte...",
            "action": "...",
            "characters": ["nom1", "nom2"],
            "mood": "tense"
        }}
    ]
}}"""

            response = self.gemini_model.generate_content(prompt)
            
            # Parser la réponse
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            script_data = json.loads(response_text.strip())
            
            return {
                "success": True,
                "script": script_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération : {str(e)}"
            }
    
    async def generate_scene_image(self, scene_description: str, style: str, 
                                   characters: List[str], location: str, 
                                   mood: str) -> Dict:
        """
        Génère une image pour une scène
        """
        try:
            # Construire le prompt pour DALL-E
            style_prompts = {
                "realistic": "photorealistic, cinematic lighting, high detail",
                "cartoon": "cartoon style, vibrant colors, animated",
                "anime": "anime style, manga art, Japanese animation",
                "comic": "comic book style, bold lines, dynamic",
                "watercolor": "watercolor painting, soft colors, artistic",
                "3d": "3D render, modern CGI, Pixar style"
            }
            
            mood_prompts = {
                "happy": "bright, cheerful atmosphere",
                "sad": "melancholic, somber tones",
                "tense": "dramatic lighting, suspenseful",
                "mysterious": "dark shadows, enigmatic",
                "romantic": "warm lighting, intimate",
                "action": "dynamic, energetic, motion blur"
            }
            
            characters_text = ", ".join(characters) if characters else "characters"
            
            prompt = f"""{scene_description}

Location: {location}
Characters: {characters_text}
Mood: {mood_prompts.get(mood, mood)}
Style: {style_prompts.get(style, style)}

High quality, detailed, professional composition."""
            
            # Générer l'image avec DALL-E 3
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt[:4000],  # Limite de DALL-E
                size="1792x1024",  # Format cinématique
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            return {
                "success": True,
                "image_url": image_url,
                "prompt": prompt
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la génération : {str(e)}"
            }
    
    async def generate_cover_image(self, title: str, synopsis: str, genre: str, style: str) -> Dict:
        """
        Génère l'image de couverture de la série
        """
        try:
            style_prompts = {
                "realistic": "photorealistic movie poster, cinematic",
                "cartoon": "animated series poster, vibrant",
                "anime": "anime series poster, manga style",
                "comic": "comic book cover, bold graphics",
                "watercolor": "artistic poster, watercolor style",
                "3d": "3D animated poster, modern CGI"
            }
            
            prompt = f"""TV Series Poster: {title}

{synopsis[:200]}

Genre: {genre}
Style: {style_prompts.get(style, style)}

Professional TV series poster, eye-catching, high quality, title text visible, dramatic composition."""
            
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt[:4000],
                size="1024x1792",  # Format poster
                quality="standard",
                n=1
            )
            
            return {
                "success": True,
                "image_url": response.data[0].url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur : {str(e)}"
            }
