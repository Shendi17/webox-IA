// Script agents - Chargé en priorité
console.log('✅ agents.js chargé');

// Variables globales
let currentAgentType = null;

const agentToAssistant = {
    'ventes': 'coach',
    'marketing': 'creatif',
    'finance': 'analyste',
    'operations': 'analyste',
    'rh': 'coach',
    'service-client': 'coach',
    'produit': 'creatif',
    'strategie': 'analyste'
};

const agentNames = {
    'ventes': 'Agent Ventes',
    'marketing': 'Agent Marketing',
    'finance': 'Agent Finance',
    'operations': 'Agent Opérations',
    'rh': 'Agent RH',
    'service-client': 'Agent Service Client',
    'produit': 'Agent Produit',
    'strategie': 'Agent Stratégie'
};

// Fonction pour ouvrir la modal
window.openAgentModal = function(type) {
    console.log('🚀 openAgentModal appelée:', type);
    
    currentAgentType = type;
    const agentName = agentNames[type] || 'Agent';
    
    const modal = document.getElementById('agentModal');
    if (!modal) {
        console.error('❌ Modal non trouvée');
        return;
    }
    
    // Mettre à jour le titre
    const title = document.getElementById('agentModalTitle');
    if (title) title.textContent = `🤖 ${agentName}`;
    
    // Message de bienvenue
    const messages = document.getElementById('agentMessages');
    if (messages) {
        messages.innerHTML = `
            <div style="text-align: center; color: #888; padding: 2rem;">
                Bonjour ! Je suis votre ${agentName}. Comment puis-je vous aider ?
            </div>
        `;
    }
    
    // Afficher la modal
    modal.classList.add('active');
    console.log('✅ Modal ouverte');
    
    // Focus sur l'input
    setTimeout(() => {
        const input = document.getElementById('agentInput');
        if (input) input.focus();
    }, 100);
};

// Fonction pour fermer la modal
window.closeAgentModal = function() {
    console.log('🚪 closeAgentModal appelée');
    const modal = document.getElementById('agentModal');
    if (modal) {
        modal.classList.remove('active');
    }
    currentAgentType = null;
};

// Les onclick inline fonctionnent déjà, pas besoin d'attacher des événements
console.log('✅ agents.js chargé - onclick inline actifs');
