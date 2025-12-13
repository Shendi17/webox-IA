# 📞 Assistant Vocal IA - Documentation Complète

## 🎯 Vue d'Ensemble

L'Assistant Vocal IA de WeBox Multi-IA permet d'automatiser les appels téléphoniques entrants et sortants en utilisant les technologies d'IA les plus avancées.

### **Technologies Utilisées**

| Composant | Technologie | Fonction |
|-----------|-------------|----------|
| **Téléphonie** | Twilio | Gestion des appels et SMS |
| **STT** | Google Cloud Speech-to-Text | Reconnaissance vocale |
| **TTS** | Google Cloud Text-to-Speech | Synthèse vocale |
| **IA** | OpenAI GPT-4 | Conversation intelligente |
| **Backend** | Python + Streamlit | Interface et logique |

---

## 📁 Architecture du Système

### **Fichiers Créés**

```
webox/
├── voice_telephony.py              # Module Twilio (téléphonie)
├── voice_stt.py                    # Module Google STT (reconnaissance vocale)
├── voice_tts.py                    # Module Google TTS (synthèse vocale)
├── voice_conversation_manager.py   # Gestionnaire de conversations
├── pages/
│   └── assistant_vocal.py         # Interface Streamlit
└── voice_conversations.json        # Historique des conversations
```

### **Flux de Données**

```
1. Appel entrant → Twilio
2. Audio → Google Cloud STT → Texte
3. Texte → OpenAI GPT-4 → Réponse IA
4. Réponse → Google Cloud TTS → Audio
5. Audio → Twilio → Appelant
```

---

## 🔑 Configuration des Clés API

### **1. Twilio (Téléphonie)**

