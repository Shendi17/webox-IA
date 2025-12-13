"""
Service de génération de contenus avec IA
"""
from typing import Dict, List, Optional
import re
from datetime import datetime

from app.services.ai_providers import AIProviderFactory


class ContentGeneratorService:
    """Service pour générer tous types de contenus avec IA"""
    
    def __init__(self, ai_model: str = "gpt-4"):
        self.ai_model = ai_model
        self.ai_provider = AIProviderFactory.get_provider(ai_model)
    
    def generate_blog_article(
        self,
        topic: str,
        keywords: List[str] = None,
        length: int = 2000,
        tone: str = "professionnel",
        include_images: bool = True
    ) -> Dict:
        """
        Générer un article de blog complet
        
        Args:
            topic: Sujet de l'article
            keywords: Mots-clés SEO
            length: Longueur en mots
            tone: Ton (professionnel, décontracté, etc.)
            include_images: Inclure des suggestions d'images
        
        Returns:
            Dict avec l'article complet
        """
        try:
            keywords_str = ", ".join(keywords) if keywords else ""
            
            prompt = f"""Tu es un rédacteur web expert en SEO.

Écris un article de blog complet sur : "{topic}"

Mots-clés à inclure : {keywords_str}
Longueur : environ {length} mots
Ton : {tone}

Structure l'article avec :
1. Titre accrocheur (H1)
2. Introduction engageante
3. 5-7 sections avec sous-titres (H2, H3)
4. Exemples concrets et données
5. Conclusion avec call-to-action
6. Meta description (150-160 caractères)

Format : HTML simple (h1, h2, h3, p, ul, li, strong, em)

{"Suggère 3-5 emplacements pour des images avec descriptions." if include_images else ""}

Optimise pour le SEO en utilisant naturellement les mots-clés.
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            content = response["content"]
            
            # Extraire le titre
            title_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else topic
            
            # Extraire la meta description
            meta_match = re.search(r'Meta description[:\s]*(.+?)(?:\n|$)', content, re.IGNORECASE)
            meta_description = meta_match.group(1).strip() if meta_match else ""
            
            # Compter les mots
            text_only = re.sub(r'<[^>]+>', '', content)
            word_count = len(text_only.split())
            
            # Temps de lecture (250 mots/minute)
            reading_time = max(1, word_count // 250)
            
            # Extraire les suggestions d'images
            images_suggestions = []
            if include_images:
                image_pattern = r'Image \d+[:\s]*(.+?)(?:\n|$)'
                images_suggestions = re.findall(image_pattern, content, re.IGNORECASE)
            
            return {
                "success": True,
                "content": {
                    "title": title,
                    "content": content,
                    "meta_description": meta_description,
                    "word_count": word_count,
                    "reading_time": reading_time,
                    "keywords": keywords or [],
                    "images_suggestions": images_suggestions
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def generate_social_posts(
        self,
        platform: str,
        topic: str,
        count: int = 5,
        format: str = "post",
        tone: str = "engageant"
    ) -> Dict:
        """
        Générer des posts pour réseaux sociaux
        
        Args:
            platform: Plateforme (linkedin, instagram, twitter, etc.)
            topic: Sujet des posts
            count: Nombre de posts à générer
            format: Format (post, carousel, story)
            tone: Ton du contenu
        
        Returns:
            Dict avec les posts générés
        """
        try:
            platform_specs = {
                "linkedin": "Professionnel, 1300 caractères max, focus business",
                "instagram": "Visuel, 2200 caractères max, emojis, hashtags",
                "twitter": "Concis, 280 caractères max, percutant",
                "facebook": "Conversationnel, 500 caractères idéal",
                "tiktok": "Jeune, dynamique, tendances, hashtags"
            }
            
            spec = platform_specs.get(platform.lower(), "Adapté à la plateforme")
            
            prompt = f"""Tu es un expert en social media pour {platform}.

Génère {count} posts sur : "{topic}"

Spécifications {platform} : {spec}
Format : {format}
Ton : {tone}

Pour chaque post, fournis :
1. Le texte du post
2. 5-10 hashtags pertinents
3. Une suggestion de visuel

Réponds en JSON avec ce format :
{{
    "posts": [
        {{
            "text": "Texte du post...",
            "hashtags": ["hashtag1", "hashtag2", ...],
            "visual_suggestion": "Description du visuel"
        }}
    ]
}}

