"""Page de contact"""
import streamlit as st


def show_contact():
    """Affiche la page de contact"""
    
    st.title("📧 Contactez-nous")
    
    st.markdown("---")
    
    st.markdown("""
    Vous avez une question, une suggestion ou besoin d'aide ? 
    N'hésitez pas à nous contacter via le formulaire ci-dessous.
    """)
    
    # Formulaire de contact
    with st.form("contact_form"):
        st.subheader("📝 Formulaire de Contact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Nom complet *", placeholder="Jean Dupont")
            email = st.text_input("📧 Email *", placeholder="votre@email.com")
        
        with col2:
            phone = st.text_input("📱 Téléphone", placeholder="+33 6 12 34 56 78")
            subject = st.selectbox("📋 Sujet *", [
                "Question générale",
                "Support technique",
                "Demande de fonctionnalité",
                "Problème de facturation",
                "Partenariat",
                "Autre"
            ])
        
        message = st.text_area("💬 Message *", placeholder="Décrivez votre demande...", height=200)
        
        submit = st.form_submit_button("📤 Envoyer le message", use_container_width=True)
        
        if submit:
            if not name or not email or not message:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                st.success("✅ Message envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.")
                st.balloons()
    
    # Informations de contact
    st.markdown("---")
    st.header("📞 Autres Moyens de Contact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📧 Email
        **support@webox.com**
        
        Réponse sous 24h
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Chat en Direct
        **Disponible 24/7**
        
        (Après connexion)
        """)
    
    with col3:
        st.markdown("""
        ### 📱 Téléphone
        **+33 1 23 45 67 89**
        
        Lun-Ven : 9h-18h
        """)
    
    # FAQ
    st.markdown("---")
    st.header("❓ Questions Fréquentes")
    
    with st.expander("💰 Quels sont les tarifs ?"):
        st.markdown("""
        Nous proposons plusieurs formules adaptées à vos besoins :
        - **Gratuit** : Accès limité aux fonctionnalités de base
        - **Pro** : 49€/mois - Accès complet
        - **Entreprise** : Sur devis - Solutions personnalisées
        """)
    
    with st.expander("🔒 Mes données sont-elles sécurisées ?"):
        st.markdown("""
        Oui, absolument ! Nous utilisons :
        - Chiffrement SSL/TLS
        - Stockage sécurisé
        - Conformité RGPD
        - Sauvegardes quotidiennes
        """)
    
    with st.expander("🤝 Proposez-vous des partenariats ?"):
        st.markdown("""
        Oui, nous sommes ouverts aux partenariats stratégiques.
        Contactez-nous à **partnerships@webox.com** pour en discuter.
        """)
    
    # Retour
    st.markdown("---")
    if st.button("← Retour à l'accueil", use_container_width=True):
        st.session_state.page = "landing"
        st.query_params.clear()
        st.rerun()
