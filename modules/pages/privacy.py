"""Page de Politique de Confidentialité"""
import streamlit as st


def show_privacy():
    """Affiche la Politique de Confidentialité"""
    
    st.title("🔒 Politique de Confidentialité")
    
    st.markdown("---")
    
    st.info("**Dernière mise à jour :** 28 octobre 2025")
    
    # Introduction
    st.header("Introduction")
    st.markdown("""
    WeBox Multi-IA s'engage à protéger la confidentialité et la sécurité de vos données personnelles.
    
    Cette politique explique comment nous collectons, utilisons et protégeons vos informations 
    conformément au Règlement Général sur la Protection des Données (RGPD).
    """)
    
    # Article 1
    st.header("1. Données Collectées")
    st.markdown("""
    ### 1.1 Données d'identification
    - Nom et prénom
    - Adresse email
    - Numéro de téléphone (optionnel)
    
    ### 1.2 Données de connexion
    - Adresse IP
    - Type de navigateur
    - Système d'exploitation
    - Pages visitées
    - Date et heure de connexion
    
    ### 1.3 Données d'utilisation
    - Historique des requêtes IA
    - Contenu généré
    - Préférences utilisateur
    - Statistiques d'utilisation
    """)
    
    # Article 2
    st.header("2. Finalités du Traitement")
    st.markdown("""
    Vos données sont collectées pour :
    - **Gestion du compte** : Création et administration de votre compte
    - **Fourniture des services** : Accès aux fonctionnalités de la plateforme
    - **Amélioration des services** : Analyse et optimisation de nos services
    - **Communication** : Envoi d'informations importantes et newsletters
    - **Sécurité** : Prévention de la fraude et des abus
    - **Conformité légale** : Respect de nos obligations légales
    """)
    
    # Article 3
    st.header("3. Base Légale du Traitement")
    st.markdown("""
    Le traitement de vos données repose sur :
    - **Consentement** : Pour les newsletters et communications marketing
    - **Exécution du contrat** : Pour la fourniture des services
    - **Intérêt légitime** : Pour l'amélioration des services et la sécurité
    - **Obligation légale** : Pour la conformité réglementaire
    """)
    
    # Article 4
    st.header("4. Partage des Données")
    st.markdown("""
    ### 4.1 Partenaires techniques
    Nous partageons vos données avec :
    - **Fournisseurs d'IA** : OpenAI, Anthropic, Google (pour les services IA)
    - **Hébergement** : Serveurs sécurisés en Europe
    - **Paiement** : Processeurs de paiement sécurisés
    
    ### 4.2 Aucune vente de données
    Nous ne vendons jamais vos données personnelles à des tiers.
    
    ### 4.3 Transferts internationaux
    Certains partenaires peuvent être situés hors de l'UE. 
    Dans ce cas, nous garantissons un niveau de protection adéquat.
    """)
    
    # Article 5
    st.header("5. Durée de Conservation")
    st.markdown("""
    - **Compte actif** : Pendant toute la durée d'utilisation du service
    - **Compte inactif** : 3 ans après la dernière connexion
    - **Données de facturation** : 10 ans (obligation légale)
    - **Logs de connexion** : 12 mois
    
    Après ces délais, vos données sont supprimées ou anonymisées.
    """)
    
    # Article 6
    st.header("6. Sécurité des Données")
    st.markdown("""
    Nous mettons en œuvre des mesures de sécurité appropriées :
    
    ### 6.1 Mesures techniques
    - Chiffrement SSL/TLS pour toutes les communications
    - Chiffrement des données sensibles en base de données
    - Pare-feu et systèmes de détection d'intrusion
    - Sauvegardes quotidiennes chiffrées
    
    ### 6.2 Mesures organisationnelles
    - Accès restreint aux données personnelles
    - Formation du personnel à la protection des données
    - Audits de sécurité réguliers
    - Plan de réponse aux incidents
    """)
    
    # Article 7
    st.header("7. Vos Droits")
    st.markdown("""
    Conformément au RGPD, vous disposez des droits suivants :
    
    ### 7.1 Droit d'accès
    Vous pouvez demander une copie de vos données personnelles.
    
    ### 7.2 Droit de rectification
    Vous pouvez corriger vos données inexactes ou incomplètes.
    
    ### 7.3 Droit à l'effacement
    Vous pouvez demander la suppression de vos données.
    
    ### 7.4 Droit à la portabilité
    Vous pouvez récupérer vos données dans un format structuré.
    
    ### 7.5 Droit d'opposition
    Vous pouvez vous opposer au traitement de vos données.
    
    ### 7.6 Droit de limitation
    Vous pouvez demander la limitation du traitement.
    
    **Pour exercer vos droits :** privacy@webox.com
    """)
    
    # Article 8
    st.header("8. Cookies")
    st.markdown("""
    ### 8.1 Types de cookies utilisés
    - **Cookies essentiels** : Nécessaires au fonctionnement du site
    - **Cookies de performance** : Analyse de l'utilisation
    - **Cookies de préférence** : Mémorisation de vos choix
    
    ### 8.2 Gestion des cookies
    Vous pouvez gérer vos préférences de cookies dans les paramètres de votre navigateur.
    """)
    
    # Article 9
    st.header("9. Modifications de la Politique")
    st.markdown("""
    Nous pouvons modifier cette politique de confidentialité à tout moment.
    
    Les modifications importantes vous seront notifiées par email.
    
    La version en vigueur est toujours disponible sur cette page.
    """)
    
    # Article 10
    st.header("10. Contact")
    st.markdown("""
    ### Délégué à la Protection des Données (DPO)
    - **Email** : dpo@webox.com
    - **Adresse** : WeBox Multi-IA, 123 Rue de l'Innovation, 75001 Paris, France
    
    ### Autorité de contrôle
    Vous avez le droit de déposer une plainte auprès de la CNIL :
    - **Site web** : www.cnil.fr
    - **Téléphone** : 01 53 73 22 22
    """)
    
    # Consentement
    st.markdown("---")
    st.success("""
    ✅ **Votre Consentement**
    
    En utilisant WeBox Multi-IA, vous acceptez la présente politique de confidentialité.
    """)
    
    # Retour
    st.markdown("---")
    if st.button("← Retour à l'accueil", use_container_width=True):
        st.session_state.page = "landing"
        st.query_params.clear()
        st.rerun()
