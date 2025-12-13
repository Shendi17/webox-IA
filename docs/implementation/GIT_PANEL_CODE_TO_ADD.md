# 🔀 CODE À AJOUTER POUR LE PANNEAU GIT

## 📋 Instructions

Ajouter ce code dans `project_editor.html`

---

## 🎨 CSS À AJOUTER

**Ajouter après le CSS de `.history-item-action.delete:hover`** (ligne ~560)

```css
/* ==================== PANNEAU GIT ==================== */
.git-section {
    padding: 1rem;
    border-bottom: 1px solid #3e3e42;
}

.git-section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    font-weight: 600;
    color: #cccccc;
    font-size: 0.9rem;
}

.git-badge {
    background: #007acc;
    color: white;
    padding: 0.15rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
}

.git-branch-selector {
    width: 100%;
    background: #2d2d30;
    border: 1px solid #3e3e42;
    color: #cccccc;
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.git-branch-selector:focus {
    outline: none;
    border-color: #007acc;
}

.git-changes-list {
    max-height: 200px;
    overflow-y: auto;
}

.git-change-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    background: #2d2d30;
    border-radius: 4px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s;
}

.git-change-item:hover {
    background: #3e3e42;
}

.git-change-status {
    margin-right: 0.5rem;
    font-weight: bold;
}

.git-change-status.modified {
    color: #f0ad4e;
}

.git-change-status.added {
    color: #5cb85c;
}

.git-change-status.deleted {
    color: #d9534f;
}

.git-commit-message {
    width: 100%;
    background: #2d2d30;
    border: 1px solid #3e3e42;
    color: #cccccc;
    padding: 0.5rem;
    border-radius: 4px;
    font-family: 'Consolas', monospace;
    font-size: 0.85rem;
    resize: vertical;
    margin-bottom: 0.5rem;
}

.git-commit-message:focus {
    outline: none;
    border-color: #007acc;
}

.git-commit-actions {
    display: flex;
    gap: 0.5rem;
}

.git-btn-primary {
    flex: 1;
    background: #007acc;
    border: none;
    color: white;
    padding: 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.2s;
}

.git-btn-primary:hover {
    background: #005a9e;
}

.git-btn-secondary {
    background: #2d2d30;
    border: 1px solid #3e3e42;
    color: #cccccc;
    padding: 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
}

.git-btn-secondary:hover {
    border-color: #007acc;
    color: #007acc;
}

.git-history-list {
    max-height: 300px;
    overflow-y: auto;
}

.git-commit-item {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: #2d2d30;
    border-radius: 4px;
    border-left: 3px solid #007acc;
}

.git-commit-hash {
    font-family: 'Consolas', monospace;
    font-size: 0.75rem;
    color: #858585;
}

.git-commit-message-text {
    font-size: 0.85rem;
    color: #cccccc;
    margin: 0.25rem 0;
}

.git-commit-meta {
    font-size: 0.75rem;
    color: #858585;
}
```

---

## 💻 JAVASCRIPT À AJOUTER

**Ajouter avant la fermeture du `</script>` (ligne ~1800)**

