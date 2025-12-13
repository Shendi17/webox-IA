# 🚀 STUDIO WEB IA - IMPLÉMENTATION

**Date** : 24 Novembre 2025  
**Statut** : 🔄 EN COURS  

---

## 🎯 OBJECTIFS

Enrichir le Studio Web IA avec :
1. ✅ Prévisualisation en temps réel
2. ⏳ Templates prédéfinis
3. ⏳ Déploiement 1 clic

---

## 📊 ÉTAT ACTUEL

### **Existant**
- ✅ Éditeur Monaco fonctionnel
- ✅ Terminal intégré (Xterm.js)
- ✅ Arborescence de fichiers
- ✅ Gestion des onglets
- ✅ Sauvegarde automatique

### **À ajouter**
- ⏳ Prévisualisation en temps réel
- ⏳ Split view (éditeur/preview)
- ⏳ Modes responsive
- ⏳ Templates
- ⏳ Déploiement

---

## 🎨 PHASE 1 : PRÉVISUALISATION

### **Layout proposé**

```
┌────────────────────────────────────────────────────┐
│ [Logo] Studio - projet.html    [Split] [Deploy]   │
├──────┬──────────────────┬──────────────────────────┤
│ 📁   │  📝 Éditeur      │  👁️ Prévisualisation     │
│Files │                  │                          │
│      │  <html>          │  [Desktop ▼] [Refresh]   │
│ 📂src│    <head>        │  ┌────────────────────┐  │
│  index│      <title>    │  │                    │  │
│  style│    </head>      │  │   Live Preview     │  │
│  script│   <body>       │  │                    │  │
│      │      <h1>Hello  │  │   [Votre site]     │  │
│ 🔧Git│    </body>       │  │                    │  │
│ 📦Tmp│  </html>         │  └────────────────────┘  │
│      │                  │                          │
│ 🚀Dep│  [Terminal ▼]    │  [Mobile] [Tablet] [PC]  │
└──────┴──────────────────┴──────────────────────────┘
```

### **Fonctionnalités**

1. **Split View**
   - Toggle split horizontal/vertical
   - Redimensionnable
   - Masquable

2. **Preview iframe**
   - Hot reload automatique
   - Sandbox sécurisé
   - Gestion des erreurs

3. **Modes responsive**
   - Desktop (1920x1080)
   - Laptop (1366x768)
   - Tablet (768x1024)
   - Mobile (375x667)
   - Custom

4. **Actions**
   - Refresh manuel
   - Toggle auto-refresh
   - Rotation (portrait/landscape)
   - Plein écran

---

## 💻 IMPLÉMENTATION

### **1. CSS pour le split view**

```css
.editor-main {
    display: flex;
    flex-direction: row; /* ou column pour vertical */
}

.editor-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.preview-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #3e3e42;
}

.preview-header {
    background: #2d2d30;
    padding: 0.5rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.preview-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #1e1e1e;
    padding: 1rem;
}

.preview-frame {
    background: white;
    border: 1px solid #3e3e42;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
```

### **2. HTML Structure**

```html
<!-- Zone principale avec split -->
<div class="editor-main" id="editorMain">
    <!-- Panel Éditeur -->
    <div class="editor-panel">
        <div class="editor-tabs" id="editorTabs"></div>
        <div id="monaco-editor"></div>
        <div class="terminal-container" id="terminalContainer">
            <!-- Terminal existant -->
        </div>
    </div>
    
    <!-- Panel Prévisualisation -->
    <div class="preview-panel" id="previewPanel" style="display: none;">
        <div class="preview-header">
            <div class="preview-title">👁️ Prévisualisation</div>
            <div class="preview-controls">
                <select id="deviceMode">
                    <option value="desktop">🖥️ Desktop</option>
                    <option value="laptop">💻 Laptop</option>
                    <option value="tablet">📱 Tablet</option>
                    <option value="mobile">📱 Mobile</option>
                </select>
                <button onclick="refreshPreview()">🔄</button>
                <button onclick="toggleAutoRefresh()">⚡</button>
                <button onclick="togglePreview()">✖️</button>
            </div>
        </div>
        <div class="preview-container">
            <iframe id="previewFrame" class="preview-frame" sandbox="allow-scripts allow-same-origin"></iframe>
        </div>
    </div>
</div>
```

### **3. JavaScript**

