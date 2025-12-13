# WeBox Multi-IA - Frontend React

Interface utilisateur moderne pour WeBox Multi-IA, construite avec React, Vite et TailwindCSS.

## 🚀 Démarrage Rapide

### Installation
```bash
npm install
```

### Développement
```bash
npm run dev
```

Le frontend sera accessible sur http://localhost:3000

### Build Production
```bash
npm run build
```

## 🛠️ Technologies

- **React 18** - Bibliothèque UI
- **Vite** - Build tool ultra-rapide
- **TailwindCSS** - Framework CSS utility-first
- **Axios** - Client HTTP
- **React Router** - Navigation
- **Lucide React** - Icônes modernes

## 📁 Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Chat.jsx          # Composant Chat Multi-IA
│   ├── App.jsx                # Composant principal
│   ├── main.jsx               # Point d'entrée
│   └── index.css              # Styles globaux
├── index.html                 # Template HTML
├── vite.config.js             # Configuration Vite
├── tailwind.config.js         # Configuration TailwindCSS
└── package.json               # Dépendances
```

## 🎨 Composants

### Chat
Composant principal pour le chat multi-IA avec :
- Sélection multiple d'IA
- Affichage des réponses en temps réel
- Interface responsive
- Gestion des erreurs

## 🔌 API

Le frontend communique avec le backend FastAPI via :
- **REST API** : `/api/chat/*`
- **WebSocket** : `/ws/chat/*` (à venir)

Configuration du proxy dans `vite.config.js` :
```javascript
proxy: {
  '/api': 'http://localhost:8000',
  '/ws': 'ws://localhost:8000'
}
```

## 🎯 Fonctionnalités

- ✅ Chat Multi-IA
- ✅ Sélection dynamique des IA
- ✅ Interface moderne et responsive
- ✅ Gestion des erreurs
- ⏳ WebSocket streaming (à venir)
- ⏳ Historique des conversations (à venir)
- ⏳ Authentification (à venir)

## 📝 Scripts

- `npm run dev` - Serveur de développement
- `npm run build` - Build production
- `npm run preview` - Prévisualiser le build

## 🌐 Ports

- **Frontend** : http://localhost:3000
- **Backend** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs
