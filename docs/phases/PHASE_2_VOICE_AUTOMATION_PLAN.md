# 🎤 PHASE 2 : VOICE AUTOMATION - PLAN COMPLET

**Date** : 23 Novembre 2025  
**Heure** : 11:05  
**Statut** : 📋 PLANIFICATION

---

## 🎯 OBJECTIF

Créer un système d'assistant vocal IA pour permettre aux clients d'entreprise de gérer leurs appels automatiquement.

---

## 📊 VUE D'ENSEMBLE

### **Cas d'usage**
- **Restaurants** : Réservations 24/7
- **Cabinets médicaux** : Prise de RDV
- **E-commerce** : Support client
- **Hôtels** : Réservations
- **Services auto** : RDV révision

### **Flux de fonctionnement**
```
Client appelle
    ↓
Twilio (numéro dédié)
    ↓
Speech-to-Text (Google Cloud / Whisper)
    ↓
IA WeBox (GPT-4 / Claude + contexte client)
    ↓
Text-to-Speech (ElevenLabs / Google TTS)
    ↓
Twilio → Réponse vocale au client
```

---

## 🏗️ ARCHITECTURE

### **Backend**
```
app/
├── services/
│   ├── voice_service.py          # Gestion des appels
│   ├── speech_to_text.py         # STT (Google/Whisper)
│   ├── text_to_speech.py         # TTS (ElevenLabs/Google)
│   └── voice_ai_handler.py       # Logique IA
├── routes/
│   └── voice_routes.py           # Routes API
└── models/
    ├── voice_assistant_db.py     # Table assistants
    └── voice_call_db.py          # Table appels
```

### **Base de données**
```sql
-- Table voice_assistants
CREATE TABLE voice_assistants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(255),
    description TEXT,
    phone_number VARCHAR(50),
    ai_model VARCHAR(50),
    voice_type VARCHAR(50),
    language VARCHAR(10),
    system_prompt TEXT,
    context_data JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table voice_calls
CREATE TABLE voice_calls (
    id SERIAL PRIMARY KEY,
    assistant_id INTEGER REFERENCES voice_assistants(id),
    caller_number VARCHAR(50),
    duration INTEGER,
    transcript TEXT,
    ai_response TEXT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📝 ÉTAPES DE DÉVELOPPEMENT

### **Phase 2.1 : Base de données** (1h)
- [ ] Créer le modèle `VoiceAssistant`
- [ ] Créer le modèle `VoiceCall`
- [ ] Migration de la base de données

### **Phase 2.2 : Services de base** (2h)
- [ ] Service Speech-to-Text (Google Cloud)
- [ ] Service Text-to-Speech (ElevenLabs)
- [ ] Service de gestion des appels

### **Phase 2.3 : Intégration Twilio** (2h)
- [ ] Configuration Twilio
- [ ] Webhook pour recevoir les appels
- [ ] Gestion des appels entrants
- [ ] Envoi de réponses vocales

### **Phase 2.4 : Logique IA** (2h)
- [ ] Handler IA pour traiter les demandes
- [ ] Contexte client (réservations, RDV, etc.)
- [ ] Gestion des conversations
- [ ] Historique des interactions

### **Phase 2.5 : Routes API** (1h)
- [ ] CRUD assistants vocaux
- [ ] Liste des appels
- [ ] Statistiques
- [ ] Configuration

### **Phase 2.6 : Interface Frontend** (3h)
- [ ] Page de gestion des assistants
- [ ] Création d'assistant (wizard)
- [ ] Tableau de bord des appels
- [ ] Statistiques et analytics

---

## 💻 CODE À DÉVELOPPER

### **1. Modèles de base de données**

**Fichier** : `app/models/voice_assistant_db.py`

```python
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class VoiceAssistant(Base):
    __tablename__ = "voice_assistants"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    phone_number = Column(String(50))
    ai_model = Column(String(50), default="gpt-4")
    voice_type = Column(String(50), default="alloy")
    language = Column(String(10), default="fr")
    system_prompt = Column(Text)
    context_data = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**Fichier** : `app/models/voice_call_db.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class VoiceCall(Base):
    __tablename__ = "voice_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    assistant_id = Column(Integer, ForeignKey("voice_assistants.id"))
    caller_number = Column(String(50))
    duration = Column(Integer)
    transcript = Column(Text)
    ai_response = Column(Text)
    status = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

---

### **2. Service Speech-to-Text**

**Fichier** : `app/services/speech_to_text.py`

```python
"""
Service Speech-to-Text
"""
import os
from google.cloud import speech_v1
from typing import Dict