**Obtenir les clés :**
1. Créez un compte sur [twilio.com](https://www.twilio.com)
2. Accédez à la console Twilio
3. Copiez votre **Account SID** et **Auth Token**
4. Achetez un numéro de téléphone

**Configuration `.env` :**
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+33123456789
```

### **2. Google Cloud (STT & TTS)**

**Obtenir les credentials :**
1. Créez un projet sur [console.cloud.google.com](https://console.cloud.google.com)
2. Activez les APIs :
   - Cloud Speech-to-Text API
   - Cloud Text-to-Speech API
3. Créez un compte de service
4. Téléchargez le fichier JSON de credentials

**Configuration `.env` :**
```env
GOOGLE_APPLICATION_CREDENTIALS=C:/chemin/vers/google-credentials.json
```

### **3. OpenAI (IA Conversationnelle)**

**Obtenir la clé :**
1. Créez un compte sur [platform.openai.com](https://platform.openai.com)
2. Accédez à **API Keys**
3. Créez une nouvelle clé

**Configuration `.env` :**
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 Utilisation

### **1. Lancer l'Application**

```bash
streamlit run app.py
```

Puis accédez à **📞 Assistant Vocal** dans le menu.

### **2. Tester la Synthèse Vocale**

1. Allez dans l'onglet **🎙️ Test Vocal**
2. Entrez un texte à synthétiser
3. Choisissez une voix (Neural2 recommandé)
4. Cliquez sur **Générer Audio**
5. Écoutez et téléchargez le résultat

### **3. Passer un Appel**

1. Allez dans l'onglet **📞 Appels**
2. Entrez le numéro à appeler (format international : +33...)
3. Entrez le message à dire
4. Cliquez sur **Passer l'appel**

### **4. Configurer un Flux d'Appel**

1. Allez dans l'onglet **🔄 Flux d'Appels**
2. Choisissez un flux prédéfini ou créez le vôtre
3. Configurez les étapes en JSON
4. Sauvegardez

---

## 🔄 Flux d'Appels Prédéfinis

### **1. Accueil Standard**

```json
{
  "name": "Accueil Standard",
  "description": "Message d'accueil et orientation",
  "steps": [
    {
      "id": "welcome",
      "type": "say",
      "message": "Bonjour et bienvenue. Comment puis-je vous aider ?",
      "next": "listen"
    },
    {
      "id": "listen",
      "type": "listen",
      "timeout": 5,
      "next": "process"
    },
    {
      "id": "process",
      "type": "ai_response",
      "provider": "openai",
      "model": "gpt-4",
      "next": "respond"
    }
  ]
}
```

### **2. Prise de Rendez-vous**

```json
{
  "name": "Prise de Rendez-vous",
  "description": "Gestion automatique des rendez-vous",
  "steps": [
    {
      "id": "welcome",
      "type": "say",
      "message": "Service de prise de rendez-vous. Pour quel service ?",
      "next": "get_service"
    },
    {
      "id": "get_service",
      "type": "listen",
      "next": "confirm_service"
    },
    {
      "id": "confirm_service",
      "type": "ai_response",
      "system_prompt": "Confirme le service et demande la date.",
      "next": "get_date"
    }
  ]
}
```

### **3. Support Technique**

```json
{
  "name": "Support Technique",
  "description": "Assistance technique automatisée",
  "steps": [
    {
      "id": "welcome",
      "type": "say",
      "message": "Support technique. Décrivez votre problème.",
      "next": "get_problem"
    },
    {
      "id": "get_problem",
      "type": "listen",
      "next": "analyze"
    },
    {
      "id": "analyze",
      "type": "ai_response",
      "system_prompt": "Analyse le problème et propose une solution.",
      "next": "provide_solution"
    }
  ]
}
```

---

## 🎙️ Voix Disponibles (Google Cloud TTS)

### **Voix Françaises**

| Nom | Genre | Type | Qualité |
|-----|-------|------|---------|
| `fr-FR-Standard-A` | Féminin | Standard | ⭐⭐⭐ |
| `fr-FR-Standard-B` | Masculin | Standard | ⭐⭐⭐ |
| `fr-FR-Wavenet-A` | Féminin | WaveNet | ⭐⭐⭐⭐ |
| `fr-FR-Wavenet-B` | Masculin | WaveNet | ⭐⭐⭐⭐ |
| `fr-FR-Neural2-A` | Féminin | Neural2 | ⭐⭐⭐⭐⭐ |
| `fr-FR-Neural2-B` | Masculin | Neural2 | ⭐⭐⭐⭐⭐ |

**Recommandation :** Utilisez les voix **Neural2** pour la meilleure qualité.

---

## 💰 Tarification

### **Twilio**

| Service | Prix |
|---------|------|
| Appel entrant | ~0.0085€/min |
| Appel sortant | ~0.013€/min |
| SMS | ~0.075€/SMS |
| Numéro de téléphone | ~1€/mois |

### **Google Cloud Speech-to-Text**

| Volume | Prix |
|--------|------|
| 0-60 min/mois | Gratuit |
| Au-delà | ~0.006€/15 secondes |

### **Google Cloud Text-to-Speech**

| Type | Prix |
|------|------|
| Standard (0-1M caractères) | Gratuit |
| WaveNet | ~0.000016€/caractère |
| Neural2 | ~0.000016€/caractère |

### **OpenAI GPT-4**

| Type | Prix |
|------|------|
| Input | ~0.03$/1K tokens |
| Output | ~0.06$/1K tokens |

### **Coût Total Estimé par Appel**

| Durée | Twilio | Google Cloud | OpenAI | **Total** |
|-------|--------|--------------|--------|-----------|
| 1 min | 0.01€ | 0.004€ | 0.05€ | **~0.06€** |
| 5 min | 0.05€ | 0.02€ | 0.05€ | **~0.12€** |
| 10 min | 0.10€ | 0.04€ | 0.05€ | **~0.19€** |

---

## 🛠️ API Reference

### **TwilioVoiceManager**

```python
from voice_telephony import twilio_manager

# Vérifier la configuration
if twilio_manager.is_configured():
    # Passer un appel
    call_sid = twilio_manager.make_call(
        to_number="+33612345678",
        message="Bonjour, ceci est un test."
    )
    
    # Envoyer un SMS
    sms_sid = twilio_manager.send_sms(
        to_number="+33612345678",
        message="Message de test"
    )
    
    # Lister les appels récents
    calls = twilio_manager.list_recent_calls(limit=10)
```

### **GoogleSTTManager**

```python
from voice_stt import google_stt_manager

# Transcrire un fichier audio
transcript = google_stt_manager.transcribe_audio_file(
    audio_file_path="recording.wav",
    language_code="fr-FR"
)

# Transcrire des bytes audio
audio_bytes = open("audio.wav", "rb").read()
transcript = google_stt_manager.transcribe_audio(
    audio_content=audio_bytes,
    language_code="fr-FR"
)
```

### **GoogleTTSManager**

```python
from voice_tts import google_tts_manager

# Synthétiser du texte
audio_content = google_tts_manager.synthesize_speech(
    text="Bonjour, comment allez-vous ?",
    voice_name="fr-FR-Neural2-A",
    speaking_rate=1.0,
    pitch=0.0
)

# Sauvegarder dans un fichier
google_tts_manager.synthesize_to_file(
    text="Bonjour",
    output_path="output.mp3",
    voice_name="fr-FR-Neural2-A"
)

# Obtenir les voix disponibles
voices = google_tts_manager.get_french_voices()
```

### **VoiceConversationManager**

```python
from voice_conversation_manager import voice_conversation_manager
import asyncio

# Créer une conversation
conversation = voice_conversation_manager.create_conversation(
    call_sid="CA123456",
    flow_type="accueil"
)

# Traiter l'entrée vocale
async def process_call():
    transcript = await voice_conversation_manager.process_voice_input(
        call_sid="CA123456",
        audio_content=audio_bytes
    )
    
    # Générer une réponse IA
    response = await voice_conversation_manager.generate_ai_response(
        call_sid="CA123456",
        user_input=transcript
    )
    
    # Générer l'audio de réponse
    audio = voice_conversation_manager.generate_voice_response(response)
    
    return audio

# Exécuter
audio_response = asyncio.run(process_call())
```

---

## 🌐 Déploiement en Production

### **1. Serveur Web (Flask/FastAPI)**

Créez un serveur pour recevoir les webhooks Twilio :

```python
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice/incoming", methods=['POST'])
def incoming_call():
    """Webhook pour les appels entrants"""
    response = VoiceResponse()
    
    # Créer une conversation
    call_sid = request.values.get('CallSid')
    conversation = voice_conversation_manager.create_conversation(call_sid)
    
    # Message d'accueil
    gather = response.gather(
        input='speech',
        language='fr-FR',
        action='/voice/process',
        method='POST'
    )
    gather.say("Bonjour, comment puis-je vous aider ?", language='fr-FR')
    
    return str(response)

@app.route("/voice/process", methods=['POST'])
async def process_speech():
    """Traite la parole de l'utilisateur"""
    call_sid = request.values.get('CallSid')
    speech_result = request.values.get('SpeechResult')
    
    # Générer une réponse IA
    ai_response = await voice_conversation_manager.generate_ai_response(
        call_sid=call_sid,
        user_input=speech_result
    )
    
    # Créer la réponse TwiML
    response = VoiceResponse()
    response.say(ai_response, language='fr-FR')
    
    return str(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### **2. Configuration Twilio**

1. Déployez votre serveur avec HTTPS (obligatoire)
2. Dans la console Twilio, configurez le webhook :
   - **Voice URL:** `https://votre-domaine.com/voice/incoming`
   - **Method:** POST

### **3. HTTPS avec Let's Encrypt**

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot --nginx -d votre-domaine.com

# Renouvellement automatique
sudo certbot renew --dry-run
```

### **4. Déploiement sur Cloud**

**Options recommandées :**
- **Heroku** : Simple, gratuit pour commencer
- **AWS EC2** : Flexible, scalable
- **Google Cloud Run** : Serverless, auto-scaling
- **DigitalOcean** : Bon rapport qualité/prix

---

## 📊 Cas d'Usage Réels

### **1. Service Client 24/7**

```python
# Flux pour le service client
{
  "name": "Service Client",
  "steps": [
    {"type": "say", "message": "Service client, comment puis-je vous aider ?"},
    {"type": "listen"},
    {"type": "ai_response", "system_prompt": "Tu es un agent de service client..."},
    {"type": "say", "message": "Puis-je vous aider avec autre chose ?"},
    {"type": "listen"},
    {"type": "transfer_to_human", "if": "complex_issue"}
  ]
}
```

### **2. Enquêtes Téléphoniques**

```python
# Flux pour les enquêtes
{
  "name": "Enquête Satisfaction",
  "steps": [
    {"type": "say", "message": "Enquête de satisfaction. Sur une échelle de 1 à 10..."},
    {"type": "listen"},
    {"type": "save_response", "field": "satisfaction_score"},
    {"type": "say", "message": "Que pouvons-nous améliorer ?"},
    {"type": "listen"},
    {"type": "save_response", "field": "feedback"}
  ]
}
```

### **3. Notifications Vocales**

```python
# Appels sortants automatiques
for customer in customers:
    twilio_manager.make_call(
        to_number=customer.phone,
        message=f"Bonjour {customer.name}, votre commande est prête."
    )
```

---

## 🔧 Dépannage

### **Problème : "Twilio n'est pas configuré"**

**Solution :**
- Vérifiez que les variables d'environnement sont définies dans `.env`
- Redémarrez l'application après modification du `.env`

### **Problème : "Google Cloud STT/TTS n'est pas configuré"**

**Solution :**
- Vérifiez que le fichier credentials.json existe
- Vérifiez que le chemin dans `GOOGLE_APPLICATION_CREDENTIALS` est correct
- Vérifiez que les APIs sont activées dans Google Cloud Console

### **Problème : Qualité audio médiocre**

**Solution :**
- Utilisez les voix Neural2 au lieu de Standard
- Ajustez le `speaking_rate` (0.9-1.0 recommandé)
- Vérifiez la qualité de l'audio entrant

### **Problème : Latence élevée**

**Solution :**
- Utilisez un serveur proche géographiquement
- Optimisez les prompts GPT-4 (plus courts)
- Utilisez GPT-3.5-turbo pour des réponses plus rapides

---

## 📈 Optimisations

### **1. Cache des Réponses Fréquentes**

```python
# Cache pour les questions fréquentes
FAQ_CACHE = {
    "horaires": "Nous sommes ouverts de 9h à 18h du lundi au vendredi.",
    "adresse": "Notre adresse est 123 rue de Paris, 75001 Paris.",
    # ...
}

# Vérifier le cache avant d'appeler GPT-4
if user_input.lower() in FAQ_CACHE:
    response = FAQ_CACHE[user_input.lower()]
else:
    response = await generate_ai_response(user_input)
```

### **2. Utilisation de GPT-3.5-turbo**

```python
# Pour des réponses plus rapides et moins chères
response = await ai_manager.get_response(
    provider_name="openai",
    messages=messages,
    model="gpt-3.5-turbo"  # Au lieu de gpt-4
)
```

### **3. Limitation de la Durée des Appels**

```python
# Timeout après 5 minutes
MAX_CALL_DURATION = 300  # secondes

if call_duration > MAX_CALL_DURATION:
    response.say("Merci pour votre appel. Au revoir.", language='fr-FR')
    response.hangup()
```

---

## ✅ Checklist de Déploiement

- [ ] Clés API Twilio configurées
- [ ] Credentials Google Cloud configurés
- [ ] Clé OpenAI configurée
- [ ] Numéro de téléphone Twilio acheté
- [ ] Serveur web déployé avec HTTPS
- [ ] Webhooks Twilio configurés
- [ ] Flux d'appels testés
- [ ] Monitoring mis en place
- [ ] Budget défini et alertes configurées
- [ ] Documentation utilisateur créée

---

## 📚 Ressources

### **Documentation Officielle**

- [Twilio Voice API](https://www.twilio.com/docs/voice)
- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/docs)
- [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs)
- [OpenAI API](https://platform.openai.com/docs)

### **Tutoriels**

- [Twilio Voice Quickstart](https://www.twilio.com/docs/voice/quickstart)
- [Google Cloud STT Python](https://cloud.google.com/speech-to-text/docs/libraries)
- [Building Voice Bots](https://www.twilio.com/blog/building-voice-bots)

---

**🎉 Votre Assistant Vocal IA est prêt à automatiser vos appels téléphoniques ! 📞**