Assure-toi que :
- Les posts sont variés et engageants
- Les hashtags sont pertinents et populaires
- Le ton est adapté à {platform}
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            # Parser la réponse JSON
            import json
            content = response["content"]
            
            # Extraire le JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                posts_data = json.loads(json_match.group())
            else:
                posts_data = json.loads(content)
            
            return {
                "success": True,
                "posts": posts_data.get("posts", []),
                "platform": platform,
                "count": len(posts_data.get("posts", []))
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def generate_email(
        self,
        email_type: str,
        topic: str,
        target_audience: str = "général",
        tone: str = "professionnel"
    ) -> Dict:
        """
        Générer un email
        
        Args:
            email_type: Type (newsletter, promo, bienvenue, etc.)
            topic: Sujet de l'email
            target_audience: Audience cible
            tone: Ton du contenu
        
        Returns:
            Dict avec l'email généré
        """
        try:
            email_specs = {
                "newsletter": "Informatif, valeur ajoutée, liens vers contenus",
                "promo": "Persuasif, urgence, call-to-action clair",
                "bienvenue": "Chaleureux, présentation, prochaines étapes",
                "abandon": "Rappel doux, bénéfices, incitation retour",
                "remerciement": "Gratitude, renforcement relation"
            }
            
            spec = email_specs.get(email_type.lower(), "Email professionnel")
            
            prompt = f"""Tu es un expert en email marketing.

Génère un email de type "{email_type}" sur : "{topic}"

Spécifications : {spec}
Audience : {target_audience}
Ton : {tone}

Fournis :
1. Objet de l'email (accrocheur, 50 caractères max)
2. Pré-header (complément objet, 100 caractères)
3. Corps de l'email en HTML (simple et responsive)
4. Call-to-action clair

Format HTML simple : <h2>, <p>, <a>, <strong>, <ul>, <li>

Assure-toi que :
- L'objet incite à ouvrir
- Le contenu apporte de la valeur
- Le CTA est clair et visible
- Le design est responsive
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            content = response["content"]
            
            # Extraire l'objet
            subject_match = re.search(r'Objet[:\s]*(.+?)(?:\n|$)', content, re.IGNORECASE)
            subject = subject_match.group(1).strip() if subject_match else topic
            
            # Extraire le pré-header
            preheader_match = re.search(r'Pré-header[:\s]*(.+?)(?:\n|$)', content, re.IGNORECASE)
            preheader = preheader_match.group(1).strip() if preheader_match else ""
            
            return {
                "success": True,
                "email": {
                    "subject": subject,
                    "preheader": preheader,
                    "content": content,
                    "type": email_type
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def generate_video_script(
        self,
        topic: str,
        duration: int = 60,
        style: str = "éducatif",
        platform: str = "youtube"
    ) -> Dict:
        """
        Générer un script vidéo
        
        Args:
            topic: Sujet de la vidéo
            duration: Durée en secondes
            style: Style (éducatif, divertissant, etc.)
            platform: Plateforme (youtube, tiktok, instagram)
        
        Returns:
            Dict avec le script vidéo
        """
        try:
            platform_specs = {
                "youtube": "Détaillé, introduction accrocheuse, structure claire",
                "tiktok": "Rapide, hook immédiat, tendances",
                "instagram": "Visuel, court, engageant"
            }
            
            spec = platform_specs.get(platform.lower(), "Script vidéo standard")
            
            prompt = f"""Tu es un créateur de contenu vidéo expert.

Génère un script vidéo sur : "{topic}"

Durée : {duration} secondes
Style : {style}
Plateforme : {platform}
Spécifications : {spec}

Structure le script avec :
1. Hook (3-5 secondes) - Accroche immédiate
2. Introduction (10% du temps)
3. Corps principal (70% du temps)
4. Conclusion + CTA (20% du temps)

Pour chaque section, indique :
- Le texte à dire (voix off)
- Les visuels à montrer
- Les transitions
- La durée approximative

Format : Markdown avec sections claires

Assure-toi que :
- Le hook capte l'attention immédiatement
- Le rythme est adapté à {platform}
- Le CTA est clair
"""
            
            messages = [{"role": "user", "content": prompt}]
            response = self.ai_provider.chat(messages)
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": "Erreur de génération IA"
                }
            
            content = response["content"]
            
            return {
                "success": True,
                "script": {
                    "content": content,
                    "duration": duration,
                    "style": style,
                    "platform": platform
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de génération: {str(e)}"
            }
    
    def optimize_seo(self, content: str, keywords: List[str]) -> Dict:
        """
        Optimiser le contenu pour le SEO
        
        Args:
            content: Contenu à optimiser
            keywords: Mots-clés cibles
        
        Returns:
            Dict avec score SEO et suggestions
        """
        try:
            score = 0
            suggestions = []
            
            # Vérifier la longueur
            word_count = len(content.split())
            if word_count >= 1000:
                score += 20
            else:
                suggestions.append(f"Augmenter la longueur (actuellement {word_count} mots, recommandé: 1000+)")
            
            # Vérifier les mots-clés
            content_lower = content.lower()
            keywords_found = sum(1 for kw in keywords if kw.lower() in content_lower)
            if keywords_found == len(keywords):
                score += 30
            else:
                suggestions.append(f"Inclure tous les mots-clés ({keywords_found}/{len(keywords)} trouvés)")
            
            # Vérifier les titres
            h1_count = len(re.findall(r'<h1>', content, re.IGNORECASE))
            h2_count = len(re.findall(r'<h2>', content, re.IGNORECASE))
            
            if h1_count == 1:
                score += 15
            else:
                suggestions.append("Utiliser exactement un titre H1")
            
            if h2_count >= 3:
                score += 15
            else:
                suggestions.append("Ajouter au moins 3 sous-titres H2")
            
            # Vérifier les liens
            links_count = len(re.findall(r'<a ', content, re.IGNORECASE))
            if links_count >= 3:
                score += 10
            else:
                suggestions.append("Ajouter au moins 3 liens internes/externes")
            
            # Vérifier les images
            images_count = len(re.findall(r'<img ', content, re.IGNORECASE))
            if images_count >= 1:
                score += 10
            else:
                suggestions.append("Ajouter au moins une image")
            
            return {
                "success": True,
                "seo_score": score,
                "suggestions": suggestions,
                "word_count": word_count,
                "keywords_found": keywords_found
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur d'analyse SEO: {str(e)}"
            }
