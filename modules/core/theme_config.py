"""Configuration des couleurs du thème de l'application"""

# ===== COULEURS PRINCIPALES DU THÈME =====
THEME_COLORS = {
    # Couleurs de base
    "primary": "#ffd700",           # Jaune principal
    "primary_light": "#ffed4e",     # Jaune clair
    "secondary": "#4169e1",         # Bleu
    "dark": "#1a1a2e",              # Bleu foncé
    "darker": "#0f3460",            # Bleu plus foncé
    "black": "#0a0a0a",             # Noir
    "white": "#ffffff",             # Blanc
    "gray_light": "#f8f9fa",        # Gris clair
    "gray": "#e0e0e0",              # Gris
    "gray_dark": "#555555",         # Gris foncé
    "beige": "#fffef0",             # Beige clair
}

# ===== COULEURS DE LA SIDEBAR =====
SIDEBAR_COLORS = {
    # Fond de la sidebar (gradient)
    "background": "linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%)",
    "background_solid": "#1a1a2e",
    
    # ========================================
    # 1️⃣ LIENS EN HAUT (app, agents ia, blog, etc.)
    # ========================================
    "top_links_text": "#ffffff",  # Couleur des liens - BLANC
    "top_links_hover": "rgba(255, 215, 0, 0.1)",  # Fond au survol
    
    # ========================================
    # 2️⃣ TITRE PRINCIPAL (🤖 WeBox Multi-IA)
    # ========================================
    "main_title_text": "#ffd700",  # JAUNE
    
    # ========================================
    # 3️⃣ NOM UTILISATEUR (👤 Administrateur)
    # ========================================
    "user_name_text": "#ffd700",  # JAUNE
    
    # ========================================
    # 4️⃣ SÉPARATEURS HORIZONTAUX (<hr>)
    # ========================================
    "separator_color": "#ffd700",  # JAUNE
    
    # ========================================
    # 5️⃣ SOUS-TITRES (📍 Navigation, 🤖 Sélection des IA)
    # ========================================
    "subtitle_text": "#ffd700",  # JAUNE
    
    # ========================================
    # 6️⃣ BOUTONS RADIO NAVIGATION (💬 Chat Multi-IA, 🎯 Assistants, etc.)
    # ========================================
    "radio_text": "#ffffff",  # Texte - BLANC
    "radio_hover_bg": "rgba(255, 215, 0, 0.1)",  # Fond au survol
    
    # ========================================
    # 7️⃣ EXPANDERS OUVERTS (💬 Texte & Conversation, etc.)
    # ========================================
    "expander_open_title": "#000000",  # Titre cliquable - NOIR
    "expander_open_content": "#ffffff",  # Contenu - BLANC
    
    # ========================================
    # 8️⃣ EXPANDERS FERMÉS (⚙️ Paramètres, ➕ Nouveau dossier, 📁 Général)
    # ========================================
    "expander_closed_title": "#ffffff",  # Titre cliquable - BLANC
    "expander_closed_content": "#ffffff",  # Contenu - BLANC
    
    # ========================================
    # 9️⃣ STYLE GÉNÉRAL DES EXPANDERS
    # ========================================
    "expander_background": "rgba(255, 255, 255, 0.05)",
    "expander_border": "rgba(255, 215, 0, 0.3)",
    
    # ========================================
    # 🔟 DROPDOWNS (Choose options)
    # ========================================
    "dropdown_text": "#000000",  # Texte - NOIR
    "dropdown_bg": "#ffffff",  # Fond - BLANC
    "dropdown_border": "#ffd700",  # Bordure - JAUNE
    
    # ========================================
    # 1️⃣1️⃣ INPUTS ET FORMULAIRES
    # ========================================
    "input_text": "#000000",
    "input_background": "#ffffff",
    "input_border": "#ffd700",
    "input_placeholder": "#666666",
    
    # ========================================
    # 1️⃣2️⃣ BOUTONS STREAMLIT (boutons jaunes en bas)
    # ========================================
    "button_text": "#1a1a2e",  # Texte - BLEU FONCÉ
    
    # ========================================
    # AUTRES
    # ========================================
    "text": "#ffffff",  # Texte général
    "text_secondary": "#e0e0e0"  # Texte secondaire
}

# ===== COULEURS DE LA PAGE PRINCIPALE =====
MAIN_COLORS = {
    "background": "#ffffff",
}

# ===== COULEURS DES CARTES =====
CARD_COLORS = {
    # AI Card
    "ai_card_bg": "linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%)",
    "ai_card_border": "#ffd700",
    "ai_card_text": "#ffffff",
    
    # Response Card
    "response_card_bg": "#f8f9fa",
    "response_card_border": "#ffd700",
    
    # Assistant Card
    "assistant_card_bg": "#ffffff",
    "assistant_card_border": "#e0e0e0",
    "assistant_card_border_hover": "#ffd700",
    
    # Prompt Card
    "prompt_card_bg": "#fffef0",
    "prompt_card_border": "#ffd700",
    
    # Feature Box
    "feature_box_bg": "#ffffff",
    "feature_box_border_hover": "#ffd700",
}

