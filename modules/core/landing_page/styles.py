"""Styles CSS de la landing page"""


def get_css():
    """Retourne tout le CSS de la landing page"""
    return """
    <style>
        .main {background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 0 !important; margin: 0 !important;}
        .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Supprimer TOUT le padding et margin en haut */
        .main > div {padding-top: 0 !important; margin-top: 0 !important;}
        .main > div > div {padding-top: 0 !important; margin-top: 0 !important;}
        .main > div > div > div {padding-left: 0 !important; padding-right: 0 !important; padding-top: 0 !important; margin-top: 0 !important;}
        .main .block-container > div {padding-top: 0 !important; margin-top: 0 !important;}
        .element-container:first-child {margin-top: 0 !important; padding-top: 0 !important;}
        
        /* ========================================
           HERO - SOLUTION FINALE SIMPLE
           ======================================== */
        
        /* FORCER LE FOND BLEU SUR TOUS LES CONTENEURS DU HERO */
        .element-container:has(.hero-section-wrapper),
        .element-container:has(.hero-title-section),
        .element-container:has(.hero-image-section),
        .element-container:has(.hero-text-section) {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%) !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Forcer aussi tous les conteneurs entre wrapper et spacer */
        .element-container:has(.hero-section-wrapper) ~ .element-container:not(:has(.spacer-top-3)) {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%) !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .hero-section-wrapper {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
            padding: 4rem 2rem 1rem 2rem;
            margin: 0;
            text-align: center;
        }
        
        /* Titre */
        .hero-title-section {
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .hero-title-section h1 {
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
            line-height: 1.2;
            color: white;
            text-align: center;
        }
        .hero-title-section h1 .emoji {color: #ffd700;}
        .hero-title-section h1 .webox {color: #ffd700;}
        .hero-title-section h1 .multi-ia {color: #4169e1;}
        
        .hero-title-section h2 {
            font-size: 1.8rem;
            opacity: 0.95;
            color: #ffd700;
            font-weight: 600;
            text-align: center;
        }
        
        /* Image - RÉDUITE À 500px */
        .hero-image-section {
            margin: 1.5rem auto;
            max-width: 500px;
            padding: 0;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .hero-image-section img,
        .element-container:has(.hero-image-section) img {
            border-radius: 20px !important;
            box-shadow: 0 30px 80px rgba(255, 215, 0, 0.4) !important;
            border: 3px solid #ffd700 !important;
            transition: all 0.4s !important;
            max-width: 500px !important;
            width: 100% !important;
            height: auto !important;
            display: block !important;
            margin: 0 auto !important;
        }
        
        .hero-image-section img:hover,
        .element-container:has(.hero-image-section) img:hover {
            transform: scale(1.03) !important;
            box-shadow: 0 40px 100px rgba(255, 215, 0, 0.6) !important;
        }
        
        /* Texte - bien centré */
        .hero-text-section {
            margin-top: 1.5rem;
            padding-bottom: 2rem;
            text-align: center;
        }
        
        .hero-features {
            font-size: 1.2rem;
            margin: 0 auto 1.5rem;
            line-height: 1.8;
            opacity: 0.95;
            color: white;
            max-width: 1000px;
            text-align: center;
        }
        
        .hero-description {
            font-size: 1.4rem;
            color: #ffd700;
            font-weight: 600;
            text-align: center;
            margin: 0 auto;
        }
        
        /* Conteneur du contenu */
        .hero-container {
            text-align: center;
            color: white;
            position: relative;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Titre principal */
        .hero-container h1 {
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.5);
            line-height: 1.2;
        }
        .hero-container h1 .emoji {color: #ffd700;}
        .hero-container h1 .webox {color: #ffd700;}
        .hero-container h1 .multi-ia {color: #4169e1;}
        
        /* Sous-titre */
        .hero-container h2 {
            font-size: 1.8rem;
            margin-bottom: 0;
            opacity: 0.95;
            color: #ffd700;
            font-weight: 600;
        }
        
        /* Features */
        .hero-features {
            font-size: 1.2rem;
            margin: 0 auto 1.5rem;
            line-height: 1.8;
            opacity: 0.95;
            color: white;
            max-width: 1000px;
        }
        
        /* Description finale */
        .hero-description {
            font-size: 1.4rem;
            color: #ffd700;
            font-weight: 600;
            margin-top: 1rem;
        }
        
        .stats {background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%); padding: 3rem 2rem; color: white; text-align: center; border-top: 3px solid #ffd700; border-bottom: 3px solid #ffd700;}
        .stats-grid {display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 3rem; max-width: 1400px; margin: 0 auto;}
        .stat {padding: 1.5rem;}
        .stat-num {font-size: 3.5rem; font-weight: 900; color: #ffd700; text-shadow: 2px 2px 6px rgba(255,215,0,0.3); margin-bottom: 0.5rem;}
        .stat-label {font-size: 1.1rem; opacity: 0.95; font-weight: 600; color: #4169e1;}
        
        /* Espacements */
        .spacer-top-3 {margin-top: 3rem;}
        .spacer-bottom-2 {margin-bottom: 2rem;}
        
        .section {background: #ffffff !important; padding: 4rem 0 !important; margin: 0 !important;}
        .section-alt {background: #f8f9fa !important; padding: 4rem 0 !important; margin: 0 !important;}
        .content-container {max-width: 1400px !important; margin: 0 auto !important; padding: 0 !important;}
        
        /* Forcer TOUS les éléments Streamlit à respecter les marges */
        .section [data-testid="stVerticalBlock"] {padding-left: 0 !important; padding-right: 0 !important;}
        .section [data-testid="column"] {padding-left: 0.5rem !important; padding-right: 0.5rem !important;}
        .section [data-testid="column"]:first-child {padding-left: 0 !important;}
        .section [data-testid="column"]:last-child {padding-right: 0 !important;}
        .section .element-container {padding: 0 !important; margin: 0 !important;}
        .section-alt [data-testid="stVerticalBlock"] {padding-left: 0 !important; padding-right: 0 !important;}
        .section-alt [data-testid="column"] {padding-left: 0.5rem !important; padding-right: 0.5rem !important;}
        .section-alt [data-testid="column"]:first-child {padding-left: 0 !important;}
        .section-alt [data-testid="column"]:last-child {padding-right: 0 !important;}
        .section-alt .element-container {padding: 0 !important; margin: 0 !important;}
        .section-title {text-align: center; font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;}
        .section-subtitle {text-align: center; font-size: 1.2rem; color: #555; margin-bottom: 3rem; max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.6;}
        
        .card {background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); margin-bottom: 2rem; transition: all 0.4s; border: 3px solid transparent; position: relative; overflow: hidden;}
        .card::before {content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: linear-gradient(90deg, #ffd700 0%, #4169e1 100%); opacity: 0; transition: opacity 0.4s;}
        .card:hover {transform: translateY(-12px); box-shadow: 0 20px 50px rgba(255,215,0,0.2); border-color: #ffd700;}
        .card:hover::before {opacity: 1;}
        .card-icon {font-size: 3rem; margin-bottom: 1.5rem;}
        .card-title {font-size: 1.6rem; font-weight: 700; background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;}
        .card-text {color: #555; line-height: 1.6; font-size: 1rem; margin-bottom: 1rem;}
        .card-list {text-align: left; padding-left: 1.5rem; margin-top: 0.5rem;}
        .card-list li {color: #666; margin-bottom: 0.5rem; line-height: 1.5; font-size: 0.95rem;}
        
        .testimonial {background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 2rem; border-left: 5px solid #ffd700; transition: all 0.3s;}
        .testimonial:hover {transform: translateX(10px); box-shadow: 0 12px 35px rgba(255,215,0,0.2);}
        .testimonial-text {font-size: 1rem; color: #555; line-height: 1.6; font-style: italic; margin-bottom: 1.5rem;}
        .testimonial-author {font-weight: 700; color: #1a1a2e; font-size: 1.1rem; margin-bottom: 0.3rem;}
        .testimonial-role {color: #4169e1; font-size: 0.9rem; font-weight: 500;}
        
        .why-box {text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); margin-bottom: 2rem; transition: all 0.3s; border: 2px solid transparent;}
        .why-box:hover {transform: scale(1.05); border-color: #ffd700; box-shadow: 0 12px 35px rgba(255,215,0,0.2);}
        .why-icon {font-size: 3rem; margin-bottom: 1.5rem;}
        .why-title {color: #1a1a2e; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 700;}
        .why-text {color: #666; line-height: 1.6; font-size: 1rem;}
        
        .cta {background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); padding: 4rem 2rem; text-align: center; color: white; border-top: 3px solid #ffd700;}
        .cta h2 {font-size: 3rem; font-weight: 800; margin-bottom: 1.5rem; color: #ffd700; text-shadow: 2px 2px 6px rgba(0,0,0,0.3);}
        .cta p {font-size: 1.2rem; margin-bottom: 2rem; max-width: 800px; margin-left: auto; margin-right: auto; line-height: 1.8; opacity: 0.95;}
        
        .footer {background: #0a0a0a; color: white; padding: 3rem 2rem; text-align: center; border-top: 3px solid #ffd700;}
        .footer-links {display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;}
        .footer-link {color: #ffd700; text-decoration: none; font-weight: 600; font-size: 1rem; transition: all 0.3s; cursor: pointer; display: inline-block;}
        .footer-link:hover {color: #4169e1; transform: translateY(-2px); text-decoration: underline;}
        .footer-title {font-size: 1.1rem; margin-bottom: 1rem;}
        .footer-tagline {opacity: 0.8;}
        .footer-features {opacity: 0.9; margin-top: 1.5rem; font-size: 1rem;}
        .footer-copyright {opacity: 0.6; margin-top: 1rem; font-size: 0.9rem;}
        
        .stButton>button {background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%) !important; color: #1a1a2e !important; border: 3px solid #ffd700 !important; padding: 0.8rem 2.5rem !important; border-radius: 50px !important; font-weight: 800 !important; font-size: 1.1rem !important; box-shadow: 0 6px 20px rgba(255,215,0,0.4) !important; transition: all 0.3s !important;}
        .stButton>button:hover {transform: translateY(-4px) !important; box-shadow: 0 10px 30px rgba(255,215,0,0.6) !important; background: linear-gradient(135deg, #ffed4e 0%, #ffd700 100%) !important;}
        
        /* Cacher complètement les boutons du footer */
        .footer ~ div[data-testid="column"] button,
        .footer ~ div button {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            opacity: 0 !important;
        }
    </style>
    """
