# 🤖 PLAN : CHAT IA INTÉGRÉ À L'ÉDITEUR

**Date** : 22 Novembre 2025  
**Heure** : 21:31  
**Statut** : 📋 PLANIFICATION

---

## 🎯 OBJECTIF

**Créer un assistant IA intégré à l'éditeur pour modifier le projet en temps réel**

Comme Windsurf/Cascade, l'utilisateur pourra :
- Discuter avec l'IA
- Demander des modifications de code
- Créer/modifier/supprimer des fichiers
- Exécuter des commandes
- Voir l'historique des conversations

---

## 🎨 DESIGN DE L'INTERFACE

### **Layout Proposé**

```
┌─────────────────────────────────────────────────────┐
│  Explorateur  │  Éditeur        │  Chat IA          │
│               │                 │                   │
│  📁 src       │  ┌───────────┐  │  💬 Assistant IA  │
│  📄 index.js  │  │ Onglets   │  │  ┌─────────────┐ │
│  📄 style.css │  ├───────────┤  │  │ Messages    │ │
│               │  │ Monaco    │  │  │             │ │
│               │  │ Editor    │  │  │ User: ...   │ │
│               │  │           │  │  │ AI: ...     │ │
│               │  └───────────┘  │  │             │ │
│               │  ┌───────────┐  │  └─────────────┘ │
│               │  │ Terminal  │  │  ┌─────────────┐ │
│               │  └───────────┘  │  │ Input       │ │
│               │  [Barre état]   │  └─────────────┘ │
└─────────────────────────────────────────────────────┘
```

### **Panneau Chat IA**

**Composants** :
1. **Header**
   - Titre : "Assistant IA"
   - Bouton : Nouvelle conversation
   - Bouton : Historique

2. **Zone de messages**
   - Messages utilisateur (droite, bleu)
   - Messages IA (gauche, gris)
   - Indicateur de typing
   - Boutons d'action (Appliquer, Copier)

3. **Zone de saisie**
   - Input multilignes
   - Bouton Envoyer
   - Raccourci : Ctrl+Enter

4. **Actions rapides**
   - "Créer un fichier"
   - "Modifier ce fichier"
   - "Expliquer ce code"
   - "Corriger les erreurs"

---

## 🏗️ ARCHITECTURE TECHNIQUE

### **Frontend**

**Composants** :
```javascript
// Chat Panel
- ChatPanel.js
  - MessageList.js
  - MessageItem.js
  - ChatInput.js
  - QuickActions.js
  - TypingIndicator.js

// State Management
- chatState = {
    messages: [],
    isTyping: false,
    currentConversation: null,
    history: []
}
```

**Communication** :
```javascript
// WebSocket pour temps réel
const ws = new WebSocket('ws://localhost:8001/ws/chat');

// Ou SSE (Server-Sent Events)
const eventSource = new EventSource('/api/chat/stream');

// Ou Polling
setInterval(() => fetchMessages(), 1000);
```

### **Backend**

**Routes API** :
```python
# app/routes/ai_chat_routes.py

@router.post("/chat/message")
async def send_message(...)
    # Envoyer un message à l'IA

@router.get("/chat/stream")
async def stream_response(...)
    # Stream la réponse de l'IA

@router.post("/chat/execute")
async def execute_action(...)
    # Exécuter une action (créer fichier, etc.)

@router.get("/chat/history")
async def get_history(...)
    # Récupérer l'historique

@router.post("/chat/conversation")
async def new_conversation(...)
    # Nouvelle conversation
```

**Modèles BDD** :
```python
class AIConversation(Base):
    id: int
    project_id: int
    user_id: int
    title: str
    created_at: datetime
    
class AIMessage(Base):
    id: int
    conversation_id: int
    role: str  # 'user' ou 'assistant'
    content: str
    actions: JSON  # Actions effectuées
    created_at: datetime
```

---

## 🤖 INTÉGRATION IA

### **Options de Modèles**

**1. OpenAI GPT-4** ⭐ (Recommandé)
```python
from openai import OpenAI

client = OpenAI(api_key="...")
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "Tu es un assistant de code..."},
        {"role": "user", "content": "Crée un fichier index.html"}
    ]
)
```

**2. Anthropic Claude**
```python
from anthropic import Anthropic

client = Anthropic(api_key="...")
response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[...]
)
```

**3. Ollama (Local)** 🆓
```python
import ollama

response = ollama.chat(
    model='codellama',
    messages=[...]
)
```

**4. Mistral**
```python
from mistralai.client import MistralClient

client = MistralClient(api_key="...")
response = client.chat(
    model="mistral-large-latest",
    messages=[...]
)
```

### **Prompt System**

```python
SYSTEM_PROMPT = """
Tu es un assistant IA intégré à WeBox Studio, un éditeur de code web.

Contexte :
- Projet : {project_name}
- Fichiers : {file_list}
- Fichier actuel : {current_file}
- Langage : {language}

Capacités :
- Créer/modifier/supprimer des fichiers
- Expliquer du code
- Corriger des erreurs
- Suggérer des améliorations
- Générer du code

Format de réponse :
- Texte explicatif
- Code avec ```language
- Actions : CREATE_FILE, MODIFY_FILE, DELETE_FILE

