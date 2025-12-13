-- Creer l'utilisateur administrateur
-- Date : 30 Octobre 2025

-- Inserer l'utilisateur (mot de passe hashe = "admin123")
INSERT INTO users (
    email,
    username,
    hashed_password,
    name,
    is_active,
    is_admin,
    is_premium,
    role,
    created_at
) VALUES (
    'admin@webox.com',
    'admin',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
    'Administrateur WeBox',
    true,
    true,
    true,
    'admin',
    NOW()
)
ON CONFLICT (email) DO NOTHING;

-- Afficher l'utilisateur cree
SELECT id, email, username, name, role, created_at 
FROM users 
WHERE email = 'admin@webox.com';