```javascript
// ==================== GIT INTERFACE ====================
let currentGitStatus = null;
let currentBranch = 'main';

// Changer d'onglet
function switchExplorerTab(tab) {
    // Mettre à jour les onglets
    document.querySelectorAll('.explorer-tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    
    // Afficher le bon contenu
    document.getElementById('explorerFiles').style.display = tab === 'files' ? 'flex' : 'none';
    document.getElementById('explorerGit').style.display = tab === 'git' ? 'block' : 'none';
    document.getElementById('explorerDeploy').style.display = tab === 'deploy' ? 'block' : 'none';
    
    // Charger les données
    if (tab === 'git') {
        loadGitStatus();
        loadGitBranches();
        loadGitHistory();
    }
}

// Charger le statut Git
async function loadGitStatus() {
    try {
        const response = await fetch('/api/git/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: projectId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentGitStatus = data;
            currentBranch = data.branch;
            renderGitChanges(data.files);
            updateChangesCount(data.files);
        } else {
            document.getElementById('gitChangesList').innerHTML = 
                '<div style="text-align: center; color: #858585; padding: 1rem;">Pas un dépôt Git</div>';
        }
    } catch (error) {
        console.error('Erreur Git status:', error);
    }
}

// Afficher les changements
function renderGitChanges(files) {
    const list = document.getElementById('gitChangesList');
    let html = '';
    
    // Fichiers modifiés
    if (files.modified && files.modified.length > 0) {
        files.modified.forEach(file => {
            html += `
                <div class="git-change-item">
                    <span class="git-change-status modified">M</span>
                    <span>${file}</span>
                </div>
            `;
        });
    }
    
    // Fichiers ajoutés
    if (files.added && files.added.length > 0) {
        files.added.forEach(file => {
            html += `
                <div class="git-change-item">
                    <span class="git-change-status added">A</span>
                    <span>${file}</span>
                </div>
            `;
        });
    }
    
    // Fichiers non suivis
    if (files.untracked && files.untracked.length > 0) {
        files.untracked.forEach(file => {
            html += `
                <div class="git-change-item">
                    <span class="git-change-status added">?</span>
                    <span>${file}</span>
                </div>
            `;
        });
    }
    
    if (!html) {
        html = '<div style="text-align: center; color: #858585; padding: 1rem;">Aucun changement</div>';
    }
    
    list.innerHTML = html;
}

// Mettre à jour le compteur
function updateChangesCount(files) {
    const count = (files.modified?.length || 0) + 
                  (files.added?.length || 0) + 
                  (files.untracked?.length || 0);
    document.getElementById('gitChangesCount').textContent = count;
}

// Charger les branches
async function loadGitBranches() {
    try {
        const response = await fetch('/api/git/branches', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: projectId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const selector = document.getElementById('gitBranchSelector');
            selector.innerHTML = '';
            
            data.branches.forEach(branch => {
                if (!branch.remote) {
                    const option = document.createElement('option');
                    option.value = branch.name;
                    option.textContent = branch.name;
                    option.selected = branch.current;
                    selector.appendChild(option);
                }
            });
        }
    } catch (error) {
        console.error('Erreur branches:', error);
    }
}

// Changer de branche
async function gitCheckout() {
    const branchName = document.getElementById('gitBranchSelector').value;
    
    try {
        const response = await fetch('/api/git/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: projectId,
                branch_name: branchName
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`✅ Basculé sur ${branchName}`, 'success');
            loadGitStatus();
        } else {
            alert('❌ ' + data.error);
        }
    } catch (error) {
        console.error('Erreur checkout:', error);
    }
}

// Créer une branche
function showCreateBranchDialog() {
    const branchName = prompt('Nom de la nouvelle branche :');
    if (!branchName) return;
    
    createGitBranch(branchName);
}

async function createGitBranch(branchName) {
    try {
        const response = await fetch('/api/git/branch/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: projectId,
                branch_name: branchName,
                checkout: true
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`✅ Branche ${branchName} créée`, 'success');
            loadGitBranches();
            loadGitStatus();
        } else {
            alert('❌ ' + data.error);
        }
    } catch (error) {
        console.error('Erreur création branche:', error);
    }
}

// Générer message de commit
async function generateCommitMessage() {
    try {
        const response = await fetch('/api/git/commit/generate-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: projectId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('gitCommitMessage').value = data.message;
        }
    } catch (error) {
        console.error('Erreur génération message:', error);
    }
}

// Commit et push
async function gitCommitAndPush() {
    const message = document.getElementById('gitCommitMessage').value.trim();
    
    if (!message) {
        alert('⚠️ Veuillez entrer un message de commit');
        return;
    }
    
    try {
        // 1. Add
        await fetch('/api/git/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: projectId })
        });
        
        // 2. Commit
        const commitResponse = await fetch('/api/git/commit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: projectId,
                message: message
            })
        });
        
        const commitData = await commitResponse.json();
        
        if (!commitData.success) {
            alert('❌ ' + commitData.error);
            return;
        }
        
        // 3. Push
        const pushResponse = await fetch('/api/git/push', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: projectId,
                remote: 'origin',
                branch: currentBranch
            })
        });
        
        const pushData = await pushResponse.json();
        
        if (pushData.success) {
            showNotification('✅ Commit et push réussis', 'success');
            document.getElementById('gitCommitMessage').value = '';
            loadGitStatus();
            loadGitHistory();
        } else {
            showNotification('⚠️ Commit réussi mais push échoué: ' + pushData.error, 'warning');
            loadGitStatus();
            loadGitHistory();
        }
    } catch (error) {
        console.error('Erreur commit/push:', error);
        alert('❌ Erreur lors du commit/push');
    }
}

// Charger l'historique
async function loadGitHistory() {
    try {
        const response = await fetch('/api/git/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: projectId,
                limit: 5
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            renderGitHistory(data.commits);
        }
    } catch (error) {
        console.error('Erreur historique:', error);
    }
}

// Afficher l'historique
function renderGitHistory(commits) {
    const list = document.getElementById('gitHistoryList');
    
    if (!commits || commits.length === 0) {
        list.innerHTML = '<div style="text-align: center; color: #858585; padding: 1rem;">Aucun commit</div>';
        return;
    }
    
    let html = '';
    commits.forEach(commit => {
        const date = new Date(commit.timestamp * 1000);
        const timeAgo = formatTimeAgo(date);
        
        html += `
            <div class="git-commit-item">
                <div class="git-commit-hash">${commit.hash.substring(0, 7)}</div>
                <div class="git-commit-message-text">${commit.message}</div>
                <div class="git-commit-meta">
                    Par ${commit.author_name} • ${timeAgo}
                </div>
            </div>
        `;
    });
    
    list.innerHTML = html;
}

// Formater le temps
function formatTimeAgo(date) {
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    
    if (hours < 1) return 'À l\'instant';
    if (hours < 24) return `Il y a ${hours}h`;
    if (days < 7) return `Il y a ${days}j`;
    return date.toLocaleDateString('fr-FR');
}
```

---

## ✅ RÉSUMÉ

1. **HTML** : Déjà ajouté ✅
2. **CSS** : À ajouter après ligne ~560
3. **JavaScript** : À ajouter avant `</script>`

---

## 🧪 TESTER

1. Redémarrer le serveur
2. Ouvrir l'éditeur
3. Cliquer sur l'onglet "🔀 Git"
4. Voir le statut, les changements, l'historique
5. Tester commit & push

---

**Interface Git prête à être intégrée ! 🚀**