Sois concis et précis.
"""
```

---

## 🔧 FONCTIONNALITÉS

### **Phase 1 : Chat de Base** 📝

- [x] Interface chat (panneau latéral)
- [ ] Envoi de messages
- [ ] Réception de réponses IA
- [ ] Historique des messages
- [ ] Indicateur de typing

### **Phase 2 : Actions sur Fichiers** 📁

- [ ] Créer un fichier
- [ ] Modifier un fichier
- [ ] Supprimer un fichier
- [ ] Lire le contenu d'un fichier
- [ ] Aperçu des modifications (diff)

### **Phase 3 : Contexte Intelligent** 🧠

- [ ] Analyser le projet
- [ ] Comprendre la structure
- [ ] Suggérer des améliorations
- [ ] Détecter les erreurs
- [ ] Auto-complétion intelligente

### **Phase 4 : Exécution de Code** ⚡

- [ ] Exécuter des commandes
- [ ] Installer des packages
- [ ] Lancer des tests
- [ ] Déployer le projet

### **Phase 5 : Collaboration** 👥

- [ ] Partager une conversation
- [ ] Exporter l'historique
- [ ] Templates de prompts
- [ ] Favoris

---

## 📊 EXEMPLES D'UTILISATION

### **Exemple 1 : Créer un fichier**

**User** :
```
Crée un fichier components/Button.jsx avec un bouton React stylisé
```

**AI** :
```
Je vais créer le fichier components/Button.jsx :

[CODE]
import React from 'react';
import './Button.css';

export const Button = ({ children, onClick, variant = 'primary' }) => {
  return (
    <button 
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
[/CODE]

Actions :
✅ Fichier créé : components/Button.jsx
```

### **Exemple 2 : Modifier un fichier**

**User** :
```
Ajoute une fonction de validation d'email dans utils.js
```

**AI** :
```
J'ai ajouté la fonction validateEmail dans utils.js :

[DIFF]
+ export const validateEmail = (email) => {
+   const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
+   return regex.test(email);
+ };
[/DIFF]

Actions :
✅ Fichier modifié : src/utils.js
```

### **Exemple 3 : Expliquer du code**

**User** :
```
Explique-moi ce code dans index.js
```

**AI** :
```
Ce code initialise une application React :

1. Import de React et ReactDOM
2. Import du composant App principal
3. Rendu de l'application dans le DOM
4. Mode strict activé pour détecter les problèmes

Le StrictMode aide à identifier les problèmes potentiels.
```

---

## 🎨 DESIGN CSS

```css
/* Chat Panel */
.chat-panel {
    width: 400px;
    height: 100%;
    background: #1e1e1e;
    border-left: 1px solid #3e3e42;
    display: flex;
    flex-direction: column;
}

.chat-header {
    padding: 15px;
    border-bottom: 1px solid #3e3e42;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
}

.message {
    margin-bottom: 15px;
    display: flex;
}

.message.user {
    justify-content: flex-end;
}

.message-content {
    max-width: 80%;
    padding: 10px 15px;
    border-radius: 8px;
}

.message.user .message-content {
    background: #007acc;
    color: white;
}

.message.assistant .message-content {
    background: #2d2d30;
    color: #cccccc;
}

.chat-input {
    padding: 15px;
    border-top: 1px solid #3e3e42;
}

.chat-input textarea {
    width: 100%;
    background: #2d2d30;
    border: 1px solid #3e3e42;
    color: #cccccc;
    padding: 10px;
    border-radius: 4px;
    resize: none;
}

.typing-indicator {
    display: flex;
    gap: 5px;
    padding: 10px;
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: #007acc;
    border-radius: 50%;
    animation: typing 1.4s infinite;
}
```

---

## 🚀 IMPLÉMENTATION

### **Étape 1 : Interface de Base**

1. Ajouter le panneau chat dans `project_editor.html`
2. Créer le CSS pour le chat
3. Implémenter l'envoi de messages
4. Afficher les réponses

### **Étape 2 : Backend API**

1. Créer `app/routes/ai_chat_routes.py`
2. Créer les modèles BDD
3. Intégrer OpenAI API
4. Implémenter le streaming

### **Étape 3 : Actions sur Fichiers**

1. Parser les actions de l'IA
2. Exécuter les actions (CREATE, MODIFY, DELETE)
3. Afficher les confirmations
4. Gérer les erreurs

### **Étape 4 : Contexte Intelligent**

1. Analyser la structure du projet
2. Lire les fichiers pertinents
3. Enrichir le contexte de l'IA
4. Optimiser les prompts

---

## 💰 COÛTS ESTIMÉS

### **OpenAI GPT-4**
- Input : $0.01 / 1K tokens
- Output : $0.03 / 1K tokens
- Coût moyen par message : ~$0.02

### **Claude 3 Opus**
- Input : $0.015 / 1K tokens
- Output : $0.075 / 1K tokens
- Coût moyen par message : ~$0.03

### **Ollama (Local)**
- Gratuit ✅
- Nécessite GPU
- Moins performant

---

## 📋 PROCHAINES ÉTAPES

1. **Concevoir l'interface** (HTML/CSS)
2. **Créer les routes API** (Backend)
3. **Intégrer OpenAI** (ou Ollama)
4. **Tester le chat de base**
5. **Ajouter les actions sur fichiers**
6. **Optimiser le contexte**

---

**Veux-tu commencer par l'interface ou le backend ? 🚀**
