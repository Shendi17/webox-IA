/**
 * Voice Automation - Piloter WeBox par commande vocale
 */

class VoiceAutomation {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.button = null;
        this.modal = null;
    }

    /**
     * Initialiser le Voice Automation
     */
    init() {
        this.createButton();
        this.createModal();
        this.attachEventListeners();
    }

    /**
     * Créer le bouton micro flottant
     */
    createButton() {
        const button = document.createElement('button');
        button.className = 'voice-automation-button';
        button.innerHTML = '🎤';
        button.title = 'Commande vocale (Ctrl+Shift+V)';
        button.onclick = () => this.toggleRecording();
        
        document.body.appendChild(button);
        this.button = button;
    }

    /**
     * Créer le modal de commande vocale
     */
    createModal() {
        const modal = document.createElement('div');
        modal.className = 'voice-automation-modal';
        modal.innerHTML = `
            <div class="voice-modal-content">
                <div class="voice-modal-header">
                    <h3>🎤 Commande Vocale</h3>
                    <button class="voice-modal-close" onclick="voiceAutomation.closeModal()">×</button>
                </div>
                <div class="voice-modal-body">
                    <div class="voice-status" id="voiceStatus">
                        <div class="voice-wave">
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                        <p>Cliquez sur le micro pour commencer</p>
                    </div>
                    <div class="voice-transcript" id="voiceTranscript" style="display: none;">
                        <strong>Vous avez dit :</strong>
                        <p id="transcriptText"></p>
                    </div>
                    <div class="voice-response" id="voiceResponse" style="display: none;">
                        <strong>Réponse :</strong>
                        <p id="responseText"></p>
                    </div>
                </div>
                <div class="voice-modal-footer">
                    <button class="voice-btn-record" onclick="voiceAutomation.toggleRecording()">
                        <span id="recordBtnText">🎤 Commencer</span>
                    </button>
                    <button class="voice-btn-cancel" onclick="voiceAutomation.closeModal()">
                        Fermer
                    </button>
                </div>
                <div class="voice-examples">
                    <strong>Exemples de commandes :</strong>
                    <ul>
                        <li>"Ouvre mes projets"</li>
                        <li>"Crée un site e-commerce"</li>
                        <li>"Génère 5 articles sur le marketing"</li>
                        <li>"Déploie en production"</li>
                    </ul>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        this.modal = modal;
    }

    /**
     * Attacher les event listeners
     */
    attachEventListeners() {
        // Raccourci clavier Ctrl+Shift+V
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'V') {
                e.preventDefault();
                this.openModal();
            }
        });

        // Fermer le modal en cliquant à l'extérieur
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
    }

    /**
     * Ouvrir le modal
     */
    openModal() {
        this.modal.style.display = 'flex';
        this.resetModal();
    }

    /**
     * Fermer le modal
     */
    closeModal() {
        if (this.isRecording) {
            this.stopRecording();
        }
        this.modal.style.display = 'none';
    }

    /**
     * Réinitialiser le modal
     */
    resetModal() {
        document.getElementById('voiceStatus').style.display = 'block';
        document.getElementById('voiceTranscript').style.display = 'none';
        document.getElementById('voiceResponse').style.display = 'none';
        document.getElementById('recordBtnText').textContent = '🎤 Commencer';
        
        const statusText = document.querySelector('#voiceStatus p');
        statusText.textContent = 'Cliquez sur le micro pour commencer';
    }

    /**
     * Toggle enregistrement
     */
    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    /**
     * Démarrer l'enregistrement
     */
    async startRecording() {
        try {
            // Demander l'accès au micro
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };
            
            this.mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                await this.processVoiceCommand(audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };
            
            this.mediaRecorder.start();
            this.isRecording = true;
            
            // Mettre à jour l'UI
            this.button.classList.add('recording');
            this.button.innerHTML = '⏹️';
            document.getElementById('recordBtnText').textContent = '⏹️ Arrêter';
            
            const statusText = document.querySelector('#voiceStatus p');
            statusText.textContent = '🎤 Parlez maintenant...';
            
            this.showNotification('🎤 Enregistrement en cours...', 'info');
            
        } catch (error) {
            console.error('Erreur micro:', error);
            this.showNotification('❌ Impossible d\'accéder au microphone', 'error');
        }
    }

    /**
     * Arrêter l'enregistrement
     */
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            // Mettre à jour l'UI
            this.button.classList.remove('recording');
            this.button.innerHTML = '🎤';
            document.getElementById('recordBtnText').textContent = '🎤 Commencer';
            
            const statusText = document.querySelector('#voiceStatus p');
            statusText.textContent = '⏳ Traitement en cours...';
        }
    }

    /**
     * Traiter la commande vocale
     */
    async processVoiceCommand(audioBlob) {
        try {
            this.showNotification('⏳ Analyse de votre commande...', 'info');
            
            // Créer FormData
            const formData = new FormData();
            formData.append('audio', audioBlob, 'command.wav');
            
            // Envoyer au serveur
            const response = await fetch('/api/voice-automation/process-audio', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Afficher la transcription
                document.getElementById('voiceTranscript').style.display = 'block';
                document.getElementById('transcriptText').textContent = result.transcript;
                
                // Afficher la réponse
                document.getElementById('voiceResponse').style.display = 'block';
                document.getElementById('responseText').textContent = result.response;
                
                document.getElementById('voiceStatus').style.display = 'none';
                
                this.showNotification(`✅ ${result.response}`, 'success');
                
                // Exécuter l'action
                await this.executeAction(result.action, result.parameters);
                
            } else {
                this.showNotification(`❌ ${result.error || 'Erreur de traitement'}`, 'error');
                this.resetModal();
            }
            
        } catch (error) {
            console.error('Erreur:', error);
            this.showNotification('❌ Erreur de traitement', 'error');
            this.resetModal();
        }
    }

    /**
     * Exécuter une action
     */
    async executeAction(action, parameters) {
        try {
            const response = await fetch('/api/voice-automation/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action, parameters })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Gérer les différentes actions
                switch (action) {
                    case 'NAVIGATION':
                        if (result.result.redirect) {
                            setTimeout(() => {
                                window.location.href = result.result.redirect;
                            }, 1500);
                        }
                        break;
                    
                    case 'CREATE_PROJECT':
                        // Rediriger vers la page de création
                        setTimeout(() => {
                            window.location.href = '/dashboard/projects';
                        }, 1500);
                        break;
                    
                    case 'GENERATE_CONTENT':
                        // Afficher un message de succès
                        this.showNotification(`✅ ${result.message}`, 'success');
                        break;
                    
                    case 'DEPLOY':
                        // Afficher un message de succès
                        this.showNotification(`✅ ${result.message}`, 'success');
                        break;
                    
                    case 'AI_CHAT':
                        // Ouvrir le chat IA
                        if (typeof openAIChat === 'function') {
                            openAIChat();
                        }
                        break;
                }
            }
            
        } catch (error) {
            console.error('Erreur exécution:', error);
        }
    }

    /**
     * Afficher une notification
     */
    showNotification(message, type = 'info') {
        // Utiliser la fonction globale si elle existe
        if (typeof showNotification === 'function') {
            showNotification(message, type);
            return;
        }
        
        // Sinon, créer une notification simple
        const notification = document.createElement('div');
        notification.className = `voice-notification voice-notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Initialiser au chargement de la page
let voiceAutomation;

document.addEventListener('DOMContentLoaded', () => {
    voiceAutomation = new VoiceAutomation();
    voiceAutomation.init();
});
