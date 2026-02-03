"""
Migration des email campaigns de l'ancienne vers la nouvelle structure
Date: 3 Février 2026
"""

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.business_db import EmailCampaignDB
from app.models.marketing_db import EmailCampaign, CampaignStatus
from app.database import get_db, engine


def map_status(old_status: str) -> CampaignStatus:
    """Mapper ancien statut vers nouveau"""
    mapping = {
        'draft': CampaignStatus.DRAFT,
        'scheduled': CampaignStatus.SCHEDULED,
        'sent': CampaignStatus.COMPLETED
    }
    return mapping.get(old_status, CampaignStatus.DRAFT)


def migrate_email_campaigns(db: Session):
    """
    Migrer toutes les campagnes email de l'ancienne structure vers la nouvelle
    """
    print("🔄 Début de la migration des email campaigns...")
    
    try:
        # Récupérer toutes les anciennes campagnes
        old_campaigns = db.query(EmailCampaignDB).all()
        print(f"📊 {len(old_campaigns)} campagnes trouvées dans email_campaigns_old")
        
        if len(old_campaigns) == 0:
            print("✅ Aucune campagne à migrer")
            return
        
        migrated_count = 0
        skipped_count = 0
        
        for old in old_campaigns:
            # Vérifier si déjà migrée (par ID ou nom)
            existing = db.query(EmailCampaign).filter(
                EmailCampaign.name == old.name,
                EmailCampaign.author_id == old.user_id
            ).first()
            
            if existing:
                print(f"⏭️  Campagne '{old.name}' déjà migrée, ignorée")
                skipped_count += 1
                continue
            
            # Calculer les taux
            open_rate = 0.0
            click_rate = 0.0
            if old.sent_count and old.sent_count > 0:
                open_rate = (old.opened_count / old.sent_count * 100) if old.opened_count else 0
                click_rate = (old.clicked_count / old.sent_count * 100) if old.clicked_count else 0
            
            # Créer nouvelle campagne
            new_campaign = EmailCampaign(
                author_id=old.user_id,
                name=old.name,
                subject=old.subject,
                preheader=old.preview_text or "",
                html_content=old.content_html,
                text_content=old.content_text or "",
                scheduled_at=old.scheduled_time,
                sent_at=old.sent_at,
                total_recipients=old.total_recipients or 0,
                total_sent=old.sent_count or 0,
                total_delivered=old.sent_count or 0,  # Approximation
                total_opened=old.opened_count or 0,
                total_clicked=old.clicked_count or 0,
                total_bounced=old.bounced_count or 0,
                total_unsubscribed=0,  # Pas disponible dans ancienne version
                open_rate=round(open_rate, 2),
                click_rate=round(click_rate, 2),
                status=map_status(old.status),
                created_at=old.created_at,
                updated_at=old.created_at
            )
            
            db.add(new_campaign)
            migrated_count += 1
            print(f"✅ Campagne '{old.name}' migrée (ID: {old.id})")
        
        # Commit toutes les migrations
        db.commit()
        
        print(f"\n🎉 Migration terminée!")
        print(f"   - Migrées: {migrated_count}")
        print(f"   - Ignorées (déjà migrées): {skipped_count}")
        print(f"   - Total: {len(old_campaigns)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la migration: {str(e)}")
        raise


def verify_migration(db: Session):
    """
    Vérifier que la migration s'est bien passée
    """
    print("\n🔍 Vérification de la migration...")
    
    old_count = db.query(EmailCampaignDB).count()
    new_count = db.query(EmailCampaign).count()
    
    print(f"   - Anciennes campagnes: {old_count}")
    print(f"   - Nouvelles campagnes: {new_count}")
    
    if new_count >= old_count:
        print("✅ Vérification OK - Toutes les campagnes ont été migrées")
        return True
    else:
        print(f"⚠️  Attention: {old_count - new_count} campagnes manquantes")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION EMAIL CAMPAIGNS: OLD → NEW")
    print("=" * 60)
    
    # Créer une session
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Exécuter la migration
        migrate_email_campaigns(db)
        
        # Vérifier
        verify_migration(db)
        
        print("\n✅ Migration complète terminée avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur fatale: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
