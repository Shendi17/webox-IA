/**
 * Widget Agent IA 24/7
 * Widget de chat flottant avec IA
 */

class AIAgentWidget {
    constructor() {
        this.isOpen = false;
        this.sessionId = this.getOrCreateSessionId();
        this.messages = [];
        this.currentModel = 'gemini-2.0-flash';
        this.init();
    }

    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('ai_agent_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Math.random().toString(36).substr(2, 16);
            localStorage.setItem('ai_agent_session_id', sessionId);
        }
        return sessionId;
    }

    init() {
        this.createWidget();
        this.loadQuickActions();
        this.setupEventListeners();
    }

    createWidget() {
        const widgetHTML = `
            <!-- Widget Button -->
            <div class="ai-agent-button" id="aiAgentButton">
                <span class="agent-icon">🤖</span>
                <span class="agent-badge" id="agentBadge" style="display: none;">1</span>
            </div>

            <!-- Widget Panel -->
            <div class="ai-agent-panel" id="aiAgentPanel">
                <div class="agent-header">
                    <div class="agent-header-left">
                        <span class="agent-avatar">🤖</span>
                        <div class="agent-info">
                            <div class="agent-name">Assistant IA</div>
                            <div class="agent-status">🟢 En ligne 24/7</div>
                        </div>
                    </div>
                    <div class="agent-header-right">
                        <button class="agent-btn" onclick="aiAgent.clearChat()" title="Nouvelle conversation">
                            🔄
                        </button>
                        <button class="agent-btn" onclick="aiAgent.toggleWidget()" title="Fermer">
                            ✖️
                        </button>
                    </div>
                </div>

                <div class="agent-quick-actions" id="agentQuickActions">
                    <!-- Quick actions will be loaded here -->
                </div>

                <div class="agent-messages" id="agentMessages">
                    <div class="agent-welcome">
                        <div class="welcome-icon">👋</div>
                        <h3>Bonjour ! Je suis votre assistant IA</h3>
                        <p>Je suis là pour vous aider 24/7. Posez-moi vos questions !</p>
                    </div>
                </div>

                <div class="agent-input-container">
                    <div class="agent-model-selector">
                        <select id="agentModelSelect" onchange="aiAgent.changeModel(this.value)">
                            <option value="gemini-2.0-flash">⚡ Gemini 2.0 (Gratuit)</option>
                            <option value="gpt-4o-mini">🤖 GPT-4o Mini</option>
                            <option value="gpt-4o">🚀 GPT-4o</option>
                        </select>
                    </div>
                    <div class="agent-input-wrapper">
                        <textarea 
                            id="agentInput" 
                            placeholder="Posez votre question..." 
                            rows="1"
                            onkeydown="aiAgent.handleKeyPress(event)"
                        ></textarea>
                        <button class="agent-send-btn" onclick="aiAgent.sendMessage()">
                            <span id="sendIcon">📤</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    setupEventListeners() {
        document.getElementById('aiAgentButton').addEventListener('click', () => {
            this.toggleWidget();
        });

        // Auto-resize textarea
        const textarea = document.getElementById('agentInput');
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }

    async loadQuickActions() {
        try {
            const response = await fetch('/api/agent/quick-actions');
            const data = await response.json();

            if (data.success) {
                const container = document.getElementById('agentQuickActions');
                container.innerHTML = data.actions.map(action => `
                    <button class="quick-action-btn" onclick="aiAgent.useQuickAction('${action.prompt}')">
                        <span class="action-icon">${action.icon}</span>
                        <span class="action-title">${action.title}</span>
                    </button>
                `).join('');
            }
        } catch (error) {
            console.error('Erreur:', error);
        }
    }

    toggleWidget() {
        this.isOpen = !this.isOpen;
        const panel = document.getElementById('aiAgentPanel');
        const button = document.getElementById('aiAgentButton');

        if (this.isOpen) {
            panel.classList.add('open');
            button.classList.add('hidden');
            document.getElementById('agentInput').focus();
        } else {
            panel.classList.remove('open');
            button.classList.remove('hidden');
        }
    }

    changeModel(model) {
        this.currentModel = model;
        console.log('Modèle changé:', model);
    }

    useQuickAction(prompt) {
        document.getElementById('agentInput').value = prompt;
        document.getElementById('agentInput').focus();
    }

    handleKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    async sendMessage() {
        const input = document.getElementById('agentInput');
        const message = input.value.trim();

        if (!message) return;

        // Clear input
        input.value = '';
        input.style.height = 'auto';

        // Hide quick actions after first message
        document.getElementById('agentQuickActions').style.display = 'none';

        // Add user message
        this.addMessage('user', message);

        // Show loading
        const loadingId = this.addMessage('assistant', '...', true);

        try {
            const response = await fetch('/api/agent/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    model: this.currentModel
                })
            });

            const data = await response.json();

            // Remove loading
            document.getElementById(loadingId)?.remove();

            if (data.success) {
                this.addMessage('assistant', data.message.content);
            } else {
                this.addMessage('assistant', '❌ Erreur: ' + (data.error || 'Erreur inconnue'));
            }
        } catch (error) {
            document.getElementById(loadingId)?.remove();
            this.addMessage('assistant', '❌ Erreur de connexion');
            console.error('Erreur:', error);
        }
    }

    addMessage(role, content, isLoading = false) {
        const messagesContainer = document.getElementById('agentMessages');
        const messageId = 'msg_' + Date.now();

        const messageHTML = `
            <div class="agent-message ${role}" id="${messageId}">
                <div class="message-avatar">${role === 'user' ? '👤' : '🤖'}</div>
                <div class="message-content ${isLoading ? 'loading' : ''}">
                    ${isLoading ? '<div class="typing-indicator"><span></span><span></span><span></span></div>' : content}
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        this.messages.push({ role, content });

        return messageId;
    }

    clearChat() {
        if (confirm('Voulez-vous vraiment effacer cette conversation ?')) {
            this.messages = [];
            this.sessionId = this.getOrCreateSessionId();
            
            const messagesContainer = document.getElementById('agentMessages');
            messagesContainer.innerHTML = `
                <div class="agent-welcome">
                    <div class="welcome-icon">👋</div>
                    <h3>Nouvelle conversation</h3>
                    <p>Comment puis-je vous aider ?</p>
                </div>
            `;

            document.getElementById('agentQuickActions').style.display = 'flex';
        }
    }
}

// Initialize widget when DOM is loaded
let aiAgent;
document.addEventListener('DOMContentLoaded', function() {
    aiAgent = new AIAgentWidget();
});
