// ============================================
// FONCTIONNALITÉS INTERACTIVES - WEBOX
// ============================================

console.log('✅ Fonctionnalités WeBox chargées');

// ============================================
// AUTOMATION - PIPEDREAM
// ============================================

function connecterPipedream() {
    console.log('Connexion à Pipedream...');
    
    Modal.show('🔗 Connexion à Pipedream', `
        <p style="margin-bottom: 1rem;">Connectez votre compte Pipedream pour créer des workflows d'automatisation puissants.</p>
        <div class="form-group">
            <label class="form-label">Clé API Pipedream</label>
            <input type="password" class="form-input" placeholder="pd_xxx..." id="pipedreamKey">
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Connecter', 
            class: 'btn-primary',
            action: 'connect',
            callback: () => {
                Modal.loading('Connexion en cours...');
                simulateLoading(() => {
                    Modal.close();
                    Toast.success('Compte Pipedream connecté avec succès !');
                }, 1500);
            }
        }
    ]);
}

function utiliserTemplate(nom) {
    console.log('Utilisation du template:', nom);
    
    Modal.confirm(
        '✨ Utiliser ce template',
        `Voulez-vous ajouter le template "${nom}" à vos workflows ?`,
        () => {
            Modal.loading('Création du workflow...');
            simulateLoading(() => {
                Modal.close();
                Toast.success(`Workflow "${nom}" créé avec succès !`);
            }, 1500);
        }
    );
}

function editerWorkflow(id) {
    console.log('Édition du workflow:', id);
    Toast.info(`Ouverture de l'éditeur pour le workflow #${id}...`);
    // Simulation de redirection
    setTimeout(() => {
        Toast.success('Éditeur de workflow prêt !');
    }, 1000);
}

function creerWorkflow() {
    console.log('Création d\'un nouveau workflow');
    
    Modal.show('➕ Nouveau Workflow', `
        <div class="form-group">
            <label class="form-label">Nom du workflow</label>
            <input type="text" class="form-input" placeholder="Mon workflow..." id="workflowName">
        </div>
        <div class="form-group">
            <label class="form-label">Description</label>
            <textarea class="form-textarea" placeholder="Description..." id="workflowDesc"></textarea>
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Créer', 
            class: 'btn-primary',
            callback: () => {
                const name = document.getElementById('workflowName').value;
                if (name) {
                    Modal.loading('Création du workflow...');
                    simulateLoading(() => {
                        Modal.close();
                        Toast.success(`Workflow "${name}" créé !`);
                    }, 1500);
                }
            }
        }
    ]);
}

// ============================================
// CATALOG - OUTILS IA
// ============================================

function utiliserOutil(nom) {
    console.log('Utilisation de l\'outil:', nom);
    
    Modal.show(`🔧 ${nom}`, `
        <p style="margin-bottom: 1rem;">Configurer et utiliser ${nom}</p>
        <div class="form-group">
            <label class="form-label">Prompt / Instructions</label>
            <textarea class="form-textarea" placeholder="Entrez vos instructions..." id="outilPrompt"></textarea>
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Lancer', 
            class: 'btn-primary',
            callback: () => {
                Modal.loading(`Lancement de ${nom}...`);
                simulateLoading(() => {
                    Modal.close();
                    Toast.success(`${nom} lancé avec succès !`);
                }, 2000);
            }
        }
    ]);
}

function rechercherOutils() {
    const query = document.getElementById('searchTools')?.value;
    console.log('Recherche d\'outils:', query);
    if (query) {
        Toast.info(`Recherche de "${query}" dans le catalogue...`);
        setTimeout(() => {
            Toast.success(`${Math.floor(Math.random() * 10) + 1} outils trouvés pour "${query}"`);
        }, 1000);
    } else {
        Toast.warning('Veuillez entrer un terme de recherche');
    }
}

// ============================================
// COLLABORATION
// ============================================

function inviterMembre() {
    console.log('Invitation d\'un membre');
    
    Modal.show('📧 Inviter un membre', `
        <div class="form-group">
            <label class="form-label">Adresse email</label>
            <input type="email" class="form-input" placeholder="email@exemple.com" id="membreEmail">
        </div>
        <div class="form-group">
            <label class="form-label">Rôle</label>
            <select class="form-select" id="membreRole">
                <option>Membre</option>
                <option>Admin</option>
                <option>Invité</option>
            </select>
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Envoyer l\'invitation', 
            class: 'btn-primary',
            callback: () => {
                const email = document.getElementById('membreEmail').value;
                if (email) {
                    Modal.loading('Envoi de l\'invitation...');
                    simulateLoading(() => {
                        Modal.close();
                        Toast.success(`Invitation envoyée à ${email} !`);
                    }, 1500);
                }
            }
        }
    ]);
}

function envoyerMessage(membre) {
    console.log('Envoi de message à:', membre);
    
    Modal.show(`💬 Message à ${membre}`, `
        <div class="form-group">
            <label class="form-label">Votre message</label>
            <textarea class="form-textarea" placeholder="Écrivez votre message..." id="messageTexte"></textarea>
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Envoyer', 
            class: 'btn-primary',
            callback: () => {
                Modal.loading('Envoi du message...');
                simulateLoading(() => {
                    Modal.close();
                    Toast.success(`Message envoyé à ${membre} !`);
                }, 1000);
            }
        }
    ]);
}

function ouvrirProjet(nom) {
    console.log('Ouverture du projet:', nom);
    Toast.info(`Ouverture du projet "${nom}"...`);
    setTimeout(() => {
        Toast.success(`Projet "${nom}" ouvert !`);
    }, 1000);
}

