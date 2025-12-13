# Script de configuration Alembic
# Date : 30 Octobre 2025

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "║           CONFIGURATION ALEMBIC - WEBOX                      ║" -ForegroundColor Cyan
Write-Host "║                                                              ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚙️  Configuration d'Alembic pour PostgreSQL..." -ForegroundColor Cyan
Write-Host ""

# Lire le .env pour obtenir DATABASE_URL
$envPath = ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "❌ Fichier .env non trouvé" -ForegroundColor Red
    pause
    exit
}

$databaseUrl = (Get-Content $envPath | Select-String "DATABASE_URL=").ToString().Split("=", 2)[1]

if (-not $databaseUrl) {
    Write-Host "❌ DATABASE_URL non trouvé dans .env" -ForegroundColor Red
    pause
    exit
}

Write-Host "✅ DATABASE_URL trouvé" -ForegroundColor Green
Write-Host ""

# Modifier alembic.ini
$alembicIniPath = "app\alembic.ini"
if (-not (Test-Path $alembicIniPath)) {
    Write-Host "❌ Fichier alembic.ini non trouvé" -ForegroundColor Red
    pause
    exit
}

Write-Host "📝 Mise à jour de alembic.ini..." -ForegroundColor Cyan
$content = Get-Content $alembicIniPath -Raw
$content = $content -replace "sqlalchemy.url = driver://user:pass@localhost/dbname", "# sqlalchemy.url = (configuré dans env.py)"
Set-Content $alembicIniPath $content -NoNewline

Write-Host "✅ alembic.ini mis à jour" -ForegroundColor Green
Write-Host ""

# Modifier env.py
$envPyPath = "app\alembic\env.py"
if (-not (Test-Path $envPyPath)) {
    Write-Host "❌ Fichier env.py non trouvé" -ForegroundColor Red
    pause
    exit
}

Write-Host "📝 Mise à jour de env.py..." -ForegroundColor Cyan

$envPyContent = @"
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Charger les variables d'environnement
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.database import Base
from app.models.user_db import UserDB
from app.models.conversation_db import ConversationDB, MessageDB

target_metadata = Base.metadata

# Override sqlalchemy.url with environment variable
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    '''Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    '''
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    '''Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    '''
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"@

Set-Content $envPyPath $envPyContent -Encoding UTF8

Write-Host "✅ env.py mis à jour" -ForegroundColor Green
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Configuration Alembic terminée !" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Prochaines étapes :" -ForegroundColor Cyan
Write-Host "  1. Créer la première migration" -ForegroundColor White
Write-Host "     cd app" -ForegroundColor Gray
Write-Host "     alembic revision --autogenerate -m 'Initial migration'" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Appliquer la migration" -ForegroundColor White
Write-Host "     alembic upgrade head" -ForegroundColor Gray
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
