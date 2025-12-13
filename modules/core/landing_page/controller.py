"""Controller - Logique de la landing page"""

import streamlit as st
from .model import LandingPageData
from .styles import get_css
from modules.core.auth import register_user, login_user


@st.dialog("🔐 Connexion")
def show_login_modal():
    """Modal de connexion"""
    st.markdown("### Connectez-vous à WeBox Multi-IA")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="admin@webox.com")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="admin123")
        remember = st.checkbox("Se souvenir de moi (30 jours)", value=True)
        submit = st.form_submit_button("Se connecter", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                success, message = login_user(email, password, remember)
                if success:
                    from modules.core.session_manager import login_with_session
                    login_with_session(email, message, remember)
                    st.success(f"✅ Bienvenue {message} !")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    st.info("💡 **Compte admin par défaut :** admin@webox.com / admin123")
    st.caption("🔒 Connexion sécurisée avec session persistante")


@st.dialog("📝 Inscription")
def show_register_modal():
    """Modal d'inscription"""
    st.markdown("### Créez votre compte WeBox Multi-IA")
    
    with st.form("register_form"):
        name = st.text_input("👤 Nom complet", placeholder="Jean Dupont")
        email = st.text_input("📧 Email", placeholder="votre@email.com")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="••••••••")
        password_confirm = st.text_input("🔒 Confirmer", type="password", placeholder="••••••••")
        terms = st.checkbox("J'accepte les conditions d'utilisation")
        submit = st.form_submit_button("Créer mon compte", use_container_width=True)
        
        if submit:
            if not all([name, email, password, password_confirm]):
                st.error("❌ Veuillez remplir tous les champs")
            elif password != password_confirm:
                st.error("❌ Les mots de passe ne correspondent pas")
            elif len(password) < 6:
                st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
            elif not terms:
                st.error("❌ Veuillez accepter les conditions")
            else:
                success, message = register_user(email, password, name)
                if success:
                    st.success(f"✅ {message}")
                    st.info("👉 Vous pouvez maintenant vous connecter")
                else:
                    st.error(f"❌ {message}")


