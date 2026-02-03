"""
Script de migration pour créer les tables e-commerce
Tables: products, cart_items, orders, order_items
Date: 24 Janvier 2026
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app.models.product_db import ProductDB, CartItemDB, OrderDB, OrderItemDB
from sqlalchemy import inspect

# Importer tous les modèles pour éviter les erreurs de relations
try:
    from app.models.user_db import UserDB
    from app.models.conversation_db import ConversationDB
    from app.models.prompt_db import PromptDB
except ImportError as e:
    print(f"⚠️ Avertissement import: {e}")


def create_ecommerce_tables():
    """Créer les tables e-commerce"""
    
    print("🚀 Création des tables e-commerce...")
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    # Créer les tables
    tables_to_create = [
        ("products", ProductDB),
        ("cart_items", CartItemDB),
        ("orders", OrderDB),
        ("order_items", OrderItemDB)
    ]
    
    for table_name, model in tables_to_create:
        if table_name in existing_tables:
            print(f"⚠️  Table '{table_name}' existe déjà, skip...")
        else:
            print(f"✅ Création de la table '{table_name}'...")
            model.__table__.create(engine, checkfirst=True)
    
    print("\n✅ Tables e-commerce créées avec succès!")
    
    # Afficher les tables créées
    print("\n📋 Tables disponibles:")
    inspector = inspect(engine)
    for table in inspector.get_table_names():
        print(f"  - {table}")


def add_sample_products():
    """Ajouter des produits d'exemple"""
    
    print("\n📦 Ajout de produits d'exemple...")
    
    db = SessionLocal()
    
    try:
        # Vérifier si des produits existent déjà
        existing_count = db.query(ProductDB).count()
        if existing_count > 0:
            print(f"⚠️  {existing_count} produits existent déjà, skip...")
            return
        
        sample_products = [
            {
                "name": "Générateur de Contenu IA Pro",
                "slug": "generateur-contenu-ia-pro",
                "description": "Créez du contenu de qualité professionnelle en quelques secondes",
                "long_description": "Notre générateur de contenu IA Pro utilise les dernières technologies d'intelligence artificielle pour vous aider à créer du contenu de qualité professionnelle en quelques secondes. Que ce soit pour vos articles de blog, vos posts sur les réseaux sociaux, ou vos descriptions de produits, cet outil vous fera gagner un temps précieux.",
                "category": "Outils IA",
                "price": 49.99,
                "original_price": 79.99,
                "discount_percentage": 37,
                "image_url": "/static/images/products/product1.jpg",
                "stock": 999,
                "is_available": True,
                "is_digital": True,
                "badge": "Populaire",
                "reviews_count": 245,
                "rating": 4.8
            },
            {
                "name": "Assistant IA Marketing",
                "slug": "assistant-ia-marketing",
                "description": "Automatisez votre marketing avec l'IA",
                "long_description": "L'Assistant IA Marketing vous aide à créer des campagnes marketing performantes en quelques clics. Génération de textes publicitaires, création de visuels, planification de posts sur les réseaux sociaux, et bien plus encore.",
                "category": "Marketing",
                "price": 79.99,
                "original_price": 129.99,
                "discount_percentage": 38,
                "image_url": "/static/images/products/product2.jpg",
                "stock": 999,
                "is_available": True,
                "is_digital": True,
                "badge": "Nouveau",
                "reviews_count": 128,
                "rating": 4.9
            },
            {
                "name": "Pack Créateur de Vidéos IA",
                "slug": "pack-createur-videos-ia",
                "description": "Créez des vidéos professionnelles avec l'IA",
                "long_description": "Le Pack Créateur de Vidéos IA vous permet de créer des vidéos professionnelles en quelques minutes. Génération de scripts, voix-off automatique, montage vidéo intelligent, et export en haute qualité.",
                "category": "Vidéo",
                "price": 99.99,
                "original_price": 149.99,
                "discount_percentage": 33,
                "image_url": "/static/images/products/product3.jpg",
                "stock": 999,
                "is_available": True,
                "is_digital": True,
                "badge": "Promo",
                "reviews_count": 89,
                "rating": 4.7
            },
            {
                "name": "Suite Design IA Complète",
                "slug": "suite-design-ia-complete",
                "description": "Tous les outils de design IA en un seul pack",
                "long_description": "La Suite Design IA Complète regroupe tous nos outils de design assisté par IA : génération d'images, création de logos, design de présentations, et bien plus encore. L'outil indispensable pour les créatifs.",
                "category": "Design",
                "price": 149.99,
                "original_price": 249.99,
                "discount_percentage": 40,
                "image_url": "/static/images/products/product4.jpg",
                "stock": 999,
                "is_available": True,
                "is_digital": True,
                "badge": "Best Seller",
                "reviews_count": 456,
                "rating": 4.9
            },
            {
                "name": "Chatbot IA Personnalisé",
                "slug": "chatbot-ia-personnalise",
                "description": "Créez votre propre chatbot IA",
                "long_description": "Le Chatbot IA Personnalisé vous permet de créer un assistant virtuel sur mesure pour votre entreprise. Entraînez-le avec vos propres données, personnalisez son apparence et intégrez-le facilement sur votre site web.",
                "category": "Chatbots",
                "price": 199.99,
                "original_price": 299.99,
                "discount_percentage": 33,
                "image_url": "/static/images/products/product5.jpg",
                "stock": 999,
                "is_available": True,
                "is_digital": True,
                "badge": "Premium",
                "reviews_count": 167,
                "rating": 4.8
            },
            {
                "name": "Générateur de Code IA",
                "slug": "generateur-code-ia",
                "description": "Générez du code de qualité avec l'IA",
                "long_description": "Le Générateur de Code IA vous aide à écrire du code plus rapidement et avec moins d'erreurs. Support de nombreux langages de programmation, génération de tests unitaires, et documentation automatique.",
                "category": "Développement",
                "price": 89.99,
                "original_price": 139.99,
                "discount_percentage": 36,
                "image_url": "/static/images/products/product6.jpg",
                "stock": 999,
                "is_available": True,
                "is_digital": True,
                "badge": "Populaire",
                "reviews_count": 312,
                "rating": 4.7
            }
        ]
        
        for product_data in sample_products:
            product = ProductDB(**product_data)
            db.add(product)
        
        db.commit()
        print(f"✅ {len(sample_products)} produits d'exemple ajoutés!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des produits: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("="*60)
    print("MIGRATION E-COMMERCE - CRÉATION DES TABLES")
    print("="*60)
    
    try:
        create_ecommerce_tables()
        add_sample_products()
        
        print("\n" + "="*60)
        print("✅ MIGRATION TERMINÉE AVEC SUCCÈS")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