function nouveauProjet() {
    console.log('Création d\'un nouveau projet');
    
    Modal.show('📁 Nouveau Projet', `
        <div class="form-group">
            <label class="form-label">Nom du projet</label>
            <input type="text" class="form-input" placeholder="Mon projet..." id="projetNom">
        </div>
        <div class="form-group">
            <label class="form-label">Description</label>
            <textarea class="form-textarea" placeholder="Description..." id="projetDesc"></textarea>
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Créer', 
            class: 'btn-primary',
            callback: () => {
                const nom = document.getElementById('projetNom').value;
                if (nom) {
                    Modal.loading('Création du projet...');
                    simulateLoading(() => {
                        Modal.close();
                        Toast.success(`Projet "${nom}" créé !`);
                    }, 1500);
                }
            }
        }
    ]);
}

// ============================================
// BLOG
// ============================================

function lireArticle(titre) {
    console.log('Lecture de l\'article:', titre);
    Toast.info(`Ouverture de l'article "${titre}"...`);
    setTimeout(() => {
        Toast.success('Article chargé !');
    }, 1000);
}

function filtrerArticles(categorie) {
    console.log('Filtrage par catégorie:', categorie);
    Toast.info(`Filtrage: ${categorie}`);
    setTimeout(() => {
        const nb = Math.floor(Math.random() * 20) + 5;
        Toast.success(`${nb} articles trouvés dans "${categorie}"`);
    }, 800);
}

function sAbonnerNewsletter() {
    const email = document.getElementById('newsletterEmail')?.value;
    if (email) {
        console.log('Abonnement newsletter:', email);
        Modal.loading('Inscription en cours...');
        simulateLoading(() => {
            Modal.close();
            Toast.success(`Bienvenue ! ${email} est abonné à la newsletter.`);
            document.getElementById('newsletterEmail').value = '';
        }, 1500);
    } else {
        Toast.warning('Veuillez entrer votre adresse email');
    }
}

// ============================================
// MEDIA - GESTIONNAIRE
// ============================================

function choisirFichiers() {
    console.log('Sélection de fichiers');
    Toast.info('Ouverture du sélecteur de fichiers...');
    setTimeout(() => {
        const nb = Math.floor(Math.random() * 5) + 1;
        Toast.success(`${nb} fichier(s) sélectionné(s) ! Upload en cours...`);
        setTimeout(() => {
            Toast.success('Fichiers uploadés avec succès !');
        }, 2000);
    }, 1000);
}

function filtrerMedia(type) {
    console.log('Filtrage des médias:', type);
    Toast.info(`Affichage: ${type}`);
    setTimeout(() => {
        const nb = Math.floor(Math.random() * 50) + 10;
        Toast.success(`${nb} fichiers ${type} affichés`);
    }, 500);
}

function changerVue(vue) {
    console.log('Changement de vue:', vue);
    Toast.success(`Vue changée: ${vue}`);
}

function ouvrirDossier(nom) {
    console.log('Ouverture du dossier:', nom);
    Toast.info(`Ouverture du dossier "${nom}"...`);
    setTimeout(() => {
        Toast.success(`Dossier "${nom}" ouvert !`);
    }, 800);
}

function nouveauDossier() {
    Modal.show('📁 Nouveau Dossier', `
        <div class="form-group">
            <label class="form-label">Nom du dossier</label>
            <input type="text" class="form-input" placeholder="Mon dossier..." id="dossierNom">
        </div>
    `, [
        { text: 'Annuler', class: 'btn-secondary' },
        { 
            text: 'Créer', 
            class: 'btn-primary',
            callback: () => {
                const nom = document.getElementById('dossierNom').value;
                if (nom) {
                    Modal.close();
                    Toast.success(`Dossier "${nom}" créé !`);
                }
            }
        }
    ]);
}

function telechargerFichier(nom) {
    console.log('Téléchargement du fichier:', nom);
    Toast.info(`Téléchargement de "${nom}"...`);
    setTimeout(() => {
        Toast.success(`"${nom}" téléchargé !`);
    }, 2000);
}

// ============================================
// VOICE - ASSISTANT VOCAL
// ============================================

function sauvegarderConfigVoice() {
    console.log('Sauvegarde de la configuration vocale');
    Modal.loading('Sauvegarde de la configuration...');
    simulateLoading(() => {
        Modal.close();
        Toast.success('Configuration vocale sauvegardée !');
    }, 1000);
}

function voirAppel(id) {
    console.log('Affichage de l\'appel:', id);
    Toast.info(`Chargement des détails de l'appel #${id}...`);
    setTimeout(() => {
        Toast.success('Détails de l\'appel chargés !');
    }, 1000);
}

// ============================================
// PROFILE
// ============================================

function sauvegarderProfil() {
    console.log('Sauvegarde du profil');
    Modal.loading('Sauvegarde du profil...');
    simulateLoading(() => {
        Modal.close();
        Toast.success('Profil mis à jour avec succès !');
    }, 1500);
}

function sauvegarderCles() {
    console.log('Sauvegarde des clés API');
    Modal.loading('Sauvegarde sécurisée des clés API...');
    simulateLoading(() => {
        Modal.close();
        Toast.success('Clés API sauvegardées de manière sécurisée !');
    }, 1500);
}

// ============================================
// INITIALISATION AU CHARGEMENT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initialisation des fonctionnalités...');
    
    // Ajouter les événements sur les boutons existants
    initBoutons();
});

function initBoutons() {
    // Cette fonction peut être étendue pour ajouter automatiquement
    // des événements aux boutons sans onclick
    console.log('✅ Boutons initialisés');
}