class SpeechToTextService:
    """Service de transcription audio"""
    
    def __init__(self):
        # Configurer Google Cloud
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
        self.client = speech_v1.SpeechClient()
    
    def transcribe_audio(self, audio_content: bytes, language: str = "fr-FR") -> Dict:
        """Transcrire l'audio en texte"""
        try:
            audio = speech_v1.RecognitionAudio(content=audio_content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=8000,
                language_code=language,
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                return {
                    "success": True,
                    "transcript": transcript
                }
            else:
                return {
                    "success": False,
                    "error": "Aucune transcription disponible"
                }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
```

---

### **3. Service Text-to-Speech**

**Fichier** : `app/services/text_to_speech.py`

```python
"""
Service Text-to-Speech
"""
import os
import requests
from typing import Dict

class TextToSpeechService:
    """Service de synthèse vocale"""
    
    def __init__(self):
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def generate_speech(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Dict:
        """Générer l'audio à partir du texte"""
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "audio_content": response.content
                }
            else:
                return {
                    "success": False,
                    "error": f"Erreur {response.status_code}"
                }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
```

---

### **4. Service de gestion des appels**

**Fichier** : `app/services/voice_service.py`

```python
"""
Service de gestion des appels vocaux
"""
from twilio.rest import Client
from typing import Dict
import os

class VoiceService:
    """Service de gestion des appels"""
    
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)
    
    def handle_incoming_call(self, call_sid: str, from_number: str) -> Dict:
        """Gérer un appel entrant"""
        try:
            # Logique de traitement de l'appel
            return {
                "success": True,
                "call_sid": call_sid
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_voice_response(self, call_sid: str, audio_url: str) -> Dict:
        """Envoyer une réponse vocale"""
        try:
            # Envoyer l'audio via Twilio
            return {
                "success": True,
                "message": "Réponse envoyée"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
```

---

## 🎨 INTERFACE FRONTEND

### **Page principale : Mes Assistants Vocaux**

```
┌─────────────────────────────────────────────────────────┐
│ 🎤 Assistants Vocaux                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [+ Créer un assistant]                                 │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🤖 Assistant Restaurant                         │   │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │   │
│  │ Numéro : +33 1 23 45 67 89                      │   │
│  │ Appels aujourd'hui : 12                         │   │
│  │ Statut : ✅ Actif                               │   │
│  │                                                 │   │
│  │ [📊 Stats] [⚙️ Config] [🗑️ Supprimer]          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🤖 Assistant Médical                            │   │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │   │
│  │ Numéro : +33 1 98 76 54 32                      │   │
│  │ Appels aujourd'hui : 8                          │   │
│  │ Statut : ✅ Actif                               │   │
│  │                                                 │   │
│  │ [📊 Stats] [⚙️ Config] [🗑️ Supprimer]          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 💰 COÛTS ESTIMÉS

### **Par appel de 5 minutes**
- Twilio : ~0.02€
- Google STT : ~0.02€
- GPT-4 : ~0.04€
- ElevenLabs TTS : ~0.02€
- **Total : ~0.10€ par appel**

### **Tarification client suggérée**
- **Starter** : 50€/mois (100 appels)
- **Pro** : 150€/mois (500 appels)
- **Business** : 500€/mois (2000 appels)

---

## 📊 PROGRESSION

```
Phase 2.1 : Base de données      ░░░░░░░░░░░░░░░░░░░░   0%
Phase 2.2 : Services de base     ░░░░░░░░░░░░░░░░░░░░   0%
Phase 2.3 : Intégration Twilio   ░░░░░░░░░░░░░░░░░░░░   0%
Phase 2.4 : Logique IA           ░░░░░░░░░░░░░░░░░░░░   0%
Phase 2.5 : Routes API           ░░░░░░░░░░░░░░░░░░░░   0%
Phase 2.6 : Interface Frontend   ░░░░░░░░░░░░░░░░░░░░   0%

TOTAL PHASE 2                    ░░░░░░░░░░░░░░░░░░░░   0%
```

**Estimation** : 11 heures de développement

---

## 🚀 PROCHAINES ÉTAPES

1. **Créer les modèles de base de données**
2. **Développer les services STT/TTS**
3. **Intégrer Twilio**
4. **Créer la logique IA**
5. **Développer l'interface**

---

**Phase 2 : Voice Automation - Prêt à démarrer ! 🎤**