```javascript
let previewEnabled = false;
let autoRefresh = true;
let refreshTimeout = null;

// Toggle preview
function togglePreview() {
    const panel = document.getElementById('previewPanel');
    previewEnabled = !previewEnabled;
    panel.style.display = previewEnabled ? 'flex' : 'none';
    
    if (previewEnabled) {
        refreshPreview();
    }
}

// Refresh preview
function refreshPreview() {
    const frame = document.getElementById('previewFrame');
    const content = generatePreviewHTML();
    
    // Écrire dans l'iframe
    const doc = frame.contentDocument || frame.contentWindow.document;
    doc.open();
    doc.write(content);
    doc.close();
}

// Generate HTML for preview
function generatePreviewHTML() {
    // Récupérer le contenu de index.html
    const htmlContent = editor.getValue();
    
    // Injecter les CSS et JS si nécessaire
    // TODO: Charger les fichiers CSS et JS du projet
    
    return htmlContent;
}

// Auto-refresh on change
editor.onDidChangeModelContent(() => {
    if (autoRefresh && previewEnabled) {
        clearTimeout(refreshTimeout);
        refreshTimeout = setTimeout(() => {
            refreshPreview();
        }, 500); // Debounce 500ms
    }
});

// Device modes
const deviceSizes = {
    desktop: { width: '100%', height: '100%' },
    laptop: { width: '1366px', height: '768px' },
    tablet: { width: '768px', height: '1024px' },
    mobile: { width: '375px', height: '667px' }
};

document.getElementById('deviceMode').addEventListener('change', (e) => {
    const mode = e.target.value;
    const frame = document.getElementById('previewFrame');
    const size = deviceSizes[mode];
    
    frame.style.width = size.width;
    frame.style.height = size.height;
});
```

---

## 📦 PHASE 2 : TEMPLATES

### **Templates à créer**

1. **Landing Page**
   - Hero section
   - Features
   - CTA
   - Footer

2. **Portfolio**
   - Header
   - Projects grid
   - About
   - Contact

3. **Blog**
   - Header
   - Articles list
   - Sidebar
   - Footer

4. **E-commerce**
   - Product grid
   - Cart
   - Checkout

5. **Dashboard**
   - Sidebar
   - Cards
   - Charts

6. **Coming Soon**
   - Countdown
   - Email form
   - Social links

### **Modal de sélection**

```html
<div id="templatesModal" class="modal">
    <div class="modal-content">
        <h2>📦 Choisir un template</h2>
        <div class="templates-grid">
            <div class="template-card" onclick="useTemplate('landing')">
                <img src="/templates/landing-preview.png">
                <h3>Landing Page</h3>
                <p>Page de destination moderne</p>
            </div>
            <!-- Autres templates -->
        </div>
    </div>
</div>
```

---

## 🚀 PHASE 3 : DÉPLOIEMENT

### **Providers**

1. **Netlify**
   - API: `https://api.netlify.com/api/v1/sites`
   - Déploiement automatique
   - Custom domain

2. **Vercel**
   - API: `https://api.vercel.com/v13/deployments`
   - Edge functions
   - Analytics

3. **GitHub Pages**
   - Via GitHub API
   - gh-pages branch
   - Custom domain

4. **FTP/SFTP**
   - Connexion directe
   - Upload fichiers

### **Interface de déploiement**

```html
<div id="deployModal" class="modal">
    <div class="modal-content">
        <h2>🚀 Déployer le projet</h2>
        
        <select id="deployProvider">
            <option value="netlify">Netlify</option>
            <option value="vercel">Vercel</option>
            <option value="github">GitHub Pages</option>
            <option value="ftp">FTP/SFTP</option>
        </select>
        
        <div id="netlifyConfig">
            <input type="text" placeholder="Site name">
            <input type="text" placeholder="Custom domain (optional)">
        </div>
        
        <button onclick="deploy()">Déployer</button>
    </div>
</div>
```

---

## ✅ CHECKLIST

### **Prévisualisation**
- [ ] CSS split view
- [ ] HTML structure
- [ ] JavaScript preview
- [ ] Auto-refresh
- [ ] Device modes
- [ ] Error handling

### **Templates**
- [ ] 6 templates HTML/CSS/JS
- [ ] Modal de sélection
- [ ] Aperçus
- [ ] Application au projet

### **Déploiement**
- [ ] Intégration Netlify
- [ ] Intégration Vercel
- [ ] Intégration GitHub Pages
- [ ] FTP/SFTP
- [ ] Status de déploiement

---

## 🔧 API BACKEND

### **Templates**
```
GET /api/studio/templates
POST /api/studio/projects/{id}/use-template
```

### **Déploiement**
```
POST /api/studio/projects/{id}/deploy
GET /api/studio/projects/{id}/deployments
```

---

**Commençons par la Phase 1 : Prévisualisation ! 🚀**
