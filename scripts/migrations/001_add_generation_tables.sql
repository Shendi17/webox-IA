-- Migration : Ajout des tables pour la génération multi-média
-- Date : 10 Novembre 2025
-- Description : Tables pour images, vidéos, audio, eBooks, vidéos short, workflows et catalogue

-- ============================================
-- TABLE : generated_images
-- ============================================
CREATE TABLE IF NOT EXISTS generated_images (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Paramètres de génération
    prompt TEXT NOT NULL,
    negative_prompt TEXT,
    model VARCHAR(50) NOT NULL,
    size VARCHAR(20),
    style VARCHAR(50),
    quality VARCHAR(20),
    
    -- Résultat
    image_url VARCHAR(500),
    local_path VARCHAR(500),
    
    -- Métadonnées
    width INTEGER,
    height INTEGER,
    file_size INTEGER,
    
    -- Coût et statut
    cost FLOAT,
    status VARCHAR(50) DEFAULT 'generating',
    error_message TEXT,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status)
);

-- ============================================
-- TABLE : generated_videos
-- ============================================
CREATE TABLE IF NOT EXISTS generated_videos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Paramètres de génération
    prompt TEXT NOT NULL,
    model VARCHAR(50) NOT NULL,
    duration INTEGER,
    resolution VARCHAR(20),
    fps INTEGER,
    
    -- Résultat
    video_url VARCHAR(500),
    local_path VARCHAR(500),
    thumbnail_url VARCHAR(500),
    
    -- Métadonnées
    width INTEGER,
    height INTEGER,
    file_size INTEGER,
    actual_duration FLOAT,
    
    -- Coût et statut
    cost FLOAT,
    status VARCHAR(50) DEFAULT 'generating',
    error_message TEXT,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status)
);

-- ============================================
-- TABLE : generated_audio
-- ============================================
CREATE TABLE IF NOT EXISTS generated_audio (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Paramètres de génération
    prompt TEXT NOT NULL,
    model VARCHAR(50) NOT NULL,
    audio_type VARCHAR(50),
    voice_id VARCHAR(100),
    language VARCHAR(10),
    duration INTEGER,
    
    -- Résultat
    audio_url VARCHAR(500),
    local_path VARCHAR(500),
    
    -- Métadonnées
    file_size INTEGER,
    actual_duration FLOAT,
    format VARCHAR(20),
    
    -- Coût et statut
    cost FLOAT,
    status VARCHAR(50) DEFAULT 'generating',
    error_message TEXT,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status)
);

-- ============================================
-- TABLE : ebooks
-- ============================================
CREATE TABLE IF NOT EXISTS ebooks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Paramètres de génération
    title VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    chapters INTEGER NOT NULL,
    tone VARCHAR(50),
    audience VARCHAR(50),
    language VARCHAR(10),
    
    -- Options
    has_cover BOOLEAN DEFAULT TRUE,
    has_toc BOOLEAN DEFAULT TRUE,
    has_illustrations BOOLEAN DEFAULT FALSE,
    has_summaries BOOLEAN DEFAULT TRUE,
    
    -- Résultat
    cover_url VARCHAR(500),
    pdf_url VARCHAR(500),
    epub_url VARCHAR(500),
    mobi_url VARCHAR(500),
    
    -- Métadonnées
    total_pages INTEGER,
    word_count INTEGER,
    file_size INTEGER,
    table_of_contents JSON,
    
    -- Coût et statut
    cost FLOAT,
    status VARCHAR(50) DEFAULT 'generating',
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status),
    INDEX idx_title (title)
);

-- ============================================
-- TABLE : video_shorts
-- ============================================
CREATE TABLE IF NOT EXISTS video_shorts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Paramètres de génération
    subject TEXT NOT NULL,
    duration INTEGER NOT NULL,
    format VARCHAR(20) NOT NULL,
    style VARCHAR(50),
    voice VARCHAR(50),
    
    -- Options
    has_music BOOLEAN DEFAULT TRUE,
    has_subtitles BOOLEAN DEFAULT TRUE,
    has_logo BOOLEAN DEFAULT FALSE,
    has_hook BOOLEAN DEFAULT TRUE,
    has_cta BOOLEAN DEFAULT TRUE,
    
    -- Résultat
    video_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    script TEXT,
    
    -- Métadonnées
    width INTEGER,
    height INTEGER,
    file_size INTEGER,
    actual_duration FLOAT,
    visuals JSON,
    audio_url VARCHAR(500),
    music_url VARCHAR(500),
    
    -- Coût et statut
    cost FLOAT,
    status VARCHAR(50) DEFAULT 'generating',
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status)
);

-- ============================================
-- TABLE : workflows
-- ============================================
CREATE TABLE IF NOT EXISTS workflows (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Informations du workflow
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    
    -- Configuration
    steps JSON NOT NULL,
    
    -- Métadonnées
    is_template BOOLEAN DEFAULT FALSE,
    is_public BOOLEAN DEFAULT FALSE,
    times_used INTEGER DEFAULT 0,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_is_template (is_template),
    INDEX idx_category (category)
);

-- ============================================
-- TABLE : workflow_executions
-- ============================================
CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    user_email VARCHAR(255),
    
    -- Inputs
    input_data JSON,
    
    -- Résultats
    results JSON,
    
    -- Métadonnées
    total_cost FLOAT,
    total_duration FLOAT,
    
    -- Statut
    status VARCHAR(50) DEFAULT 'running',
    current_step INTEGER DEFAULT 0,
    error_message TEXT,
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Index
    INDEX idx_workflow_id (workflow_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status),
    
    -- Foreign key
    FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
);

-- ============================================
-- TABLE : catalog_favorites
-- ============================================
CREATE TABLE IF NOT EXISTS catalog_favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    tool_id VARCHAR(100) NOT NULL,
    tool_name VARCHAR(255),
    tool_category VARCHAR(50),
    
    -- Dates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index
    INDEX idx_user_id (user_id),
    INDEX idx_tool_id (tool_id),
    
    -- Contrainte unique
    UNIQUE KEY unique_user_tool (user_id, tool_id)
);

-- ============================================
-- COMMENTAIRES
-- ============================================
COMMENT ON TABLE generated_images IS 'Images générées par IA (DALL-E, Midjourney, Stable Diffusion)';
COMMENT ON TABLE generated_videos IS 'Vidéos générées par IA (Runway, Pika, Luma)';
COMMENT ON TABLE generated_audio IS 'Audio/Musique générés par IA (Suno, Udio, ElevenLabs)';
COMMENT ON TABLE ebooks IS 'eBooks générés automatiquement (GPT-4 + DALL-E + PDF)';
COMMENT ON TABLE video_shorts IS 'Vidéos short pour TikTok/Reels/Shorts';
COMMENT ON TABLE workflows IS 'Workflows de combinaisons IA';
COMMENT ON TABLE workflow_executions IS 'Historique d''exécution des workflows';
COMMENT ON TABLE catalog_favorites IS 'Favoris du catalogue d''outils IA';

-- ============================================
-- FIN DE LA MIGRATION
-- ============================================
