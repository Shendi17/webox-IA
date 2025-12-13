# 🚀 Guide de Migration FastAPI - WeBox Multi-IA

**Date de début :** 30 Octobre 2025  
**Framework cible :** FastAPI + React/Vue.js  
**Durée estimée :** 3-4 mois

---

## 📋 TABLE DES MATIÈRES

1. [Prérequis](#prérequis)
2. [Configuration Initiale](#configuration-initiale)
3. [Migration Chat Multi-IA](#migration-chat-multi-ia)
4. [Migration Dashboard](#migration-dashboard)
5. [Migration Autres Fonctionnalités](#migration-autres-fonctionnalités)
6. [Tests et Déploiement](#tests-et-déploiement)

---

## 🔧 PRÉREQUIS

### Logiciels à Installer

#### 1. PostgreSQL (Base de données)
```powershell
# Télécharger depuis : https://www.postgresql.org/download/windows/
# Ou via Chocolatey :
choco install postgresql

# Créer la base de données
psql -U postgres
CREATE DATABASE webox_db;
CREATE USER webox_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE webox_db TO webox_user;
\q
```

#### 2. Node.js (Pour le frontend)
```powershell
# Télécharger depuis : https://nodejs.org/
# Ou via Chocolatey :
choco install nodejs

# Vérifier l'installation
node --version
npm --version
```

#### 3. Redis (Pour le cache et les queues)
```powershell
# Télécharger depuis : https://github.com/microsoftarchive/redis/releases
# Ou via Chocolatey :
choco install redis-64

# Démarrer Redis
redis-server
```

### Dépendances Python

```powershell
# Installer les dépendances FastAPI
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary
pip install python-jose[cryptography] passlib[bcrypt]
pip install python-multipart aiofiles
pip install redis celery
pip install pytest pytest-asyncio httpx

# Installer les dépendances existantes
pip install -r requirements_fastapi.txt
```

---

## ⚙️ CONFIGURATION INITIALE

### 1. Configuration Base de Données

**Créer :** `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://webox_user:votre_mot_de_passe@localhost/webox_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Configuration Alembic (Migrations)

```powershell
# Initialiser Alembic
cd app
alembic init alembic

# Éditer alembic.ini
# sqlalchemy.url = postgresql://webox_user:votre_mot_de_passe@localhost/webox_db
```

**Éditer :** `app/alembic/env.py`

```python
from app.database import Base
from app.models import user, conversation, message  # Importer tous les modèles

target_metadata = Base.metadata
```

### 3. Créer les Modèles de Données

**Créer :** `app/models/conversation.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    folder = Column(String(100), default="Général")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    ai_responses = Column(JSON, nullable=True)  # Pour stocker les réponses multi-IA
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    conversation = relationship("Conversation", back_populates="messages")
```

**Créer :** `app/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Préférences utilisateur
    preferences = Column(JSON, default={})
    api_keys = Column(JSON, default={})  # Clés API chiffrées
    
    # Relations
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
```

### 4. Créer la Première Migration

```powershell
# Créer la migration
alembic revision --autogenerate -m "Initial migration"

# Appliquer la migration
alembic upgrade head
```

### 5. Mettre à Jour .env

```env
# Base de données
DATABASE_URL=postgresql://webox_user:votre_mot_de_passe@localhost/webox_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=votre_secret_key_super_securisee
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Clés API IA (existantes)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
# ... autres clés
```

---

## 💬 MIGRATION CHAT MULTI-IA

### 1. Créer les Routes API

**Créer :** `app/routes/chat_routes.py`

```python
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.schemas.chat import ChatRequest, ChatResponse, ConversationResponse
from modules.core.ai_providers import ai_manager
import asyncio
import json

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Envoyer un message et obtenir les réponses des IA"""
    
    # Récupérer ou créer la conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        conversation = Conversation(
            user_id=current_user.id,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # Sauvegarder le message utilisateur
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()
    
    # Générer les réponses des IA
    messages = [{"role": "user", "content": request.message}]
    
    ai_responses = await ai_manager.generate_multi_response(
        messages=messages,
        providers=request.selected_providers,
        models=request.selected_models,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    # Sauvegarder les réponses
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content="",
        ai_responses=ai_responses
    )
    db.add(assistant_message)
    db.commit()
    
    return ChatResponse(
        conversation_id=conversation.id,
        user_message=request.message,
        ai_responses=ai_responses
    )

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer toutes les conversations de l'utilisateur"""
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.updated_at.desc()).all()
    
    return conversations

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les messages d'une conversation"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    return messages

@router.websocket("/ws/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """WebSocket pour le streaming en temps réel"""
    await websocket.accept()
    
    try:
        while True:
            # Recevoir le message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Générer les réponses en streaming
            for provider in message_data["providers"]:
                async for chunk in ai_manager.stream_response(
                    provider=provider,
                    message=message_data["message"]
                ):
                    await websocket.send_json({
                        "provider": provider,
                        "chunk": chunk
                    })
            
            # Envoyer la fin du streaming
            await websocket.send_json({"status": "complete"})
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for conversation {conversation_id}")
```

### 2. Créer les Schémas Pydantic

**Créer :** `app/schemas/chat.py`

```python
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str
    selected_providers: List[str]
    selected_models: Dict[str, str]
    temperature: float = 0.7
    max_tokens: int = 2000

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    ai_responses: Dict[str, str]

class ConversationResponse(BaseModel):
    id: int
    title: str
    folder: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### 3. Intégrer dans main.py

**Modifier :** `main.py`

```python
from app.routes import auth_router, dashboard_router, chat_router

# Inclure les routes
app.include_router(auth_router, tags=["Authentication"])
app.include_router(dashboard_router, tags=["Dashboard"])
app.include_router(chat_router, tags=["Chat"])  # NOUVEAU
```

### 4. Créer le Frontend React

**Créer :** `frontend/src/components/Chat.jsx`

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Chat() {
  const [message, setMessage] = useState('');
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [selectedProviders, setSelectedProviders] = useState(['GPT-4']);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/api/chat/send', {
        conversation_id: currentConversation?.id,
        message: message,
        selected_providers: selectedProviders,
        selected_models: { 'GPT-4': 'gpt-4-turbo' },
        temperature: 0.7,
        max_tokens: 2000
      });
      
      // Ajouter les messages à l'affichage
      setMessages([...messages, {
        role: 'user',
        content: message
      }, {
        role: 'assistant',
        ai_responses: response.data.ai_responses
      }]);
      
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            {msg.role === 'user' ? (
              <p>{msg.content}</p>
            ) : (
              <div className="ai-responses">
                {Object.entries(msg.ai_responses).map(([provider, response]) => (
                  <div key={provider} className="ai-response">
                    <h4>{provider}</h4>
                    <p>{response}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Posez votre question..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          {loading ? 'Envoi...' : 'Envoyer'}
        </button>
      </div>
    </div>
  );
}

export default Chat;
```

---

## 📊 MIGRATION DASHBOARD

### 1. Créer les Routes API

**Créer :** `app/routes/stats_routes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.conversation import Conversation, Message
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/stats", tags=["Statistics"])

@router.get("/user")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Statistiques de l'utilisateur"""
    
    # Nombre total de conversations
    total_conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).count()
    
    # Nombre total de messages
    total_messages = db.query(Message).join(Conversation).filter(
        Conversation.user_id == current_user.id
    ).count()
    
    # Conversations cette semaine
    week_ago = datetime.utcnow() - timedelta(days=7)
    conversations_this_week = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.created_at >= week_ago
    ).count()
    
    # IA les plus utilisées (à implémenter selon votre logique)
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "conversations_this_week": conversations_this_week,
        "member_since": current_user.created_at,
        "is_premium": current_user.is_premium
    }
```

---

## ✅ CHECKLIST DE MIGRATION

### Configuration Initiale
- [ ] PostgreSQL installé et configuré
- [ ] Base de données `webox_db` créée
- [ ] Node.js installé
- [ ] Redis installé et démarré
- [ ] Dépendances Python installées
- [ ] Alembic initialisé
- [ ] Modèles de données créés
- [ ] Migrations appliquées
- [ ] `.env` configuré

### Chat Multi-IA
- [ ] Routes API créées
- [ ] Schémas Pydantic créés
- [ ] WebSocket implémenté
- [ ] Frontend React créé
- [ ] Tests API réussis
- [ ] Tests WebSocket réussis

### Dashboard
- [ ] Routes statistiques créées
- [ ] Frontend dashboard créé
- [ ] Graphiques implémentés
- [ ] Tests réussis

---

**📅 Dernière mise à jour :** 30 Octobre 2025  
**👤 Créé par :** Cascade AI  
**🎯 Objectif :** Migration complète vers FastAPI