def show_landing_page():
    """Affiche la landing page complète"""
    
    # Charger les données
    data = LandingPageData()
    
    # Appliquer les styles CSS
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # ===== HERO PLEINE PAGE - SOLUTION FINALE =====
    # Utiliser st.image dans un conteneur avec CSS forcé
    st.markdown('<div class="hero-section-wrapper">', unsafe_allow_html=True)
    
    # Titre
    st.markdown(f"""
    <div class="hero-title-section">
        <h1><span class="emoji">{data.TITLE_EMOJI}</span> <span class="webox">{data.TITLE_WEBOX}</span> <span class="multi-ia">{data.TITLE_MULTI_IA}</span></h1>
        <h2>{data.SUBTITLE}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Image
    st.markdown('<div class="hero-image-section">', unsafe_allow_html=True)
    st.image("media/images/Webox-IA.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Texte
    st.markdown(f"""
    <div class="hero-text-section">
        <p class="hero-features">{data.HERO_FEATURES}</p>
        <p class="hero-description">{data.HERO_DESCRIPTION}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Espacement avant les boutons
    st.markdown('<div class="spacer-top-3"></div>', unsafe_allow_html=True)
    
    # ===== BOUTONS CTA =====
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔐 Connexion", use_container_width=True):
                show_login_modal()
        with col_b:
            if st.button("📝 Inscription", use_container_width=True):
                show_register_modal()
    
    # Espacement après les boutons
    st.markdown('<div class="spacer-bottom-2"></div>', unsafe_allow_html=True)
    
    # ===== STATS =====
    stats_html = '<div class="stats"><div class="stats-grid">'
    for stat in data.STATS:
        stats_html += f'<div class="stat"><div class="stat-num">{stat["number"]}</div><div class="stat-label">{stat["label"]}</div></div>'
    stats_html += '</div></div>'
    st.markdown(stats_html, unsafe_allow_html=True)
    
    # ===== FONCTIONNALITÉS =====
    st.markdown('<div class="section"><h2 class="section-title">✨ Fonctionnalités Puissantes</h2><p class="section-subtitle">Découvrez tout ce que WeBox Multi-IA peut faire pour vous</p></div>', unsafe_allow_html=True)
    
    # Utiliser des colonnes pour créer les marges
    margin_left, content_col, margin_right = st.columns([1, 10, 1])
    
    with content_col:
        col1, col2, col3 = st.columns(3, gap="medium")
        
        # Colonne 1
        with col1:
            for feature in data.FEATURES_COL1:
                items_html = "".join([f"<li>{item}</li>" for item in feature["items"]])
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">{feature["icon"]}</div>
                    <h3 class="card-title">{feature["title"]}</h3>
                    <p class="card-text">{feature["description"]}</p>
                    <ul class="card-list">{items_html}</ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Colonne 2
        with col2:
            for feature in data.FEATURES_COL2:
                items_html = "".join([f"<li>{item}</li>" for item in feature["items"]])
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">{feature["icon"]}</div>
                    <h3 class="card-title">{feature["title"]}</h3>
                    <p class="card-text">{feature["description"]}</p>
                    <ul class="card-list">{items_html}</ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Colonne 3
        with col3:
            for feature in data.FEATURES_COL3:
                items_html = "".join([f"<li>{item}</li>" for item in feature["items"]])
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">{feature["icon"]}</div>
                    <h3 class="card-title">{feature["title"]}</h3>
                    <p class="card-text">{feature["description"]}</p>
                    <ul class="card-list">{items_html}</ul>
                </div>
                """, unsafe_allow_html=True)
    
    # ===== TÉMOIGNAGES =====
    st.markdown('<div class="section-alt"><h2 class="section-title">💬 Ce Que Disent Nos Utilisateurs</h2><p class="section-subtitle">Rejoignez des milliers d\'utilisateurs satisfaits</p></div>', unsafe_allow_html=True)
    
    margin_left, content_col, margin_right = st.columns([1, 10, 1])
    with content_col:
        cols = st.columns(3, gap="medium")
        for i, testimonial in enumerate(data.TESTIMONIALS):
            with cols[i]:
                st.markdown(f"""
                <div class="testimonial">
                    <div class="testimonial-text">"{testimonial["text"]}"</div>
                    <div class="testimonial-author">{testimonial["author"]}</div>
                    <div class="testimonial-role">{testimonial["role"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ===== POURQUOI CHOISIR WEBOX =====
    st.markdown('<div class="section"><h2 class="section-title">🌟 Pourquoi Choisir WeBox Multi-IA ?</h2><p class="section-subtitle">Les raisons qui font de WeBox la meilleure solution IA</p></div>', unsafe_allow_html=True)
    
    margin_left, content_col, margin_right = st.columns([1, 10, 1])
    with content_col:
        cols = st.columns(3, gap="medium")
        for i, item in enumerate(data.WHY_CHOOSE):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="why-box">
                    <div class="why-icon">{item["icon"]}</div>
                    <div class="why-title">{item["title"]}</div>
                    <div class="why-text">{item["description"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ===== CTA =====
    st.markdown("""
    <div class="cta">
        <h2>🚀 Prêt à Révolutionner Votre Workflow ?</h2>
        <p>Rejoignez des milliers d'utilisateurs qui automatisent leur travail avec l'IA. Commencez gratuitement dès aujourd'hui !</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Espacement avant les boutons CTA finaux
    st.markdown('<div class="spacer-top-3"></div>', unsafe_allow_html=True)
    
    # Boutons CTA finaux
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Commencer Maintenant", use_container_width=True, key="cta_start"):
                show_register_modal()
        with col_b:
            if st.button("🔐 Se Connecter", use_container_width=True, key="cta_login"):
                show_login_modal()
    
    # Espacement avant footer
    st.markdown('<div class="spacer-bottom-2"></div>', unsafe_allow_html=True)
    
    # ===== FOOTER =====
    st.markdown(f"""
    <div class="footer">
        <div class="footer-links">
            <a class="footer-link" href="?page=documentation">📖 Documentation interne</a>
            <a class="footer-link" href="?page=contact">📧 Page de contact</a>
            <a class="footer-link" href="?page=cgu">📜 Conditions d'utilisation</a>
            <a class="footer-link" href="?page=privacy">🔒 Politique de confidentialité</a>
        </div>
        <p class="footer-title">🤖 {data.TITLE_WEBOX} {data.TITLE_MULTI_IA} {data.VERSION}</p>
        <p class="footer-tagline">{data.FOOTER_TAGLINE}</p>
        <p class="footer-features">{data.FOOTER_FEATURES}</p>
        <p class="footer-copyright">{data.COPYRIGHT}</p>
    </div>
    """, unsafe_allow_html=True)
