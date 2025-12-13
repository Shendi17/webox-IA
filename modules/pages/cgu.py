"""Page des Conditions Générales d'Utilisation"""
import streamlit as st


def show_cgu():
    """Affiche les Conditions Générales d'Utilisation"""
    
    st.title("📜 Conditions Générales d'Utilisation")
    
    st.markdown("---")
    
    st.info("**Dernière mise à jour :** 28 octobre 2025")
    
    # Article 1
    st.header("1. Objet")
    st.markdown("""
    Les présentes Conditions Générales d'Utilisation (CGU) ont pour objet de définir les modalités 
    et conditions dans lesquelles WeBox Multi-IA met à disposition ses services.
    
    L'utilisation de la plateforme implique l'acceptation pleine et entière des présentes CGU.
    """)
    
    # Article 2
    st.header("2. Accès aux Services")
    st.markdown("""
    ### 2.1 Inscription
    - L'accès aux services nécessite la création d'un compte utilisateur
    - Les informations fournies doivent être exactes et à jour
    - Chaque utilisateur est responsable de la confidentialité de ses identifiants
    
    ### 2.2 Conditions d'accès
    - Être âgé d'au moins 18 ans
    - Accepter les présentes CGU
    - Fournir des informations exactes lors de l'inscription
    """)
    
    # Article 3
    st.header("3. Services Proposés")
    st.markdown("""
    WeBox Multi-IA propose :
    - Accès à 50+ APIs d'intelligence artificielle
    - 8 agents IA spécialisés
    - Chat multi-IA avec 12+ modèles
    - Assistant vocal IA
    - Génération multi-média (images, vidéos, audio, musique)
    
    Les services peuvent évoluer et être modifiés sans préavis.
    """)
    
    # Article 4
    st.header("4. Obligations de l'Utilisateur")
    st.markdown("""
    L'utilisateur s'engage à :
    - Utiliser les services de manière conforme à leur destination
    - Ne pas porter atteinte aux droits de tiers
    - Ne pas utiliser les services à des fins illégales
    - Ne pas tenter de contourner les mesures de sécurité
    - Respecter les droits de propriété intellectuelle
    """)
    
    # Article 5
    st.header("5. Propriété Intellectuelle")
    st.markdown("""
    ### 5.1 Contenu de la plateforme
    - Tous les éléments de la plateforme sont protégés par le droit d'auteur
    - Toute reproduction non autorisée est interdite
    
    ### 5.2 Contenu généré par l'utilisateur
    - L'utilisateur conserve les droits sur le contenu qu'il génère
    - WeBox Multi-IA se réserve le droit d'utiliser ce contenu à des fins d'amélioration des services
    """)
    
    # Article 6
    st.header("6. Responsabilité")
    st.markdown("""
    ### 6.1 Limitation de responsabilité
    - WeBox Multi-IA ne garantit pas l'absence d'interruption des services
    - La responsabilité est limitée au montant payé par l'utilisateur
    
    ### 6.2 Force majeure
    - WeBox Multi-IA ne peut être tenu responsable en cas de force majeure
    """)
    
    # Article 7
    st.header("7. Données Personnelles")
    st.markdown("""
    Le traitement des données personnelles est régi par notre 
    [Politique de Confidentialité](#).
    
    Conformément au RGPD, vous disposez d'un droit d'accès, de rectification 
    et de suppression de vos données.
    """)
    
    # Article 8
    st.header("8. Résiliation")
    st.markdown("""
    ### 8.1 Par l'utilisateur
    - L'utilisateur peut résilier son compte à tout moment
    - La résiliation prend effet immédiatement
    
    ### 8.2 Par WeBox Multi-IA
    - En cas de non-respect des CGU
    - En cas d'utilisation frauduleuse
    - Avec un préavis de 30 jours sans motif
    """)
    
    # Article 9
    st.header("9. Modification des CGU")
    st.markdown("""
    WeBox Multi-IA se réserve le droit de modifier les présentes CGU à tout moment.
    
    Les utilisateurs seront informés par email des modifications importantes.
    """)
    
    # Article 10
    st.header("10. Droit Applicable")
    st.markdown("""
    Les présentes CGU sont soumises au droit français.
    
    En cas de litige, les tribunaux français seront seuls compétents.
    """)
    
    # Contact
    st.markdown("---")
    st.info("""
    **Questions sur les CGU ?**
    
    Contactez-nous à : legal@webox.com
    """)
    
    # Retour
    st.markdown("---")
    if st.button("← Retour à l'accueil", use_container_width=True):
        st.session_state.page = "landing"
        st.query_params.clear()
        st.rerun()
