"""Page de documentation interne"""
import streamlit as st


def show_documentation():
    """Affiche la page de documentation"""
    
    st.title("📖 Documentation WeBox Multi-IA")
    
    st.markdown("---")
    
    # Introduction
    st.header("🎯 Introduction")
    st.markdown("""
    Bienvenue dans la documentation de **WeBox Multi-IA**, votre interface complète d'automatisation IA.
    
    Cette plateforme vous permet d'accéder à plus de 50 APIs d'intelligence artificielle, 
    8 agents spécialisés, un assistant vocal et des outils de génération multi-média.
    """)
    
    # Démarrage rapide
    st.header("🚀 Démarrage Rapide")
    st.markdown("""
    ### 1. Créer un compte
    - Cliquez sur **"Inscription"** sur la page d'accueil
    - Remplissez vos informations
    - Validez votre compte
    
    ### 2. Se connecter
    - Utilisez vos identifiants pour vous connecter
    - Accédez au tableau de bord principal
    
    ### 3. Commencer à utiliser
    - Explorez les différents modules dans la barre latérale
    - Testez les agents IA
    - Générez du contenu multi-média
    """)
    
    # Fonctionnalités
    st.header("✨ Fonctionnalités Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Agents IA")
        st.markdown("""
        - **Agent Ventes** : Prospection et closing
        - **Agent Marketing** : Stratégie et contenu
        - **Agent Finance** : Analyse et budget
        - **Agent RH** : Recrutement et formation
        - **Agent Service Client** : Support 24/7
        - **Agent Produit** : Roadmap et UX
        - **Agent Opérations** : Optimisation
        - **Agent Stratégie** : Vision et planning
        """)
        
        st.subheader("💬 Chat Multi-IA")
        st.markdown("""
        - GPT-4 & GPT-3.5 (OpenAI)
        - Claude 3 (Anthropic)
        - Gemini Pro (Google)
        - Mistral, Cohere, Perplexity
        - DeepSeek, Groq, Together AI
        """)
    
    with col2:
        st.subheader("🎨 Génération Multi-Média")
        st.markdown("""
        - **Images** : DALL-E, Stable Diffusion, Midjourney
        - **Vidéos** : Runway, Pika, Luma AI
        - **Audio** : ElevenLabs, OpenAI TTS
        - **Musique** : Suno, Udio
        """)
        
        st.subheader("📞 Assistant Vocal")
        st.markdown("""
        - Appels sortants/entrants (Twilio)
        - Reconnaissance vocale (Google STT)
        - 10 voix françaises (Google TTS)
        - Conversation IA (GPT-4)
        - Historique complet des appels
        """)
    
    # Support
    st.header("💡 Support")
    st.markdown("""
    Besoin d'aide ? Contactez-nous :
    - 📧 Email : support@webox.com
    - 💬 Chat en direct (disponible après connexion)
    - 📚 Base de connaissances (en construction)
    """)
    
    # Retour
    st.markdown("---")
    if st.button("← Retour à l'accueil", use_container_width=True):
        st.session_state.page = "landing"
        st.query_params.clear()
        st.rerun()
