// ============================================
// SYSTÈME UI - MODALS & NOTIFICATIONS
// ============================================

// ============================================
// TOAST NOTIFICATIONS
// ============================================

const Toast = {
    container: null,
    
    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },
    
    show(message, type = 'info', duration = 3000) {
        this.init();
        
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        
        const titles = {
            success: 'Succès',
            error: 'Erreur',
            warning: 'Attention',
            info: 'Information'
        };
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-icon">${icons[type]}</div>
            <div class="toast-content">
                <div class="toast-title">${titles[type]}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">×</button>
        `;
        
        this.container.appendChild(toast);
        
        // Close button
        toast.querySelector('.toast-close').addEventListener('click', () => {
            this.remove(toast);
        });
        
        // Auto remove
        if (duration > 0) {
            setTimeout(() => this.remove(toast), duration);
        }
        
        return toast;
    },
    
    remove(toast) {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    },
    
    success(message, duration) {
        return this.show(message, 'success', duration);
    },
    
    error(message, duration) {
        return this.show(message, 'error', duration);
    },
    
    warning(message, duration) {
        return this.show(message, 'warning', duration);
    },
    
    info(message, duration) {
        return this.show(message, 'info', duration);
    }
};

// ============================================
// MODAL SYSTEM
// ============================================

const Modal = {
    overlay: null,
    currentModal: null,
    
    init() {
        if (!this.overlay) {
            this.overlay = document.createElement('div');
            this.overlay.className = 'modal-overlay';
            document.body.appendChild(this.overlay);
            
            this.overlay.addEventListener('click', (e) => {
                if (e.target === this.overlay) {
                    this.close();
                }
            });
        }
    },
    
    show(title, content, buttons = []) {
        this.init();
        
        const modal = document.createElement('div');
        modal.className = 'modal';
        
        let buttonsHTML = '';
        if (buttons.length > 0) {
            buttonsHTML = '<div class="modal-footer">';
            buttons.forEach(btn => {
                buttonsHTML += `<button class="btn ${btn.class || 'btn-secondary'}" data-action="${btn.action || ''}">${btn.text}</button>`;
            });
            buttonsHTML += '</div>';
        }
        
        modal.innerHTML = `
            <div class="modal-header">
                <h2 class="modal-title">${title}</h2>
                <button class="modal-close">×</button>
            </div>
            <div class="modal-body">${content}</div>
            ${buttonsHTML}
        `;
        
        this.overlay.innerHTML = '';
        this.overlay.appendChild(modal);
        this.overlay.classList.add('active');
        this.currentModal = modal;
        
        // Close button
        modal.querySelector('.modal-close').addEventListener('click', () => {
            this.close();
        });
        
        // Button actions
        buttons.forEach(btn => {
            if (btn.action) {
                modal.querySelector(`[data-action="${btn.action}"]`).addEventListener('click', () => {
                    if (btn.callback) btn.callback();
                    if (btn.closeOnClick !== false) this.close();
                });
            }
        });
        
        return modal;
    },
    
    close() {
        if (this.overlay) {
            this.overlay.classList.remove('active');
            this.currentModal = null;
        }
    },
    
    confirm(title, message, onConfirm, onCancel) {
        return this.show(title, `<p>${message}</p>`, [
            {
                text: 'Annuler',
                class: 'btn-secondary',
                action: 'cancel',
                callback: onCancel
            },
            {
                text: 'Confirmer',
                class: 'btn-primary',
                action: 'confirm',
                callback: onConfirm
            }
        ]);
    },
    
    loading(message = 'Chargement en cours...') {
        return this.show('', `
            <div style="text-align: center; padding: 2rem;">
                <div class="spinner spinner-large" style="border-top-color: #4169e1; border-color: rgba(65, 105, 225, 0.2); margin: 0 auto 1rem;"></div>
                <p style="color: #666;">${message}</p>
            </div>
        `, []);
    }
};

// ============================================
// LOADING UTILITIES
// ============================================

function showLoading(button) {
    if (!button) return;
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner"></span> Chargement...';
}

function hideLoading(button) {
    if (!button) return;
    button.disabled = false;
    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
    }
}

function simulateLoading(callback, duration = 2000) {
    return new Promise(resolve => {
        setTimeout(() => {
            if (callback) callback();
            resolve();
        }, duration);
    });
}

// ============================================
// EXPORT GLOBAL
// ============================================

window.Toast = Toast;
window.Modal = Modal;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.simulateLoading = simulateLoading;

console.log('✅ Système UI initialisé');
