"""
Migration des funnels de l'ancienne vers la nouvelle structure
Date: 3 Février 2026
"""

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.funnel_db import FunnelDB
from app.models.marketing_db import Funnel, FunnelPage, FunnelType, FunnelPageType
from app.database import get_db, engine


def map_funnel_type(template: str) -> FunnelType:
    """Mapper ancien template vers nouveau type"""
    if not template:
        return FunnelType.OTHER
    
    template_lower = template.lower()
    mapping = {
        'webinar': FunnelType.WEBINAR,
        'product-sale': FunnelType.PRODUCT,
        'product': FunnelType.PRODUCT,
        'lead-gen': FunnelType.LEAD_MAGNET,
        'lead': FunnelType.LEAD_MAGNET,
        'ecommerce': FunnelType.PRODUCT,
        'launch': FunnelType.PRODUCT,
        'service': FunnelType.SERVICE,
        'membership': FunnelType.MEMBERSHIP
    }
    
    for key, value in mapping.items():
        if key in template_lower:
            return value
    
    return FunnelType.OTHER


def map_page_type(step_type: str) -> FunnelPageType:
    """Mapper type de step vers type de page"""
    if not step_type:
        return FunnelPageType.SALES
    
    step_lower = step_type.lower()
    mapping = {
        'landing-page': FunnelPageType.OPTIN,
        'landing': FunnelPageType.OPTIN,
        'optin': FunnelPageType.OPTIN,
        'opt-in': FunnelPageType.OPTIN,
        'presentation': FunnelPageType.VSL,
        'vsl': FunnelPageType.VSL,
        'video': FunnelPageType.VSL,
        'sales': FunnelPageType.SALES,
        'sale': FunnelPageType.SALES,
        'upsell': FunnelPageType.UPSELL,
        'up-sell': FunnelPageType.UPSELL,
        'downsell': FunnelPageType.DOWNSELL,
        'down-sell': FunnelPageType.DOWNSELL,
        'thank-you': FunnelPageType.THANK_YOU,
        'thankyou': FunnelPageType.THANK_YOU,
        'thanks': FunnelPageType.THANK_YOU,
        'webinar': FunnelPageType.WEBINAR
    }
    
    for key, value in mapping.items():
        if key in step_lower:
            return value
    
    return FunnelPageType.SALES


def migrate_funnels(db: Session):
    """
    Migrer tous les funnels de l'ancienne structure vers la nouvelle
    """
    print("🔄 Début de la migration des funnels...")
    
    try:
        # Récupérer tous les anciens funnels
        old_funnels = db.query(FunnelDB).all()
        print(f"📊 {len(old_funnels)} funnels trouvés dans funnels_old")
        
        if len(old_funnels) == 0:
            print("✅ Aucun funnel à migrer")
            return
        
        migrated_count = 0
        skipped_count = 0
        pages_created = 0
        
        for old in old_funnels:
            # Vérifier si déjà migré
            existing = db.query(Funnel).filter(
                Funnel.name == old.name,
                Funnel.author_id == old.user_id
            ).first()
            
            if existing:
                print(f"⏭️  Funnel '{old.name}' déjà migré, ignoré")
                skipped_count += 1
                continue
            
            # Créer nouveau funnel
            new_funnel = Funnel(
                author_id=old.user_id,
                name=old.name,
                description=old.description or "",
                funnel_type=map_funnel_type(old.template),
                is_active=old.is_active if hasattr(old, 'is_active') else True,
                is_template=False,
                total_visitors=old.total_entries if hasattr(old, 'total_entries') else 0,
                total_leads=old.total_conversions if hasattr(old, 'total_conversions') else 0,
                total_sales=old.total_conversions if hasattr(old, 'total_conversions') else 0,
                total_revenue=old.total_revenue if hasattr(old, 'total_revenue') else 0.0,
                conversion_rate=old.conversion_rate if hasattr(old, 'conversion_rate') else 0.0,
                created_at=old.created_at,
                updated_at=old.updated_at if hasattr(old, 'updated_at') else old.created_at
            )
            
            db.add(new_funnel)
            db.flush()  # Pour obtenir l'ID du funnel
            
            # Créer les pages à partir des steps
            if old.steps:
                try:
                    steps = old.steps if isinstance(old.steps, list) else json.loads(old.steps)
                    
                    for idx, step in enumerate(steps):
                        if not isinstance(step, dict):
                            continue
                        
                        # Extraire les informations du step
                        step_name = step.get('name', f'Step {idx + 1}')
                        step_type = step.get('type', 'sales')
                        step_config = step.get('config', {})
                        
                        # Créer la page
                        page = FunnelPage(
                            funnel_id=new_funnel.id,
                            name=step_name,
                            page_type=map_page_type(step_type),
                            slug=f"funnel-{new_funnel.id}-step-{idx + 1}",
                            html_content=step_config.get('html', '') if isinstance(step_config, dict) else '',
                            css_content=step_config.get('css', '') if isinstance(step_config, dict) else '',
                            js_content=step_config.get('js', '') if isinstance(step_config, dict) else '',
                            order=idx,
                            is_published=old.is_published if hasattr(old, 'is_published') else False,
                            meta_title=step_name,
                            meta_description=step.get('description', ''),
                            visitors=0,
                            conversions=0,
                            conversion_rate=0.0
                        )
                        
                        db.add(page)
                        pages_created += 1
                        
                except (json.JSONDecodeError, TypeError) as e:
                    print(f"⚠️  Erreur lors du parsing des steps pour '{old.name}': {str(e)}")
            
            migrated_count += 1
            print(f"✅ Funnel '{old.name}' migré (ID: {old.id}) avec {len(old.steps) if old.steps else 0} pages")
        
        # Commit toutes les migrations
        db.commit()
        
        print(f"\n🎉 Migration terminée!")
        print(f"   - Funnels migrés: {migrated_count}")
        print(f"   - Pages créées: {pages_created}")
        print(f"   - Ignorés (déjà migrés): {skipped_count}")
        print(f"   - Total: {len(old_funnels)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la migration: {str(e)}")
        raise


def verify_migration(db: Session):
    """
    Vérifier que la migration s'est bien passée
    """
    print("\n🔍 Vérification de la migration...")
    
    old_count = db.query(FunnelDB).count()
    new_count = db.query(Funnel).count()
    pages_count = db.query(FunnelPage).count()
    
    print(f"   - Anciens funnels: {old_count}")
    print(f"   - Nouveaux funnels: {new_count}")
    print(f"   - Pages créées: {pages_count}")
    
    if new_count >= old_count:
        print("✅ Vérification OK - Tous les funnels ont été migrés")
        return True
    else:
        print(f"⚠️  Attention: {old_count - new_count} funnels manquants")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION FUNNELS: OLD → NEW")
    print("=" * 60)
    
    # Créer une session
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Exécuter la migration
        migrate_funnels(db)
        
        # Vérifier
        verify_migration(db)
        
        print("\n✅ Migration complète terminée avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur fatale: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
