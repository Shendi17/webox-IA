"""
Bibliothèque de templates de projets
"""

TEMPLATES = {
    "landing-page": {
        "name": "Landing Page",
        "description": "Page d'atterrissage moderne avec hero section, features et CTA",
        "category": "Marketing",
        "tags": ["landing", "marketing", "conversion"],
        "preview_image": "https://via.placeholder.com/400x300?text=Landing+Page",
        "files": {
            "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page Moderne</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="logo">MonApp</div>
            <nav class="nav">
                <a href="#features">Fonctionnalités</a>
                <a href="#pricing">Tarifs</a>
                <a href="#contact">Contact</a>
                <button class="btn-primary">Commencer</button>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>Transformez votre business avec notre solution</h1>
            <p>La plateforme tout-en-un pour développer votre activité en ligne</p>
            <div class="hero-cta">
                <button class="btn-primary btn-large">Essai gratuit</button>
                <button class="btn-secondary btn-large">En savoir plus</button>
            </div>
        </div>
    </section>

    <!-- Features -->
    <section id="features" class="features">
        <div class="container">
            <h2>Fonctionnalités puissantes</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <h3>Rapide</h3>
                    <p>Performance optimale pour une expérience utilisateur exceptionnelle</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Sécurisé</h3>
                    <p>Vos données sont protégées avec les dernières technologies</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>Responsive</h3>
                    <p>Fonctionne parfaitement sur tous les appareils</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="cta">
        <div class="container">
            <h2>Prêt à commencer ?</h2>
            <p>Rejoignez des milliers d'utilisateurs satisfaits</p>
            <button class="btn-primary btn-large">Démarrer maintenant</button>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 MonApp. Tous droits réservés.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>""",
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.header {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #007bff;
}

.nav {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav a {
    text-decoration: none;
    color: #333;
    transition: color 0.3s;
}

.nav a:hover {
    color: #007bff;
}

/* Buttons */
.btn-primary {
    background: #007bff;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s;
}

.btn-primary:hover {
    background: #0056b3;
}

.btn-secondary {
    background: transparent;
    color: #007bff;
    border: 2px solid #007bff;
    padding: 0.75rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s;
}

.btn-secondary:hover {
    background: #007bff;
    color: white;
}

.btn-large {
    padding: 1rem 2rem;
    font-size: 1.1rem;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 8rem 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

/* Features */
.features {
    padding: 6rem 0;
    background: #f8f9fa;
}

.features h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

/* CTA */
.cta {
    background: #007bff;
    color: white;
    padding: 6rem 0;
    text-align: center;
}

.cta h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.cta p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Footer */
.footer {
    background: #333;
    color: white;
    padding: 2rem 0;
    text-align: center;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }
    
    .hero-cta {
        flex-direction: column;
        align-items: center;
    }
    
    .nav {
        display: none;
    }
}""",
            "script.js": """// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Button animations
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 100);
    });
});

console.log('Landing Page chargée avec succès !');"""
        }
    },
    
    "portfolio": {
        "name": "Portfolio",
        "description": "Portfolio créatif pour présenter vos projets et compétences",
        "category": "Personnel",
        "tags": ["portfolio", "cv", "projets"],
        "preview_image": "https://via.placeholder.com/400x300?text=Portfolio",
        "files": {
            "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">John Doe</div>
            <ul class="nav-links">
                <li><a href="#about">À propos</a></li>
                <li><a href="#skills">Compétences</a></li>
                <li><a href="#projects">Projets</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div class="container">
            <h1>Développeur Full Stack</h1>
            <p>Je crée des expériences web modernes et performantes</p>
            <a href="#projects" class="btn">Voir mes projets</a>
        </div>
    </section>

    <!-- About -->
    <section id="about" class="about">
        <div class="container">
            <h2>À propos de moi</h2>
            <p>Passionné par le développement web depuis 5 ans, je transforme des idées en applications web élégantes et fonctionnelles.</p>
        </div>
    </section>

    <!-- Skills -->
    <section id="skills" class="skills">
        <div class="container">
            <h2>Compétences</h2>
            <div class="skills-grid">
                <div class="skill">
                    <h3>Frontend</h3>
                    <p>React, Vue.js, HTML/CSS, JavaScript</p>
                </div>
                <div class="skill">
                    <h3>Backend</h3>
                    <p>Node.js, Python, FastAPI, PostgreSQL</p>
                </div>
                <div class="skill">
                    <h3>Outils</h3>
                    <p>Git, Docker, AWS, CI/CD</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects -->
    <section id="projects" class="projects">
        <div class="container">
            <h2>Mes Projets</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <h3>Projet 1</h3>
                    <p>Application web moderne avec React et Node.js</p>
                    <a href="#" class="btn-small">Voir le projet</a>
                </div>
                <div class="project-card">
                    <h3>Projet 2</h3>
                    <p>E-commerce avec Vue.js et FastAPI</p>
                    <a href="#" class="btn-small">Voir le projet</a>
                </div>
                <div class="project-card">
                    <h3>Projet 3</h3>
                    <p>Dashboard analytics avec D3.js</p>
                    <a href="#" class="btn-small">Voir le projet</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact -->
    <section id="contact" class="contact">
        <div class="container">
            <h2>Contact</h2>
            <p>Envie de travailler ensemble ?</p>
            <a href="mailto:john@example.com" class="btn">Me contacter</a>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>""",
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navbar */
.navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #3498db;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 10rem 0 6rem;
    text-align: center;
    margin-top: 60px;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
}

.btn {
    display: inline-block;
    background: white;
    color: #667eea;
    padding: 1rem 2rem;
    border-radius: 5px;
    text-decoration: none;
    font-weight: bold;
    transition: transform 0.3s;
}

.btn:hover {
    transform: translateY(-3px);
}

/* Sections */
section {
    padding: 4rem 0;
}

section h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

/* About */
.about {
    background: #f8f9fa;
}

.about p {
    text-align: center;
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto;
}

/* Skills */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.skill {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
}

.skill h3 {
    margin-bottom: 1rem;
    color: #667eea;
}

/* Projects */
.projects {
    background: #f8f9fa;
}

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.project-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.project-card h3 {
    margin-bottom: 1rem;
}

.btn-small {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    text-decoration: none;
    margin-top: 1rem;
}

/* Contact */
.contact {
    text-align: center;
    background: #2c3e50;
    color: white;
}

@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }
    
    .nav-links {
        display: none;
    }
}""",
            "script.js": """// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    } else {
        navbar.style.boxShadow = 'none';
    }
});"""
        }
    },
    
    "blog": {
        "name": "Blog",
        "description": "Blog minimaliste pour partager vos articles",
        "category": "Contenu",
        "tags": ["blog", "articles", "contenu"],
        "preview_image": "https://via.placeholder.com/400x300?text=Blog",
        "files": {
            "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mon Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="blog-title">Mon Blog</h1>
            <p class="blog-subtitle">Réflexions et découvertes</p>
        </div>
    </header>

    <main class="container">
        <article class="post">
            <h2>Premier article de blog</h2>
            <div class="post-meta">
                <span>23 Nov 2025</span>
                <span>•</span>
                <span>5 min de lecture</span>
            </div>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            <a href="#" class="read-more">Lire la suite →</a>
        </article>

        <article class="post">
            <h2>Deuxième article</h2>
            <div class="post-meta">
                <span>22 Nov 2025</span>
                <span>•</span>
                <span>3 min de lecture</span>
            </div>
            <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <a href="#" class="read-more">Lire la suite →</a>
        </article>

        <article class="post">
            <h2>Troisième article</h2>
            <div class="post-meta">
                <span>21 Nov 2025</span>
                <span>•</span>
                <span>7 min de lecture</span>
            </div>
            <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
            <a href="#" class="read-more">Lire la suite →</a>
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Mon Blog</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>""",
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.8;
    color: #333;
    background: #fafafa;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
}

.header {
    background: white;
    padding: 4rem 0;
    text-align: center;
    border-bottom: 1px solid #eee;
}

.blog-title {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.blog-subtitle {
    color: #666;
    font-size: 1.2rem;
}

main {
    padding: 4rem 0;
}

.post {
    background: white;
    padding: 3rem;
    margin-bottom: 2rem;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.post h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

.post-meta {
    color: #999;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

.post-meta span {
    margin: 0 0.5rem;
}

.post p {
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
}

.read-more {
    color: #007bff;
    text-decoration: none;
    font-weight: bold;
}

.read-more:hover {
    text-decoration: underline;
}

.footer {
    background: white;
    padding: 2rem 0;
    text-align: center;
    border-top: 1px solid #eee;
}

@media (max-width: 768px) {
    .blog-title {
        font-size: 2rem;
    }
    
    .post {
        padding: 2rem;
    }
}""",
            "script.js": """// Animation au scroll
const posts = document.querySelectorAll('.post');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});

posts.forEach(post => {
    post.style.opacity = '0';
    post.style.transform = 'translateY(20px)';
    post.style.transition = 'all 0.5s ease';
    observer.observe(post);
});"""
        }
    },
    
    "blog-pro": {
        "name": "Blog Pro",
        "description": "Blog professionnel avec catégories, recherche et newsletter",
        "category": "Contenu",
        "tags": ["blog", "professionnel", "newsletter", "seo"],
        "preview_image": "https://via.placeholder.com/400x300?text=Blog+Pro",
        "files": {
            "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Pro - Articles & Actualités</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">📝 Blog Pro</div>
                <nav class="nav">
                    <a href="#" class="nav-link active">Accueil</a>
                    <a href="#" class="nav-link">Tech</a>
                    <a href="#" class="nav-link">Business</a>
                    <a href="#" class="nav-link">Lifestyle</a>
                    <a href="#" class="nav-link">À propos</a>
                </nav>
                <div class="search-box">
                    <input type="text" placeholder="Rechercher..." class="search-input">
                    <button class="search-btn">🔍</button>
                </div>
            </div>
        </div>
    </header>

    <!-- Hero Article -->
    <section class="hero-article">
        <div class="container">
            <div class="hero-content">
                <span class="category-badge">Tech</span>
                <h1>L'avenir de l'IA en 2025 : Tendances et Prédictions</h1>
                <p class="hero-excerpt">Découvrez les innovations qui vont transformer notre quotidien dans les années à venir...</p>
                <div class="author-info">
                    <img src="https://via.placeholder.com/40" alt="Author" class="author-avatar">
                    <div>
                        <div class="author-name">John Doe</div>
                        <div class="post-date">24 Nov 2025 • 8 min de lecture</div>
                    </div>
                </div>
            </div>
            <div class="hero-image">
                <img src="https://via.placeholder.com/600x400?text=Featured+Article" alt="Hero">
            </div>
        </div>
    </section>

    <!-- Articles Grid -->
    <section class="articles-section">
        <div class="container">
            <div class="section-header">
                <h2>Derniers Articles</h2>
                <div class="filter-tabs">
                    <button class="filter-tab active">Tous</button>
                    <button class="filter-tab">Tech</button>
                    <button class="filter-tab">Business</button>
                    <button class="filter-tab">Lifestyle</button>
                </div>
            </div>

            <div class="articles-grid">
                <article class="article-card">
                    <div class="article-image">
                        <img src="https://via.placeholder.com/400x250?text=Article+1" alt="Article">
                        <span class="category-badge">Business</span>
                    </div>
                    <div class="article-content">
                        <h3>10 Stratégies pour Booster votre Productivité</h3>
                        <p>Des méthodes éprouvées pour optimiser votre temps et atteindre vos objectifs...</p>
                        <div class="article-footer">
                            <div class="author-mini">
                                <img src="https://via.placeholder.com/30" alt="Author">
                                <span>Jane Smith</span>
                            </div>
                            <span class="read-time">5 min</span>
                        </div>
                    </div>
                </article>

                <article class="article-card">
                    <div class="article-image">
                        <img src="https://via.placeholder.com/400x250?text=Article+2" alt="Article">
                        <span class="category-badge">Tech</span>
                    </div>
                    <div class="article-content">
                        <h3>Les Meilleures Pratiques de Développement Web</h3>
                        <p>Guide complet pour créer des applications web modernes et performantes...</p>
                        <div class="article-footer">
                            <div class="author-mini">
                                <img src="https://via.placeholder.com/30" alt="Author">
                                <span>Mike Johnson</span>
                            </div>
                            <span class="read-time">12 min</span>
                        </div>
                    </div>
                </article>

                <article class="article-card">
                    <div class="article-image">
                        <img src="https://via.placeholder.com/400x250?text=Article+3" alt="Article">
                        <span class="category-badge">Lifestyle</span>
                    </div>
                    <div class="article-content">
                        <h3>Équilibre Vie Pro/Perso : Le Guide Ultime</h3>
                        <p>Comment maintenir un équilibre sain entre travail et vie personnelle...</p>
                        <div class="article-footer">
                            <div class="author-mini">
                                <img src="https://via.placeholder.com/30" alt="Author">
                                <span>Sarah Lee</span>
                            </div>
                            <span class="read-time">7 min</span>
                        </div>
                    </div>
                </article>
            </div>
        </div>
    </section>

    <!-- Newsletter -->
    <section class="newsletter">
        <div class="container">
            <div class="newsletter-content">
                <h2>📬 Restez Informé</h2>
                <p>Recevez nos meilleurs articles directement dans votre boîte mail</p>
                <form class="newsletter-form">
                    <input type="email" placeholder="Votre email..." class="newsletter-input">
                    <button type="submit" class="newsletter-btn">S'abonner</button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-col">
                    <h4>Blog Pro</h4>
                    <p>Votre source d'inspiration quotidienne</p>
                </div>
                <div class="footer-col">
                    <h4>Catégories</h4>
                    <a href="#">Tech</a>
                    <a href="#">Business</a>
                    <a href="#">Lifestyle</a>
                </div>
                <div class="footer-col">
                    <h4>Liens</h4>
                    <a href="#">À propos</a>
                    <a href="#">Contact</a>
                    <a href="#">Mentions légales</a>
                </div>
                <div class="footer-col">
                    <h4>Suivez-nous</h4>
                    <div class="social-links">
                        <a href="#">Twitter</a>
                        <a href="#">LinkedIn</a>
                        <a href="#">Instagram</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Blog Pro. Tous droits réservés.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>""",
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f8f9fa;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.header {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
    gap: 2rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: #667eea;
}

.nav {
    display: flex;
    gap: 2rem;
}

.nav-link {
    text-decoration: none;
    color: #666;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-link:hover, .nav-link.active {
    color: #667eea;
}

.search-box {
    display: flex;
    gap: 0.5rem;
}

.search-input {
    padding: 0.5rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 25px;
    outline: none;
    width: 200px;
    transition: border-color 0.3s;
}

.search-input:focus {
    border-color: #667eea;
}

.search-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    cursor: pointer;
}

/* Hero Article */
.hero-article {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    margin-top: 2rem;
}

.hero-content {
    max-width: 600px;
}

.category-badge {
    background: rgba(255,255,255,0.2);
    padding: 0.25rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    display: inline-block;
    margin-bottom: 1rem;
}

.hero-article h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.hero-excerpt {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 2rem;
}

.author-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.author-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.author-name {
    font-weight: 600;
}

.post-date {
    font-size: 0.875rem;
    opacity: 0.8;
}

/* Articles Section */
.articles-section {
    padding: 4rem 0;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.section-header h2 {
    font-size: 2rem;
}

.filter-tabs {
    display: flex;
    gap: 1rem;
}

.filter-tab {
    padding: 0.5rem 1.5rem;
    border: 2px solid #e0e0e0;
    background: white;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s;
}

.filter-tab.active, .filter-tab:hover {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
}

.article-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
}

.article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.article-image {
    position: relative;
    height: 200px;
    overflow: hidden;
}

.article-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.article-image .category-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: #667eea;
    color: white;
}

.article-content {
    padding: 1.5rem;
}

.article-content h3 {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: #333;
}

.article-content p {
    color: #666;
    margin-bottom: 1rem;
}

.article-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid #e0e0e0;
}

.author-mini {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.author-mini img {
    width: 30px;
    height: 30px;
    border-radius: 50%;
}

.author-mini span {
    font-size: 0.875rem;
    color: #666;
}

.read-time {
    font-size: 0.875rem;
    color: #999;
}

/* Newsletter */
.newsletter {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    margin: 4rem 0;
}

.newsletter-content {
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}

.newsletter-content h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

.newsletter-content p {
    margin-bottom: 2rem;
    opacity: 0.9;
}

.newsletter-form {
    display: flex;
    gap: 1rem;
    max-width: 500px;
    margin: 0 auto;
}

.newsletter-input {
    flex: 1;
    padding: 1rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
}

.newsletter-btn {
    padding: 1rem 2rem;
    background: white;
    color: #667eea;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s;
}

.newsletter-btn:hover {
    transform: scale(1.05);
}

/* Footer */
.footer {
    background: #1a1a2e;
    color: white;
    padding: 3rem 0 1rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-col h4 {
    margin-bottom: 1rem;
    color: #667eea;
}

.footer-col p {
    color: #999;
}

.footer-col a {
    display: block;
    color: #999;
    text-decoration: none;
    margin-bottom: 0.5rem;
    transition: color 0.3s;
}

.footer-col a:hover {
    color: white;
}

.social-links {
    display: flex;
    gap: 1rem;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #333;
    color: #999;
}

@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
    }
    
    .nav {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero-article h1 {
        font-size: 1.75rem;
    }
    
    .articles-grid {
        grid-template-columns: 1fr;
    }
    
    .newsletter-form {
        flex-direction: column;
    }
}""",
            "script.js": """// Animations au scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.article-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
});

// Filtres
document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
    });
});

// Newsletter
document.querySelector('.newsletter-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Merci pour votre inscription ! 🎉');
});

// Recherche
document.querySelector('.search-btn').addEventListener('click', () => {
    const query = document.querySelector('.search-input').value;
    if (query) {
        alert(`Recherche pour: ${query}`);
    }
});"""
        }
    },
    
    "ecommerce": {
        "name": "E-commerce",
        "description": "Boutique en ligne complète avec panier et checkout",
        "category": "E-commerce",
        "tags": ["shop", "panier", "produits", "vente"],
        "preview_image": "https://via.placeholder.com/400x300?text=E-commerce",
        "files": {
            "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ma Boutique - E-commerce</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">🛍️ Ma Boutique</div>
                <nav class="nav">
                    <a href="#" class="nav-link">Accueil</a>
                    <a href="#" class="nav-link">Produits</a>
                    <a href="#" class="nav-link">Catégories</a>
                    <a href="#" class="nav-link">Contact</a>
                </nav>
                <div class="header-actions">
                    <button class="icon-btn">🔍</button>
                    <button class="icon-btn">👤</button>
                    <button class="icon-btn cart-btn" onclick="toggleCart()">
                        🛒 <span class="cart-count">0</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Hero Banner -->
    <section class="hero-banner">
        <div class="container">
            <div class="hero-content">
                <h1>Nouvelle Collection 2025</h1>
                <p>Découvrez nos dernières nouveautés</p>
                <button class="btn-primary">Découvrir</button>
            </div>
        </div>
    </section>

    <!-- Categories -->
    <section class="categories-section">
        <div class="container">
            <h2 class="section-title">Catégories</h2>
            <div class="categories-grid">
                <div class="category-card">
                    <div class="category-icon">👕</div>
                    <div class="category-name">Vêtements</div>
                </div>
                <div class="category-card">
                    <div class="category-icon">👟</div>
                    <div class="category-name">Chaussures</div>
                </div>
                <div class="category-card">
                    <div class="category-icon">👜</div>
                    <div class="category-name">Accessoires</div>
                </div>
                <div class="category-card">
                    <div class="category-icon">⌚</div>
                    <div class="category-name">Montres</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Products -->
    <section class="products-section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Produits Populaires</h2>
                <div class="filters">
                    <button class="filter-btn active">Tous</button>
                    <button class="filter-btn">Nouveautés</button>
                    <button class="filter-btn">Promotions</button>
                </div>
            </div>

            <div class="products-grid">
                <div class="product-card" data-id="1" data-name="T-shirt Premium" data-price="29.99">
                    <div class="product-image">
                        <img src="https://via.placeholder.com/300x400?text=T-shirt" alt="Product">
                        <div class="product-badge">-20%</div>
                        <button class="wishlist-btn">❤️</button>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">T-shirt Premium</h3>
                        <div class="product-rating">⭐⭐⭐⭐⭐ (4.5)</div>
                        <div class="product-price">
                            <span class="price-current">29,99€</span>
                            <span class="price-old">37,99€</span>
                        </div>
                        <button class="btn-add-cart" onclick="addToCart(1, 'T-shirt Premium', 29.99)">
                            Ajouter au panier
                        </button>
                    </div>
                </div>

                <div class="product-card" data-id="2" data-name="Jean Slim" data-price="59.99">
                    <div class="product-image">
                        <img src="https://via.placeholder.com/300x400?text=Jean" alt="Product">
                        <button class="wishlist-btn">❤️</button>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">Jean Slim</h3>
                        <div class="product-rating">⭐⭐⭐⭐☆ (4.0)</div>
                        <div class="product-price">
                            <span class="price-current">59,99€</span>
                        </div>
                        <button class="btn-add-cart" onclick="addToCart(2, 'Jean Slim', 59.99)">
                            Ajouter au panier
                        </button>
                    </div>
                </div>

                <div class="product-card" data-id="3" data-name="Sneakers" data-price="89.99">
                    <div class="product-image">
                        <img src="https://via.placeholder.com/300x400?text=Sneakers" alt="Product">
                        <div class="product-badge">Nouveau</div>
                        <button class="wishlist-btn">❤️</button>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">Sneakers</h3>
                        <div class="product-rating">⭐⭐⭐⭐⭐ (5.0)</div>
                        <div class="product-price">
                            <span class="price-current">89,99€</span>
                        </div>
                        <button class="btn-add-cart" onclick="addToCart(3, 'Sneakers', 89.99)">
                            Ajouter au panier
                        </button>
                    </div>
                </div>

                <div class="product-card" data-id="4" data-name="Sac à dos" data-price="49.99">
                    <div class="product-image">
                        <img src="https://via.placeholder.com/300x400?text=Sac" alt="Product">
                        <button class="wishlist-btn">❤️</button>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">Sac à dos</h3>
                        <div class="product-rating">⭐⭐⭐⭐☆ (4.2)</div>
                        <div class="product-price">
                            <span class="price-current">49,99€</span>
                        </div>
                        <button class="btn-add-cart" onclick="addToCart(4, 'Sac à dos', 49.99)">
                            Ajouter au panier
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Cart Sidebar -->
    <div class="cart-sidebar" id="cartSidebar">
        <div class="cart-header">
            <h3>Panier</h3>
            <button class="close-btn" onclick="toggleCart()">✖️</button>
        </div>
        <div class="cart-items" id="cartItems">
            <p class="cart-empty">Votre panier est vide</p>
        </div>
        <div class="cart-footer">
            <div class="cart-total">
                <span>Total:</span>
                <span id="cartTotal">0,00€</span>
            </div>
            <button class="btn-checkout">Commander</button>
        </div>
    </div>
    <div class="cart-overlay" id="cartOverlay" onclick="toggleCart()"></div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-col">
                    <h4>Ma Boutique</h4>
                    <p>Votre destination shopping en ligne</p>
                </div>
                <div class="footer-col">
                    <h4>Liens</h4>
                    <a href="#">À propos</a>
                    <a href="#">Contact</a>
                    <a href="#">Livraison</a>
                </div>
                <div class="footer-col">
                    <h4>Suivez-nous</h4>
                    <div class="social-links">
                        <a href="#">Facebook</a>
                        <a href="#">Instagram</a>
                        <a href="#">Twitter</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Ma Boutique. Tous droits réservés.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>""",
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.header {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: #667eea;
}

.nav {
    display: flex;
    gap: 2rem;
}

.nav-link {
    text-decoration: none;
    color: #666;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-link:hover {
    color: #667eea;
}

.header-actions {
    display: flex;
    gap: 1rem;
}

.icon-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    position: relative;
}

.cart-count {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #ff4757;
    color: white;
    font-size: 0.75rem;
    padding: 2px 6px;
    border-radius: 10px;
}

/* Hero */
.hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 6rem 0;
    text-align: center;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-content p {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.btn-primary {
    padding: 1rem 2rem;
    background: white;
    color: #667eea;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s;
}

.btn-primary:hover {
    transform: scale(1.05);
}

/* Categories */
.categories-section {
    padding: 4rem 0;
}

.section-title {
    font-size: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
}

.category-card {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: transform 0.3s;
}

.category-card:hover {
    transform: translateY(-5px);
}

.category-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.category-name {
    font-weight: 600;
}

/* Products */
.products-section {
    padding: 4rem 0;
    background: #f8f9fa;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.filters {
    display: flex;
    gap: 1rem;
}

.filter-btn {
    padding: 0.5rem 1.5rem;
    border: 2px solid #e0e0e0;
    background: white;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s;
}

.filter-btn.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
}

.product-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.product-card:hover {
    transform: translateY(-5px);
}

.product-image {
    position: relative;
    height: 300px;
    overflow: hidden;
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.product-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: #ff4757;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.875rem;
}

.wishlist-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.25rem;
}

.product-info {
    padding: 1.5rem;
}

.product-name {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.product-rating {
    font-size: 0.875rem;
    color: #666;
    margin-bottom: 0.5rem;
}

.product-price {
    margin-bottom: 1rem;
}

.price-current {
    font-size: 1.5rem;
    font-weight: 700;
    color: #667eea;
}

.price-old {
    font-size: 1rem;
    color: #999;
    text-decoration: line-through;
    margin-left: 0.5rem;
}

.btn-add-cart {
    width: 100%;
    padding: 0.75rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s;
}

.btn-add-cart:hover {
    background: #5568d3;
}

/* Cart Sidebar */
.cart-sidebar {
    position: fixed;
    top: 0;
    right: -400px;
    width: 400px;
    height: 100vh;
    background: white;
    box-shadow: -2px 0 10px rgba(0,0,0,0.1);
    transition: right 0.3s;
    z-index: 1000;
    display: flex;
    flex-direction: column;
}

.cart-sidebar.active {
    right: 0;
}

.cart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}

.cart-items {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
}

.cart-empty {
    text-align: center;
    color: #999;
    padding: 2rem;
}

.cart-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #e0e0e0;
}

.cart-item-image {
    width: 80px;
    height: 80px;
    background: #f0f0f0;
    border-radius: 10px;
}

.cart-item-info {
    flex: 1;
}

.cart-item-name {
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.cart-item-price {
    color: #667eea;
    font-weight: 600;
}

.cart-item-remove {
    background: none;
    border: none;
    color: #ff4757;
    cursor: pointer;
}

.cart-footer {
    padding: 1.5rem;
    border-top: 1px solid #e0e0e0;
}

.cart-total {
    display: flex;
    justify-content: space-between;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.btn-checkout {
    width: 100%;
    padding: 1rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
}

.cart-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: none;
    z-index: 999;
}

.cart-overlay.active {
    display: block;
}

/* Footer */
.footer {
    background: #1a1a2e;
    color: white;
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-col h4 {
    margin-bottom: 1rem;
    color: #667eea;
}

.footer-col a {
    display: block;
    color: #999;
    text-decoration: none;
    margin-bottom: 0.5rem;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #333;
    color: #999;
}

@media (max-width: 768px) {
    .hero-content h1 {
        font-size: 2rem;
    }
    
    .products-grid {
        grid-template-columns: 1fr;
    }
    
    .cart-sidebar {
        width: 100%;
        right: -100%;
    }
}""",
            "script.js": """let cart = [];

function toggleCart() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('cartOverlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

function addToCart(id, name, price) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    
    updateCart();
    toggleCart();
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    updateCart();
}

function updateCart() {
    const cartItems = document.getElementById('cartItems');
    const cartCount = document.querySelector('.cart-count');
    const cartTotal = document.getElementById('cartTotal');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="cart-empty">Votre panier est vide</p>';
        cartCount.textContent = '0';
        cartTotal.textContent = '0,00€';
        return;
    }
    
    let total = 0;
    let itemCount = 0;
    
    cartItems.innerHTML = cart.map(item => {
        total += item.price * item.quantity;
        itemCount += item.quantity;
        
        return `
            <div class="cart-item">
                <div class="cart-item-image"></div>
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${item.price.toFixed(2)}€ x ${item.quantity}</div>
                </div>
                <button class="cart-item-remove" onclick="removeFromCart(${item.id})">🗑️</button>
            </div>
        `;
    }).join('');
    
    cartCount.textContent = itemCount;
    cartTotal.textContent = total.toFixed(2) + '€';
}

// Filtres
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    });
});

// Animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});

document.querySelectorAll('.product-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
});"""
        }
    },
    
    "dashboard": {
        "name": "Dashboard Admin",
        "description": "Dashboard administrateur avec statistiques et graphiques",
        "category": "Business",
        "tags": ["admin", "dashboard", "stats", "graphiques"],
        "preview_image": "https://via.placeholder.com/400x300?text=Dashboard",
        "files": {
            "index.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Admin</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Sidebar -->
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h2>📊 Dashboard</h2>
            <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
        </div>
        <nav class="sidebar-nav">
            <a href="#" class="nav-item active">
                <span class="nav-icon">📈</span>
                <span class="nav-text">Tableau de bord</span>
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">👥</span>
                <span class="nav-text">Utilisateurs</span>
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">📦</span>
                <span class="nav-text">Produits</span>
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">💰</span>
                <span class="nav-text">Ventes</span>
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">📊</span>
                <span class="nav-text">Rapports</span>
            </a>
            <a href="#" class="nav-item">
                <span class="nav-icon">⚙️</span>
                <span class="nav-text">Paramètres</span>
            </a>
        </nav>
        <div class="sidebar-footer">
            <div class="user-profile">
                <div class="user-avatar">👤</div>
                <div class="user-info">
                    <div class="user-name">Admin</div>
                    <div class="user-role">Administrateur</div>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
        <!-- Header -->
        <header class="header">
            <div class="header-left">
                <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
                <h1>Tableau de bord</h1>
            </div>
            <div class="header-right">
                <div class="search-box">
                    <input type="text" placeholder="Rechercher..." class="search-input">
                    <button class="search-btn">🔍</button>
                </div>
                <button class="icon-btn">🔔 <span class="badge">3</span></button>
                <button class="icon-btn">👤</button>
            </div>
        </header>

        <!-- Stats Cards -->
        <section class="stats-section">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon blue">👥</div>
                    <div class="stat-info">
                        <div class="stat-value">2,543</div>
                        <div class="stat-label">Utilisateurs</div>
                        <div class="stat-change positive">+12.5%</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon green">💰</div>
                    <div class="stat-info">
                        <div class="stat-value">45,678€</div>
                        <div class="stat-label">Revenus</div>
                        <div class="stat-change positive">+8.2%</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon purple">📦</div>
                    <div class="stat-info">
                        <div class="stat-value">1,234</div>
                        <div class="stat-label">Commandes</div>
                        <div class="stat-change positive">+15.3%</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon orange">⭐</div>
                    <div class="stat-info">
                        <div class="stat-value">4.8</div>
                        <div class="stat-label">Satisfaction</div>
                        <div class="stat-change positive">+0.3</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Charts -->
        <section class="charts-section">
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Revenus mensuels</h3>
                        <select class="chart-filter">
                            <option>2025</option>
                            <option>2024</option>
                        </select>
                    </div>
                    <canvas id="revenueChart"></canvas>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Répartition des ventes</h3>
                    </div>
                    <canvas id="salesChart"></canvas>
                </div>
            </div>
        </section>

        <!-- Recent Activity -->
        <section class="activity-section">
            <div class="section-header">
                <h2>Activité récente</h2>
                <button class="btn-secondary">Voir tout</button>
            </div>
            <div class="activity-list">
                <div class="activity-item">
                    <div class="activity-icon blue">👤</div>
                    <div class="activity-content">
                        <div class="activity-title">Nouvel utilisateur inscrit</div>
                        <div class="activity-time">Il y a 5 minutes</div>
                    </div>
                </div>
                <div class="activity-item">
                    <div class="activity-icon green">💰</div>
                    <div class="activity-content">
                        <div class="activity-title">Nouvelle commande #1234</div>
                        <div class="activity-time">Il y a 15 minutes</div>
                    </div>
                </div>
                <div class="activity-item">
                    <div class="activity-icon purple">📦</div>
                    <div class="activity-content">
                        <div class="activity-title">Produit ajouté au catalogue</div>
                        <div class="activity-time">Il y a 1 heure</div>
                    </div>
                </div>
                <div class="activity-item">
                    <div class="activity-icon orange">⭐</div>
                    <div class="activity-content">
                        <div class="activity-title">Nouvel avis client (5/5)</div>
                        <div class="activity-time">Il y a 2 heures</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Users Table -->
        <section class="table-section">
            <div class="section-header">
                <h2>Derniers utilisateurs</h2>
                <button class="btn-primary">+ Ajouter</button>
            </div>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Email</th>
                            <th>Rôle</th>
                            <th>Statut</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="user-cell">
                                    <div class="user-avatar-small">JD</div>
                                    <span>John Doe</span>
                                </div>
                            </td>
                            <td>john@example.com</td>
                            <td><span class="badge-role admin">Admin</span></td>
                            <td><span class="badge-status active">Actif</span></td>
                            <td>24/11/2025</td>
                            <td>
                                <button class="btn-icon">✏️</button>
                                <button class="btn-icon">🗑️</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="user-cell">
                                    <div class="user-avatar-small">JS</div>
                                    <span>Jane Smith</span>
                                </div>
                            </td>
                            <td>jane@example.com</td>
                            <td><span class="badge-role user">Utilisateur</span></td>
                            <td><span class="badge-status active">Actif</span></td>
                            <td>23/11/2025</td>
                            <td>
                                <button class="btn-icon">✏️</button>
                                <button class="btn-icon">🗑️</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="user-cell">
                                    <div class="user-avatar-small">MJ</div>
                                    <span>Mike Johnson</span>
                                </div>
                            </td>
                            <td>mike@example.com</td>
                            <td><span class="badge-role user">Utilisateur</span></td>
                            <td><span class="badge-status inactive">Inactif</span></td>
                            <td>22/11/2025</td>
                            <td>
                                <button class="btn-icon">✏️</button>
                                <button class="btn-icon">🗑️</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    </main>

    <script src="script.js"></script>
</body>
</html>""",
            "style.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f5f6fa;
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 260px;
    background: #1a1a2e;
    color: white;
    display: flex;
    flex-direction: column;
    position: fixed;
    height: 100vh;
    transition: transform 0.3s;
    z-index: 1000;
}

.sidebar.collapsed {
    transform: translateX(-260px);
}

.sidebar-header {
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-header h2 {
    font-size: 1.25rem;
}

.sidebar-toggle {
    background: none;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    display: none;
}

.sidebar-nav {
    flex: 1;
    padding: 1rem 0;
    overflow-y: auto;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    color: rgba(255,255,255,0.7);
    text-decoration: none;
    transition: all 0.3s;
}

.nav-item:hover {
    background: rgba(255,255,255,0.1);
    color: white;
}

.nav-item.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.nav-icon {
    font-size: 1.25rem;
    margin-right: 1rem;
}

.sidebar-footer {
    padding: 1rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.user-avatar {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}

.user-info {
    flex: 1;
}

.user-name {
    font-weight: 600;
    font-size: 0.9rem;
}

.user-role {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.5);
}

/* Main Content */
.main-content {
    flex: 1;
    margin-left: 260px;
    transition: margin-left 0.3s;
}

.sidebar.collapsed ~ .main-content {
    margin-left: 0;
}

/* Header */
.header {
    background: white;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.mobile-toggle {
    display: none;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}

.header h1 {
    font-size: 1.5rem;
    color: #1a1a2e;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.search-box {
    display: flex;
    gap: 0.5rem;
}

.search-input {
    padding: 0.5rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 25px;
    outline: none;
    width: 250px;
}

.search-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    cursor: pointer;
}

.icon-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    position: relative;
}

.badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #ff4757;
    color: white;
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 10px;
}

/* Stats Section */
.stats-section {
    padding: 2rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    display: flex;
    gap: 1rem;
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.75rem;
}

.stat-icon.blue { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.stat-icon.green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.stat-icon.purple { background: linear-gradient(135deg, #a8c0ff 0%, #3f2b96 100%); }
.stat-icon.orange { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }

.stat-info {
    flex: 1;
}

.stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1a1a2e;
}

.stat-label {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}

.stat-change {
    font-size: 0.875rem;
    font-weight: 600;
}

.stat-change.positive {
    color: #11998e;
}

.stat-change.negative {
    color: #ff4757;
}

/* Charts Section */
.charts-section {
    padding: 0 2rem 2rem;
}

.charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
}

.chart-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.chart-header h3 {
    font-size: 1.1rem;
    color: #1a1a2e;
}

.chart-filter {
    padding: 0.5rem 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    outline: none;
}

/* Activity Section */
.activity-section {
    padding: 0 2rem 2rem;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.section-header h2 {
    font-size: 1.25rem;
    color: #1a1a2e;
}

.activity-list {
    background: white;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    padding: 1rem;
}

.activity-item {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
    border-bottom: none;
}

.activity-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}

.activity-content {
    flex: 1;
}

.activity-title {
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 0.25rem;
}

.activity-time {
    font-size: 0.875rem;
    color: #999;
}

/* Table Section */
.table-section {
    padding: 0 2rem 2rem;
}

.table-container {
    background: white;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table thead {
    background: #f8f9fa;
}

.data-table th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: #666;
    font-size: 0.875rem;
    text-transform: uppercase;
}

.data-table td {
    padding: 1rem;
    border-top: 1px solid #f0f0f0;
}

.user-cell {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.user-avatar-small {
    width: 35px;
    height: 35px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.875rem;
    font-weight: 600;
}

.badge-role {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-role.admin {
    background: #667eea;
    color: white;
}

.badge-role.user {
    background: #e0e0e0;
    color: #666;
}

.badge-status {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-status.active {
    background: #d4edda;
    color: #155724;
}

.badge-status.inactive {
    background: #f8d7da;
    color: #721c24;
}

/* Buttons */
.btn-primary {
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s;
}

.btn-primary:hover {
    transform: translateY(-2px);
}

.btn-secondary {
    padding: 0.5rem 1rem;
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
}

.btn-icon {
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0.25rem;
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-260px);
    }
    
    .sidebar.active {
        transform: translateX(0);
    }
    
    .main-content {
        margin-left: 0;
    }
    
    .mobile-toggle {
        display: block;
    }
    
    .sidebar-toggle {
        display: block;
    }
    
    .search-box {
        display: none;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .charts-grid {
        grid-template-columns: 1fr;
    }
}""",
            "script.js": """// Toggle Sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
    sidebar.classList.toggle('active');
}

// Charts
document.addEventListener('DOMContentLoaded', function() {
    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
            datasets: [{
                label: 'Revenus 2025',
                data: [12000, 19000, 15000, 25000, 22000, 30000, 28000, 35000, 32000, 40000, 38000, 45000],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString() + '€';
                        }
                    }
                }
            }
        }
    });

    // Sales Chart
    const salesCtx = document.getElementById('salesChart').getContext('2d');
    new Chart(salesCtx, {
        type: 'doughnut',
        data: {
            labels: ['Produits A', 'Produits B', 'Produits C', 'Produits D'],
            datasets: [{
                data: [35, 25, 20, 20],
                backgroundColor: [
                    '#667eea',
                    '#11998e',
                    '#f5576c',
                    '#ffa502'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
});

// Animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});

document.querySelectorAll('.stat-card, .chart-card, .activity-list, .table-container').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease';
    observer.observe(el);
});"""
        }
    }
}

# Fonction pour obtenir tous les templates
def get_all_templates():
    """Retourner tous les templates disponibles"""
    return {
        template_id: {
            "id": template_id,
            **template_data
        }
        for template_id, template_data in TEMPLATES.items()
    }

# Fonction pour obtenir un template spécifique
def get_template(template_id):
    """Retourner un template spécifique"""
    if template_id in TEMPLATES:
        return {
            "id": template_id,
            **TEMPLATES[template_id]
        }
    return None

# Fonction pour obtenir les catégories
def get_categories():
    """Retourner toutes les catégories"""
    categories = set()
    for template in TEMPLATES.values():
        categories.add(template["category"])
    return sorted(list(categories))
