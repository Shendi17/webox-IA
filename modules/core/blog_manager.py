"""Gestionnaire de blog pour WeBox Multi-IA"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

BLOG_FILE = "data/blog_articles.json"


class BlogManager:
    """Gestionnaire d'articles de blog"""
    
    def __init__(self):
        self.articles = self.load_articles()
    
    def load_articles(self) -> List[Dict]:
        """Charge les articles depuis le fichier"""
        if os.path.exists(BLOG_FILE):
            try:
                with open(BLOG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_articles(self):
        """Sauvegarde les articles dans le fichier"""
        with open(BLOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
    
    def add_article(self, title: str, content: str, category: str, author: str = "WeBox Team") -> str:
        """Ajoute un nouvel article"""
        article_id = f"article_{len(self.articles) + 1}"
        article = {
            "id": article_id,
            "title": title,
            "content": content,
            "category": category,
            "author": author,
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0
        }
        self.articles.insert(0, article)  # Ajouter au début
        self.save_articles()
        return article_id
    
    def get_article(self, article_id: str) -> Optional[Dict]:
        """Récupère un article par son ID"""
        for article in self.articles:
            if article["id"] == article_id:
                return article
        return None
    
    def get_all_articles(self) -> List[Dict]:
        """Retourne tous les articles"""
        return self.articles
    
    def get_articles_by_category(self, category: str) -> List[Dict]:
        """Retourne les articles d'une catégorie"""
        return [a for a in self.articles if a["category"] == category]
    
    def increment_views(self, article_id: str):
        """Incrémente le nombre de vues"""
        for article in self.articles:
            if article["id"] == article_id:
                article["views"] += 1
                self.save_articles()
                break
    
    def increment_likes(self, article_id: str):
        """Incrémente le nombre de likes"""
        for article in self.articles:
            if article["id"] == article_id:
                article["likes"] += 1
                self.save_articles()
                break
    
    def get_categories(self) -> List[str]:
        """Retourne la liste des catégories"""
        categories = set()
        for article in self.articles:
            categories.add(article["category"])
        return sorted(list(categories))


# Instance globale
blog_manager = BlogManager()


def init_blog_with_top50():
    """Initialise le blog avec les articles principaux"""
    if len(blog_manager.articles) == 0:
        # Article 1 : Top 50 des IA
        try:
            with open("TOP_50_IA.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            blog_manager.add_article(
                title="🏆 Top 50 des IA - Classement par Catégories",
                content=content,
                category="Guide IA",
                author="WeBox Team"
            )
        except:
            pass
        
        # Article 2 : Génération de Médias
        try:
            with open("GENERATION_MEDIA_IA.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            blog_manager.add_article(
                title="🎨 Génération de Médias IA - Guide Complet",
                content=content,
                category="Tutoriel",
                author="WeBox Team"
            )
        except:
            pass
        
        # Article 3 : Démarrage Rapide
        try:
            with open("DEMARRAGE_RAPIDE_GENERATION.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            blog_manager.add_article(
                title="🚀 Démarrage Rapide - Génération de Médias en 5 Minutes",
                content=content,
                category="Démarrage",
                author="WeBox Team"
            )
        except:
            pass
        
        return True
    return False