# ===== COULEURS DES BOUTONS =====
BUTTON_COLORS = {
    "bg": "linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)",
    "bg_hover": "linear-gradient(135deg, #ffed4e 0%, #ffd700 100%)",
    "text": "#1a1a2e",
    "border": "#ffd700",
}

# ===== COULEURS DES HEADERS =====
HEADER_COLORS = {
    "main_gradient": "linear-gradient(135deg, #ffd700 0%, #4169e1 100%)",
    "sub_header_text": "#555555",
}

# ===== COULEURS DES METRICS =====
METRIC_COLORS = {
    "value": "#ffd700",
}

# ===== COULEURS DU LANDING PAGE (pour compatibilité) =====
LANDING_COLORS = {
    "primary": "#ffd700",
    "secondary": "#4169e1",
    "dark": "#1a1a2e",
    "darker": "#0f3460",
    "black": "#0a0a0a",
    "white": "#ffffff",
    "gray": "#f8f9fa",
}


def get_sidebar_css():
    """Génère le CSS de la sidebar à partir des couleurs configurées"""
    return f"""
    /* === SIDEBAR - FOND BLEU FONCÉ === */
    section[data-testid="stSidebar"] {{
        background: {SIDEBAR_COLORS['background']} !important;
        color: {SIDEBAR_COLORS['text']} !important;
    }}
    
    /* Forcer le fond sur tous les conteneurs de la sidebar */
    section[data-testid="stSidebar"] > div:first-child {{
        background: {SIDEBAR_COLORS['background']} !important;
    }}
    
    /* Texte général (sauf dans les expanders) */
    section[data-testid="stSidebar"] > div > div > div .stMarkdown,
    section[data-testid="stSidebar"] > div > div > div p {{
        color: {SIDEBAR_COLORS['text']} !important;
    }}
    
    /* ========================================
       1️⃣ LIENS EN HAUT (app, agents ia, blog, etc.)
       ======================================== */
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] a span,
    section[data-testid="stSidebar"] a p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a,
    section[data-testid="stSidebar"] div a {{
        color: {SIDEBAR_COLORS['top_links_text']} !important;
        text-decoration: none !important;
        font-weight: normal !important;
    }}
    section[data-testid="stSidebar"] a:hover {{
        background: {SIDEBAR_COLORS['top_links_hover']} !important;
    }}
    
    /* ========================================
       2️⃣ TITRE PRINCIPAL (🤖 WeBox Multi-IA)
       ======================================== */
    section[data-testid="stSidebar"] h2 {{
        color: {SIDEBAR_COLORS['main_title_text']} !important;
        text-align: center !important;
        font-weight: normal !important;
    }}
    
    /* ========================================
       3️⃣ NOM UTILISATEUR (👤 Administrateur)
       ======================================== */
    section[data-testid="stSidebar"] p {{
        color: {SIDEBAR_COLORS['user_name_text']} !important;
        text-align: center !important;
        font-weight: normal !important;
        font-size: 1.1rem !important;
    }}
    
    /* ========================================
       4️⃣ SÉPARATEURS HORIZONTAUX (<hr>)
       ======================================== */
    section[data-testid="stSidebar"] hr {{
        border: 1px solid {SIDEBAR_COLORS['separator_color']} !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* ========================================
       5️⃣ SOUS-TITRES (📍 Navigation, 🤖 Sélection des IA)
       ======================================== */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h3 {{
        color: {SIDEBAR_COLORS['subtitle_text']} !important;
        font-weight: normal !important;
    }}
    
    /* ========================================
       EXPANDERS - CONFIGURATION COMPLÈTE
       Utilise l'attribut [open] pour différencier
       ======================================== */
    
    /* Style de base pour tous les expanders */
    section[data-testid="stSidebar"] details {{
        background-color: {SIDEBAR_COLORS['expander_background']} !important;
        border: 1px solid {SIDEBAR_COLORS['expander_border']} !important;
    }}
    
    /* ===== EXPANDERS FERMÉS (par défaut) ===== */
    section[data-testid="stSidebar"] details summary {{
        color: {SIDEBAR_COLORS['expander_closed_title']} !important;
        font-weight: 600 !important;
        -webkit-text-fill-color: {SIDEBAR_COLORS['expander_closed_title']} !important;
    }}
    section[data-testid="stSidebar"] details summary * {{
        color: {SIDEBAR_COLORS['expander_closed_title']} !important;
        -webkit-text-fill-color: {SIDEBAR_COLORS['expander_closed_title']} !important;
    }}
    section[data-testid="stSidebar"] details > div {{
        color: {SIDEBAR_COLORS['expander_closed_content']} !important;
    }}
    section[data-testid="stSidebar"] details > div p,
    section[data-testid="stSidebar"] details > div span,
    section[data-testid="stSidebar"] details > div label {{
        color: {SIDEBAR_COLORS['expander_closed_content']} !important;
    }}
    
    /* ===== EXPANDERS OUVERTS (Sélection IA) ===== */
    section[data-testid="stSidebar"] details[open] summary {{
        color: {SIDEBAR_COLORS['expander_open_title']} !important;
        -webkit-text-fill-color: {SIDEBAR_COLORS['expander_open_title']} !important;
    }}
    section[data-testid="stSidebar"] details[open] summary * {{
        color: {SIDEBAR_COLORS['expander_open_title']} !important;
        -webkit-text-fill-color: {SIDEBAR_COLORS['expander_open_title']} !important;
    }}
    section[data-testid="stSidebar"] details[open] > div {{
        color: {SIDEBAR_COLORS['expander_open_content']} !important;
    }}
    section[data-testid="stSidebar"] details[open] > div p,
    section[data-testid="stSidebar"] details[open] > div span,
    section[data-testid="stSidebar"] details[open] > div label {{
        color: {SIDEBAR_COLORS['expander_open_content']} !important;
    }}
    
    /* ===== DROPDOWNS DANS LES EXPANDERS ===== */
    section[data-testid="stSidebar"] details select {{
        color: {SIDEBAR_COLORS['dropdown_text']} !important;
        background-color: {SIDEBAR_COLORS['dropdown_bg']} !important;
        border: 1px solid {SIDEBAR_COLORS['dropdown_border']} !important;
    }}
    section[data-testid="stSidebar"] details .stSelectbox {{
        color: {SIDEBAR_COLORS['dropdown_text']} !important;
    }}
    section[data-testid="stSidebar"] details .stSelectbox > div {{
        color: {SIDEBAR_COLORS['dropdown_text']} !important;
        background-color: {SIDEBAR_COLORS['dropdown_bg']} !important;
    }}
    
    /* === BOUTONS RADIO DE NAVIGATION === */
    section[data-testid="stSidebar"] .stRadio label {{
        color: {SIDEBAR_COLORS['radio_text']} !important;
        font-weight: normal !important;
        font-size: 1.05rem !important;
        padding: 0.8rem 1rem !important;
        border-radius: 10px !important;
        transition: all 0.3s !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio label span {{
        color: {SIDEBAR_COLORS['radio_text']} !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio label:hover {{
        background: {SIDEBAR_COLORS['radio_hover_bg']} !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        color: {SIDEBAR_COLORS['radio_text']} !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {{
        color: {SIDEBAR_COLORS['radio_text']} !important;
    }}
    
    /* === INPUTS ET FORMULAIRES (priorité maximale) === */
    section[data-testid="stSidebar"] input[type="text"],
    section[data-testid="stSidebar"] input[type="search"],
    section[data-testid="stSidebar"] input[type="number"],
    section[data-testid="stSidebar"] input[type="email"],
    section[data-testid="stSidebar"] input[type="password"],
    section[data-testid="stSidebar"] input {{
        color: {SIDEBAR_COLORS['input_text']} !important;
        background-color: {SIDEBAR_COLORS['input_background']} !important;
        border: 1px solid {SIDEBAR_COLORS['input_border']} !important;
        -webkit-text-fill-color: {SIDEBAR_COLORS['input_text']} !important;
    }}
    
    section[data-testid="stSidebar"] textarea {{
        color: {SIDEBAR_COLORS['input_text']} !important;
        background-color: {SIDEBAR_COLORS['input_background']} !important;
        border: 1px solid {SIDEBAR_COLORS['input_border']} !important;
    }}
    
    section[data-testid="stSidebar"] select {{
        color: {SIDEBAR_COLORS['input_text']} !important;
        background-color: {SIDEBAR_COLORS['input_background']} !important;
        border: 1px solid {SIDEBAR_COLORS['input_border']} !important;
    }}
    
    /* Placeholders */
    section[data-testid="stSidebar"] input::placeholder,
    section[data-testid="stSidebar"] textarea::placeholder {{
        color: {SIDEBAR_COLORS['input_placeholder']} !important;
        opacity: 0.7 !important;
    }}
    
    /* ========================================
       1️⃣2️⃣ BOUTONS STREAMLIT (➕ Nouvelle conversation, 🚪 Déconnexion)
       ======================================== */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] .stButton > button,
    section[data-testid="stSidebar"] .stButton button {{
        color: {SIDEBAR_COLORS['button_text']} !important;
        font-weight: normal !important;
    }}
    
    section[data-testid="stSidebar"] button p,
    section[data-testid="stSidebar"] button span,
    section[data-testid="stSidebar"] button div,
    section[data-testid="stSidebar"] .stButton button p,
    section[data-testid="stSidebar"] .stButton button span,
    section[data-testid="stSidebar"] .stButton button div {{
        color: {SIDEBAR_COLORS['button_text']} !important;
        font-weight: normal !important;
    }}
    """
